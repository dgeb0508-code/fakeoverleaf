# 수능 물리 숏폼 (manim + TTS)

수능·평가원 유형 물리 문제를 manim 세로 영상(1080×1920)으로 풀이하고, 한국어 TTS 나레이션을 자동으로 싱크한다.

## 구조

| 경로 | 역할 |
|---|---|
| `scripts/narration_*.py` | 대본. 세그먼트마다 `say`(TTS가 읽는 문장, 수식은 한글로)와 `caption`(화면 자막) |
| `scripts/tts.py` | 문장 단위로 합성하고 사이에 무음을 넣어 wav 생성, 길이를 `durations.json`에 기록 |
| `scenes/csat2024_math12.py` | 2024학년도 수능 수학 12번 씬 (현재 메인) |
| `scenes/kinematics_short.py` | 물리 역학 씬 (초기 테스트, 문항은 재구성) |
| `setup.sh` | apt(한글 폰트, TeX Live + kotex, cairo/pango) + venv + TTS 모델 다운로드 |
| `render.sh` | TTS → 렌더 → `output/kinematics_short.mp4` |

## 사용

```bash
./setup.sh            # 최초 1회
./render.sh math12    # 또는 ./render.sh physics
```

## 싱크 방식

`Scene.segment(seg_id, steps)` 가 오디오를 `add_sound` 로 깔고 자막을 띄운 뒤,
`steps = [(애니메이션 목록, 가중치), ...]` 를 오디오 길이에 비례해 `run_time` 으로 나눠 재생한다.
대본을 고치면 음성 길이가 바뀌고 애니메이션이 자동으로 따라간다.

## TTS 교체

`scripts/tts.py` 의 `synth()` 만 바꾸면 된다. 현재는 sherpa-onnx + VITS(KSS, 여성 음성)이며 CPU에서 실시간의 10배 이상 속도로 돈다.
허깅페이스 보이스 클로닝 모델(본인 음성 파인튜닝)로 바꾸려면 해당 모델을 받아 `synth()` 에서 호출하고 wav를 같은 경로에 쓰면 된다.

## 영상

### `output/csat2024_math12.mp4` (108초) — 2024학년도 수능 수학(홀수형) 공통 12번
실제 기출. 출처: 시험지 PDF (justinbrianhwang/Korean-CSAT-Math 레포에 수록된 평가원 원본).
f(x)=x(x−6)(x−9)/9 와 기울기 −1 직선을 t에서 이어 붙인 g(x)의 그래프와 x축 사이 넓이의 최댓값.
t를 움직이며 넓이 변화를 보여주고, A′(t)=f(t)(1+f′(t)) 로부터 "접선 기울기가 −1이 되어 꺾임이 사라질 때 최대"임을
접선이 직선과 겹치는 장면으로 보여준다. t=3, 답 129/4 (③).

### `output/kinematics_short.mp4` (77초) — 물리 역학, 평가원 유형 재구성
초기 테스트용. 문항은 원문이 아니다.
