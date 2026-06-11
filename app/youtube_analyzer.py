import logging
import re
from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import YouTubeTranscriptApi

logger = logging.getLogger(__name__)


class YouTubeResumidor:
    def __init__(self):
        self.transcript_languages = ["pt", "pt-BR", "en", "es"]

    def extract_video_id(self, url):
        parsed_url = urlparse(url)

        if parsed_url.hostname in ["www.youtube.com", "youtube.com", "m.youtube.com"]:
            if parsed_url.path == "/watch":
                video_id = parse_qs(parsed_url.query).get("v", [None])[0]

                if video_id:
                    return video_id

            path_patterns = [r"/shorts/([^/?]+)", r"/embed/([^/?]+)", r"/live/([^/?]+)"]

            for pattern in path_patterns:
                match = re.search(pattern, parsed_url.path)

                if match:
                    return match.group(1)

        if parsed_url.hostname in ["youtu.be", "www.youtu.be"]:
            video_id = parsed_url.path.strip("/")

            if video_id:
                return video_id

        raise ValueError("URL do YouTube inválida ou não reconhecida.")

    def pegar_transcricao_completa(self, url_video):
        video_id = self.extract_video_id(url_video)
        logger.info("Buscando transcrição para vídeo: %s", video_id)

        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        for language in self.transcript_languages:
            try:
                transcript = transcript_list.find_transcript([language])
                transcript_items = transcript.fetch()
                return self.formatar_transcricao(transcript_items), language
            except Exception:
                continue

        try:
            generated_transcript = transcript_list.find_generated_transcript(self.transcript_languages)
            transcript_items = generated_transcript.fetch()
            return self.formatar_transcricao(transcript_items), generated_transcript.language_code
        except Exception as error:
            logger.warning("Transcrição não encontrada: %s", error)

        raise ValueError("Este vídeo não possui transcrição pública disponível.")

    def formatar_transcricao(self, transcript_items):
        linhas = []

        for item in transcript_items:
            segundos = int(item.get("start", 0))
            minuto = segundos // 60
            segundo = segundos % 60
            texto = item.get("text", "").replace("\n", " ").strip()

            if texto:
                linhas.append({
                    "tempo": f"{minuto:02d}:{segundo:02d}",
                    "texto": texto,
                })

        return linhas

    def limpar_texto(self, linhas_transcricao):
        texto = " ".join(item["texto"] for item in linhas_transcricao)
        texto = re.sub(r"\[.*?\]", "", texto)
        texto = re.sub(r"\(.*?\)", "", texto)
        texto = re.sub(r"\s+", " ", texto)

        return texto.strip()

    def dividir_frases(self, texto):
        frases = re.split(r"(?<=[.!?])\s+", texto)
        return [frase.strip() for frase in frases if frase.strip()]

    def gerar_resumo(self, texto):
        frases = self.dividir_frases(texto)

        if not frases:
            return "Não foi possível gerar um resumo para este vídeo."

        if len(frases) <= 12:
            return " ".join(frases)

        total = len(frases)
        inicio = frases[:4]
        meio_inicio = max((total // 2) - 3, 0)
        meio = frases[meio_inicio:meio_inicio + 6]
        fim = frases[-5:]

        frases_resumo = list(dict.fromkeys(inicio + meio + fim))
        return " ".join(frases_resumo)

    def gerar_topicos(self, texto):
        frases = self.dividir_frases(texto)
        palavras_chave = [
            "importante", "principal", "problema", "solução", "exemplo", "resultado",
            "conclusão", "objetivo", "explica", "mostra", "precisa", "deve"
        ]

        topicos = []

        for frase in frases:
            frase_lower = frase.lower()

            if any(palavra in frase_lower for palavra in palavras_chave):
                topicos.append(frase)

            if len(topicos) == 6:
                break

        if len(topicos) < 4:
            topicos.extend(frases[:6 - len(topicos)])

        return list(dict.fromkeys(topicos))[:6]

    def gerar_conclusao(self, texto):
        frases = self.dividir_frases(texto)

        if not frases:
            return "Não foi possível identificar uma conclusão."

        conclusao = " ".join(frases[-4:])
        return conclusao

    def analisar_video(self, url_video):
        linhas_transcricao, idioma = self.pegar_transcricao_completa(url_video)
        texto_limpo = self.limpar_texto(linhas_transcricao)

        return {
            "resumo": self.gerar_resumo(texto_limpo),
            "topicos": self.gerar_topicos(texto_limpo),
            "conclusao": self.gerar_conclusao(texto_limpo),
            "idioma_transcricao": idioma,
            "total_palavras": len(texto_limpo.split()),
            "tamanho_transcricao": len(texto_limpo),
            "transcricao": linhas_transcricao,
        }
