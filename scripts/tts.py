"""대본의 각 세그먼트를 음성 파일로 만들고 길이를 output/audio/durations.json에 기록한다.

TTS 백엔드를 바꾸려면 synth() 하나만 교체하면 된다 (허깅페이스 보이스 클로닝 모델 등).
"""
import json
import os
import sys

import sherpa_onnx
import soundfile as sf

sys.path.insert(0, os.path.dirname(__file__))
from narration import SEGMENTS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(ROOT, "tts_models", "vits-mimic3-ko_KO-kss_low")
OUT_DIR = os.path.join(ROOT, "output", "audio")
SPEED = 1.08  # 인강 템포. 1.0이 기본.


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


def synth(tts, text, path):
    audio = tts.generate(text, sid=0, speed=SPEED)
    sf.write(path, audio.samples, audio.sample_rate)
    return len(audio.samples) / audio.sample_rate


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    tts = load_tts()
    durations = {}
    for seg in SEGMENTS:
        path = os.path.join(OUT_DIR, f"{seg['id']}.wav")
        durations[seg["id"]] = synth(tts, seg["say"], path)
        print(f"{seg['id']:>8}: {durations[seg['id']]:5.2f}s")
    with open(os.path.join(OUT_DIR, "durations.json"), "w") as f:
        json.dump(durations, f, indent=2)
    print(f"total {sum(durations.values()):.1f}s")


if __name__ == "__main__":
    main()
