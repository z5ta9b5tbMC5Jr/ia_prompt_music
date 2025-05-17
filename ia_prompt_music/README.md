# IA Prompt Music 🎵

Aplicação em Python que gera prompts detalhados para composição musical a partir de faixas de áudio MP3.

## Requisitos

* Python 3.9+
* FFmpeg disponível no PATH (necessário para `pydub`)

## Instalação

```bash
# clone ou copie o projeto
cd ia_prompt_music
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Caso pretenda gerar áudio com modelos locais (MusicGen, etc.), será necessário instalar PyTorch e demais dependências extras.

# copie o arquivo de variáveis de ambiente
copy .env.example .env  # Linux/macOS: cp .env.example .env
# edite .env e insira sua chave GEMINI_API_KEY
```

## Variáveis de ambiente

Adicione um arquivo `.env` (baseado em `.env.example`) com sua chave Google Gemini e o modelo desejado:

```dotenv
GEMINI_API_KEY=SEU_TOKEN
GEMINI_MODEL=gemini-1.5-flash   # ou gemini-pro, text-bison-001, etc.
MAX_TOKENS=300
TEMPERATURE=0.7
```

## Execução

```bash
python -m ia_prompt_music.gui.main_window
```

Na interface, clique em "Carregar MP3", escolha um arquivo e aguarde o prompt ser gerado.

## Estrutura

```
ia_prompt_music/
├─ audio_processing/
│  └─ extractor.py           # extração de BPM, tonalidade, etc.
├─ prompt_generation/
│  └─ generator.py           # integração com Google Gemini
├─ gui/
│  └─ main_window.py         # interface Tkinter
├─ requirements.txt
└─ README.md
```