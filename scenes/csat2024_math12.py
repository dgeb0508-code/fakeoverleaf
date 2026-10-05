"""2024학년도 수능 수학(홀수형) 공통 12번. 세로 9:16.

f(x)=x(x-6)(x-9)/9, g는 x<t 에서 f, x>=t 에서 기울기 -1 직선.
y=g(x)와 x축이 둘러싸는 넓이의 최댓값 -> 꺾임이 사라질 때(f'(t)=-1, t=3) 최대, 129/4.
렌더: manim -qm scenes/csat2024_math12.py Csat2024Math12
"""
import json
import os
import sys

import numpy as np
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
AREA = "#4CC9F0"
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
    # ---------- 오디오 싱크 ----------
    def segment(self, seg_id, steps, tail=0.3):
        """오디오를 깔고 자막을 띄운 뒤 steps=[(animations, weight), ...]를
        오디오 길이에 비례 배분해 재생한다. 애니메이션 없는 step은 wait."""
        d = self.durations[seg_id]
        self.add_sound(os.path.join(AUDIO, f"{seg_id}.wav"))
        self.show_caption(self.segs[seg_id]["caption"])
        total_w = sum(w for _, w in steps)
        budget = d - tail
        for anims, w in steps:
            rt = max(budget * w / total_w, 0.15)
            if anims:
                self.play(*anims, run_time=rt)
            else:
                self.wait(rt)
        self.wait(tail)

    def show_caption(self, text):
        cap = ktext(text, size=42, line_spacing=1.1).move_to(DOWN * 6.7)
        bg = BackgroundRectangle(cap, color="#1b1e2b", fill_opacity=0.92, buff=0.3)
        bg.set_stroke(ACCENT, width=3, opacity=0.6)
        new = VGroup(bg, cap)
        if getattr(self, "caption", None):
            self.remove(self.caption)
        self.caption = new
        self.add(new)

    # ---------- 구성 ----------
    def construct(self):
        with open(os.path.join(AUDIO, "durations.json")) as fp:
            self.durations = json.load(fp)
        self.segs = {s["id"]: s for s in SEGMENTS}

        header = self.build_header()
        problem = self.build_problem()
        ax, curve, zero_labels, f_label = self.build_graph()

        # 1. 문제 제시
        self.segment("intro", [
            ([FadeIn(header, shift=DOWN * 0.2)], 1),
            ([FadeIn(problem)], 2),
            ([Indicate(problem[2], color=ACCENT, scale_factor=1.05)], 1.5),
            ([Indicate(problem[3], color=ACCENT, scale_factor=1.05)], 1.5),
        ])

        # 2. f 의 그래프
        self.segment("graph", [
            ([Create(ax)], 1),
            ([Create(curve), FadeIn(f_label)], 2),
            ([LaggedStart(*[FadeIn(z, scale=1.5) for z in zero_labels], lag_ratio=0.4)], 1.2),
            ([], 0.8),
        ])

        # 3. g 의 정의: t 까지 곡선, 그 뒤 기울기 -1 직선, 색칠
        tt = ValueTracker(2.0)
        g_curve = always_redraw(lambda: ax.plot(f, x_range=[-0.35, tt.get_value()], color=CURVE, stroke_width=7))
        g_line = always_redraw(lambda: Line(
            ax.c2p(tt.get_value(), f(tt.get_value())),
            ax.c2p(tt.get_value() + f(tt.get_value()), 0), color=LINE, stroke_width=7))
        region = always_redraw(lambda: VGroup(
            ax.get_area(ax.plot(f, x_range=[0, tt.get_value()]), x_range=[0, tt.get_value()],
                        color=AREA, opacity=0.35, stroke_width=0),
            Polygon(ax.c2p(tt.get_value(), f(tt.get_value())), ax.c2p(tt.get_value(), 0),
                    ax.c2p(tt.get_value() + f(tt.get_value()), 0),
                    color=LINE, fill_opacity=0.35, stroke_width=0)))
        kink = always_redraw(lambda: Dot(ax.c2p(tt.get_value(), f(tt.get_value())), color=ACCENT, radius=0.11))
        t_label = always_redraw(lambda: MathTex("t", color=ACCENT, font_size=40)
                                .next_to(ax.c2p(tt.get_value(), 0), DOWN, buff=0.15))
        t_drop = always_redraw(lambda: DashedLine(ax.c2p(tt.get_value(), 0),
                                                  ax.c2p(tt.get_value(), f(tt.get_value())), color=ACCENT, stroke_width=2))
        slope_label = ktext("기울기 −1", size=28, color=LINE)
        slope_label.add_updater(lambda m: m.next_to(g_line.get_center(), UR, buff=0.15))
        area_num = always_redraw(lambda: VGroup(
            ktext("넓이", size=34, color=GREY_A),
            DecimalNumber(area(tt.get_value()), num_decimal_places=2, font_size=48, color=ACCENT),
        ).arrange(RIGHT, buff=0.3).move_to(DOWN * 4.7))

        self.segment("define", [
            ([Create(t_drop), FadeIn(t_label), GrowFromCenter(kink)], 1),
            ([Create(g_curve)], 1.5),
            ([Create(g_line), FadeIn(slope_label)], 1.5),
            ([FadeIn(region), FadeIn(area_num)], 1.5),
            ([], 0.8),
        ])
        curve.set_stroke(opacity=0.35)

        # 4. t 를 움직이며 넓이 관찰
        self.segment("slide", [
            ([tt.animate.set_value(0.8)], 1.2),
            ([tt.animate.set_value(5.2)], 3.5),
            ([tt.animate.set_value(2.0)], 2.2),
            ([], 0.6),
        ])

        # 5. 넓이 식과 미분
        self.remove(area_num)
        A = MathTex(r"A(t)=\int_0^t f(x)\,dx+\tfrac12 f(t)^2", font_size=40).move_to(DOWN * 4.2)
        dA = MathTex(r"A'(t)=f(t)\bigl(1+f'(t)\bigr)", font_size=40).move_to(DOWN * 5.2)
        cond = MathTex(r"f'(t)=-1", font_size=44, color=ACCENT).move_to(DOWN * 5.2)
        legs = VGroup(
            MathTex("f(t)", font_size=32, color=LINE).add_updater(
                lambda m: m.next_to(ax.c2p(tt.get_value(), f(tt.get_value()) / 2), LEFT, buff=0.1)),
            MathTex("f(t)", font_size=32, color=LINE).add_updater(
                lambda m: m.next_to(ax.c2p(tt.get_value() + f(tt.get_value()) / 2, 0), DOWN, buff=0.1)),
        )
        self.segment("formula", [
            ([Write(A)], 2),
            ([FadeIn(legs)], 1.5),
            ([Write(dA)], 2.5),
            ([FadeOut(legs), Transform(dA, cond)], 2),
            ([Indicate(dA, color=ACCENT)], 1),
        ])

        # 6. 접선이 직선과 겹치는 순간 = 꺾임이 사라짐
        tangent = always_redraw(lambda: Line(
            ax.c2p(tt.get_value() - 1.6, f(tt.get_value()) - 1.6 * df(tt.get_value())),
            ax.c2p(tt.get_value() + 1.6, f(tt.get_value()) + 1.6 * df(tt.get_value())),
            color=ACCENT, stroke_width=4).set_opacity(0.9))
        smooth = ktext("매끄럽게 이어짐", size=30, color=ACCENT)
        self.segment("tangent", [
            ([Create(tangent)], 1.2),
            ([], 1),
            ([tt.animate.set_value(3.0)], 3),
            ([Flash(kink, color=ACCENT, flash_radius=0.6), FadeIn(smooth.next_to(kink, RIGHT, buff=0.35).shift(UP * 0.15))], 1),
            ([], 1.2),
        ])

        # 7. 계산
        self.play(FadeOut(A), FadeOut(dA), FadeOut(smooth), FadeOut(tangent), run_time=0.3)
        c1 = MathTex(r"f'(x)=\tfrac13\left(x^2-10x+18\right)=-1", font_size=38).move_to(DOWN * 4.0)
        c2 = MathTex(r"x^2-10x+21=0\ \Rightarrow\ (x-3)(x-7)=0", font_size=38).move_to(DOWN * 4.65)
        c3 = MathTex(r"t=3,\quad f(3)=6", font_size=42, color=ACCENT).move_to(DOWN * 5.3)
        pt = Dot(ax.c2p(3, 6), color=GREEN, radius=0.12)
        pt_label = MathTex("(3,\\,6)", font_size=36, color=GREEN).next_to(pt, UR, buff=0.1)
        self.segment("compute", [
            ([Write(c1)], 2),
            ([Write(c2)], 2.5),
            ([Write(c3)], 1.5),
            ([GrowFromCenter(pt), FadeIn(pt_label)], 1),
            ([], 0.8),
        ])

        # 8. 정답
        self.play(FadeOut(c1), FadeOut(c2), FadeOut(c3), run_time=0.3)
        ans = MathTex(r"A(3)=\tfrac{57}{4}+18=\tfrac{129}{4}", font_size=44, color=GREEN).move_to(DOWN * 4.3)
        choices = self.build_choices().move_to(DOWN * 5.25)
        ring = Circle(radius=0.5, color=GREEN, stroke_width=5).move_to(choices[2])
        self.segment("answer", [
            ([Write(ans)], 2.5),
            ([FadeIn(choices)], 1),
            ([Create(ring)], 0.8),
            ([], 0.8),
        ])

        # 9. 정리
        takeaway = VGroup(
            ktext("꺾임이 사라질 때", size=48, color=ACCENT),
            ktext("넓이가 최대", size=48),
        ).arrange(DOWN, buff=0.2).move_to(DOWN * 5.05)
        self.segment("outro", [
            ([FadeOut(ans), FadeOut(choices), FadeOut(ring)], 0.4),
            ([FadeIn(takeaway, scale=0.9)], 1),
            ([], 1.6),
        ])
        self.wait(0.5)

    # ---------- 부품 ----------
    def build_header(self):
        badge = ktext("2024학년도 수능 수학 (홀수형) · 공통 12번 · 4점", size=28, color=ACCENT)
        bg = SurroundingRectangle(badge, color=ACCENT, buff=0.18, corner_radius=0.3)
        return VGroup(bg, badge).move_to(UP * 7.3)

    def build_problem(self):
        l1 = VGroup(ktext("함수", size=28, weight=NORMAL),
                    MathTex(r"f(x)=\tfrac{1}{9}x(x-6)(x-9)", font_size=36),
                    ktext("와 실수", size=28, weight=NORMAL),
                    MathTex(r"t\,(0<t<6)", font_size=36)).arrange(RIGHT, buff=0.15)
        l2 = VGroup(ktext("에 대하여 함수", size=28, weight=NORMAL),
                    MathTex(r"g(x)", font_size=36), ktext("는", size=28, weight=NORMAL)).arrange(RIGHT, buff=0.15)
        piece = MathTex(r"g(x)=\begin{cases} f(x) & (x<t)\\ -(x-t)+f(t) & (x\ge t)\end{cases}", font_size=36)
        q = VGroup(ktext("이다. 함수", size=28, weight=NORMAL), MathTex("y=g(x)", font_size=36),
                   ktext("의 그래프와", size=28, weight=NORMAL), MathTex("x", font_size=36),
                   ktext("축으로", size=28, weight=NORMAL)).arrange(RIGHT, buff=0.15)
        q2 = ktext("둘러싸인 영역의 넓이의 최댓값은?", size=28, color=ACCENT)
        body = VGroup(l1, l2, piece, q, q2).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        box = SurroundingRectangle(body, color=GREY_B, buff=0.3, corner_radius=0.2, stroke_width=2)
        return VGroup(box, l1, l2, piece, q, q2).move_to(UP * 4.9)

    def build_graph(self):
        ax = Axes(x_range=[-1, 10.5, 1], y_range=[-3, 8, 1], x_length=8.2, y_length=6.8,
                  axis_config={"include_tip": True, "tip_width": 0.18, "tip_height": 0.18,
                               "color": GREY_A, "stroke_width": 2},
                  x_axis_config={"numbers_to_include": []}, y_axis_config={"numbers_to_include": []},
                  ).move_to(DOWN * 0.6)
        curve = ax.plot(f, x_range=[-0.35, 9.9], color=CURVE, stroke_width=4)
        zeros = VGroup(*[MathTex(str(z), font_size=34, color=GREY_A).next_to(ax.c2p(z, 0), DOWN, buff=0.15)
                         for z in (0, 6, 9)])
        f_label = MathTex("y=f(x)", font_size=36, color=CURVE).next_to(ax.c2p(9.9, f(9.9)), UP, buff=0.15)
        return ax, curve, zeros, f_label

    def build_choices(self):
        items = VGroup(*[VGroup(ktext(c, size=32), MathTex(r"\tfrac{%d}{4}" % n, font_size=42)).arrange(RIGHT, buff=0.1)
                         for c, n in zip(["①", "②", "③", "④", "⑤"], [125, 127, 129, 131, 133])])
        items.arrange(RIGHT, buff=0.35)
        items[2].set_color(GREEN)
        return items
