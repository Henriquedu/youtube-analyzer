# YouTube Analyzer

O **YouTube Analyzer** é um projeto web que recebe o link de um vídeo do YouTube, busca a transcrição pública disponível e gera uma análise organizada do conteúdo.

O sistema retorna:

- Resumo completo do vídeo
- Tópicos principais
- Conclusão
- Quantidade de palavras analisadas
- Idioma da transcrição
- Transcrição completa com marcação de tempo

## Demonstração do fluxo

```txt
Usuário cola o link do vídeo
↓
Frontend envia o link para a API
↓
Backend busca a transcrição do YouTube
↓
Backend processa o texto
↓
Frontend exibe resumo, tópicos, conclusão e transcrição
```

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

## Pré-requisitos

Antes de rodar o projeto, instale:

- Python 3.10 ou superior
- Git
- VS Code
- Extensão Live Server no VS Code

Durante a instalação do Python no Windows, marque a opção:

```txt
Add python.exe to PATH
```

## Como baixar o projeto

### Opção 1: usando Git

```bash
git clone https://github.com/Henriquedu/youtube-analyzer.git
cd youtube-analyzer
```

### Opção 2: baixando ZIP

1. Acesse o repositório no GitHub
2. Clique em `Code`
3. Clique em `Download ZIP`
4. Extraia o arquivo
5. Abra a pasta extraída no VS Code

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
    ├── Procfile
    └── render.yaml
```

## Como rodar localmente

O projeto possui duas partes:

- Frontend: site em HTML, CSS e JavaScript
- Backend: API em Python com Flask

Para o projeto funcionar localmente, o backend precisa estar rodando enquanto o site estiver aberto.

## 1. Abrir o projeto no VS Code

Abra a pasta do projeto no VS Code.

Depois abra o terminal:

```txt
Terminal > New Terminal
```

## 2. Entrar na pasta do backend

```bash
cd app
```

## 3. Criar o ambiente virtual

```bash
python -m venv venv
```

## 4. Ativar o ambiente virtual

### Windows PowerShell

```bash
.\venv\Scripts\activate
```

### Linux ou macOS

```bash
source venv/bin/activate
```

Quando o ambiente virtual estiver ativo, o terminal mostrará algo parecido com:

```txt
(venv)
```

## 5. Instalar as dependências

```bash
pip install -r requirements.txt
```

## 6. Rodar a API

```bash
python app.py
```

Se tudo estiver correto, será exibido algo parecido com:

```txt
Running on http://127.0.0.1:5000
```

Mantenha esse terminal aberto.

## 7. Testar se a API está funcionando

Abra no navegador:

```txt
http://localhost:5000/health
```

A resposta esperada é parecida com:

```json
{
  "status": "healthy",
  "success": true
}
```

## 8. Rodar o frontend

Na raiz do projeto, abra o arquivo:

```txt
index.html
```

Clique com o botão direito e selecione:

```txt
Open with Live Server
```

O navegador abrirá uma URL parecida com:

```txt
http://127.0.0.1:5500/index.html
```

Não abra o arquivo diretamente como `file:///`, pois isso pode causar erro na comunicação com a API.

## 9. Usar o sistema

1. Abra um vídeo do YouTube que possua transcrição pública
2. Copie o link do vídeo
3. Cole o link no campo do YouTube Analyzer
4. Clique em `Analisar`
5. Aguarde o processamento
6. Veja o resumo, tópicos, conclusão e transcrição completa

## Configuração da API no frontend

No arquivo `script.js`, existe esta linha:

```js
const API_URL = "http://localhost:5000/analyze";
```

Essa URL é usada para rodar localmente.

Quando o backend for publicado em produção, altere para a URL do serviço publicado:

```js
const API_URL = "https://sua-api.onrender.com/analyze";
```

## Como publicar o frontend no GitHub Pages

1. Acesse o repositório no GitHub
2. Clique em `Settings`
3. Clique em `Pages`
4. Em `Source`, selecione `Deploy from a branch`
5. Em `Branch`, selecione `main`
6. Em `Folder`, selecione `/root`
7. Clique em `Save`

Após alguns minutos, o site ficará disponível em:

```txt
https://henriquedu.github.io/youtube-analyzer/
```

## Como publicar o backend no Render

O GitHub Pages não executa Python. Por isso, o backend precisa ser hospedado separadamente.

Uma opção gratuita é o Render.

### Passo a passo no Render

1. Acesse o Render
2. Crie uma conta ou entre usando GitHub
3. Clique em `New`
4. Clique em `Web Service`
5. Selecione o repositório `youtube-analyzer`
6. Configure o serviço assim:

```txt
Name: youtube-analyzer-api
Language: Python
Branch: main
Root Directory: app
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

7. Escolha o plano gratuito
8. Clique em `Create Web Service`

Quando o deploy finalizar, o Render gerará uma URL parecida com:

```txt
https://youtube-analyzer-api.onrender.com
```

Teste a API publicada acessando:

```txt
https://youtube-analyzer-api.onrender.com/health
```

## Conectar o site publicado com o backend publicado

Depois de publicar o backend no Render, abra o arquivo `script.js` e troque:

```js
const API_URL = "http://localhost:5000/analyze";
```

por:

```js
const API_URL = "https://youtube-analyzer-api.onrender.com/analyze";
```

Use a URL real gerada pelo Render.

Depois envie a alteração para o GitHub:

```bash
git add .
git commit -m "Connect frontend to production API"
git push
```

## Possíveis erros e soluções

### Erro: Failed to fetch

Causas comuns:

- Backend não está rodando
- `API_URL` está incorreta
- Site foi aberto como `file:///`
- API online está fora do ar

Soluções:

- Rode `python app.py`
- Abra o site com Live Server
- Verifique se `http://localhost:5000/health` funciona
- Confira a URL configurada no `script.js`

### Erro: vídeo sem transcrição

O projeto só funciona com vídeos que possuem transcrição pública disponível.

No YouTube, verifique se o vídeo possui a opção:

```txt
Mostrar transcrição
```

### Erro de certificado SSL no Windows

Atualize as bibliotecas:

```bash
pip install --upgrade certifi requests urllib3
```

Depois rode novamente:

```bash
python app.py
```

### Erro: Python não foi encontrado

Instale o Python e marque:

```txt
Add python.exe to PATH
```

Depois feche e abra novamente o VS Code.

### Erro: requirements.txt não encontrado

Entre na pasta correta antes de instalar:

```bash
cd app
pip install -r requirements.txt
```

## Limitações

- O projeto depende da transcrição pública do vídeo
- Alguns vídeos podem bloquear transcrições
- Vídeos sem legenda não poderão ser analisados
- O resumo atual é baseado em processamento de texto, sem IA generativa

## Melhorias futuras

- Integrar com IA para gerar resumos mais completos
- Exibir título, canal e thumbnail do vídeo
- Criar histórico de análises
- Exportar resumo em PDF
- Adicionar tradução automática
- Permitir seleção de idioma
- Criar autenticação para usuários

## Autor

Desenvolvido por Henrique Eduardo da Maia Farias.

GitHub: https://github.com/Henriquedu
