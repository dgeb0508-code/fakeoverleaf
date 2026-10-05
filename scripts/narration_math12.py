"""2024학년도 수능 수학(홀수형) 공통 12번. 쇼츠용 비트(beat) 대본.

한 비트 = 한 호흡의 말 + 그 순간 화면에 일어나는 변화 하나.
say = TTS가 읽는 문장(수식은 한글로), cap = 자막(없으면 say 그대로)."""

SEGMENTS = [
    dict(id="hook",     say="이 넓이, 언제 최대일까요.",                         cap="이 넓이,\n언제 최대일까?"),
    dict(id="title",    say="2024 수능 수학 12번입니다.",                        cap="2024 수능 수학 12번"),
    dict(id="cubic",    say="곡선은 이 삼차함수.",                               cap="삼차함수 f(x)"),
    dict(id="zeros",    say="영, 육, 구에서 엑스축과 만납니다.",                   cap="0, 6, 9 에서\nx축과 만난다"),
    dict(id="curve",    say="티까지는 이 곡선을 따라가고,",                       cap="t 까지는 곡선"),
    dict(id="line",     say="티부터는 기울기 마이너스 일로 쭉 내려옵니다.",         cap="t 부터는 기울기 −1"),
    dict(id="ask",      say="이 색칠된 넓이의 최댓값을 묻습니다.",                 cap="이 넓이의 최댓값은?"),
    dict(id="move",     say="티를 움직여 볼게요.",                               cap="t 를 움직이면"),
    dict(id="grow",     say="커지다가,",                                        cap="커지다가,"),
    dict(id="shrink",   say="줄어듭니다.",                                       cap="줄어든다"),
    dict(id="where",    say="최대는 어디일까요.",                                cap="최대는 어디?"),
    dict(id="part1",    say="넓이는, 곡선 아래 부분,",                           cap="넓이 = 곡선 아래"),
    dict(id="part2",    say="더하기 삼각형.",                                    cap="+ 삼각형"),
    dict(id="diff",     say="티로 미분하면 이렇게 묶입니다.",                      cap="t 로 미분"),
    dict(id="pos",      say="에프 티는 양수니까,",                               cap="f(t) > 0 이니까"),
    dict(id="cond",     say="에프 프라임 티가 마이너스 일일 때 최대.",             cap="f′(t) = −1 일 때 최대"),
    dict(id="tangent",  say="접선을 그려 보면,",                                 cap="접선을 그리면"),
    dict(id="rotate",   say="기울기가 마이너스 일이 되는 순간,",                   cap="기울기가 −1 이 되는 순간"),
    dict(id="smooth",   say="꺾임이 사라집니다.",                                cap="꺾임이 사라진다"),
    dict(id="maxhere",  say="그때가 최대예요.",                                  cap="그때가 최대"),
    dict(id="solve",    say="에프 프라임 엑스, 이퀄, 마이너스 일을 풀면,",          cap="f′(x) = −1 을 풀면"),
    dict(id="roots",    say="엑스는 삼 또는 칠. 범위 안은 삼.",                   cap="x = 3 또는 7 → t = 3"),
    dict(id="f3",       say="에프 삼은 육.",                                     cap="f(3) = 6"),
    dict(id="sum",      say="적분은 사분의 오십칠, 삼각형은 십팔.",               cap="57/4 + 18"),
    dict(id="answer",   say="합치면 사분의 백이십구. 정답 삼번.",                 cap="= 129/4   정답 ③"),
    dict(id="outro",    say="꺾임이 사라질 때, 넓이가 최대.",                     cap="꺾임이 사라질 때\n넓이가 최대"),
]
