from PIL import Image
import tkinter as tk
import app_window_class as window_helper
from image_editing_functions import *

def update_image(window: tk.Tk, img: Image):
    """Update the Tk window to re-display its picture. This needs to be called
    any time an image is changed."""

    window.display_image(img)

def open_image(window: tk.Tk) -> None:
    """Prompt for an Image file, load that image, and display it in the
    Tk window"""

    # Keep a reference to the picture so it can be modified.
    window.img = window.OpenFile()
    update_image(window, window.img)


def save_image(window: tk.Tk) -> None:
    """Save the image in the Tk window"""

    window.SaveFile()


def save_image_as(window: tk.Tk) -> None:
    """Prompt for an Image file name to save the image in the Tk window"""

    # Keep a reference to the picture so it can be modified.
    window.img = window.SaveFileAs()
    update_image(window, window.img)


def quit(root: tk.Tk)-> None:
    """Close the Tk root"""
    root.destroy()

def reset(window):
    window.img = window.ResertFile()
    update_image(window, window.img)

def filter_image(window, filter_function):
    window.img = filter_function(window.img)
    update_image(window, window.img)

if __name__ == "__main__":

    root = tk.Tk()
    window = window_helper.ImageEditingApp(root)
    window.img = None
    window.pack(side="top", fill="both", expand=True)

    # To be removed before assignment is published ----------------
    # Automatically open an image when app is launched for easy testing
    window.img = Image.open('test.png')
    window.image_file_name = 'test.png'
    window.update_root_name()
    window.display_image(window.img)
    #---------------------------------------------------------------

    # Add a menu bar
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # -------------------------------------------------------------------------
    # The File menu in the menubar --------------------------------------------
    # -------------------------------------------------------------------------
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)

    file_menu.add_command(label="Open", command = lambda: open_image(window))
    file_menu.add_separator()
    file_menu.add_command(label="Save", command = lambda: save_image(window))
    file_menu.add_command(label="Save As...",
                          command = lambda: save_image_as(window))
    file_menu.add_separator()

    file_menu.add_command(label="Quit", command = lambda: quit(root))

    # -------------------------------------------------------------------------
    # The Filter menu in the menubar ------------------------------------------
    # -------------------------------------------------------------------------

    filter_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Filter", menu=filter_menu)

    filter_menu.add_command(label="Reset Image", command=lambda: reset(window))
    filter_menu.add_separator()
    for c in COMMANDS:
        filter_menu.add_command(label=c, \
                                command= lambda c=c: filter_image(window, COMMANDS[c]))

    window.mainloop()
