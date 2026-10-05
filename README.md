# 수능 물리 숏폼 (manim + TTS)

수능·평가원 유형 물리 문제를 manim 세로 영상(1080×1920)으로 풀이하고, 한국어 TTS 나레이션을 자동으로 싱크한다.

## 구조

| 경로 | 역할 |
|---|---|
| `scripts/narration.py` | 대본. 세그먼트마다 `say`(TTS가 읽는 문장, 숫자는 한글)와 `caption`(화면 자막) |
| `scripts/tts.py` | 세그먼트별 wav 생성, 길이를 `output/audio/durations.json`에 기록 |
| `scenes/kinematics_short.py` | manim 씬. 각 세그먼트의 애니메이션을 오디오 길이에 비례 배분 |
| `setup.sh` | apt(한글 폰트, TeX Live + kotex, cairo/pango) + venv + TTS 모델 다운로드 |
| `render.sh` | TTS → 렌더 → `output/kinematics_short.mp4` |

## 사용

```bash
./setup.sh     # 최초 1회
./render.sh
```

## 싱크 방식

`Scene.segment(seg_id, steps)` 가 오디오를 `add_sound` 로 깔고 자막을 띄운 뒤,
`steps = [(애니메이션 목록, 가중치), ...]` 를 오디오 길이에 비례해 `run_time` 으로 나눠 재생한다.
대본을 고치면 음성 길이가 바뀌고 애니메이션이 자동으로 따라간다.

## TTS 교체

`scripts/tts.py` 의 `synth()` 만 바꾸면 된다. 현재는 sherpa-onnx + VITS(KSS, 여성 음성)이며 CPU에서 실시간의 10배 이상 속도로 돈다.
허깅페이스 보이스 클로닝 모델(본인 음성 파인튜닝)로 바꾸려면 해당 모델을 받아 `synth()` 에서 호출하고 wav를 같은 경로에 쓰면 된다.

## 첫 영상

`output/kinematics_short.mp4` (77초). 등가속도 운동에서 "구간 평균 속도 = 구간 중간 시각의 순간 속도" 로
공식 연립 없이 v-t 그래프에 점 두 개를 찍어 푸는 평가원 유형 문항.
문항은 평가원 원문이 아니라 같은 유형으로 재구성한 것이다 (이 작업 환경에서 kice.re.kr 접근이 막혀 원문을 가져올 수 없었음).
