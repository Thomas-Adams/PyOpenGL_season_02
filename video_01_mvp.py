import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy
from pyrr import matrix44, Vector3
import TextureLoader


def window_resize(window, width, height):
    glViewport(0, 0, width, height)


def main():

    # initialize glfw
    if not glfw.init():
        return

    w_width, w_height = 1280, 720
    aspect_ratio = w_width / w_height

    window = glfw.create_window(w_width, w_height, "My OpenGL window", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, window_resize)

    #        positions        texture_coords
    cube = [-0.5, -0.5,  0.5, 0.0, 0.0,
             0.5, -0.5,  0.5, 1.0, 0.0,
             0.5,  0.5,  0.5, 1.0, 1.0,
            -0.5,  0.5,  0.5, 0.0, 1.0,

            -0.5, -0.5, -0.5, 0.0, 0.0,
             0.5, -0.5, -0.5, 1.0, 0.0,
             0.5,  0.5, -0.5, 1.0, 1.0,
            -0.5,  0.5, -0.5, 0.0, 1.0,

             0.5, -0.5, -0.5, 0.0, 0.0,
             0.5,  0.5, -0.5, 1.0, 0.0,
             0.5,  0.5,  0.5, 1.0, 1.0,
             0.5, -0.5,  0.5, 0.0, 1.0,

            -0.5,  0.5, -0.5, 0.0, 0.0,
            -0.5, -0.5, -0.5, 1.0, 0.0,
            -0.5, -0.5,  0.5, 1.0, 1.0,
            -0.5,  0.5,  0.5, 0.0, 1.0,

            -0.5, -0.5, -0.5, 0.0, 0.0,
             0.5, -0.5, -0.5, 1.0, 0.0,
             0.5, -0.5,  0.5, 1.0, 1.0,
            -0.5, -0.5,  0.5, 0.0, 1.0,

             0.5,  0.5, -0.5, 0.0, 0.0,
            -0.5,  0.5, -0.5, 1.0, 0.0,
            -0.5,  0.5,  0.5, 1.0, 1.0,
             0.5,  0.5,  0.5, 0.0, 1.0]

    cube = numpy.array(cube, dtype=numpy.float32)

    indices = [ 0,  1,  2,  2,  3,  0,
                4,  5,  6,  6,  7,  4,
                8,  9, 10, 10, 11,  8,
               12, 13, 14, 14, 15, 12,
               16, 17, 18, 18, 19, 16,
               20, 21, 22, 22, 23, 20]

    indices = numpy.array(indices, dtype=numpy.uint32)

    vertex_shader = """
    #version 330
    in layout(location = 0) vec3 position;
    in layout(location = 1) vec2 texture_cords;

    uniform mat4 mvp;

    out vec2 textures;

    void main()
    {
        gl_Position =  mvp * vec4(position, 1.0f);
        textures = texture_cords;
    }
    """

    fragment_shader = """
    #version 330
    in vec2 textures;

    out vec4 color;
    uniform sampler2D tex_sampler;

    void main()
    {
        color = texture(tex_sampler, textures);
    }
    """
    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, cube.itemsize * len(cube), cube, GL_STATIC_DRAW)

    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.itemsize * len(indices), indices, GL_STATIC_DRAW)

    #position
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, cube.itemsize * 5, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    #textures
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, cube.itemsize * 5, ctypes.c_void_p(12))
    glEnableVertexAttribArray(1)

    texture = TextureLoader.load_texture("res/crate.jpg")

    glUseProgram(shader)

    glClearColor(0.2, 0.3, 0.2, 1.0)
    glEnable(GL_DEPTH_TEST)

    model = matrix44.create_from_translation(Vector3([1.0, 0.0, 0.0]))
    view = matrix44.create_from_translation(Vector3([0.0, 0.0, -3.0]))
    projection = matrix44.create_perspective_projection_matrix(45.0, aspect_ratio, 0.1, 100.0)

    mv = matrix44.multiply(model, view)
    mvp = matrix44.multiply(mv, projection)
    #print(mvp)

    mvp_loc = glGetUniformLocation(shader, "mvp")
    glUniformMatrix4fv(mvp_loc, 1, GL_FALSE, mvp)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()