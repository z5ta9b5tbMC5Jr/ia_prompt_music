from __future__ import annotations

from dataclasses import dataclass
from typing import List

import librosa
import numpy as np

__all__ = [
    "AudioFeatures",
    "analyse_audio",
]


@dataclass
class AudioFeatures:
    """Estrutura com as principais características extraídas do áudio."""

    duration: float  # duração em segundos
    bpm: float  # batidas por minuto
    key: str  # tonalidade estimada (ex: "C", "G#")
    instruments: List[str] | None = None  # reservado para futuras detecções

    def __post_init__(self):
        # Evite None em listas mutáveis
        if self.instruments is None:
            self.instruments = []


NOTE_NAMES = [
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B",
]


def _estimate_key(y: np.ndarray, sr: int) -> str:
    """Estimativa simples de tonalidade via cromagrama.

    A técnica assume que a nota com maior energia média no cromagrama indica
    a tonalidade principal. Métodos mais robustos podem ser adotados no futuro.
    """

    # Cromagrama Constant-Q transform – adequado para análise harmônica
    chroma_cq = librosa.feature.chroma_cqt(y=y, sr=sr)
    # Energia média por classe de nota
    chroma_mean = chroma_cq.mean(axis=1)
    note_idx = int(np.argmax(chroma_mean))
    return NOTE_NAMES[note_idx]


def analyse_audio(path: str) -> AudioFeatures:
    """Carrega o arquivo e retorna um objeto ``AudioFeatures``.

    Parameters
    ----------
    path: str
        Caminho para o arquivo de áudio (MP3, WAV, etc.).
    """

    # Carrega mantendo a taxa original (sr=None)
    y, sr = librosa.load(path, sr=None, mono=True)

    # Duração total (segundos)
    duration = float(librosa.get_duration(y=y, sr=sr))

    # Detecção de BPM (tempo)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    # Estimativa de tonalidade principal
    key = _estimate_key(y, sr)

    return AudioFeatures(duration=duration, bpm=float(tempo), key=key) 