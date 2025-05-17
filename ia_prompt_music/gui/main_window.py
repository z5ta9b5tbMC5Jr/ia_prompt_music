from __future__ import annotations

import threading
import tkinter as tk
from tkinter import filedialog, messagebox

from ia_prompt_music.audio_processing.extractor import analyse_audio, AudioFeatures
from ia_prompt_music.prompt_generation.generator import generate_prompt


class App(tk.Tk):
    """Janela principal do gerador de prompts a partir de áudio."""

    def __init__(self) -> None:
        super().__init__()

        self.title("Gerador de Prompts – IA")
        self.geometry("700x500")
        self._build_ui()

    # ---------------------------------------------------------------------
    # Construção de interface
    # ---------------------------------------------------------------------

    def _build_ui(self) -> None:
        tk.Button(self, text="Carregar MP3", command=self._on_load).pack(pady=15)

        self.lbl_info_var = tk.StringVar(value="Nenhum arquivo carregado.")
        tk.Label(self, textvariable=self.lbl_info_var).pack()

        # Caixa de texto para exibir prompt
        self.txt_prompt = tk.Text(self, height=20, wrap="word")
        self.txt_prompt.pack(fill="both", expand=True, padx=15, pady=15)

    # ------------------------------------------------------------------
    # Handlers
    # ------------------------------------------------------------------

    def _on_load(self) -> None:
        """Abre diálogo para seleção de arquivo e inicia processamento."""
        path = filedialog.askopenfilename(filetypes=[("Arquivos MP3", "*.mp3")])
        if not path:
            return

        self.lbl_info_var.set("Processando… Aguarde…")
        self.txt_prompt.delete("1.0", tk.END)

        # Processamento em thread separada para não travar GUI
        thread = threading.Thread(target=self._process_file, args=(path,), daemon=True)
        thread.start()

    def _process_file(self, path: str) -> None:
        try:
            features: AudioFeatures = analyse_audio(path)
            prompt: str = generate_prompt(features)
            self._display_result(features, prompt)
        except Exception as exc:  # pylint: disable=broad-except
            self._show_error(exc)

    def _display_result(self, features: AudioFeatures, prompt: str) -> None:
        """Atualiza GUI com resultados (executado no thread principal)."""
        info_text = f"Duração: {features.duration:.1f}s – {features.bpm:.0f} BPM – {features.key}"
        self.after(0, lambda: (
            self.lbl_info_var.set(info_text),
            self.txt_prompt.insert(tk.END, prompt),
        ))

    def _show_error(self, exc: Exception) -> None:
        self.after(0, lambda: messagebox.showerror("Erro", str(exc)))


if __name__ == "__main__":
    App().mainloop() 