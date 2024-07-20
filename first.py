from manim import *
import numpy as np

# config.frame_size = (720, 1280)
# config.frame_rate = 30
config.frame_width = 9


def get_base_coords(coords, axis):
    if axis == "x":
        return coords * np.array((1, 0, 0))
    if axis == "y":
        return coords * np.array((0, 1, 0))


def get_perp_to_axis(coords, axis):
    return DashedLine(coords, get_base_coords(coords, axis), dash_length=0.1, dashed_ratio=0.66)


class DistanceFormula(MovingCameraScene):
    point_a_coords = np.array((1.5, 1.5, 0))
    point_b_coords = np.array((5, 4.5, 0))
    text_size = 36
    axes_size = (6, 6)

    def create_mapped_number_plane(self, x_range, y_range, extra_offset=np.array((0, 0, 0))):
        """
        Creates a number plane such that the point coordinates matches with the scene,
        and do not need to map points everytime.
        """
        x_length = abs(x_range[0] - x_range[1])
        y_length = abs(y_range[0] - y_range[1])
        shift_array = np.array((x_length/2, y_length/2, 0))
        axes = Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=x_length,
            y_length=y_length,
            axis_config={
                "include_ticks": False,
                "include_tip": True,
                "tip_width": 0.1,
                "tip_height": 0.1,
                "stroke_width": 2,
            }
        ).shift(shift_array)
        self.camera.frame.shift(shift_array+extra_offset)
        return axes

    def construct(self):
        point_a_x_coord = ValueTracker(3)
        point_a_y_coord = ValueTracker(3)

        title = Text("Distance Formula", color=RED,
                     font_size=48, font="Proxima Nova Bl")
        title.move_to((0, 0, 0))
        self.play(DrawBorderThenFill(title, stroke_color=RED))
        self.wait(duration=0.5)
        self.play(Uncreate(title), run_time=0.5)

        axes = self.create_mapped_number_plane(
            x_range=(0, self.axes_size[0]),
            y_range=(0, self.axes_size[1]),
            extra_offset=np.array((0, -2.5, 0)),
        )
        dot_a = Dot(np.array((point_a_x_coord.get_value(),
                    point_a_y_coord.get_value(), 0)), color=RED)
        label_a = MathTex("A(", "x_1", ",", "y_1", ")",
                          font_size=self.text_size, color=RED)
        dot_b = Dot(self.point_b_coords, color=RED)
        label_b = MathTex("B(", "x_2", ",", "y_2", ")", font_size=self.text_size, color=RED).next_to(
            dot_b, UP, buff=0.1)
        dot_c = Dot([self.point_b_coords[0],
                    self.point_a_coords[1], 0], color=PURE_GREEN)
        label_c = MathTex("C", font_size=self.text_size,
                          color=PURE_GREEN).next_to(dot_c, DR, buff=0.1)
        main_line_group = VGroup(
            dot_a, dot_b, label_a, label_b, dot_c, label_c)
        main_line_group.set_z_index(10)

        perp_a_x = get_perp_to_axis(dot_a.get_center(), "x")
        perp_b_x = get_perp_to_axis(dot_b.get_center(), "x")
        perp_a_y = get_perp_to_axis(dot_a.get_center(), "y")
        perp_b_y = get_perp_to_axis(dot_b.get_center(), "y")

        brace_x_1 = Brace(Line(ORIGIN, get_base_coords(dot_a.get_center(), "x")), buff=0.05,
                          direction=DOWN, color=YELLOW).stretch_to_fit_height(0.1)
        label_x_1 = MathTex("x_1", font_size=self.text_size, color=YELLOW)
        brace_x_2 = Brace(Line(ORIGIN, get_base_coords(dot_b.get_center(), "x")), buff=0.05,
                          color=YELLOW).stretch_to_fit_height(0.1)
        label_x_2 = MathTex("x_2", font_size=self.text_size, color=YELLOW).next_to(
            brace_x_2, DOWN, buff=0.1)
        x_distance_helper_group = VGroup(
            perp_a_x, perp_b_x, brace_x_1, brace_x_2, label_x_1, label_x_2
        )

        brace_y_1 = Brace(Line(ORIGIN, get_base_coords(dot_a.get_center(), "y")), buff=0.05,
                          direction=LEFT, color=YELLOW).stretch_to_fit_width(0.1)
        label_y_1 = MathTex("y_1", font_size=self.text_size, color=YELLOW)
        brace_y_2 = Brace(Line(ORIGIN, get_base_coords(dot_b.get_center(), "y")), buff=0.05, direction=LEFT,
                          color=YELLOW).stretch_to_fit_width(0.1)
        label_y_2 = MathTex("y_2", font_size=self.text_size, color=YELLOW).next_to(
            brace_y_2, LEFT, buff=0.1)
        # point_a_coords_label_group = VGroup(label_x_1, label_y_1)
        y_distance_helper_group = VGroup(
            perp_a_y, perp_b_y, brace_y_1, brace_y_2, label_y_1, label_y_2
        )

        point_a_coords_group = VGroup(
            dot_a, perp_a_x, perp_a_y,
            label_a, brace_x_1, brace_y_1,
            label_x_1, label_y_1,
        )

        self.play(Create(axes))

        def dot_a_coords_updater(group):
            new_a_coords = np.array(
                (point_a_x_coord.get_value(), point_a_y_coord.get_value(), 0))
            if np.all(group[0].get_center() == new_a_coords):
                return

            group[0].move_to(new_a_coords)
            # group[1].set_points([new_a_coords, get_base_coords(new_a_coords, "x")])
            # group[2].set_points([new_a_coords, get_base_coords(new_a_coords, "y")])
            group[1].become(get_perp_to_axis(new_a_coords, "x"))
            group[2].become(get_perp_to_axis(new_a_coords, "y"))
            group[3].next_to(group[0], UP, buff=0.1)
            group[4].become(Brace(
                Line(ORIGIN, get_base_coords(new_a_coords, "x")),
                buff=0.05,
                direction=DOWN,
                color=YELLOW
            ).stretch_to_fit_height(0.1))
            group[5].become(Brace(
                Line(ORIGIN, get_base_coords(dot_a.get_center(), "y")),
                buff=0.05,
                direction=LEFT,
                color=YELLOW
            ).stretch_to_fit_width(0.1))
            group[6].next_to(brace_x_1, DOWN, buff=0.1)
            group[7].next_to(brace_y_1, LEFT, buff=0.1)

        # Generate Point A(x_1, y_1)
        label_a.next_to(dot_a, UP, buff=0.1)
        self.play(FadeIn(dot_a))
        self.play(FadeIn(label_a))

        label_x_1.next_to(brace_x_1, DOWN, buff=0.1)
        label_y_1.next_to(brace_y_1, LEFT, buff=0.1)

        self.wait()
        self.play(Create(perp_a_x), Create(perp_a_y), run_time=1)
        self.wait()
        self.play(
            FadeIn(brace_x_1, brace_y_1),
            ReplacementTransform(label_a[1].copy(), label_x_1),
            ReplacementTransform(label_a[3].copy(), label_y_1),
        )

        self.add(point_a_coords_group)
        point_a_coords_group.add_updater(dot_a_coords_updater)
        self.wait()
        self.play(
            point_a_x_coord.animate.set_value(5),
            point_a_y_coord.animate.set_value(1),
        )
        self.play(
            point_a_x_coord.animate.set_value(3),
            point_a_y_coord.animate.set_value(5),
        )
        self.play(
            point_a_x_coord.animate.set_value(2),
            point_a_y_coord.animate.set_value(4),
        )
        self.play(
            point_a_x_coord.animate.set_value(self.point_a_coords[0]),
            point_a_y_coord.animate.set_value(self.point_a_coords[1]),
        )

        self.wait()
        self.play(
            FadeOut(perp_a_x, perp_a_y, brace_x_1,
                    brace_y_1, label_x_1, label_y_1),
            label_a.animate.next_to(dot_a, DOWN, buff=0.1)
        )

        # Clean Up of first part
        point_a_coords_group.remove_updater(dot_a_coords_updater)

        # Generate Point B(x_2, y_2)
        self.play(FadeIn(dot_b), FadeIn(label_b))

        # Daw line segment AB
        line_ab = Line(dot_a.get_center(), dot_b.get_center(), color=RED)
        self.play(Create(line_ab))

        unknown_value = Text("?", font_size=self.text_size,
                             color=RED, font="Itim")
        unknown_value.move_to(line_ab.get_center())
        unknown_value.shift(UL*0.25)
        self.play(DrawBorderThenFill(unknown_value))
        self.wait(duration=2)
        self.play(Uncreate(unknown_value), run_time=0.5)

        # Reset x_1 label for point A style
        base_a_x = get_base_coords(dot_a.get_center(), "x")
        base_b_x = get_base_coords(dot_b.get_center(), "x")
        brace_x_1.become(Brace(
            Line(ORIGIN, base_a_x),
            buff=0.05,
            direction=UP,
            color=YELLOW
        ).stretch_to_fit_height(0.1))
        label_x_1.next_to(brace_x_1, UP, buff=0.1)

        # Draw perpendiculars from points to x_axis
        base_a_x_point = Dot(base_a_x, color=PURE_GREEN)
        base_b_x_point = Dot(base_b_x, color=PURE_GREEN)
        x_diff_line = Line(base_a_x, base_b_x,
                           color=PURE_GREEN, stroke_width=4)
        x_diff_text = MathTex(
            "|", "x_2", "-", "x_1", "|", font_size=self.text_size, color=PURE_GREEN)
        x_diff_text.next_to(x_diff_line, direction=UP, buff=0.1)
        new_x_diff_line = x_diff_line.copy().shift(
            get_base_coords(dot_a.get_center(), "y"))

        self.play(label_a.animate.next_to(dot_a, LEFT, buff=0.1))
        self.play(Create(perp_a_x))
        self.play(Create(perp_b_x))

        # Show the lengths of the projections on x axis
        self.play(FadeIn(brace_x_1), ReplacementTransform(
            label_a[1].copy(), label_x_1))
        self.play(FadeIn(brace_x_2), ReplacementTransform(
            label_b[1].copy(), label_x_2))
        self.wait()

        # Show difference between x bases
        self.play(FadeIn(base_a_x_point), run_time=0.5)
        self.play(Create(x_diff_line), run_time=0.5)
        self.play(FadeIn(base_b_x_point), run_time=0.5)
        self.play(
            FadeIn(x_diff_text[::2]),
            ReplacementTransform(label_x_2.copy(), x_diff_text[1]),
            ReplacementTransform(label_x_1.copy(), x_diff_text[3]),
        )

        # Animate the difference towards the line
        self.play(
            ReplacementTransform(base_a_x_point, dot_a),
            ReplacementTransform(base_b_x_point, dot_c),
            Transform(x_diff_line, new_x_diff_line),
            x_diff_text.animate.next_to(
                new_x_diff_line, direction=DOWN, buff=0.1),
            FadeOut(x_distance_helper_group),
            label_a.animate.next_to(dot_a, DOWN, buff=0.1),
            FadeIn(label_c),
        )
        self.wait()

        base_a_y = get_base_coords(dot_a.get_center(), "y")
        base_b_y = get_base_coords(dot_b.get_center(), "y")
        brace_y_1.become(Brace(
            Line(ORIGIN, base_a_y),
            buff=0.05,
            direction=RIGHT,
            color=YELLOW
        ).stretch_to_fit_width(0.1))
        label_y_1.next_to(brace_y_1, RIGHT, buff=0.1)

        # Draw perpendiculars from points to y_axis
        base_a_y_point = Dot(base_a_y, color=PURE_GREEN)
        base_b_y_point = Dot(base_b_y, color=PURE_GREEN)
        y_diff_line = Line(base_a_y, base_b_y,
                           color=PURE_GREEN, stroke_width=4)
        y_diff_text = MathTex(
            "|", "y_2", "-", "y_1", "|", font_size=self.text_size, color=PURE_GREEN)
        y_diff_text.next_to(y_diff_line, direction=RIGHT, buff=0.1)
        new_y_diff_line = y_diff_line.copy().shift(base_b_x)

        self.play(Create(perp_a_y))
        self.play(Create(perp_b_y))

        # Show the lengths of the projections on x axis
        self.play(
            FadeIn(brace_y_1),
            ReplacementTransform(label_a[3].copy(), label_y_1),
            FadeIn(brace_y_2),
            ReplacementTransform(label_b[3].copy(), label_y_2),
        )

        # Show difference between x bases
        self.play(FadeIn(base_a_y_point), run_time=0.5)
        self.play(Create(y_diff_line), run_time=0.5)
        self.play(FadeIn(base_b_y_point), run_time=0.5)
        self.play(
            FadeIn(y_diff_text[::2]),
            ReplacementTransform(label_y_2.copy(), y_diff_text[1]),
            ReplacementTransform(label_y_1.copy(), y_diff_text[3]),
        )

        # Animate the difference towards the line
        self.play(
            ReplacementTransform(base_b_y_point, dot_b),
            ReplacementTransform(base_a_y_point, dot_c),
            Transform(y_diff_line, new_y_diff_line),
            y_diff_text.animate.next_to(
                new_y_diff_line, direction=RIGHT, buff=0.1),
            FadeOut(y_distance_helper_group)
        )
        self.wait()

        x_diff_line.reverse_direction()
        right_angle = Angle(x_diff_line, y_diff_line,
                            color=YELLOW, radius=0.3, elbow=True)

        self.play(Create(right_angle))

        # Add final derivation
        text1 = Text("According to Pythogoras Theorem,",
                     font="Itim", font_size=28)
        text1.next_to(axes, DOWN, 0.5)
        text1.align_to(axes, LEFT)
        pythagoras_thoerem = MathTex(
            r"\text{AC}", "^2 +", r"\text{BC}", "^2", "=", r"\text{AB}", "^2", font_size=33)
        pythagoras_thoerem.next_to(text1, DOWN, 0.5)
        pythagoras_thoerem.align_to(axes, ORIGIN)
        self.play(Create(text1))
        self.play(FadeIn(pythagoras_thoerem))
        self.wait()

        formula_1 = MathTex("| x_2 - x_1 |", "^2 +", "| y_2 - y_1 |",
                            "^2", "=", r"\text{AB}", "^2", font_size=33)
        formula_1.next_to(pythagoras_thoerem, DOWN, 0.5)
        self.play(
            ReplacementTransform(pythagoras_thoerem.copy()[
                                 1:4:2], formula_1[1:4:2]),
            ReplacementTransform(pythagoras_thoerem.copy()
                                 [-3:], formula_1[-3:]),
            ReplacementTransform(x_diff_text.copy(), formula_1[0]),
            ReplacementTransform(y_diff_text.copy(), formula_1[2]),
        )
        self.wait()

        final_formula = MathTex(
            r"\text{AB}", "=", r"\sqrt{", "(x_2 - x_1)^2 + (y_2 - y_1)^2", "}", font_size=33)
        final_formula.next_to(formula_1, DOWN, 0.5)
        self.play(FadeIn(final_formula))
        self.wait()

        final_formula_1 = MathTex(
            r"\sqrt{ (x_2 - x_1)^2 + (y_2 - y_1)^2 }", font_size=self.text_size, color=RED)
        final_formula_1.move_to(line_ab.get_center())
        final_formula_1.rotate(line_ab.get_angle())
        final_formula_1.shift(UL*0.25)
        self.play(Create(final_formula_1))

        self.wait(duration=2)


class TestScene(Scene):
    def construct(self):
        dot_a = Dot()
        dot_b = Dot([3, 0, 0])
        dot_c = Dot([3, 4, 0])

        line_ab = Line(dot_a.get_center(), dot_b.get_center())
        line_bc = Line(dot_b.get_center(), dot_c.get_center())

        right_angle = Angle(line_ab, line_bc, radius=1)

        self.add(dot_a, dot_b, dot_c, line_ab, line_bc, right_angle)
