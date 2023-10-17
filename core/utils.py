import secrets

import pygame


def rotate_center(image, angle):
    """rotate an image while keeping its center and size"""

    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def cleanup_angle(angle):
    angle_rem = angle % 360
    if angle_rem <= 180:
        return angle_rem
    else:
        return angle_rem - 360


def unique_object_id():
    return secrets.token_hex(nbytes=24)


def final_score_sort_key(player):
    return player.score, player.health
