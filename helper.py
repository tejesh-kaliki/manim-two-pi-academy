from manim import *

class CustomMovingCameraScene(MovingCameraScene):
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