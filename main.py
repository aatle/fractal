import typing
from array import array
from pathlib import Path

import moderngl
import pygame as pg

pg.init()

anchor = Path(__file__).resolve().parent

SIZE: typing.Final[tuple[int, int]] = 1920, 1080

screen = pg.display.set_mode(SIZE, pg.OPENGL | pg.DOUBLEBUF)


def to_texture(
    context: moderngl.Context,
    surface: pg.Surface,
    filter_: int = moderngl.LINEAR,
    /,
    *,
    repeat: bool = False,
) -> moderngl.Texture:
    texture = context.texture(
        size=surface.size,
        components=surface.get_bytesize(),
        data=surface.get_view("1"),
    )
    texture.swizzle = "BGRA"
    texture.filter = filter_, filter_
    texture.repeat_x = texture.repeat_y = repeat
    return texture


def create_program(
    context: moderngl.Context, vert_name: str, frag_name: str
) -> moderngl.Program:
    with (anchor / "shaders" / vert_name).open() as vert_file:
        vert_shader = vert_file.read()
    with (anchor / "shaders" / frag_name).open() as frag_file:
        frag_shader = frag_file.read()
    return context.program(vert_shader, frag_shader)


def create_uv_buffer(
    context: moderngl.Context, *, invert: bool = True
) -> moderngl.Buffer:
    # fmt: off
    if invert:
        # pygame coordinate axes (+y down)
        data = [
            # position (x, y), uv (u, v)
            -1.0, -1.0, 0.0, 0.0,  # Bottomleft
            1.0, -1.0, 1.0, 0.0,  # Bottomright
            -1.0, 1.0, 0.0, 1.0,  # Topleft
            1.0, 1.0, 1.0, 1.0,  # Topright
        ]
    else:
        # OpenGL coordinate axes (+y up)
        data = [
            # position (x, y), uv (u, v)
            -1.0, 1.0, 0.0, 1.0,  # Topleft
            1.0, 1.0, 1.0, 1.0,  # Topright
            -1.0, -1.0, 0.0, 0.0,  # Bottomleft
            1.0, -1.0, 1.0, 0.0,  # Bottomright
        ]
    # fmt: on
    return context.buffer(array("f", data))


ctx = moderngl.create_context()

mode = moderngl.TRIANGLE_STRIP
program = create_program(ctx, "uv.vert", "mandelbrot.frag")
buffer = create_uv_buffer(ctx, invert=False)
vertex_array = ctx.vertex_array(program, buffer, "in_vert", "in_uv", mode=mode)


def main() -> None:
    clock = pg.time.Clock()
    program["max_iterations"] = 100
    program["viewport_size"] = 4.5, 4.5 * (SIZE[1] / SIZE[0])
    program["viewport_center"] = 0.0, 0.0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        vertex_array.render()
        pg.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
