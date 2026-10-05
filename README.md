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

## 싱크 방식 (비트 단위)

대본은 "한 호흡의 말" 단위(비트, 1~4초)로 쪼개고, 비트마다 wav를 따로 만든다.
`Scene.beat(seg_id, *steps)` 가 그 wav를 깔고 자막을 띄운 뒤, 그 말에 해당하는 화면 변화를 **말이 시작되는 순간** 재생한다.
전환(등장·강조)은 0.6초 안에 끝내고 남는 시간은 기다리며, t 슬라이더 같은 움직임만 `quick=False` 로 말 길이 전체를 쓴다.
말한 것이 그 순간 화면에 뜨는 것이 원칙이고, 자막은 말한 문장 그대로다.

## TTS 교체

`scripts/tts.py` 의 `synth()` 만 바꾸면 된다. 현재는 sherpa-onnx + VITS(KSS, 여성 음성)이며 CPU에서 실시간의 10배 이상 속도로 돈다.
허깅페이스 보이스 클로닝 모델(본인 음성 파인튜닝)로 바꾸려면 해당 모델을 받아 `synth()` 에서 호출하고 wav를 같은 경로에 쓰면 된다.

## 영상

### `output/csat2024_math12.mp4` (61초) — 2024학년도 수능 수학(홀수형) 공통 12번
실제 기출. 출처: 시험지 PDF (justinbrianhwang/Korean-CSAT-Math 레포에 수록된 평가원 원본).
f(x)=x(x−6)(x−9)/9 와 기울기 −1 직선을 t에서 이어 붙인 g(x)의 그래프와 x축 사이 넓이의 최댓값.
첫 2초는 완성된 그림이 움직이는 훅. 이후 곡선 → t까지 곡선 → 기울기 −1 직선 → t 를 움직이며 넓이 변화 →
A′(t)=f(t)(1+f′(t)) → 접선이 직선과 겹치며 꺾임이 사라지는 순간 → 계산 → 정답 ③ 129/4. 문제 원문 박스는 두지 않는다.

### `output/kinematics_short.mp4` (77초) — 물리 역학, 평가원 유형 재구성
초기 테스트용. 문항은 원문이 아니다.
