import pygame.image


class TankExplosion:
    def __init__(self, center):

        sprite_container = pygame.image.load("images/explosion_sprite.png").convert_alpha()

        self.center = center
        self.parts = []
        self.current_part_idx = -1
        self.launched = False
        self.time_accum = 0
        self._completed = False

        sprite_cols = 8
        sprite_rows = 4

        part_width = sprite_container.get_width() / sprite_cols
        part_height = sprite_container.get_height() / sprite_rows

        for row in range(0, sprite_rows):
            for col in range(0, sprite_cols):
                x = col * part_width
                y = row * part_height

                part = pygame.Surface((part_width, part_height), pygame.SRCALPHA, 32)
                part.blit(sprite_container, (0, 0), (x, y, part_width, part_height))
                self.parts.append(part)

    @property
    def completed(self):
        return self._completed

    def launch(self, center):
        if not self.launched:
            self.launched = True
            self.center = center

    def draw(self, surface):
        if self.launched:
            surface.blit(self.parts[self.current_part_idx], self.center)

            if self.current_part_idx < len(self.parts) - 1:
                self.current_part_idx += 1
            elif not self.completed:
                self._completed = True
