"""물리학Ⅰ 역학 숏폼: 등가속도 운동, '평균 속도 = 중간 시각 속도' 풀이.

세로 9:16. 각 세그먼트는 output/audio/<id>.wav 길이에 애니메이션을 맞춘다.
렌더: manim -qh scenes/kinematics_short.py KinematicsShort
"""
import json
import os
import sys

from manim import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from narration import SEGMENTS  # noqa: E402

config.pixel_width, config.pixel_height = 1080, 1920
config.frame_width, config.frame_height = 9, 16
config.background_color = "#0f1117"

KR = "Noto Sans CJK KR"
ACCENT = "#FFD166"   # 노랑: 핵심
BLUE = "#4CC9F0"     # 1구간
PINK = "#F72585"     # 2구간
GREEN = "#80ED99"    # 정답


def ktext(s, size=34, color=WHITE, weight=BOLD, **kw):
    return Text(s, font=KR, font_size=size, color=color, weight=weight, **kw)


class KinematicsShort(Scene):
    # ---------- 오디오 싱크 ----------
    def load_audio(self):
        with open(os.path.join(ROOT, "output", "audio", "durations.json")) as f:
            self.durations = json.load(f)
        self.segs = {s["id"]: s for s in SEGMENTS}

    def segment(self, seg_id, steps, tail=0.3):
        """오디오를 깔고 자막을 띄운 뒤, steps=[(animations, weight), ...]를
        오디오 길이에 비례 배분해 재생한다. 애니메이션 없는 step은 wait."""
        seg = self.segs[seg_id]
        d = self.durations[seg_id]
        self.add_sound(os.path.join(ROOT, "output", "audio", f"{seg_id}.wav"))
        self.show_caption(seg["caption"], seg.get("hi", []))
        total_w = sum(w for _, w in steps)
        budget = d - tail
        for anims, w in steps:
            rt = max(budget * w / total_w, 0.15)
            if anims:
                self.play(*anims, run_time=rt)
            else:
                self.wait(rt)
        self.wait(tail)

    def show_caption(self, text, hi):
        t2c = {h: ACCENT for h in hi}
        cap = ktext(text, size=44, t2c=t2c, line_spacing=1.1).move_to(DOWN * 6.6)
        bg = BackgroundRectangle(cap, color="#1b1e2b", fill_opacity=0.92, buff=0.3)
        bg.set_stroke(ACCENT, width=3, opacity=0.6)
        new = VGroup(bg, cap)
        if getattr(self, "caption", None):
            self.remove(self.caption)
        self.caption = new
        self.add(new)

    # ---------- 구성 ----------
    def construct(self):
        self.load_audio()
        self.build_header()
        self.build_road()
        self.build_graph()

        # 1. 훅: 문제 박스 등장, 공식 뭉치가 날아왔다가 ✋ 로 튕겨나감
        formulas = VGroup(
            MathTex(r"v = v_0 + at"), MathTex(r"s = v_0 t + \tfrac12 a t^2"),
            MathTex(r"v^2 - v_0^2 = 2as"),
        ).arrange(DOWN, buff=0.3).set_color(GREY_A).move_to(UP * 0.4)
        stop = ktext("멈춰", size=90, color=PINK).move_to(UP * 0.4).rotate(-0.15)
        self.segment("hook", [
            ([FadeIn(self.header, shift=DOWN * 0.3), Write(self.problem_box)], 2),
            ([LaggedStart(*[FadeIn(f, shift=LEFT) for f in formulas], lag_ratio=0.3)], 1.5),
            ([FadeIn(stop, scale=3)], 0.6),
            ([FadeOut(formulas, shift=RIGHT * 4), stop.animate.scale(0.3).set_opacity(0)], 0.8),
            ([FadeIn(self.road)], 1),
        ])
        self.remove(stop)

        # 2. 문제 읽기: 자동차가 p→q (2초), q→r (1초) 이동 (실제 시간 비 2:1 유지)
        self.segment("problem", [
            ([], 1.2),
            ([MoveAlongPath(self.car, Line(self.P, self.Q)), self.t_pq.animate.set_color(BLUE)], 2),
            ([MoveAlongPath(self.car, Line(self.Q, self.R)), self.t_qr.animate.set_color(PINK)], 1),
            ([Indicate(self.lbl_r, color=ACCENT, scale_factor=1.6)], 0.8),
            ([], 0.8),
        ])

        # 3. 핵심 문장: 평균 속도는 중간 시각
        key = VGroup(
            ktext("등가속도에서", size=36, color=GREY_A),
            ktext("평균 속도 = 중간 시각의 순간 속도", size=38, color=ACCENT),
        ).arrange(DOWN, buff=0.2).move_to(UP * 0.4)
        key_bg = SurroundingRectangle(key, color=ACCENT, buff=0.25, corner_radius=0.15)
        # 그래프 위 설명용 미니 도식: 평균값이 중간 시각에 걸리는 모습
        self.segment("insight", [
            ([FadeIn(key, key_bg)], 1.5),
            ([Flash(key[1], color=ACCENT, flash_radius=2.2, line_length=0.4)], 0.8),
            ([FadeIn(self.axes), FadeIn(self.axis_labels)], 1.2),
            ([], 1),
        ])
        self.play(FadeOut(key), FadeOut(key_bg), run_time=0.3)

        # 4. 1구간: 평균 3 m/s → t=1 s 에 점
        calc1 = MathTex(r"\bar v_{pq} = \frac{6\,\mathrm{m}}{2\,\mathrm{s}} = 3\ \mathrm{m/s}",
                        color=BLUE).scale(0.9).move_to(UP * 0.4)
        seg1 = self.highlight_segment(self.P, self.Q, BLUE)
        pt1 = Dot(self.axes.c2p(1, 3), color=BLUE, radius=0.12)
        mid1 = DashedLine(self.axes.c2p(1, 0), self.axes.c2p(1, 3), color=BLUE)
        lab1 = MathTex("(1,\ 3)", color=BLUE).scale(0.7).next_to(pt1, UL, buff=0.1)
        self.segment("seg1", [
            ([FadeIn(seg1)], 0.8),
            ([Write(calc1)], 1.6),
            ([Create(mid1)], 0.8),
            ([GrowFromCenter(pt1), FadeIn(lab1)], 0.8),
            ([], 0.6),
        ])

        # 5. 2구간: 평균 6 m/s → t=2.5 s 에 점
        calc2 = MathTex(r"\bar v_{qr} = \frac{6\,\mathrm{m}}{1\,\mathrm{s}} = 6\ \mathrm{m/s}",
                        color=PINK).scale(0.9).next_to(calc1, DOWN, buff=0.25)
        seg2 = self.highlight_segment(self.Q, self.R, PINK)
        pt2 = Dot(self.axes.c2p(2.5, 6), color=PINK, radius=0.12)
        mid2 = DashedLine(self.axes.c2p(2.5, 0), self.axes.c2p(2.5, 6), color=PINK)
        lab2 = MathTex("(2.5,\ 6)", color=PINK).scale(0.7).next_to(pt2, UL, buff=0.1)
        self.segment("seg2", [
            ([FadeIn(seg2)], 0.8),
            ([Write(calc2)], 1.6),
            ([Create(mid2)], 0.8),
            ([GrowFromCenter(pt2), FadeIn(lab2)], 0.8),
            ([], 0.6),
        ])

        # 6. 직선 확정, 가속도
        line = Line(self.axes.c2p(0, 1), self.axes.c2p(3.3, 7.6), color=ACCENT, stroke_width=6)
        slope = MathTex(r"a = \frac{6-3}{2.5-1} = 2\ \mathrm{m/s^2}", color=ACCENT).scale(0.9)
        slope.move_to(UP * 0.4)
        self.segment("line", [
            ([FadeOut(calc1), FadeOut(calc2)], 0.4),
            ([Create(line)], 1.4),
            ([Write(slope)], 1.6),
            ([Indicate(slope, color=WHITE)], 0.6),
            ([], 0.6),
        ])

        # 7. 정답: t=3 에서 7 m/s
        pt3 = Dot(self.axes.c2p(3, 7), color=GREEN, radius=0.14)
        mid3 = DashedLine(self.axes.c2p(3, 0), self.axes.c2p(3, 7), color=GREEN)
        lab3 = MathTex("(3,\ 7)", color=GREEN).scale(0.8).next_to(pt3, UR, buff=0.1)
        final = MathTex(r"v_r = 6 + 2 \times 0.5 = 7\ \mathrm{m/s}", color=GREEN).scale(1.0)
        final.move_to(UP * 0.4)
        choices = self.build_choices()
        self.segment("answer", [
            ([FadeOut(slope)], 0.3),
            ([Create(mid3)], 0.8),
            ([GrowFromCenter(pt3), FadeIn(lab3)], 0.6),
            ([Write(final)], 1.4),
            ([FadeIn(choices)], 0.6),
            ([Create(self.answer_ring), Flash(self.answer_ring, color=GREEN, flash_radius=0.8)], 1.0),
            ([], 0.8),
        ])

        # 8. 아웃트로
        outro = VGroup(
            ktext("평균 속도는 중간 시각", size=46, color=ACCENT),
            ktext("공식 X   점 찍기 O", size=40, t2c={"X": PINK, "O": GREEN}),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.4)
        self.segment("outro", [
            ([FadeOut(final), FadeOut(choices), FadeOut(self.answer_ring)], 0.4),
            ([FadeIn(outro, scale=0.8)], 1),
            ([], 1.4),
        ])
        self.wait(0.5)

    # ---------- 부품 ----------
    def build_header(self):
        badge = ktext("물리학Ⅰ · 역학 · 평가원 유형", size=30, color=ACCENT)
        badge_bg = SurroundingRectangle(badge, color=ACCENT, buff=0.18, corner_radius=0.3)
        self.header = VGroup(badge_bg, badge).move_to(UP * 7.2)

        lines = [
            "직선 도로에서 등가속도 운동을 하는",
            "자동차가 점 p, q, r 를 차례로 지난다.",
            "p–q, q–r 거리는 각각 6 m 이고,",
            "p→q 에 2 초, q→r 에 1 초가 걸렸다.",
            "r 에서 자동차의 속력은?",
        ]
        body = VGroup(*[ktext(s, size=30, weight=NORMAL) for s in lines[:-1]],
                      ktext(lines[-1], size=30, color=ACCENT)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        box = SurroundingRectangle(body, color=GREY_B, buff=0.3, corner_radius=0.2, stroke_width=2)
        self.problem_box = VGroup(box, body).move_to(UP * 5.1)

    def build_road(self):
        y = 2.6
        road = Line(LEFT * 4.2 + UP * y, RIGHT * 4.2 + UP * y, color=GREY_B, stroke_width=10)
        self.P, self.Q, self.R = LEFT * 3.6 + UP * y, UP * y, RIGHT * 3.6 + UP * y
        dots = VGroup(*[Dot(p, color=WHITE, radius=0.09) for p in (self.P, self.Q, self.R)])
        lp = ktext("p", size=34).next_to(self.P, DOWN, buff=0.2)
        lq = ktext("q", size=34).next_to(self.Q, DOWN, buff=0.2)
        self.lbl_r = ktext("r", size=34).next_to(self.R, DOWN, buff=0.2)
        self.t_pq = ktext("6 m · 2초", size=28, color=GREY_A).move_to((self.P + self.Q) / 2 + DOWN * 0.75)
        self.t_qr = ktext("6 m · 1초", size=28, color=GREY_A).move_to((self.Q + self.R) / 2 + DOWN * 0.75)
        body = RoundedRectangle(width=0.8, height=0.38, corner_radius=0.1, color=ACCENT,
                                fill_opacity=1, stroke_width=0)
        wheels = VGroup(*[Circle(radius=0.09, color=WHITE, fill_opacity=1, stroke_width=0)
                          .move_to(body.get_bottom() + RIGHT * dx) for dx in (-0.25, 0.25)])
        self.car = VGroup(body, wheels).move_to(self.P + UP * 0.35)
        self.road = VGroup(road, dots, lp, lq, self.lbl_r, self.t_pq, self.t_qr, self.car)

    def highlight_segment(self, a, b, color):
        return Line(a, b, color=color, stroke_width=14).set_opacity(0.7)

    def build_graph(self):
        self.axes = Axes(
            x_range=[0, 3.6, 1], y_range=[0, 8.5, 1], x_length=6.4, y_length=4.6,
            axis_config={"include_tip": True, "tip_width": 0.18, "tip_height": 0.18,
                         "color": GREY_A, "font_size": 26},
            x_axis_config={"numbers_to_include": [1, 2, 3]},
            y_axis_config={"numbers_to_include": [3, 6, 7]},
        ).move_to(DOWN * 2.9)
        xl = MathTex("t\,(\\mathrm{s})", font_size=30).next_to(self.axes.x_axis.get_end(), DOWN, buff=0.15)
        yl = MathTex("v\,(\\mathrm{m/s})", font_size=30).next_to(self.axes.y_axis.get_end(), RIGHT, buff=0.15)
        self.axis_labels = VGroup(xl, yl)

    def build_choices(self):
        items = VGroup(*[ktext(s, size=30) for s in ["① 5", "② 6", "③ 7", "④ 8", "⑤ 9"]])
        items.arrange(RIGHT, buff=0.45).next_to(self.problem_box, DOWN, buff=0.25)
        items[2].set_color(GREEN)
        self.answer_ring = Circle(radius=0.42, color=GREEN, stroke_width=5).move_to(items[2])
        return items
