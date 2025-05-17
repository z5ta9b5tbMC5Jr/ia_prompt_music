from __future__ import annotations

import os

from dotenv import load_dotenv
import google.generativeai as genai

from ia_prompt_music.audio_processing.extractor import AudioFeatures

# Garantir que variáveis do .env estejam disponíveis
load_dotenv()

# ---------------------------------------------------------------------------
# Configurações via variáveis de ambiente (com valores padrão razoáveis)
# ---------------------------------------------------------------------------

OPENAI_API_KEY = os.getenv("GEMINI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("Variável de ambiente 'GEMINI_API_KEY' não encontrada. "
                           "Crie um arquivo .env baseado em .env.example.")

genai.configure(api_key=OPENAI_API_KEY)

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-pro")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "300"))
TEMP = float(os.getenv("TEMPERATURE", "0.7"))

# ---------------------------------------------------------------------------
# Template de prompt
# ---------------------------------------------------------------------------

PROMPT_TEMPLATE = """
Crie um prompt detalhado para compor uma nova música.
Características extraídas do áudio de referência:
• Duração: {duration:.1f} s
• BPM: {bpm:.0f}
• Tonalidade: {key}

Instruções:
1. Defina estilo musical, atmosfera e instrumentação adequados.
2. Sugira variações harmônicas e melódicas coerentes.
3. Proponha estrutura (intro, verso, refrão, ponte, etc.).
4. Seja objetivo, porém rico em detalhes técnicos.
"""

# ---------------------------------------------------------------------------
# Função principal
# ---------------------------------------------------------------------------

def generate_prompt(features: AudioFeatures) -> str:
    """Gera um prompt textual a partir das características do áudio."""

    user_prompt = PROMPT_TEMPLATE.format(
        duration=features.duration,
        bpm=features.bpm,
        key=features.key,
    )

    # Instancia o modelo Gemini
    try:
        _model = genai.GenerativeModel(MODEL_NAME)
    except Exception as exc:  # pylint: disable=broad-except
        raise RuntimeError(f"Falha ao carregar modelo '{MODEL_NAME}'. Verifique se o ID está correto e disponível na sua conta. Mensagem original: {exc}") from exc

    response = _model.generate_content(
        user_prompt,
        generation_config={
            "temperature": TEMP,
            "max_output_tokens": MAX_TOKENS,
        },
    )
    return response.text.strip() 