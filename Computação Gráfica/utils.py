import glfw

class WindowHandler:
    def __init__(self, width: int, height: int, title: str):
        if not glfw.init():
            raise Exception("glfw didn't initialize")
        
        self.window = glfw.create_window(width, height, title, None, None)

        if not self.window:
            glfw.terminate()
            raise Exception("glfw window cannot be created")
        
        glfw.set_window_pos(self.window, 200, 150)
        glfw.make_context_current(self.window)

    def main_loop(self):
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            glfw.swap_buffers(self.window)
        
        glfw.terminate()

if __name__ == "__main__":
    window_handler = WindowHandler(1280, 720, "www")
    window_handler.main_loop()

