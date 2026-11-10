"""Make the studio's sound effects (assets/sfx/*.wav) from scratch with ffmpeg's generators.

    python make_sfx.py

They are synthesised here (noise sweeps, decaying tones), not taken from any library, so no one owns them
and they can never match anything in YouTube's Content ID (M3 plan S-R9: "no added track can cause a
claim"). Short, mono, 48 kHz."""

import subprocess
from pathlib import Path

from aigcm.media import tool

OUT = Path(__file__).resolve().parent / "assets" / "sfx"

# name: (lavfi source, filter chain)
SOUNDS = {
    # a rising swoosh: pink noise through a band-pass sweeping up, faded in and out
    "whoosh": ("anoisesrc=color=pink:amplitude=0.6:d=0.7:r=48000",
               "bandpass=f=900:width_type=o:w=1.2,volume='0.2+1.6*t':eval=frame,afade=t=in:d=0.25,afade=t=out:st=0.45:d=0.25,volume=14dB"),
    # a deep hit: a 55 Hz tone, low-passed, decaying fast
    "boom": ("sine=f=55:d=0.9:r=48000",
             "volume='3*exp(-5*t)':eval=frame,lowpass=f=180,afade=t=out:st=0.6:d=0.3,volume=4.5dB"),
    # a bright bell for a chicken dinner or a marked moment
    "ding": ("sine=f=1320:d=0.8:r=48000",
             "volume='0.8*exp(-6*t)':eval=frame,afade=t=out:st=0.6:d=0.2,volume=16dB"),
    # a short pop for text or a cut
    "pop": ("sine=f=600:d=0.12:r=48000",
            "volume='1.2*exp(-30*t)':eval=frame,highpass=f=200,volume=12dB"),
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (source, chain) in SOUNDS.items():
        subprocess.run([tool("ffmpeg"), "-v", "error", "-y", "-f", "lavfi", "-i", source, "-af",
                        chain + ",alimiter=limit=0.9", "-ac", "1", "-ar", "48000", "-c:a", "pcm_s16le",
                        str(OUT / f"{name}.wav")], check=True)
        print("made", name)


if __name__ == "__main__":
    main()
