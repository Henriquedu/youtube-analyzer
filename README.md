# 🎬 YouTube Video Analyzer

![Badge Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Badge Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
![Badge License](https://img.shields.io/badge/License-MIT-green)
![Badge Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)

## 🧠 Sobre o Projeto

O **YouTube Video Analyzer** é uma aplicação desenvolvida em **Python + Streamlit** que utiliza **inteligência artificial (OpenAI GPT e Whisper)** para:
- Baixar o áudio de vídeos do YouTube 🎧  
- Transcrever automaticamente a fala 🗣️  
- Gerar um **resumo inteligente** do conteúdo 🧠  

💡 Ideal para estudantes, criadores de conteúdo e pesquisadores que desejam extrair informações rapidamente de vídeos longos do YouTube.

---

## 🌐 Demonstração Online

🔗 **Acesse o app aqui:**  
👉 [https://henriquemaia-youtubeanalyzer.streamlit.app](https://henriquemaia-youtubeanalyzer.streamlit.app)

🌎 **Landing Page no GitHub Pages:**  
👉 [https://henriquedu.github.io/youtube-analyzer-site/](https://henriquedu.github.io/youtube-analyzer-site/)

---

## 🧩 Funcionalidades

- 🔗 Insira o link de qualquer vídeo do YouTube  
- 🎧 Baixa e converte o áudio automaticamente  
- 🗣️ Transcreve com o modelo **Whisper (OpenAI)**  
- 🧠 Resume com **GPT-4**  
- 💾 Exporta o texto da transcrição e do resumo  
- 🖥️ Interface simples e intuitiva com **Streamlit**

---

## ⚙️ Tecnologias Utilizadas

| Categoria | Ferramenta |
|------------|-------------|
| Linguagem | [Python 3.10+](https://www.python.org) |
| Framework Web | [Streamlit](https://streamlit.io) |
| IA / NLP | [OpenAI API (GPT e Whisper)](https://platform.openai.com) |
| Download de vídeos | [pytube](https://pytube.io) |
| Transcrição | [Whisper](https://github.com/openai/whisper) |
| Hospedagem Web | [Streamlit Cloud](https://streamlit.io/cloud) |
| Página estática | [GitHub Pages](https://pages.github.com) |

---

## 🧭 Estrutura do Projeto

📦 youtube-analyzer
├── app.py
├── requirements.txt
├── utils/
│   ├── transcript.py
│   ├── summarize.py
│   └── downloader.py
│
📦 youtube-analyzer-site
├── index.html
└── style.css

---

##🚀 Como Executar Localmente

1️⃣ Clone o repositório
git clone https://github.com/henriquedu/youtube-analyzer.git
cd youtube-analyzer

2️⃣ Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # (Linux/Mac)
venv\Scripts\activate     # (Windows)

3️⃣ Instale as dependências
pip install -r requirements.txt

4️⃣ Crie um arquivo .env com sua chave da OpenAI
OPENAI_API_KEY=your_api_key_here

5️⃣ Execute o app
streamlit run app.py
