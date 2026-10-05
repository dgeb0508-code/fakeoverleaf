#!/usr/bin/env bash
# 대본 -> 음성 -> manim 렌더. 사용: ./render.sh math12 | ./render.sh physics
set -euo pipefail
cd "$(dirname "$0")"
PY=/opt/manim-venv/bin/python
case "${1:-math12}" in
  math12)  NARR=narration_math12;  SCENE=scenes/csat2024_math12.py; CLASS=Csat2024Math12; OUT=csat2024_math12 ;;
  physics) NARR=narration_physics; SCENE=scenes/kinematics_short.py; CLASS=KinematicsShort; OUT=kinematics_short ;;
  *) echo "unknown target: $1"; exit 1 ;;
esac
$PY scripts/tts.py $NARR output/audio/${1:-math12}
$PY -m manim -qm $SCENE $CLASS
cp media/videos/$(basename ${SCENE%.py})/1920p30/$CLASS.mp4 output/$OUT.mp4
echo "-> output/$OUT.mp4"
