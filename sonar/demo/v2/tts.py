"""Text-to-speech with Kokoro (open-weight model, Apache-2.0), fully offline.

python tts.py "<text>" <out.wav> [voice] [speed]
Model files live in %LOCALAPPDATA%/kokoro (kokoro-v1.0.onnx, voices-v1.0.bin).
"""
import os, sys
from pathlib import Path
import numpy as np
import soundfile as sf

MODEL = Path(os.environ["LOCALAPPDATA"]) / "kokoro"
VOICE = "af_heart"
SPEED = 0.95
_k = None

# words the model reads badly -> how to say them
SAY = {"SonarQube": "Sonar Cube", "sonarqube": "sonar cube", "DomiAffaire": "Domi Affaire", ".env": "dot env",
       "localhost": "local host", "PostgreSQL": "Postgres Q L", "JWT": "J W T", "XSS": "X S S", "CWE": "C W E",
       "YAML": "yaml", "TypeScript": "TypeScript", "MongoDB": "Mongo D B", "--rm": "dash dash R M"}


def speakable(text):
    for a, b in SAY.items():
        text = text.replace(a, b)
    return text


def synth(text, out, voice=VOICE, speed=SPEED):
    global _k
    if _k is None:
        from kokoro_onnx import Kokoro
        _k = Kokoro(str(MODEL / "kokoro-v1.0.onnx"), str(MODEL / "voices-v1.0.bin"))
    samples, sr = _k.create(speakable(text), voice=voice, speed=speed, lang="en-us")
    samples = np.asarray(samples, dtype=np.float32)
    peak = float(np.max(np.abs(samples))) or 1.0
    samples = samples / peak * 0.89          # normalise
    sf.write(str(out), samples, sr)
    return len(samples) / sr


if __name__ == "__main__":
    v = sys.argv[3] if len(sys.argv) > 3 else VOICE
    s = float(sys.argv[4]) if len(sys.argv) > 4 else SPEED
    print(f"{synth(sys.argv[1], sys.argv[2], v, s):.2f}s")
