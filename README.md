# YouTube Analyzer

Projeto web para analisar vídeos do YouTube a partir da transcrição pública do vídeo.

O usuário informa o link de um vídeo, a API busca a transcrição disponível, processa o conteúdo e retorna:

- Resumo completo
- Tópicos principais
- Conclusão
- Quantidade de palavras analisadas
- Transcrição completa com marcação de tempo

## Tecnologias utilizadas

### Frontend

- HTML
- CSS
- JavaScript
- GitHub Pages

### Backend

- Python
- Flask
- Flask-CORS
- YouTube Transcript API
- Gunicorn

## Estrutura do projeto

```txt
youtube-analyzer/
│
├── index.html
├── style.css
├── script.js
├── README.md
│
└── app/
    ├── app.py
    ├── youtube_analyzer.py
    ├── requirements.txt
    └── Procfile
```

## Como rodar o backend localmente

Acesse a pasta do backend:

```bash
cd app
```

Crie o ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente virtual no Windows:

```bash
.\venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute a API:

```bash
python app.py
```

A API ficará disponível em:

```txt
http://localhost:5000
```

Teste a rota de saúde:

```txt
http://localhost:5000/health
```

## Como rodar o frontend localmente

Na raiz do projeto, abra o arquivo:

```txt
index.html
```

Ou use a extensão Live Server do VS Code.

## Configuração do frontend

No arquivo `script.js`, a URL da API está configurada assim:

```js
const API_URL = "http://localhost:5000/analyze";
```

Para usar em produção, altere para a URL do backend publicado no Render:

```js
const API_URL = "https://sua-api.onrender.com/analyze";
```

## Deploy do frontend no GitHub Pages

1. Acesse o repositório no GitHub
2. Vá em `Settings`
3. Vá em `Pages`
4. Em `Source`, selecione `Deploy from a branch`
5. Escolha a branch `main`
6. Escolha a pasta `/root`
7. Salve

O site ficará disponível em:

```txt
https://henriquedu.github.io/youtube-analyzer/
```

## Deploy do backend no Render

Crie um novo Web Service no Render e use estas configurações:

```txt
Root Directory: app
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

Depois copie a URL gerada pelo Render e atualize o `API_URL` no arquivo `script.js`.

## Limitações

Este projeto funciona apenas com vídeos que possuem transcrição pública disponível no YouTube.

Caso o vídeo não tenha legenda ou transcrição liberada, a API retornará uma mensagem de erro.

## Melhorias futuras

- Integrar com IA para gerar resumos mais completos
- Exibir título, canal e thumbnail do vídeo
- Criar histórico de análises
- Permitir exportar resumo em PDF
- Adicionar tradução automática
