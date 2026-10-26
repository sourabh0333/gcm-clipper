"""Audio signals every half second: loudness, gunfire-like bursts, and how far loudness rises above the
streamer's normal level (a proxy for shouting, hype and laughter)."""

import wave

import numpy as np

SUB_S = 0.01      # 10 ms energy frames
BURST_RATIO = 6   # a frame this many times louder than the 50 ms before it counts as a burst
BURST_FLOOR = 1e-4


def rolling_robust_z(x, window):
    """How unusual each value is compared with the surrounding `window` values (median and MAD)."""
    if len(x) == 0:
        return x
    half = window // 2
    # Reflect rather than repeat the edge values, which skewed the median and made the first and last
    # seconds of a section look unusually loud.
    padded = np.pad(x, (half, half), mode="reflect" if len(x) > half else "edge")
    view = np.lib.stride_tricks.sliding_window_view(padded, 2 * half + 1)
    med = np.median(view, axis=1)
    mad = np.median(np.abs(view - med[:, None]), axis=1)
    return (x - med) / (1.4826 * mad + 1e-6)


def smooth(x, n):
    if n <= 1 or len(x) == 0:
        return x
    return np.convolve(x, np.ones(n) / n, mode="same")


def analyse(wav_path, hop_s=0.5):
    with wave.open(str(wav_path), "rb") as w:
        if w.getnchannels() != 1 or w.getsampwidth() != 2:
            raise ValueError("expected mono 16-bit audio")
        sr = w.getframerate()
        hop, sub = int(sr * hop_s), int(sr * SUB_S)
        loud, bursts = [], []
        tail = np.full(5, 1e-10)
        while True:
            raw = w.readframes(hop)
            x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
            n = len(x) // sub
            if n == 0:
                break
            e = (x[: n * sub].reshape(n, sub) ** 2).mean(axis=1) + 1e-10
            loud.append(10 * np.log10(e.mean()))
            ctx = np.concatenate([tail, e])
            before = np.convolve(ctx, np.ones(5) / 5, mode="valid")[:n]
            bursts.append(int(((e > BURST_RATIO * before) & (e > BURST_FLOOR)).sum()))
            tail = ctx[-5:]

    loud = np.array(loud, dtype=np.float32)
    bursts = np.array(bursts, dtype=np.float32)
    t = np.arange(len(loud), dtype=np.float32) * hop_s
    excitement = rolling_robust_z(loud, int(120 / hop_s)).astype(np.float32)
    action = smooth(bursts, int(2 / hop_s)).astype(np.float32)
    return {"t": t, "loudness": loud, "bursts": bursts, "action": action, "excitement": excitement}


def save(path, features):
    np.savez_compressed(path, **features)


def load(path):
    with np.load(path) as data:
        return {k: data[k] for k in data.files}
