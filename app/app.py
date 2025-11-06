from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_analyzer import YouTubeResumidor
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Inicializa o resumidor
resumidor = YouTubeResumidor()

@app.route('/')
def home():
    return jsonify({
        "message": "YouTube Analyzer API", 
        "status": "online",
        "version": "1.0"
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/analyze', methods=['POST'])
def analyze_video():
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                "success": False,
                "error": "URL do vídeo é obrigatória"
            }), 400
        
        video_url = data['url'].strip()
        logger.info(f"🔍 Analisando vídeo: {video_url}")
        
        # Validação básica da URL
        if not any(domain in video_url for domain in ['youtube.com', 'youtu.be']):
            return jsonify({
                "success": False,
                "error": "URL do YouTube inválida"
            }), 400
        
        # Analisa o vídeo
        resultado = resumidor.analisar_video(video_url)
        
        logger.info("✅ Análise concluída com sucesso")
        return jsonify({
            "success": True,
            "result": resultado
        })
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"❌ Erro na análise: {error_msg}")
        
        return jsonify({
            "success": False,
            "error": error_msg
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
