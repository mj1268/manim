from manim import *


class CoordinatesTest(Scene):
    def construct(self):
        dots = []
        for x in range(-7, 8):
            for y in range(-4, 5):
                dots.append(Dot(np.array([x, y, 0])))

        self.play(Animation(VGroup(*dots)))


class ArcTest(Scene):
    def construct(self):
        a = Arc(PI)
        self.play(Animation(a))


class ArcBetweenPointsTest(Scene):
    def construct(self):
        a = ArcBetweenPoints(np.array([1, 1, 0]), np.array([2, 2, 0]))
        self.play(Animation(a))


class CurvedArrowTest(Scene):
    def construct(self):
        a = CurvedArrow(np.array([1, 1, 0]), np.array([2, 2, 0]))
        self.play(Animation(a))


class CircleTest(Scene):
    def construct(self):
        circle = Circle()

        self.play(Animation(circle))


class DotTest(Scene):
    def construct(self):
        dot = Dot()

        self.play(Animation(dot))


class EllipseTest(Scene):
    def construct(self):
        e = Ellipse()

        self.play(Animation(e))


class SectorTest(Scene):
    def construct(self):
        e = Sector()

        self.play(Animation(e))


class AnnulusTest(Scene):
    def construct(self):
        a = Annulus()

        self.play(Animation(a))


class AnnularSectorTest(Scene):
    def construct(self):
        a = AnnularSector()

        self.play(Animation(a))


class LineTest(Scene):
    def construct(self):
        a = Line(np.array([1, 1, 0]), np.array([2, 2, 0]))

        self.play(Animation(a))


class Elbowtest(Scene):
    def construct(self):
        a = Elbow()

        self.play(Animation(a))


class DoubleArrowTest(Scene):
    def construct(self):
        a = DoubleArrow()

        self.play(Animation(a))


class VectorTest(Scene):
    def construct(self):
        a = Vector(UP)

        self.play(Animation(a))


class PolygonTest(Scene):
    def construct(self):
        a = Polygon(
            *[np.array([1, 1, 0]), np.array([2, 2, 0]), np.array([2, 3, 0])])

        self.play(Animation(a))


class RectangleTest(Scene):
    def construct(self):
        a = Rectangle()

        self.play(Animation(a))

class RoundedRectangleTest(Scene):
    def construct(self):
        a = RoundedRectangle()

        self.play(Animation(a))

def test_scenes(get_config_test, Tester):
    CONFIG = get_config_test
    module_name = os.path.splitext(os.path.basename(__file__))[0].replace('test_', '')
    for _, scene_tested in inspect.getmembers(sys.modules[__name__], lambda m: inspect.isclass(m) and m.__module__ == __name__):
        Tester(scene_tested, CONFIG, module_name).test()