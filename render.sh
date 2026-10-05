#!/usr/bin/env bash
# 대본 -> 음성 -> manim 렌더 -> output/kinematics_short.mp4
set -euo pipefail
cd "$(dirname "$0")"
PY=/opt/manim-venv/bin/python
$PY scripts/tts.py
$PY -m manim -qm scenes/kinematics_short.py KinematicsShort
cp media/videos/kinematics_short/1920p30/KinematicsShort.mp4 output/kinematics_short.mp4
echo "-> output/kinematics_short.mp4"
