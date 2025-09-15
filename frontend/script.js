function onRepresentationChange() {
  const rep = document.getElementById("representation").value;
  document.getElementById("embedding_options").style.display = (rep === "embedding") ? "block" : "none";
}

async function runOffline() {
  const dataset = document.getElementById("dataset").value;
  const representation = document.getElementById("representation").value;

  const method = (representation === "embedding")
    ? document.querySelector('input[name="embedding_method"]:checked').value
    : "default";

  const loading = document.getElementById("loading");
  loading.style.display = "block";

  const endpointMap = {
    "tfidf": "http://localhost:8000/run_tfidf_pipeline",
    "embedding": "http://localhost:8007/run_embedding_pipeline",
    "hybrid": "http://localhost:8008/run_hybrid_pipeline",
    "bm25": "http://localhost:8022/run_bm25_pipeline",
  };

  try {
    const res = await fetch(endpointMap[representation], {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ dataset_name: dataset, method })
    });

    const data = await res.json();
    if (data.error) {
      alert("❌ خطأ أثناء تنفيذ pipeline: " + data.error);
    } else {
      alert("✅ تمت المعالجة الأولية!");
      console.log("Pipeline response:", data);
    }
  } catch (err) {
    alert("❌ فشل الاتصال بالخادم.");
    console.error(err);
  } finally {
    loading.style.display = "none";
  }
}



async function search(customQuery = null) {
  const query = customQuery || document.getElementById("query").value.trim();
  if (!query) {
    alert("يرجى إدخال استعلام.");
    return;
  }

  if (customQuery) {
    document.getElementById("query").value = customQuery;
  }

  const dataset = document.getElementById("dataset").value;
  const representation = document.getElementById("representation").value;

  const method = (representation === "embedding")
    ? document.querySelector('input[name="embedding_method"]:checked').value
    : "default";

  const loading = document.getElementById("loading");
  loading.style.display = "block";

  const endpointMap = {
    "tfidf": "http://localhost:8016/run_query_tfidf",
    "embedding": "http://localhost:8018/run_query_embedding",
    "hybrid": "http://localhost:8017/run_query_hybrid",
    "bm25": "http://localhost:8021/run_query_bm25",
  };

  try {
    // 1. جلب الاقتراحات
    const suggestionRes = await fetch("http://localhost:8027/suggestions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: query,
        dataset_name: dataset
      })
    });
    const suggestionData = await suggestionRes.json();

    // 2. تحديد أفضل استعلام تلقائيًا
    const finalQuery = suggestionData.corrected_query || suggestionData.expanded_query || query;

   // 3. عرض الاقتراحات
const suggestionBox = document.getElementById("suggestion_box");
let suggestionHtml = "";

// عرض التصحيح فقط إذا اختلف عن الاستعلام الأصلي
if (
  suggestionData.corrected_query &&
  suggestionData.corrected_query.toLowerCase() !== query.toLowerCase()
) {
  suggestionHtml += `
    <p><strong>هل تقصد:</strong> 
      <button type="button" onclick="onSuggestionClick('${suggestionData.corrected_query}')">${suggestionData.corrected_query}</button>
    </p>
  `;
}

// عرض التوسيع دائمًا إذا مختلف
if (
  suggestionData.expanded_query &&
  suggestionData.expanded_query.toLowerCase() !== query.toLowerCase()
) {
  suggestionHtml += `
    <p><strong>اقتراح توسيع:</strong> 
      <button type="button" onclick="onSuggestionClick('${suggestionData.expanded_query}')">${suggestionData.expanded_query}</button>
    </p>
  `;
}
suggestionBox.innerHTML = suggestionHtml;
    const res = await fetch(endpointMap[representation], {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: finalQuery,
        dataset_name: dataset,
        method: method
      })
    });

    const data = await res.json();
    const resultsContainer = document.getElementById("results");
    resultsContainer.innerHTML = "";

    if (data.error) {
      resultsContainer.textContent = "❌ حدث خطأ: " + data.error;
      return;
    }

    if (!data.texts || data.texts.length === 0) {
      resultsContainer.textContent = "لا توجد نتائج.";
      return;
    }

    data.texts.forEach(item => {
      const div = document.createElement("div");
      div.classList.add("result-item");

      const title = document.createElement("h4");
      title.textContent = `معرف المستند: ${item.doc_id || "غير معروف"}`;

      const paragraph = document.createElement("p");
      paragraph.textContent = item.text;

      div.appendChild(title);
      div.appendChild(paragraph);
      resultsContainer.appendChild(div);
    });

  } catch (err) {
    alert("❌ فشل الاتصال بالخادم.");
    console.error(err);
  } finally {
    loading.style.display = "none";
  }
}

function onSuggestionClick(newQuery) {
  document.getElementById("query").value = newQuery;
  search(newQuery);
}
onRepresentationChange();


// ... الكود الحالي الموجود في script.js (مثلاً دالة search، وغيرها)

let currentFocus = -1;
const queryInput = document.getElementById("query");
let autocompleteBox = null;

