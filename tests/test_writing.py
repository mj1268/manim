from manim import *

#NOTE : All of those tests use cached data (in /test_cache)
# Cache functionality is tested within test_CLI.

class TextTest(Scene):
    def construct(self):
        t = Text('testing')

        self.play(Animation(t))


class TextMobjectTest(Scene):
    def construct(self):
        t = TextMobject('Hello world !')

        self.play(Animation(t))


class TexMobjectTest(Scene):
    def construct(self):
        t = TexMobject(
            "\\sum_{n=1}^\\infty "
            "\\frac{1}{n^2} = \\frac{\\pi^2}{6}"
        )

        self.play(Animation(t))


def test_scenes(get_config_test, Tester):
    CONFIG = get_config_test
    module_name = os.path.splitext(os.path.basename(__file__))[
        0].replace('test_', '')
    for name, scene_tested in inspect.getmembers(sys.modules[__name__], lambda m: inspect.isclass(m) and m.__module__ == __name__):
        Tester(scene_tested, CONFIG, module_name, caching_needed=True).test()
