"""What kind of sound is playing, about once a second: laughter, screaming, speech, gunfire, music.

Uses Google's YAMNet audio classifier (521 AudioSet classes) through MediaPipe, on the laptop's CPU; 30
minutes of audio takes under a minute. In stream audio, gunfire and speech come through clearly. Laughter
scores stay low (rarely above 0.1) because game sound and music are mixed over the voices, so laughter is
used relative to the stream's own quiet level, not as an absolute score.
"""

import urllib.request
import wave

import numpy as np

from .config import ROOT
from .jobs import log

MODEL_URL = "https://storage.googleapis.com/mediapipe-models/audio_classifier/yamnet/float32/1/yamnet.tflite"
MODEL_PATH = ROOT / "models" / "yamnet.tflite"

GROUPS = {
    "laugh": ["Laughter", "Giggle", "Snicker", "Belly laugh", "Chuckle, chortle", "Baby laughter"],
    "scream": ["Screaming", "Shout", "Yell", "Battle cry", "Children shouting"],
    "speech": ["Speech", "Conversation", "Narration, monologue"],
    "gunfire": ["Gunshot, gunfire", "Machine gun", "Explosion", "Artillery fire", "Cap gun", "Fusillade"],
    "music": ["Music"],
}
CHUNK_S = 60


def model_path():
    if not MODEL_PATH.exists():
        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        log("sounds: downloading the YAMNet model (4 MB, first run only)")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    return MODEL_PATH


def analyse(wav_path):
    from mediapipe.tasks import python as mp_tasks
    from mediapipe.tasks.python import audio as mp_audio
    from mediapipe.tasks.python.components.containers import audio_data

    with wave.open(str(wav_path), "rb") as w:
        rate = w.getframerate()
        samples = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    options = mp_audio.AudioClassifierOptions(
        base_options=mp_tasks.BaseOptions(model_asset_path=str(model_path())),
        running_mode=mp_audio.RunningMode.AUDIO_CLIPS, max_results=-1)
    times, rows = [], []
    with mp_audio.AudioClassifier.create_from_options(options) as classifier:
        step = rate * CHUNK_S
        for offset in range(0, len(samples), step):
            clip = audio_data.AudioData.create_from_array(samples[offset:offset + step], rate)
            for result in classifier.classify(clip):
                scores = {c.category_name: c.score for c in result.classifications[0].categories}
                times.append(offset / rate + result.timestamp_ms / 1000)
                rows.append([max(scores.get(name, 0.0) for name in names) for names in GROUPS.values()])
    values = np.array(rows, dtype=np.float32).reshape(-1, len(GROUPS))
    features = {"t": np.array(times, dtype=np.float32)}
    features.update({group: values[:, i] for i, group in enumerate(GROUPS)})
    return features


def at(sounds, group, start, end):
    """The group's scores between start and end seconds."""
    t = sounds["t"]
    return sounds[group][(t >= start) & (t < end)]


def save(path, features):
    np.savez_compressed(path, **features)


def load(path):
    with np.load(path) as data:
        return {k: data[k] for k in data.files}
