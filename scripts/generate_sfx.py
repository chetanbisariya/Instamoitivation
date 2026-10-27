import math
import os
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

def generate_cinematic_sfx(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    sr = 44100

    # 1. SFX Whoosh Transition (1.2s)
    # Swept noise bandpass from 200Hz -> 2800Hz -> 300Hz
    dur_whoosh = 1.2
    t = np.linspace(0, dur_whoosh, int(sr * dur_whoosh), False)
    noise = np.random.normal(0, 0.4, len(t))
    # Gaussian amplitude envelope
    env = np.exp(-((t - dur_whoosh * 0.45) ** 2) / (2 * (0.22 ** 2)))
    # Swept sine sub-layer
    sweep_freq = 80 + 260 * np.sin(np.pi * (t / dur_whoosh))
    sweep_phase = 2 * np.pi * np.cumsum(sweep_freq) / sr
    sub_layer = 0.3 * np.sin(sweep_phase) * env
    whoosh = (noise * env * 0.7 + sub_layer)
    whoosh = np.clip(whoosh, -0.95, 0.95)
    wav_whoosh = (whoosh * 32767).astype(np.int16)
    wavfile.write(os.path.join(output_dir, "sfx_whoosh.wav"), sr, wav_whoosh)
    print("Generated: sfx_whoosh.wav")

    # 2. SFX Sub-Bass Boom / Impact Drop (2.0s)
    # 48Hz deep exponential decay boom
    dur_sub = 2.0
    t_sub = np.linspace(0, dur_sub, int(sr * dur_sub), False)
    decay = np.exp(-t_sub * 3.2)
    # Pitch drop from 68Hz down to 36Hz
    freq_sub = 36 + 32 * np.exp(-t_sub * 8.0)
    phase_sub = 2 * np.pi * np.cumsum(freq_sub) / sr
    sub_boom = np.sin(phase_sub) * decay * 0.85
    # 2nd harmonic for warmth
    sub_boom += 0.25 * np.sin(phase_sub * 2.0) * decay * np.exp(-t_sub * 5.0)
    sub_boom = np.clip(sub_boom, -0.95, 0.95)
    wav_sub = (sub_boom * 32767).astype(np.int16)
    wavfile.write(os.path.join(output_dir, "sfx_sub_bass.wav"), sr, wav_sub)
    print("Generated: sfx_sub_bass.wav")

    # 3. SFX Cinematic Tension Riser (2.5s)
    dur_riser = 2.5
    t_riser = np.linspace(0, dur_riser, int(sr * dur_riser), False)
    env_riser = (t_riser / dur_riser) ** 2.2
    freq_riser = 60 + 380 * (t_riser / dur_riser) ** 1.8
    phase_riser = 2 * np.pi * np.cumsum(freq_riser) / sr
    noise_shimmer = np.random.normal(0, 0.15, len(t_riser)) * env_riser
    riser = (0.6 * np.sin(phase_riser) + 0.3 * np.sin(phase_riser * 1.5) + noise_shimmer) * env_riser
    riser = np.clip(riser, -0.95, 0.95)
    wav_riser = (riser * 32767).astype(np.int16)
    wavfile.write(os.path.join(output_dir, "sfx_riser.wav"), sr, wav_riser)
    print("Generated: sfx_riser.wav")

    # 4. SFX Cinematic Impact Hit (2.2s)
    dur_hit = 2.2
    t_hit = np.linspace(0, dur_hit, int(sr * dur_hit), False)
    env_hit = np.exp(-t_hit * 3.8)
    initial_click = np.random.normal(0, 0.8, len(t_hit)) * np.exp(-t_hit * 40.0)
    hit_sub = np.sin(2 * np.pi * 50 * t_hit) * env_hit * 0.75
    hit_metal = np.sin(2 * np.pi * 180 * t_hit) * np.exp(-t_hit * 12.0) * 0.3
    impact = initial_click + hit_sub + hit_metal
    impact = np.clip(impact, -0.95, 0.95)
    wav_hit = (impact * 32767).astype(np.int16)
    wavfile.write(os.path.join(output_dir, "sfx_impact.wav"), sr, wav_hit)
    print("Generated: sfx_impact.wav")

if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets" / "sfx"
    generate_cinematic_sfx(str(out))
