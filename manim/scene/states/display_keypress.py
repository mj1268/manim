from manim.animation.animation import Wait
from manim.animation.composition import Succession
from manim.mobject.text.text_mobject import Text
from pyglet.window import key as KEY

class DisplayKeypress(Text):
    """Display keypresses on the screen."""
    fade_delay: float = 0.5

    def __init__(
        self,
        symbol,
        modifiers,
        fade_delay: float = 0.5,
        *args,
        **kwargs
    ):
        default_styles = dict(
            fill_opacity=1.0,
            color="#FFFFFF",
            stroke_width=0.0,
        )
        k_str = KEY.symbol_string(symbol)
        m_strs = KEY.modifiers_string(modifiers)
        keypress_str = ' + '.join([k_str, m_strs]) if m_strs else k_str
        self.fade_delay = fade_delay
        super().__init__(text=keypress_str, *args, **default_styles, **kwargs)

    def show(self):
        return Succession(
            Wait(self.fade_delay),
            self.animate.set_opacity(0.0),
        )