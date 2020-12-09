from PIL import Image
import random

# NOTE: Feel free to add in any constant values you find useful to use
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# NOTE: Feel free to add in any helper functions to organize your code but
#       do NOT rename any existing functions (or else, autograder
#       won't be able to find them!!)

# HELPER FUNCTIONS


def multi_avg(x):
    """return average colour of list of pixels"""
    r = 0
    g = 0
    b = 0
    for i in x:
        r += i[0]
        g += i[1]
        b += i[2]
    y = len(x)
    return (int(r/y),int(g/y),int(b/y))


def avg(x):
    """return average colour of pixel"""
    a,b,c = x
    y = (a+b+c)/3
    return y


def unique_num(x):
    a = []
    b = random.randint(0, x)
    for i in range(x):
        while b in a:
            b = random.randint(0, x)
        a.append(b)
    return a


def remove_red(img: Image) -> Image:
    """
    Given an Image, img, update the img to have all the reds in the original
    image turned to 0 intensity. Return img.
    """

    img_width, img_height = img.size
    pixels = img.load()  # create the pixel map

    # for every pixel
    for i in range(img_width):
        for j in range(img_height):
            r, g, b = pixels[i, j]
            pixels[i, j] = (0, g, b)

    return img


def scale_new_image(orig_img, goal_width: int = None, goal_height: int = None):
    """
    Create and return a new image which resizes the given original Image,
    orig_img to a the given goal_width and goal_height. If no goal dimensions
    are provided, scale the image down to half its original width and height.
    Return the new image.
    """

    orig_width, orig_height = orig_img.size
    orig_pixels = orig_img.load()

    if not goal_width and not goal_height:
        goal_width, goal_height = orig_width//2, orig_height//2

    img = Image.new('RGB', (goal_width, goal_height))
    new_pixels = img.load()

    width_factor = goal_width / orig_width
    height_factor = goal_height / orig_height

    for i in range(goal_width):
        for j in range(goal_height):
            new_pixels[i, j] = orig_pixels[i // width_factor, j // height_factor]
    return img


def greyscale(img: Image) -> Image:
    """
    Change the Image, img, to greyscale by taking the average color of each
    pixel in the image and set the red, blue and green values of the pixel
    with that average. Return img.
    """

    img_width, img_height = img.size
    pixels = img.load()  # create the pixel map

    # for every pixel
    for i in range(img_width):
        for j in range(img_height):
            r, g, b = pixels[i, j]
            avg = int((r + g + b) / 2)
            pixels[i, j] = (avg, avg, avg)
    return img


def black_and_white(img: Image) -> Image:
    """
    Given an Image, img, update the img to have ONLY black or white pixels.
    Return img.

    Hints:
    - Get the average color of each pixel
    - If the average is higher than the "middle" color (i.e. 255/2),
      change it to white; if it's equal to or lower, change it to black
    """

    img_width, img_height = img.size
    pixels = img.load()  # create the pixel map
    avg = 255/2
    # for every pixel
    for i in range(img_width):
        for j in range(img_height):
            r, g, b = pixels[i, j]
            pixave = (r+g+b)/2
            if pixave > avg:
                pixels[i, j] = (255, 255, 255)
            else:
                pixels[i, j] = (0,0,0)
    return img


def sepia(img: Image) -> Image:
    """
    Given an Image, img, update the img to have a sepia scheme.
    Return img.

    Hints:
    - Get the RGB value of the pixel.
    - Calculate newRed, newGree, newBlue using the formula below:

        newRed = 0.393*R + 0.769*G + 0.189*B
        newGreen = 0.349*R + 0.686*G + 0.168*B
        newBlue = 0.272*R + 0.534*G + 0.131*B
        (Take the integer value of each.)

        If any of these output values is greater than 255, simply set it to 255.
        These specific values are the recommended values for sepia tone.

    - Set the new RGB value of each pixel based on the above calculations
        (i.e. Replace the value of each R, G and B with the new value
              that we calculated for the pixel.)
    """
    img_width, img_height = img.size
    pixels = img.load()  # create the pixel map

    # for every pixel
    for i in range(img_width):
        for j in range(img_height):
            R, G, B = pixels[i, j]
            newRed = 0.393 * R + 0.769 * G + 0.189 * B
            newGreen = 0.349 * R + 0.686 * G + 0.168 * B
            newBlue = 0.272 * R + 0.534 * G + 0.131 * B
            pixels[i, j] = (int(newRed), int(newGreen), int(newBlue))
    return img


def normalize_brightness(img: Image) -> Image:
    """
    Normalize the brightness of the given Image img by:
    1. computing the average brightness of the picture:
        - this can be done by calculating the average brightness of each pixel
          in img (the average brightness of each pixel is the sum of the values
          of red, blue and green of the pixel, divided by 3 as a float division)
        - the average brightness of the picture is then the sum of all the
          pixel averages, divided by the product of the width and hight of img

    2. find the factor, let's call it x, which we can multiply the
       average brightness by to get the value of 128

    3. multiply the colors in each pixel by this factor x
    """
    b_vals = []
    img_width, img_height = img.size
    pixels = img.load()  # create the pixel map

    # for every pixel
    for i in range(img_width):
        for j in range(img_height):
            r, g, b = pixels[i, j]
            avg_b = (sum(pixels[i,j]))/3
            b_vals.append(avg_b)
    total_avg = sum(b_vals) / (img_width*img_height)
    print (total_avg)
    x = 128 / total_avg

    for i in range(img_width):
        for j in range(img_height):
            r, g, b = pixels[i, j]
            pixels[i, j] = (int(r*x),int(g*x),int(b*x))
    return img


def sort_pixels(img: Image) -> Image:
    """
    Given an Image, img, sort (in non-descending order) each row of pixels
    by the average of their RGB values. Return the updated img.

    Tip: When testing this function out, first choose the greyscale
    feature. This will make it easier to spot whether or not the pixels in each
    row are actually sorted (it should go from darkest to lightest in a
    black and white image, if the sort is working correctly).
    """
    img_width, img_height = img.size
    pixels = img.load()  # create the pixel map

    j = 0
    while j < img_height:
        d = {}
        for i in range(img_width):
            d[avg(pixels[i,j])] = pixels[i,j]
        x = sorted(d.items())
        i = 0
        while i < (len(x)):
            pixels[i,j] = x[i][1]
            i+=1
        j+=1
    print(len(x))
    return img


def blur(img: Image) -> Image:
    """Blur Image, img, based on the given pixel_size

    Hints:
    - For each pixel, calculate average RGB values of its neighbouring pixels
        (i.e. newRed = average of all the R values of each adjacent pixel, ...)
    - Set the RGB value of the center pixel to be the average RGB values of all
        the pixels around it

    Be careful at the edges of the image: not all pixels have 8 neighboring pixels!
    """

    img_width, img_height = img.size
    pixels = img.load()  # create the pixel map

    new_img = Image.new('RGB', (img_width, img_height))
    new_pixels = new_img.load()

    for i in range(img_width):
        for j in range(img_height):
            r,g,b = new_pixels[i,j]
            if i == 0 and j == 0: #topleft
                adj = [pixels[i+1,j+1], pixels[i+1,j], pixels[i,j+1]]
            elif i == (img_width-1) and j == 0: #topright
                adj = [pixels[i-1,j], pixels[i-1,j+1], pixels[i,j+1]]
            elif i == 0 and j == (img_height-1): #bottomleft
                adj = [pixels[i,j-1], pixels[i+1,j-1], pixels[i+1,j]]
            elif i == (img_width-1) and j == (img_height-1): #bottomright
                adj = [pixels[i-1,j-1], pixels[i-1,j], pixels[i,j-1]]
            elif i == 0: #leftwall
                adj = [pixels[i,j-1], pixels[i,j+1], pixels[i+1,j-1], pixels[i+1,j+1], pixels[i+1,j]]
            elif j == 0: #topwall
                adj = [pixels[i-1,j], pixels[i+1,j], pixels[i-1,j+1], pixels[i+1,j+1], pixels[i,j+1]]
            elif i == (img_width-1): #rightwall
                adj = [pixels[i-1,j-1], pixels[i-1,j], pixels[i-1,j+1], pixels[i,j-1], pixels[i,j+1]]
            elif j == (img_height-1): #bottomwall
                adj = [pixels[i,j-1], pixels[i-1,j-1], pixels[i+1,j-1], pixels[i-1,j], pixels[i+1,j]]
            else:
                adj = [pixels[i - 1, j - 1], pixels[i - 1, j], pixels[i - 1, j + 1], pixels[i, j + 1], pixels[i, j - 1],
                       pixels[i + 1, j], pixels[i + 1, j - 1], pixels[i + 1, j + 1]]
            new_pixels[i,j] = multi_avg(adj)
    return new_img


def rotate_picture_90_left(img: Image) -> Image:
    """Return a NEW picture that is the given Image img rotated 90 degrees
    to the left.

    Hints:
    - create a new blank image that has reverse width and height
    - reverse the coordinates of each pixel in the original picture, img,
        and put it into the new picture
    """
    img_width, img_height = img.size
    orig_pixels = img.load()

    new_img = Image.new('RGB', (img_height, img_width))
    new_width, new_height = new_img.size
    new_pixels = new_img.load()

    for i in range(new_width):
        for j in range(new_height):
            new_pixels[i,j] = orig_pixels[img_width-(1+j),i]
    return new_img


def rotate_picture_90_right(img: Image) -> Image:
    """
    Return a NEW picture that is the given Image img rotated 90 degrees
    to the right.
    """

    # NOTE: Remove the "pass" placeholder when you put your own code in
    img_width, img_height = img.size
    orig_pixels = img.load()

    new_img = Image.new('RGB', (img_height, img_width))
    new_width, new_height = new_img.size
    new_pixels = new_img.load()

    for i in range(new_width):
        for j in range(new_height):
            new_pixels[i, j] = orig_pixels[j,img_height-(1+i)]
    return new_img


def flip_horizontal(img: Image) -> Image:
    """
    Given an Image, img, update it so it looks like a mirror
    was placed horizontally down the middle.

    Tip: Remember Python allows you to switch values using a, b = b, a notation.
         You don't HAVE to use this here, but it might come in handy.
    """

    # NOTE: Remove the "pass" placeholder when you put your own code in
    img_width, img_height = img.size
    pixels = img.load()

    copy_img = Image.new('RGB', (img_width, img_height))
    copy_pixels = copy_img.load()

    for i in range(img_width):
        for j in range(img_height):
            copy_pixels[i,j] = pixels[i,j]

    for i in range(img_width):
        for j in range(img_height):
            pixels[i, j] = copy_pixels[i, img_height - (j + 1)]
    return img


def flip_vertical(img: Image) -> Image:
    """
    Given an Image, img, update it so it looks like a mirror
    was placed vertically down the middle.

    Tip: Remember Python allows you to switch values using a, b = b, a notation.
         You don't HAVE to use this here, but it might come in handy.
    """

    img_width, img_height = img.size
    pixels = img.load()

    copy_img = Image.new('RGB', (img_width, img_height))
    copy_pixels = copy_img.load()

    for i in range(img_width):
        for j in range(img_height):
            copy_pixels[i, j] = pixels[i, j]

    for i in range(img_width):
        for j in range(img_height):
            pixels[i, j] = copy_pixels[img_width - (i+1), j]
    return img


def kaleidoscope(img: Image) -> Image:
    """
    Given an Image, img, update it to create a kaleidoscope.
    You must maintain the size dimensions of the original image.
    Return the updated img.

    The kaleidoscope effect should have this image repeated four times:
    - the original image will be in the lower left quadrant
    - the lower right will be the original image flipped on the vertical axis
    - the two top images will be the bottom two images flipped on the horizontal axis

    Tip: You may want to use helper functions to organize the code here.
            This filter can be broken down into a series of other operations, such as
            flip vertical / horizontal, scale / downscale, etc.
    """
    img_width, img_height = img.size
    pixels = img.load()

    A_img = scale_new_image(img)
    A_width, A_height = A_img.size
    A_pixels = A_img.load()

    for i in range(A_width):
        for j in range(A_height):
                pixels[i,j+img_height//2] = A_pixels[i,j]

    B_img = flip_vertical(A_img)
    B_width, B_height = B_img.size
    B_pixels = B_img.load()

    for i in range(B_width):
        for j in range(B_height):
                pixels[i+img_width//2,j+img_height//2] = B_pixels[i,j]

    C_img = Image.new('RGB', (img_width, A_height))
    C_pixels = C_img.load()

    for i in range(img_width):
        for j in range(A_height):
            C_pixels[i,j] = pixels[i,j+img_height//2]

    D_img = flip_horizontal(C_img)
    D_pixels = D_img.load()

    for i in range(img_width):
        for j in range(A_height):
            pixels[i,j] = D_pixels[i,j]

    return img


def draw_border(img: Image) -> Image:
    """
    Given an Image, img, update it to have a five pixel wide black border
    around the edges. Return the updated img.
    """

    img_width, img_height = img.size
    pixels = img.load()  # create the pixel map

    # for every pixel
    for i in range(img_width):
        for j in range(5):
           r,g,b =  pixels[i,j]
           pixels[i,j] = (0,0,0)
        for j in range(img_height - 5, img_height):
            r, g, b = pixels[i, j]
            pixels[i, j] = (0,0,0)

    for v in range(img_height):
        for k in range(5):
           r,g,b =  pixels[k,v]
           pixels[k,v] = (0,0,0)
        for k in range(img_width - 5, img_width):
            r, g, b = pixels[k,v]
            pixels[k,v] = (0, 0, 0)

    return img


def scramble(img: Image) -> Image:
    """
    Scramble the pixels in the image by re-assigning each color intensity
    value to a unique randomly generated number. Store information that can
    be used to decrypt (e.g. what each original intensity value is now mapped
    to) in a file named key.txt. Return the scrambled image.

    Note:
    Figure out a good way to assign each number from 0-255 to a specific
    new number (there should be a 1-1 relationship between the old number and
    a new one). Consider using random.randint to generate numbers.
    Then, go through each pixel in the image and reset each RGB value to the
    newly mapped number.

    You should use helper functions to clean up your code, if applicable.
    """
    d = {}
    nums = unique_num(256)
    for i in range(256):
        d[i] = nums[i]

    with open('key.txt', 'w') as key:
        x = d.items()
        for i in x:
            key.write(str(i) + '\n')

    img_width, img_height = img.size
    pixels = img.load()  # create the pixel map

    # for every pixel
    for i in range(img_width):
        for j in range(img_height):
            r,g,b = pixels[i,j]
            pixels[i,j] = (d[r],d[g],d[b])
    return img


def unscramble(img: Image) -> Image:
    """
    Unscramble the pixels in the image by re-assigning each color intensity
    value to its original value based on the information in file named "key.txt".

    If the file is empty, do nothing and just return the original image back.
    You may assume this file exists.

    Note:
        You can't just hard-code some calculations in to unscramble each pixel
        Your key.txt file must be formatted in a way that the data in it lets you
        revert each pixel, and that file data must be used in this function.
    """
    reverse_key = {}
    with open('key.txt', 'r') as key:
        for line in key:
            x = line.strip('  ()\n').split(',')
            if int(x[1]) not in reverse_key:
                reverse_key[int(x[1])] = int(x[0])
            else:
                print (str(x[1])+'  '+str(x[0]))
    img_width, img_height = img.size
    pixels = img.load()  # create the pixel map

    # for every pixel
    for i in range(img_width):
        for j in range(img_height):
            r, g, b = pixels[i, j]
            pixels[i, j] = (reverse_key[r], reverse_key[g], reverse_key[b])
    return img


def pastelify(img: Image) -> Image:
    '''
    changes the tint of a pic to a pinkish purplish pastel colour
    '''
    img_width, img_height = img.size
    pixels = img.load()
    b_vals = []
    for i in range(img_width):
        for j in range(img_height):
            r, g, b = pixels[i, j]
            avg_b = (r+b+g)/3
            b_vals.append(avg_b)
    total_avg = sum(b_vals) / (img_width*img_height)
    x = 128 / total_avg

    for i in range(img_width):
        for j in range(img_height):
            r, g, b = pixels[i, j]
            r2 = int(r*x)
            g2 = int(b*x)
            b2 = int(g*x)
            pixels[i, j] = (r2,g2,b2)
    return img


def endgame(img: Image) -> Image:
    '''
    Re-arrange the pixels in the image according RGB averages to achieve
    the thanos snap effect from endgame
    '''
    img_width, img_height = img.size
    pixels = img.load()  # create the pixel map

    j = 0
    while j < img_height:
        pix_avs = []
        for i in range(img_width):
            r, g, b = pixels[i,j]
            avg_val = (r+g+b)/3
            pix_avs.append(avg_val)
        pix_avs.sort()
        for item in pix_avs:
            for i in range(img_width):
                if avg(pixels[i,j]) == item:
                    g = pix_avs.index(item)
                    pixels[g,j] = pixels[i,j]
        j+=1
    return img


def inverse(img: Image) -> Image:
    """
    Returns a inverted colour image
    """
    img_width, img_height = img.size
    pixels = img.load()  # create the pixel map

    # for every pixel
    for i in range(img_width):
        for j in range(img_height):
            r,g,b = pixels[i, j]
            newR = 255 - r
            newG = 255 - g
            newB = 255 - b
            pixels[i, j] = (newR, newG, newB)
    return img

COMMANDS = {
    "Remove red": remove_red,
    "Downscale": scale_new_image,
    "Greyscale": greyscale,
    "Black and White": black_and_white,
    "Sepia": sepia,
    "Normalize Brightness": normalize_brightness,
    "Sort Pixels": sort_pixels,
    "Blur": blur,
    "Kaleidoscope": kaleidoscope,
    "Rotate Clockwise": rotate_picture_90_right,
    "Rotate Counter-clockwise": rotate_picture_90_left,
    "Flip Horizontal": flip_horizontal,
    "Flip Vertical": flip_vertical,
    "Add border": draw_border,
    "Scramble": scramble,
    "Unscramble": unscramble,
    "Pastelify": pastelify,
    "EndGame": endgame,
    "Inverse": inverse
    }

