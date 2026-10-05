"""대본 모듈의 세그먼트를 음성 파일로 만들고 길이를 durations.json에 기록한다.

사용: python scripts/tts.py narration_math12 output/audio/math12
TTS 백엔드를 바꾸려면 synth_sentence() 하나만 교체하면 된다.
"""
import importlib
import json
import os
import re
import sys

import numpy as np
import sherpa_onnx
import soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(ROOT, "tts_models", "vits-mimic3-ko_KO-kss_low")
SPEED = 1.0
SENTENCE_GAP = 0.25   # 문장 사이 무음(초)
COMMA_GAP = 0.12


def load_tts():
    cfg = sherpa_onnx.OfflineTtsConfig(
        model=sherpa_onnx.OfflineTtsModelConfig(
            vits=sherpa_onnx.OfflineTtsVitsModelConfig(
                model=os.path.join(MODEL_DIR, "ko_KO-kss_low.onnx"),
                tokens=os.path.join(MODEL_DIR, "tokens.txt"),
                data_dir=os.path.join(MODEL_DIR, "espeak-ng-data"),
            ),
            num_threads=4,
        )
    )
    return sherpa_onnx.OfflineTts(cfg)


def synth_sentence(tts, text):
    """한 문장 -> (samples, sample_rate)"""
    audio = tts.generate(text, sid=0, speed=SPEED)
    return np.asarray(audio.samples, dtype=np.float32), audio.sample_rate


def synth(tts, text, path):
    """문장 단위로 합성하고 사이에 무음을 넣어 이어 붙인다. 길이(초)를 돌려준다."""
    parts = []
    sr = None
    for sentence in re.split(r"(?<=[.?!])\s+", text.strip()):
        if not sentence:
            continue
        chunks = [c.strip() for c in sentence.split(",") if c.strip()]
        for i, chunk in enumerate(chunks):
            samples, sr = synth_sentence(tts, chunk)
            parts.append(samples)
            parts.append(np.zeros(int(sr * (COMMA_GAP if i < len(chunks) - 1 else SENTENCE_GAP)), np.float32))
    wav = np.concatenate(parts)
    wav = wav / max(np.abs(wav).max(), 1e-6) * 0.9   # 피크 정규화
    sf.write(path, wav, sr)
    return len(wav) / sr


def main():
    module, out_dir = sys.argv[1], sys.argv[2]
    sys.path.insert(0, os.path.dirname(__file__))
    segments = importlib.import_module(module).SEGMENTS
    os.makedirs(out_dir, exist_ok=True)
    tts = load_tts()
    durations = {}
    for seg in segments:
        durations[seg["id"]] = synth(tts, seg["say"], os.path.join(out_dir, f"{seg['id']}.wav"))
        print(f"{seg['id']:>8}: {durations[seg['id']]:5.2f}s")
    with open(os.path.join(out_dir, "durations.json"), "w") as f:
        json.dump(durations, f, indent=2)
    print(f"total {sum(durations.values()):.1f}s")


if __name__ == "__main__":
    main()
