class TextObject:
    def __init__(self, text: str, font, color, center=None, topright=None):
        self._font = font
        self._color = color
        self._center = center
        self._topright = topright
        self._text = text

    @property
    def font(self):
        return self._font

    @property
    def color(self):
        return self._color

    @property
    def center(self):
        return self._center

    @property
    def topright(self):
        return self._topright

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    @color.setter
    def color(self, color):
        self._color = color

    def update(self, text, center=None, topright=None):
        self._text = text
        self._center = center
        self._topright = topright

    def draw(self, surface):
        text_surface, text_rect = self.render_text()
        if self.center is not None:
            text_rect.center = self.center
        elif self.topright is not None:
            text_rect.topright = self.topright

        surface.blit(text_surface, text_rect)

    def render_text(self):
        r = self.font.render(self.text, True, self.color)
        return r, r.get_rect()
