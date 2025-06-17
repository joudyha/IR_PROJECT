async function runOffline() {
  const dataset = document.getElementById("dataset").value;
  const representation = document.getElementById("representation").value;

  const endpointMap = {
    "tfidf": "http://localhost:8000/run_tfidf_pipeline",
    "embedding": "http://localhost:8007/run_embedding_pipeline",
    "hybrid": "http://localhost:8008/run_hybrid_pipeline"
  };

  const res = await fetch(endpointMap[representation], {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ dataset_name: dataset })
  });

  const data = await res.json();
  alert("تمت المعالجة الأولية!");
}

async function search() {
  const query = document.getElementById("query").value;
  const dataset = document.getElementById("dataset").value;
  const representation = document.getElementById("representation").value;

  const endpointMap = {
    "tfidf": "http://localhost:8016/run_query_tfidf",
    "embedding": "http://localhost:8018/run_query_embedding",
    "hybrid": "http://localhost:8017/run_query_hybrid",
  };

  const res = await fetch(endpointMap[representation], {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query: query, dataset_name: dataset })
  });

  const data = await res.json();

  if (data.error) {
    alert("حدث خطأ: " + data.error);
    return;
  }

  const resultsContainer = document.getElementById("results");
  resultsContainer.innerHTML = ""; // نفضي النتائج القديمة

  if (!data.texts || data.texts.length === 0) {
    resultsContainer.textContent = "لا توجد نتائج.";
    return;
  }

  data.texts.forEach(item => {
    const div = document.createElement("div");
    div.classList.add("result-item");

    const title = document.createElement("h4");
    title.textContent = `معرف المستند: ${item.doc_id}`;

    const paragraph = document.createElement("p");
    paragraph.textContent = item.text;

    div.appendChild(title);
    div.appendChild(paragraph);

    resultsContainer.appendChild(div);
  });
}
