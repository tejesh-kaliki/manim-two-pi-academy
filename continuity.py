from manim import *
import numpy as np

from helper import CustomMovingCameraScene

# config.frame_size = (720, 1280)
# config.frame_rate = 30
config.frame_width = 9

class ContinuityExplanation(CustomMovingCameraScene):
    text_size = 36
    axes_size = (6, 6)

    def construct(self):
        axes = self.create_mapped_number_plane(
            x_range=(0, self.axes_size[0]),
            y_range=(0, self.axes_size[1]),
            extra_offset=np.array((0, -2.5, 0)),
        )
        self.play(Create(axes))
        self.wait(1)

        test_graph = Line((0, 0, 0), (3, 2, 0), color=YELLOW, stroke_width=6)
        test_graph_2 = ArcBetweenPoints((3, 3, 0), (6, 6, 0), angle=PI/2, color=YELLOW, stroke_width=6)
        graph_f = VGroup(test_graph, test_graph_2)
        self.play(Create(graph_f))
        self.wait(1)

        perp_x = DashedLine((3, 3, 0), (3, 0, 0), dash_length=0.1, dashed_ratio=0.66)
        self.play(Create(perp_x))
        self.wait()

        perp_y_1 = DashedLine((0, 2, 0), (3, 2, 0), dash_length=0.1, dashed_ratio=0.66)
        perp_y_2 = DashedLine((0, 3, 0), (3, 3, 0), dash_length=0.1, dashed_ratio=0.66)
        self.play(Create(perp_y_1), Create(perp_y_2))
        self.wait(1)
        self.play(FadeOut(perp_y_1, perp_y_2))
        self.wait(1)

        x_value = ValueTracker(2)

        x = x_value.get_value()
        point = Dot((x, 2*x/3, 0), color=RED)
        self.play(FadeIn(point))

        def update_point(p, f):
            x = x_value.get_value()
            y = f(x)
            point.move_to((x, y, 0))

        point.add_updater(lambda x: update_point(x, lambda a: a*2/3))
        self.play(x_value.animate.set_value(3))
        self.wait(1)
        self.play(FadeOut(point))
        self.wait(1)

        x_value.set_value(4)
        x = x_value.get_value()
        point = Dot((x, x, 0), color=RED)
        self.play(FadeIn(point))

        def update_point(p, f):
            x = x_value.get_value()
            y = f(x)
            point.move_to((x, y, 0))

        point.add_updater(lambda x: update_point(x, lambda a: a))
        self.play(x_value.animate.set_value(3))
        self.wait(1)
        self.play(FadeOut(point))
        self.wait(1)

        self.wait(1)