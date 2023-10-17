from pygame.math import Vector2

frame_ms = 17


def quadratic_formula(a, b, c):
    if a == 0:
        return [0, 0]
    desc = (b * b - 4 * a * c)
    if desc >= 0:
        desc = desc ** (1 / 2)
        return [(-b + desc) / (2 * a), (-b - desc) / (2 * a)]
    else:
        return [0, 0]


def manage_obj_collision(obj1, obj2):
    v1 = obj1.velocity
    v2 = obj2.velocity
    p1 = obj1.position
    p2 = obj2.position

    # print(f'Tank 1 - {obj1.name}, Tank 2 - {obj2.name}')
    # print(f'Initial p1: {p1}')
    # print(f'Initial p2: {p2}')
    # print(f"Initial v1: {v1}")
    # print(f"Initial v2: {v2}")

    D = p2 - p1
    # print(f'Distance between: {D.magnitude()}')
    if D.length() == 0:
        # print('equal position of tanks')
        return

    p1_next = p1 + (v1 * frame_ms)
    p2_next = p2 + (v2 * frame_ms)

    d_next = p2_next - p1_next
    # print(f'Distance between on next frame: {d_next.magnitude()}')
    if d_next.magnitude() > D.magnitude():
        # print(f'already moving away each other, omit vector calculations')
        return

    unit_norm = D.normalize()
    unit_tan = Vector2(-unit_norm.y, unit_norm.x)

    v1n = unit_norm * v1
    v1t = unit_tan * v1
    v2n = unit_norm * v2
    v2t = unit_tan * v2

    v1t_prime_scal = v1t
    v2t_prime_scal = v2t

    v1n_prime_scal = v2n
    v2n_prime_scal = v1n

    v1n_prime = v1n_prime_scal * unit_norm
    v1t_prime = v1t_prime_scal * unit_tan
    v2n_prime = v2n_prime_scal * unit_norm
    v2t_prime = v2t_prime_scal * unit_tan

    v1_prime = v1n_prime + v1t_prime
    v2_prime = v2n_prime + v2t_prime

    obj1.velocity = v1_prime
    obj2.velocity = v2_prime

    # Check if balls have overlapped each other.
    v1 = v1_prime
    v2 = v2_prime
    norm = p1 - p2
    distance = norm.magnitude()
    overlap = obj2.radius + obj1.radius - distance

    # print(f'New v1: {v1}')
    # print(f'New v2: {v2}')
    # print(f'Overlapping {overlap} px.')
    if overlap > 0:
        # Re-set the positions so the balls don't get stuck, by passing a small amount of time for the two balls.
        a = (v1 - v2).magnitude() ** 2
        b = (p1 - p2) * (v1 - v2)
        c = (p1 - p2).magnitude() ** 2 - (obj2.radius + obj1.radius) ** 2
        solutions = quadratic_formula(a, b, c)
        if solutions[0] > 0:
            delta_t = solutions[0]
        else:
            delta_t = solutions[1]

        # print(f'Overlap calc: a = {a}, b = {b}, c = {c}, solutions = {solutions[0]}, {solutions[1]}')
        # print(f'Result dt = {delta_t}')
        obj1.update(delta_t)
        obj2.update(delta_t)
