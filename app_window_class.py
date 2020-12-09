from tkinter import *
from tkinter import filedialog, ttk
from PIL import ImageTk, Image
import os

IMAGE_FORMATS = "*.jpg *.jpeg *.bmp *.gif *.tif *.tiff *.im *.msp *.png " \
                "*.pcx *.ppm"
# ************************
# Scrollable Frame Class
# ************************
class ScrollFrame(Frame):
    """A GUI frame with a scrollbar"""

    # Credit for this class is given to
    # https://gist.github.com/mp035/9f2027c3ef9172264532fcd6262f3b01
    # with some modifications

    def __init__(self, parent: Frame) -> None:
        """Initiate a frame with a scrollbar"""

        super().__init__(parent)  # create a frame (self)

        self.canvas = Canvas(self, borderwidth=0)  # place canvas on self
        # place a frame on the canvas, this frame will hold the child widgets
        self.viewPort = Frame(self.canvas)
        # place a scrollbar on self
        self.vsb = Scrollbar(self, orient="vertical",
                                command=self.canvas.yview)
        self.hsb = Scrollbar(self, orient="horizontal", command=self.canvas.xview)

        # attach scrollbar action to scroll of canvas
        self.canvas.configure(yscrollcommand=self.vsb.set,
                              xscrollcommand=self.hsb.set)

        # pack scrollbar to right of self
        self.vsb.pack(side="right", fill="y")
        # pack scrollbar to bottom of self
        self.hsb.pack(side="bottom", fill="x")
        # pack canvas to left of self and expand to fil
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_window = self.canvas.create_window((4, 4),
                                        window=self.viewPort, anchor="nw",
                                        # add view port frame to canvas
                                        tags="self.viewPort")

        # bind an event whenever the size of the viewPort frame changes.
        self.viewPort.bind("<Configure>", self.onFrameConfigure)
        # bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>", self.onCanvasConfigure)
        # perform an initial stretch on render, otherwise the scroll region has
        # a tiny border until the first resize
        self.onFrameConfigure(None)

    def onFrameConfigure(self, event) -> None:
        """Reset the scroll region to encompass the inner frame"""

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def onCanvasConfigure(self, event) -> None:
        """Reset the canvas window to encompass inner frame when required"""

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


# ************************
# ImageEditingApp Class
# ************************
class ImageEditingApp(Frame):
    """A GUI of the Image Editing application"""

    def __init__(self, root: Frame) -> None:
        """Initiate the Image Editing App along with its gadgets"""

        root.title("Image Editor")
        ws = root.winfo_screenwidth()  # width of the screen
        hs = root.winfo_screenheight()  # height of the screen
        w, h = ws * 0.6, hs * 0.7
        self.w, self.h = w, h
        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        # set the dimensions of the screen and where it is placed
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.master = root

        # set some styles
        self.style = ttk.Style()
        self.style.configure('Black.TLabelframe.Label', foreground ='black')

        Frame.__init__(self, root)
        self.scrollFrame = ScrollFrame(self)  # add a new scrollable frame.

        self.create_screen_components()
        # pack scrollFrame itself
        self.scrollFrame.pack(side="top", fill="both", expand=True, padx=(5,0),
                              pady=(5,0))

    def create_screen_components(self)-> None:
        """Create the components of the app screen including text and
        image box"""

        # Put things in rows to organize gadgets.
        r = 0
        # select a file Label
        Label(self.scrollFrame.viewPort, text=' Select options to open/modify images from'
                                              ' the menu bar at the top',
              font = "Arial 15 bold").grid(row=r, column=0, sticky=W)
        r += 1

        # Create image box
        self.image_box = ttk.LabelFrame(self.scrollFrame.viewPort,
                                        text="Loaded image will be shown here",
                                        height=int(self.h / 1.4),
                                        width=int(self.w / 1.05),
                                        style='Black.TLabelframe')

        self.image_box.grid(row=r, sticky="ew")
        self.image_label, self.image_row = None, r
        self.img, self.image_file_name= None, None
        r += 1

        self.error_massage = Label(self.scrollFrame.viewPort, fg='red',
                                   anchor=W, justify=LEFT)
        self.error_massage.grid(row=r, column=0, columnspan = 1, sticky=W)

    def OpenFile(self) -> None:
        """Prompt the user to select an image to process"""

        self.image_file_name = filedialog.askopenfilename(
            filetypes=(("Image File", IMAGE_FORMATS), ("All Files", "*.*")),
            title="Choose a file.")

        # If a file is selected, check its validity
        try:
            self.update_root_name()
            self.error_massage['text'] = ""
            self.img = Image.open(self.image_file_name)
            return self.img

        except:
            self.error_massage.config(fg='red')
            self.error_massage['text'] = \
                "couldn't open the file. Try again."

    def SaveFile(self) -> None:
        """Save the self.img Image into self.image_file_name file"""

        if self.image_file_name:
            try:
                self.img.save(self.image_file_name)
                self.error_massage['text'] = ""
            except:
                self.error_massage.config(fg='red')
                self.error_massage['text'] = \
                    "couldn't save the file. try again later"
        else:
            self.error_massage.config(fg='red')
            self.error_massage['text'] = "Open an image first"

    def SaveFileAs(self) -> None:
        """Save the self.img Image into a file picked by the user"""

        if self.image_file_name:
            try:
                new_file_name = filedialog.asksaveasfile(mode='wb',
                                defaultextension=".png", filetypes=(
                                ("Image File", "*.png"),("All Files", "*.*")),
                                title="Choose a file.")

                self.img.save(new_file_name)

                self.image_file_name = new_file_name.name
                self.update_root_name()
                self.error_massage['text'] = ""
                self.img = Image.open(self.image_file_name)
                return self.img

            except:
                return self.img

        else:
            self.error_massage.config(fg='red')
            self.error_massage['text'] = "Open an image first"

    def ResertFile(self) -> Image:
        """Return the last saved state of the Image self.img and update
        self.img to that state"""

        self.img.close()
        self.img = Image.open(self.image_file_name)
        return self.img

    def update_root_name(self) -> None:
        """Update the window name at the top to add the opened file name"""

        new_root_title = "Image Editor --- Current image:  " + \
                         os.path.split(str(self.image_file_name))[1]
        self.master.title(new_root_title)

    def display_image(self, img: Image) -> None:
        """Display the selected image file in its appropriate frame"""

        try:
            # If there is already an image there, remove it
            if self.image_label:
                self.image_label.image = None

            # properly display the loaded image
            img = ImageTk.PhotoImage(self.resize_image(img))
            self.image_label = Label(self.image_box, image=img)
            self.image_label.image = img
            self.image_label.grid(row=self.image_row, column=0, sticky=W)
            self.error_massage['text'] = ""

        except:
            self.error_massage.config(fg='red')
            self.error_massage['text'] = "The selected image cannot be opened"


    def resize_image(self, img: Image) -> Image:
        """Uniformly resize the provided img to fit the app image frame and
        return the img"""

        img_w, img_h = img.size
        frame_w, frame_h = self.w/1.05, self.h/1.4

        ratio = min(1, frame_w/img_w, frame_h/img_h)

        new_img_w, new_img_h = int(img_w*ratio), int(img_h*ratio)
        return img.resize((new_img_w, new_img_h), Image.ANTIALIAS)
