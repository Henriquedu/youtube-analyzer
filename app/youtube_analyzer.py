from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import re
import logging

logger = logging.getLogger(__name__)

class YouTubeResumidor:
    def __init__(self):
        self.transcript_languages = ['pt', 'pt-BR', 'en', 'es']
    
    def extract_video_id(self, url):
        """Extrai o ID do vídeo da URL"""
        try:
            if 'v=' in url:
                return url.split('v=')[1].split('&')[0]
            elif 'youtu.be/' in url:
                return url.split('youtu.be/')[1].split('?')[0]
            else:
                return url.split('/')[-1]
        except:
            raise Exception("Não foi possível extrair o ID do vídeo")
    
    def pegar_transcricao_completa(self, url_video):
        """Pega a transcrição completa do vídeo"""
        try:
            video_id = self.extract_video_id(url_video)
            logger.info(f"📝 Buscando transcrição para vídeo: {video_id}")
            
            # Tenta diferentes idiomas
            for lang in self.transcript_languages:
                try:
                    transcricao = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
                    logger.info(f"✅ Transcrição encontrada em {lang}")
                    
                    texto_completo = ' '.join([item['text'] for item in transcricao])
                    if texto_completo.strip():
                        return texto_completo
                except:
                    continue
            
            raise Exception("Transcrição não disponível para este vídeo")
            
        except Exception as e:
            if "transcript" in str(e).lower():
                raise Exception("Este vídeo não possui transcrição disponível")
            raise Exception(f"Erro ao obter transcrição: {str(e)}")
    
    def limpar_texto(self, texto):
        """Limpa e prepara o texto para sumarização"""
        if not texto:
            return ""
            
        # Remove marcadores de áudio
        texto = re.sub(r'\[.*?\]', '', texto)
        texto = re.sub(r'\(.*?\)', '', texto)
        texto = re.sub(r'\s+', ' ', texto)
        return texto.strip()
    
    def resumir_texto_inteligente(self, texto):
        """Faz um resumo inteligente do conteúdo"""
        if not texto:
            return "Não foi possível gerar resumo."
        
        # Divide em frases
        frases = [f.strip() for f in texto.split('.') if f.strip()]
        
        if len(frases) <= 6:
            return texto + '.' if not texto.endswith('.') else texto
        
        # Estratégia: início (contexto), meio (conteúdo), fim (conclusão)
        total_frases = len(frases)
        
        # Primeiras frases (contexto)
        frases_selecionadas = frases[:2]
        
        # Frases do meio (conteúdo principal)
        if total_frases > 8:
            meio = total_frases // 2
            frases_selecionadas.extend(frases[meio-1:meio+2])
        
        # Últimas frases (conclusão)
        frases_selecionadas.extend(frases[-3:])
        
        # Remove duplicatas e junta
        frases_unicas = []
        for frase in frases_selecionadas:
            if frase and frase not in frases_unicas:
                frases_unicas.append(frase)
        
        resumo = '. '.join(frases_unicas)
        return resumo + '.' if not resumo.endswith('.') else resumo
    
    def analisar_video(self, url_video):
        """Analisa o vídeo e retorna dados formatados"""
        # Pega informações do vídeo
        try:
            yt = YouTube(url_video)
            video_info = {
                'titulo': yt.title or 'Título não disponível',
                'canal': yt.author or 'Canal não disponível',
                'duracao': f"{yt.length // 60}min {yt.length % 60}seg" if yt.length else 'N/A',
                'visualizacoes': f"{yt.views:,}" if yt.views else 'N/A',
                'thumbnail': yt.thumbnail_url
            }
        except Exception as e:
            logger.warning(f"⚠️ Erro ao obter info do vídeo: {e}")
            video_info = {
                'titulo': 'Título não disponível',
                'canal': 'Canal não disponível',
                'duracao': 'N/A',
                'visualizacoes': 'N/A',
                'thumbnail': None
            }
        
        # Pega e processa a transcrição
        transcricao = self.pegar_transcricao_completa(url_video)
        texto_limpo = self.limpar_texto(transcricao)
        
        # Gera o resumo
        resumo = self.resumir_texto_inteligente(texto_limpo)
        
        return {
            'video_info': video_info,
            'resumo': resumo,
            'tamanho_transcricao': len(texto_limpo),
            'palavras': len(texto_limpo.split())
        }
