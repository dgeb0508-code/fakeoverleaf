"""2024학년도 수능 수학(홀수형) 공통 12번. 세로 9:16 쇼츠.

비트 단위 싱크: 한 호흡의 말(output/audio/math12/<id>.wav)이 시작되는 순간
그 말에 해당하는 화면 변화 하나가 일어난다.
렌더: manim -qm scenes/csat2024_math12.py Csat2024Math12
"""
import json
import os
import sys

from manim import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from narration_math12 import SEGMENTS  # noqa: E402

AUDIO = os.path.join(ROOT, "output", "audio", "math12")

config.pixel_width, config.pixel_height = 1080, 1920
config.frame_width, config.frame_height = 9, 16
config.background_color = "#0f1117"

KR = "Noto Sans CJK KR"
ACCENT = "#FFD166"
CURVE = "#4CC9F0"
LINE = "#F72585"
GREEN = "#80ED99"


def f(x):
    return x * (x - 6) * (x - 9) / 9


def df(x):
    return (x * x - 10 * x + 18) / 3


def area(t):
    return (t ** 4 / 4 - 5 * t ** 3 + 27 * t * t) / 9 + f(t) ** 2 / 2


def ktext(s, size=34, color=WHITE, weight=BOLD, **kw):
    return Text(s, font=KR, font_size=size, color=color, weight=weight, **kw)


