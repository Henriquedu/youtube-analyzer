const API_URL = "http://localhost:5000/analyze";

const form = document.getElementById("analyzerForm");
const videoUrlInput = document.getElementById("videoUrl");
const analyzeButton = document.getElementById("analyzeButton");
const statusBox = document.getElementById("statusBox");
const resultSection = document.getElementById("resultSection");
const summaryText = document.getElementById("summaryText");
const topicsList = document.getElementById("topicsList");
const conclusionText = document.getElementById("conclusionText");
const wordCount = document.getElementById("wordCount");
const transcriptSize = document.getElementById("transcriptSize");
const transcriptLanguage = document.getElementById("transcriptLanguage");
const transcriptBox = document.getElementById("transcriptBox");
const toggleTranscriptButton = document.getElementById("toggleTranscriptButton");
const copySummaryButton = document.getElementById("copySummaryButton");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const videoUrl = videoUrlInput.value.trim();

    if (!videoUrl) {
        showStatus("Informe o link do vídeo.", "error");
        return;
    }

    await analyzeVideo(videoUrl);
});

toggleTranscriptButton.addEventListener("click", () => {
    transcriptBox.classList.toggle("hidden");
    const isHidden = transcriptBox.classList.contains("hidden");
    toggleTranscriptButton.textContent = isHidden ? "Mostrar" : "Ocultar";
});

copySummaryButton.addEventListener("click", async () => {
    const text = summaryText.textContent.trim();

    if (!text) {
        return;
    }

    await navigator.clipboard.writeText(text);
    copySummaryButton.textContent = "Copiado";

    setTimeout(() => {
        copySummaryButton.textContent = "Copiar resumo";
    }, 1600);
});

async function analyzeVideo(videoUrl) {
    setLoadingState(true);
    showStatus("Analisando vídeo. Isso pode levar alguns segundos.", "loading");
    resultSection.classList.add("hidden");

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: videoUrl })
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(data.error || "Não foi possível analisar o vídeo.");
        }

        renderResult(data.result);
        showStatus("Análise concluída com sucesso.", "success");
    } catch (error) {
        showStatus(error.message, "error");
    } finally {
        setLoadingState(false);
    }
}

function renderResult(result) {
    summaryText.textContent = result.resumo || "Resumo não disponível.";
    conclusionText.textContent = result.conclusao || "Conclusão não disponível.";
    wordCount.textContent = result.total_palavras || 0;
    transcriptSize.textContent = result.tamanho_transcricao || 0;
    transcriptLanguage.textContent = result.idioma_transcricao || "-";

    renderTopics(result.topicos || []);
    renderTranscript(result.transcricao || []);

    resultSection.classList.remove("hidden");
}

function renderTopics(topics) {
    topicsList.innerHTML = "";

    if (!topics.length) {
        const item = document.createElement("li");
        item.textContent = "Nenhum tópico encontrado.";
        topicsList.appendChild(item);
        return;
    }

    topics.forEach((topic) => {
        const item = document.createElement("li");
        item.textContent = topic;
        topicsList.appendChild(item);
    });
}

function renderTranscript(transcript) {
    transcriptBox.innerHTML = "";
    transcriptBox.classList.add("hidden");
    toggleTranscriptButton.textContent = "Mostrar";

    if (!transcript.length) {
        transcriptBox.textContent = "Transcrição não disponível.";
        return;
    }

    transcript.forEach((line) => {
        const row = document.createElement("div");
        const time = document.createElement("span");
        const text = document.createElement("p");

        row.className = "transcript-line";
        time.className = "transcript-time";
        time.textContent = line.tempo;
        text.textContent = line.texto;

        row.appendChild(time);
        row.appendChild(text);
        transcriptBox.appendChild(row);
    });
}

function showStatus(message, type) {
    statusBox.textContent = message;
    statusBox.className = `status ${type}`;
}

function setLoadingState(isLoading) {
    analyzeButton.disabled = isLoading;
    analyzeButton.textContent = isLoading ? "Analisando..." : "Analisar";
}
