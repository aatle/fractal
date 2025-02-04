#version 330

uniform sampler2D surface;

in vec2 uv;

void main() {
    gl_FragColor = vec4(texture(surface, uv).rgb, 1.0);
}