class Csat2024Math12(Scene):
    # ---------- 비트 싱크 ----------
    def beat(self, seg_id, *steps, tail=0.1, quick=True):
        """오디오를 깔고 자막을 띄운 뒤 steps 를 순서대로 재생한다.
        step = (animations, seconds) 또는 animations(남는 시간을 균등 분배).
        애니메이션은 말이 시작되는 순간 시작되고, 남는 시간은 기다린다."""
        d = self.durations[seg_id]
        self.add_sound(os.path.join(AUDIO, f"{seg_id}.wav"))
        self.show_caption(self.segs[seg_id].get("cap") or self.segs[seg_id]["say"])
        steps = [s if isinstance(s, tuple) else (s, None) for s in steps]
        fixed = sum(sec for _, sec in steps if sec is not None)
        n_auto = sum(1 for _, sec in steps if sec is None)
        auto = max(d - tail - fixed, 0.15 * n_auto) / n_auto if n_auto else 0
        if quick:
            auto = min(auto, 0.6)
        used = 0.0
        for anims, sec in steps:
            rt = sec if sec is not None else auto
            if anims:
                self.play(*anims, run_time=rt)
            else:
                self.wait(rt)
            used += rt
        if d - used > 0.05:
            self.wait(d - used)

    def show_caption(self, text):
        cap = ktext(text, size=52, line_spacing=1.05).move_to(DOWN * 6.3)
        bg = BackgroundRectangle(cap, color="#1b1e2b", fill_opacity=0.92, buff=0.3)
        bg.set_stroke(ACCENT, width=3, opacity=0.6)
        new = VGroup(bg, cap)
        if getattr(self, "caption", None):
            self.remove(self.caption)
        self.caption = new
        self.add(new)

    def top(self, mobj, y=5.9):
        """상단 설명 영역에 하나만 띄운다."""
        mobj.move_to(UP * y)
        anims = [FadeIn(mobj, shift=UP * 0.2)]
        if getattr(self, "top_obj", None):
            anims.append(FadeOut(self.top_obj))
        self.top_obj = mobj
        return anims

    # ---------- 구성 ----------
    def construct(self):
        with open(os.path.join(AUDIO, "durations.json")) as fp:
            self.durations = json.load(fp)
        self.segs = {s["id"]: s for s in SEGMENTS}

        ax = Axes(x_range=[-1, 10.5, 1], y_range=[-3, 8, 1], x_length=8.4, y_length=7,
                  axis_config={"include_tip": True, "tip_width": 0.18, "tip_height": 0.18,
                               "color": GREY_A, "stroke_width": 2},
                  x_axis_config={"numbers_to_include": []}, y_axis_config={"numbers_to_include": []},
                  ).move_to(UP * 0.3)
        curve = ax.plot(f, x_range=[-0.35, 9.9], color=CURVE, stroke_width=4)
        tt = ValueTracker(2.0)
        T = tt.get_value

        def g_curve_fn():
            return ax.plot(f, x_range=[-0.35, T()], color=CURVE, stroke_width=8)

        def g_line_fn():
            return Line(ax.c2p(T(), f(T())), ax.c2p(T() + f(T()), 0), color=LINE, stroke_width=8)

        def region_fn():
            return VGroup(
                ax.get_area(ax.plot(f, x_range=[0, T()]), x_range=[0, T()], color=CURVE, opacity=0.4, stroke_width=0),
                Polygon(ax.c2p(T(), f(T())), ax.c2p(T(), 0), ax.c2p(T() + f(T()), 0),
                        color=LINE, fill_opacity=0.4, stroke_width=0))

        def kink_fn():
            return Dot(ax.c2p(T(), f(T())), color=ACCENT, radius=0.12)

        def t_label_fn():
            return MathTex("t", color=ACCENT, font_size=44).next_to(ax.c2p(T(), 0), DOWN, buff=0.15)

        def area_fn():
            return VGroup(ktext("넓이", size=36, color=GREY_A),
                          DecimalNumber(area(T()), num_decimal_places=1, font_size=60, color=ACCENT)
                          ).arrange(RIGHT, buff=0.3).move_to(UP * 5.9)

        # ---- 훅: 완성된 그림이 움직이는 모습부터 (0~2초)
        hook_group = VGroup(always_redraw(region_fn), always_redraw(g_curve_fn), always_redraw(g_line_fn),
                            always_redraw(kink_fn), always_redraw(t_label_fn))
        self.add(ax, curve, hook_group)
        tt.set_value(1.0)
        self.beat("hook", [tt.animate.set_value(4.0)], quick=False)

        # ---- 제목
        badge = ktext("2024학년도 수능 수학 · 공통 12번", size=34, color=ACCENT)
        badge_bg = SurroundingRectangle(badge, color=ACCENT, buff=0.2, corner_radius=0.3)
        title = VGroup(badge_bg, badge).move_to(UP * 7.2)
        self.beat("title", [FadeIn(title, scale=1.2), FadeOut(hook_group)])
        self.remove(hook_group)
        tt.set_value(2.0)

        # ---- 곡선 소개
        f_tex = MathTex(r"f(x)=\tfrac{1}{9}\,x(x-6)(x-9)", font_size=52, color=CURVE)
        self.beat("cubic", self.top(f_tex))
        zeros = [MathTex(str(z), font_size=44, color=ACCENT).next_to(ax.c2p(z, 0), DOWN, buff=0.15) for z in (0, 6, 9)]
        self.beat("zeros", ([FadeIn(zeros[0], scale=2)], 0.45), ([FadeIn(zeros[1], scale=2)], 0.45),
                  ([FadeIn(zeros[2], scale=2)], 0.45), [])

        # ---- g 의 정의
        region, g_curve, g_line = always_redraw(region_fn), always_redraw(g_curve_fn), always_redraw(g_line_fn)
        kink, t_label = always_redraw(kink_fn), always_redraw(t_label_fn)
        g_def = MathTex(r"g(x)=\begin{cases} f(x) & (x<t)\\ -(x-t)+f(t) & (x\ge t)\end{cases}", font_size=40)
        self.beat("curve", [FadeIn(kink), FadeIn(t_label), Create(g_curve), *self.top(g_def)])
        slope_lbl = ktext("기울기 −1", size=32, color=LINE)
        slope_lbl.add_updater(lambda m: m.next_to(g_line.get_center(), UR, buff=0.15))
        self.beat("line", ([Create(g_line)], 1.2), ([FadeIn(slope_lbl)], 0.4), [])
        self.add(region)
        self.bring_to_front(g_curve, g_line, kink)
        curve.set_stroke(opacity=0.3)
        self.beat("ask", ([FadeIn(region)], 0.5), ([Indicate(region, color=WHITE, scale_factor=1.0)], 1.2))

        # ---- t 를 움직여 본다
        area_num = always_redraw(area_fn)
        self.beat("move", [*self.top(area_num), tt.animate.set_value(0.8)], quick=False)
        self.beat("grow", [tt.animate.set_value(3.0)], quick=False)
        self.beat("shrink", [tt.animate.set_value(5.2)], quick=False)
        q = ktext("?", size=90, color=ACCENT)
        q.add_updater(lambda m: m.next_to(ax.c2p(T(), f(T())), UR, buff=0.2))
        self.beat("where", [tt.animate.set_value(2.0), FadeIn(q)], quick=False)

        # ---- 넓이 식 -> 미분 -> 조건
        A1 = MathTex(r"A(t)=\int_0^t f(x)\,dx", font_size=46).move_to(DOWN * 4.2 + LEFT * 1.0)
        A2 = MathTex(r"+\tfrac12 f(t)^2", font_size=46).next_to(A1, RIGHT, buff=0.15)
        self.beat("part1", [FadeOut(q), Write(A1), Indicate(region[0], color=CURVE, scale_factor=1.0)])
        legs = VGroup(
            MathTex("f(t)", font_size=34, color=LINE).next_to(ax.c2p(T(), f(T()) / 2), LEFT, buff=0.1),
            MathTex("f(t)", font_size=34, color=LINE).next_to(ax.c2p(T() + f(T()) / 2, 0), DOWN, buff=0.1))
        self.beat("part2", [Write(A2), FadeIn(legs), Indicate(region[1], color=LINE, scale_factor=1.0)])
        dA = MathTex(r"A'(t)=", r"f(t)", r"\bigl(1+f'(t)\bigr)", font_size=46).move_to(DOWN * 5.0)
        self.beat("diff", [Write(dA)])
        self.beat("pos", [dA[1].animate.set_color(LINE), Indicate(legs, color=LINE)])
        cond = MathTex(r"f'(t)=-1", font_size=60, color=ACCENT)
        cond_box = SurroundingRectangle(cond, color=ACCENT, buff=0.2, corner_radius=0.15)
        cond_g = VGroup(cond_box, cond)
        self.beat("cond", [FadeOut(A1), FadeOut(A2), FadeOut(dA), FadeOut(legs), *self.top(cond_g)])

        # ---- 접선이 직선과 겹치는 순간
        tangent = always_redraw(lambda: Line(
            ax.c2p(T() - 1.7, f(T()) - 1.7 * df(T())), ax.c2p(T() + 1.7, f(T()) + 1.7 * df(T())),
            color=ACCENT, stroke_width=5))
        self.beat("tangent", [Create(tangent)])
        self.beat("rotate", [tt.animate.set_value(3.0)], quick=False)
        smooth = ktext("매끄럽게", size=36, color=ACCENT).next_to(ax.c2p(3, 6), RIGHT, buff=0.4).shift(UP * 0.1)
        self.beat("smooth", [Flash(kink, color=ACCENT, flash_radius=0.7, line_length=0.35), FadeIn(smooth)])
        self.beat("maxhere", [*self.top(area_num), Indicate(area_num, color=ACCENT)])

        # ---- 계산
        s1 = MathTex(r"f'(x)=\tfrac13\left(x^2-10x+18\right)=-1", font_size=42).move_to(DOWN * 3.8)
        self.beat("solve", [FadeOut(tangent), FadeOut(smooth), Write(s1)])
        s2 = MathTex(r"(x-3)(x-7)=0\ \Rightarrow\ ", r"t=3", font_size=42).move_to(DOWN * 4.45)
        s2[1].set_color(ACCENT)
        self.beat("roots", ([Write(s2)], 1.2), [Indicate(s2[1], color=ACCENT)])
        pt = Dot(ax.c2p(3, 6), color=GREEN, radius=0.13)
        pt_lbl = MathTex("(3,\\,6)", font_size=40, color=GREEN).next_to(pt, UR, buff=0.1)
        self.beat("f3", [GrowFromCenter(pt), FadeIn(pt_lbl)])
        s3 = MathTex(r"\tfrac{57}{4}", r"+", r"18", font_size=48).move_to(DOWN * 5.1)
        s3[0].set_color(CURVE)
        s3[2].set_color(LINE)
        self.beat("sum", ([Write(s3[0]), Indicate(region[0], color=CURVE, scale_factor=1.0)], 1.3),
                  ([Write(s3[1:]), Indicate(region[1], color=LINE, scale_factor=1.0)], 1.3), [])
        s4 = MathTex(r"=\tfrac{129}{4}", font_size=48, color=GREEN).next_to(s3, RIGHT, buff=0.2)
        ans = ktext("정답 ③", size=56, color=GREEN)
        ans_box = SurroundingRectangle(ans, color=GREEN, buff=0.2, corner_radius=0.2)
        self.beat("answer", ([Write(s4)], 1.0), ([FadeOut(s1), FadeOut(s2), *self.top(VGroup(ans_box, ans))], 0.8), [])

        # ---- 정리
        self.beat("outro", [FadeOut(s3), FadeOut(s4), FadeOut(pt_lbl), Flash(pt, color=ACCENT, flash_radius=0.7, line_length=0.35)],
                  ([Indicate(region, color=WHITE, scale_factor=1.0)], 1.2))
        self.wait(0.6)
