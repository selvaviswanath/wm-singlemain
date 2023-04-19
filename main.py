#!/usr/bin/env python3

import Xlib.display
import Xlib.X
import Xlib.XK
import Xlib.protocol.event

# Constants
MOD = Xlib.X.Mod4Mask
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3

# Class representing a workspace
class Workspace:
    def __init__(self, windows=[]):
        self.windows = windows

# Class representing the window manager
class WindowManager:
    def __init__(self):
        # Initialize X11 display and root window
        self.display = Xlib.display.Display()
        self.root = self.display.screen().root

        # Set up key bindings
        self.bind_keys()

        # Initialize workspaces
        self.workspaces = [Workspace()]

        # Run main event loop
        self.run()

    def bind_keys(self):
        # Bind keys for window management
        self.root.grab_key(Xlib.X.AnyKey, MOD, True, Xlib.X.GrabModeAsync, Xlib.X.GrabModeAsync)
        self.root.grab_button(Xlib.X.AnyButton, MOD, True, Xlib.X.ButtonPressMask|Xlib.X.ButtonReleaseMask|Xlib.X.PointerMotionMask, Xlib.X.GrabModeAsync, Xlib.X.GrabModeAsync, None, None)

        self.root.bind_key(Xlib.XK.XK_h, MOD, self.move_window, LEFT)
        self.root.bind_key(Xlib.XK.XK_l, MOD, self.move_window, RIGHT)
        self.root.bind_key(Xlib.XK.XK_k, MOD, self.move_window, UP)
        self.root.bind_key(Xlib.XK.XK_j, MOD, self.move_window, DOWN)

        self.root.bind_key(Xlib.XK.XK_Tab, MOD, self.cycle_workspace, 1)
        self.root.bind_key(Xlib.XK.XK_1, MOD, self.switch_workspace, 0)
        self.root.bind_key(Xlib.XK.XK_2, MOD, self.switch_workspace, 1)
        self.root.bind_key(Xlib.XK.XK_3, MOD, self.switch_workspace, 2)

    def run(self):
        while True:
            event = self.display.next_event()
            if event.type == Xlib.X.KeyPress:
                key = event.detail
                if key == Xlib.XK.XK_q:
                    break

    def move_window(self, direction):
        window = self.display.get_input_focus().focus
        if not window:
            return
        workspace = self.get_current_workspace()
        if direction == LEFT:
            window.configure(x=window.get_geometry().x - 20)
        elif direction == RIGHT:
            window.configure(x=window.get_geometry().x + 20)
        elif direction == UP:
            window.configure(y=window.get_geometry().y - 20)
        elif direction == DOWN:
            window.configure(y=window.get_geometry().y + 20)
        if window not in workspace.windows:
            workspace.windows.append(window)

    def cycle_workspace(self, direction):
        current_workspace = self.get_current_workspace_index()
        num_workspaces = len(self.workspaces)
        new_workspace = (current_workspace + direction) % num_workspaces
        self.set_current_workspace(new_workspace)

    def switch_workspace(self, index):
        self.set_current_workspace(index)

    def get_current_workspace(self):
        current_workspace_index = self.get_current_workspace_index()
        return self.workspaces[current_workspace_index]

    def get_current_workspace_index(self):
        for i, workspace in enumerate(self.workspaces):
            if self.root.get_full_property(self.display
