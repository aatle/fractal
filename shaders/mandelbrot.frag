#version 330

const float escape_radius = 20.0;
const float escape_radius_squared = escape_radius * escape_radius;

in vec2 uv;

uniform vec2 viewport_size;
uniform vec2 viewport_center;
uniform int max_iterations;

vec2 square_complex(vec2 z) {
    return vec2(z[0] * z[0] - z[1] * z[1], 2.0 * z[0] * z[1]);
}

vec3 hue_to_rgb(float hue) {
  vec3 h = vec3(hue, hue + 1.0/3.0, hue + 2.0/3.0);
  return clamp(6.0 * abs(h - floor(h) - 0.5) - 1.0, 0.0, 1.0);
}

void main() {
    vec2 c = viewport_center + (uv - 0.5) * viewport_size;
    // z[0] is real part, z[1] is imaginary part
    vec2 z = vec2(0.0);
    bool escaped = false;
    int i = 0;
    for (; i < max_iterations; i++) {
        z = square_complex(z) + c;
        if (dot(z, z) > escape_radius_squared) {
            // equivalent to |z| > escape radius
            escaped = true;
            break;
        }
    }
    float log_zn = log(dot(z, z)) / 2;
    float nu = log(log_zn / log(2)) / log(2);
    float val = i + 1 - nu;
    vec3 color;
    if (escaped) {
        color = hue_to_rgb(val / 30.0 + 0.3);
    } else {
        color = vec3(0.0);
    }
    gl_FragColor = vec4(color, 1.0);
}
