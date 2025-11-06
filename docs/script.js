// YouTube Analyzer - Frontend
class YouTubeAnalyzer {
    constructor() {
        this.API_URL = 'https://youtube-analyzer-api-y07l.onrender.com'; // ← VOCÊ VAI MUDAR ISSO
        
        this.form = document.getElementById('analyzeForm');
        this.videoUrlInput = document.getElementById('videoUrl');
        this.analyzeBtn = document.getElementById('analyzeBtn');
        this.resultDiv = document.getElementById('result');
        this.errorDiv = document.getElementById('error');
        
        this.btnText = this.analyzeBtn.querySelector('.btn-text');
        this.btnLoading = this.analyzeBtn.querySelector('.btn-loading');
        
        this.init();
    }
    
    init() {
        this.hideResult();
        this.hideError();
        this.setLoading(false);
        
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.analyzeVideo();
        });
        
        // Mostrar placeholder da API URL no console para debug
        console.log('🔧 Lembre-se de atualizar API_URL no script.js para:', this.API_URL);
    }
    
    async analyzeVideo() {
        const videoUrl = this.videoUrlInput.value.trim();
        
        if (!videoUrl) {
            this.showError('Por favor, cole o link do vídeo do YouTube');
            return;
        }
        
        if (!this.isValidYouTubeUrl(videoUrl)) {
            this.showError('Por favor, insira um link válido do YouTube');
            return;
        }
        
        this.setLoading(true);
        this.hideError();
        this.hideResult();
        
        try {
            const response = await fetch(`${this.API_URL}/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: videoUrl })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showResult(data.result);
            } else {
                this.showError(data.error || 'Erro ao analisar o vídeo');
            }
            
        } catch (error) {
            console.error('Erro:', error);
            this.showError('Erro de conexão. Verifique se o backend está online e a URL da API está correta.');
        } finally {
            this.setLoading(false);
        }
    }
    
    isValidYouTubeUrl(url) {
        const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$/;
        return youtubeRegex.test(url);
    }
    
    setLoading(loading) {
        if (loading) {
            this.btnText.style.display = 'none';
            this.btnLoading.style.display = 'flex';
            this.analyzeBtn.disabled = true;
        } else {
            this.btnText.style.display = 'flex';
            this.btnLoading.style.display = 'none';
            this.analyzeBtn.disabled = false;
        }
    }
    
    showResult(result) {
        // Preenche informações do vídeo
        document.getElementById('videoTitle').textContent = result.video_info.titulo;
        document.getElementById('videoChannel').textContent = result.video_info.canal;
        document.getElementById('videoDuration').textContent = `⏱️ ${result.video_info.duracao}`;
        document.getElementById('videoViews').textContent = `👀 ${result.video_info.visualizacoes} views`;
        
        // Thumbnail
        const thumbnailImg = document.getElementById('videoThumbnail');
        if (result.video_info.thumbnail) {
            thumbnailImg.src = result.video_info.thumbnail;
            thumbnailImg.style.display = 'block';
        } else {
            thumbnailImg.style.display = 'none';
        }
        
        // Resumo
        document.getElementById('videoSummary').textContent = result.resumo;
        
        this.resultDiv.style.display = 'block';
        
        // Scroll suave para o resultado
        setTimeout(() => {
            this.resultDiv.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start' 
            });
        }, 100);
    }
    
    hideResult() {
        this.resultDiv.style.display = 'none';
    }
    
    showError(message) {
        document.getElementById('errorText').textContent = message;
        this.errorDiv.style.display = 'block';
        
        // Scroll suave para o erro
        setTimeout(() => {
            this.errorDiv.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start' 
            });
        }, 100);
    }
    
    hideError() {
        this.errorDiv.style.display = 'none';
    }
}

// Inicializa a aplicação
document.addEventListener('DOMContentLoaded', () => {
    new YouTubeAnalyzer();

});
