import numpy as np
import subprocess
import imageio_ffmpeg

class AudioSpectrumVisualizer:
    def __init__(self, audio_file: str, num_bars: int = 42, fps: int = 30):
        self.audio_file = audio_file
        self.num_bars = num_bars
        self.fps = fps
        self.sample_rate = 22050
        self.samples = self._load_pcm_mono()
        self.duration = len(self.samples) / self.sample_rate if len(self.samples) > 0 else 1.0
        self.total_frames = int(self.duration * fps)
        self.frame_bars = self._precompute_all_frames()

    def _load_pcm_mono(self) -> np.ndarray:
        """Extracts mono raw PCM 16-bit 22050Hz audio using ffmpeg."""
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        cmd = [
            ffmpeg_exe, "-i", self.audio_file,
            "-vn", "-ac", "1", "-ar", str(self.sample_rate),
            "-f", "s16le", "-"
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        raw_bytes = res.stdout
        if not raw_bytes:
            return np.zeros(self.sample_rate, dtype=np.float32)
        samples = np.frombuffer(raw_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        return samples

    def _precompute_all_frames(self) -> list[np.ndarray]:
        """Precomputes frequency spectrum bars for every video frame with smooth decay."""
        if len(self.samples) == 0:
            return [np.zeros(self.num_bars) for _ in range(self.total_frames)]

        window_size = 1024
        half_bars = self.num_bars // 2
        # Human vocal frequencies logarithmic spacing (80Hz to 4000Hz)
        freq_bins = np.logspace(np.log10(80), np.log10(4200), half_bars + 1)
        freq_indices = (freq_bins / (self.sample_rate / 2) * (window_size // 2)).astype(int)
        freq_indices = np.clip(freq_indices, 0, window_size // 2 - 1)

        prev_bars = np.zeros(half_bars)
        precomputed = []

        for frame_idx in range(self.total_frames):
            center_sample = int((frame_idx / self.fps) * self.sample_rate)
            start_s = max(0, center_sample - window_size // 2)
            end_s = min(len(self.samples), start_s + window_size)
            chunk = self.samples[start_s:end_s]

            if len(chunk) < window_size:
                chunk = np.pad(chunk, (0, window_size - len(chunk)))

            # Windowing function to prevent spectral leakage
            windowed = chunk * np.hanning(window_size)
            fft_vals = np.abs(np.fft.rfft(windowed))

            curr_half = np.zeros(half_bars)
            for b in range(half_bars):
                i_start = freq_indices[b]
                i_end = max(i_start + 1, freq_indices[b + 1])
                curr_half[b] = np.mean(fft_vals[i_start:i_end])

            # Apply vocal boost & scale
            curr_half = np.log1p(curr_half * 8.0) * 0.45
            curr_half = np.clip(curr_half, 0.0, 1.0)

            # Smooth attack and decay physics
            smoothed = np.where(
                curr_half > prev_bars,
                prev_bars * 0.35 + curr_half * 0.65,  # fast attack
                prev_bars * 0.82 + curr_half * 0.18   # smooth decay
            )
            prev_bars = smoothed

            # Create symmetric visualizer (mirrored left and right)
            # Low frequencies in the middle, high frequencies at the outer edges
            left_side = smoothed[::-1]
            right_side = smoothed
            if self.num_bars % 2 == 1:
                full_bars = np.concatenate([left_side, [smoothed[0]], right_side])
            else:
                full_bars = np.concatenate([left_side, right_side])

            precomputed.append(full_bars)

        return precomputed

    def get_bars_for_frame(self, frame_idx: int) -> np.ndarray:
        """Returns array of normalized bar heights (0.0 to 1.0) for the given frame."""
        if 0 <= frame_idx < len(self.frame_bars):
            return self.frame_bars[frame_idx]
        return np.zeros(self.num_bars)

if __name__ == "__main__":
    from agent.config import Config
    test_audio = str(Config.OUTPUT_DIR / "test_voice.mp3")
    viz = AudioSpectrumVisualizer(test_audio, num_bars=42, fps=30)
    print(f"Visualizer initialized: {viz.total_frames} frames, {viz.duration:.2f}s duration")
    bars = viz.get_bars_for_frame(30)
    print("Sample frame 30 bars (min, max, mean):", np.min(bars), np.max(bars), np.mean(bars))
