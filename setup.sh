#!/usr/bin/env bash
# 클라우드 세션/새 머신에서 렌더링 환경을 만든다 (Debian/Ubuntu, root 또는 sudo).
set -euo pipefail
cd "$(dirname "$0")"

export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq --no-install-recommends \
  ffmpeg libcairo2-dev libpango1.0-dev pkg-config python3-dev python3-venv build-essential \
  fonts-noto-cjk fonts-nanum \
  texlive-latex-base texlive-latex-extra texlive-fonts-recommended texlive-science texlive-lang-korean dvisvgm
fc-cache -f

# Debian 시스템 pip은 srt 휠 빌드가 깨지므로 venv를 쓴다.
python3 -m venv /opt/manim-venv
/opt/manim-venv/bin/pip install -q -U pip setuptools wheel
/opt/manim-venv/bin/pip install -q -r requirements.txt

# 한국어 TTS 모델 (GitHub 릴리스; huggingface.co 가 막힌 환경에서도 받아진다)
if [ ! -f tts_models/vits-mimic3-ko_KO-kss_low/ko_KO-kss_low.onnx ]; then
  mkdir -p tts_models
  curl -sSL -o /tmp/ko.tar.bz2 \
    https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-mimic3-ko_KO-kss_low.tar.bz2
  tar xjf /tmp/ko.tar.bz2 -C tts_models && rm /tmp/ko.tar.bz2
fi
echo "setup done. render with: ./render.sh"
