import logging
import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from youtube_analyzer import YouTubeResumidor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

resumidor = YouTubeResumidor()


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "YouTube Analyzer API",
        "status": "online",
        "version": "2.0",
        "endpoints": {
            "health": "/health",
            "analyze": "/analyze"
        }
    }), 200


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "success": True,
        "status": "healthy"
    }), 200


@app.route("/analyze", methods=["POST"])
def analyze_video():
    try:
        data = request.get_json(silent=True)

        if not data or not data.get("url"):
            return jsonify({
                "success": False,
                "error": "Informe a URL do vídeo."
            }), 400

        video_url = data["url"].strip()

        if "youtube.com" not in video_url and "youtu.be" not in video_url:
            return jsonify({
                "success": False,
                "error": "Informe uma URL válida do YouTube."
            }), 400

        logger.info("Analisando vídeo: %s", video_url)
        resultado = resumidor.analisar_video(video_url)

        return jsonify({
            "success": True,
            "result": resultado
        }), 200

    except ValueError as error:
        logger.warning("Erro de validação: %s", error)
        return jsonify({
            "success": False,
            "error": str(error)
        }), 400

    except Exception as error:
        logger.exception("Erro inesperado na análise")
        return jsonify({
            "success": False,
            "error": "Não foi possível analisar este vídeo no momento. Tente outro vídeo com transcrição disponível.",
            "details": str(error)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