queryInput.addEventListener("input", async (e) => {
  const val = e.target.value.trim();
  if (!val) {
    closeAutocomplete();
    return;
  }
  const lastWord = val.split(/\s+/).pop();
  if (lastWord.length === 0) {
    closeAutocomplete();
    return;
  }
  const dataset = document.getElementById("dataset").value;

  try {
    const res = await fetch("http://localhost:8027/autocomplete", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prefix: lastWord, dataset_name: dataset }),
    });
    const data = await res.json();

    showAutocomplete(data.suggestions, lastWord);
  } catch (err) {
    console.error("Autocomplete error:", err);
  }
});

queryInput.addEventListener("keydown", function(e) {
  if (!autocompleteBox) return;

  const items = autocompleteBox.getElementsByTagName("div");
  if (items.length === 0) return;

  if (e.key === "ArrowDown") {
    currentFocus++;
    if (currentFocus >= items.length) currentFocus = 0;
    addActive(items);
    e.preventDefault();
  } else if (e.key === "ArrowUp") {
    currentFocus--;
    if (currentFocus < 0) currentFocus = items.length -1;
    addActive(items);
    e.preventDefault();
  } else if (e.key === "Enter") {
    e.preventDefault();
    if (currentFocus > -1) {
      items[currentFocus].click();
    }
  }
});

function showAutocomplete(suggestions, prefix) {
  closeAutocomplete();
  currentFocus = -1;

  if (suggestions.length === 0) return;

  autocompleteBox = document.createElement("div");
  autocompleteBox.setAttribute("id", "autocomplete-list");
  autocompleteBox.style.width = queryInput.offsetWidth + "px";

  suggestions.forEach((item) => {
    const itemDiv = document.createElement("div");
    itemDiv.textContent = item;
    itemDiv.style.padding = "5px";
    itemDiv.style.cursor = "pointer";

    itemDiv.addEventListener("click", () => {
      applyAutocomplete(item, prefix);
      closeAutocomplete();
      queryInput.focus();
    });
    autocompleteBox.appendChild(itemDiv);
  });

  document.body.appendChild(autocompleteBox);
  const rect = queryInput.getBoundingClientRect();
  autocompleteBox.style.top = rect.bottom + window.scrollY + "px";
  autocompleteBox.style.left = rect.left + window.scrollX + "px";
  autocompleteBox.style.position = "absolute";
  autocompleteBox.style.width = rect.width + "px";

}

function addActive(items) {
  removeActive(items);
  if (currentFocus >= items.length) currentFocus = 0;
  if (currentFocus < 0) currentFocus = items.length - 1;
  items[currentFocus].classList.add("autocomplete-active");
}

function removeActive(items) {
  for (const item of items) {
    item.classList.remove("autocomplete-active");
  }
}

function applyAutocomplete(selectedWord, prefix) {
  let val = queryInput.value.trim();
  let words = val.split(/\s+/);
  words[words.length - 1] = selectedWord;
  queryInput.value = words.join(" ") + " ";
}

function closeAutocomplete() {
  if (autocompleteBox) {
    autocompleteBox.remove();
    autocompleteBox = null;
    currentFocus = -1;
  }
}

document.addEventListener("click", function (e) {
  if (e.target !== queryInput) {
    closeAutocomplete();
  }
});

async function runTopicDetection() {
  const dataset = document.getElementById("dataset").value;
  const resultDiv = document.getElementById("topicDetectionResult");
  resultDiv.textContent = "جاري الكشف عن المواضيع...";

  try {
    const res = await fetch(`http://localhost:8029/topic_detection?dataset_name=${encodeURIComponent(dataset)}`, {
      method: "POST"
    });

    if (!res.ok) {
      throw new Error("خطأ في الاستجابة من الخادم");
    }

    const data = await res.text();  // حسب رد السيرفر، ممكن JSON أو نص

    resultDiv.textContent = data;
  } catch (error) {
    resultDiv.textContent = "حدث خطأ أثناء الكشف عن المواضيع.";
    console.error(error);
  }
}

// ربط الزر بالدالة
document.getElementById("runTopicDetectionBtn").addEventListener("click", runTopicDetection);

const toggleBtn = document.getElementById("toggleDarkMode");
const body = document.body;

function applyDarkMode(enabled) {
  if (enabled) {
    body.classList.add("dark-mode");
    toggleBtn.textContent = "☀️ الوضع النهاري";
    localStorage.setItem("darkMode", "true");
  } else {
    body.classList.remove("dark-mode");
    toggleBtn.textContent = "🌙 الوضع الليلي";
    localStorage.setItem("darkMode", "false");
  }
}

toggleBtn.addEventListener("click", () => {
  const isDark = body.classList.contains("dark-mode");
  applyDarkMode(!isDark);
});

// التحقق من التفضيلات المخزنة
window.addEventListener("DOMContentLoaded", () => {
  const isDarkSaved = localStorage.getItem("darkMode") === "true";
  applyDarkMode(isDarkSaved);
});