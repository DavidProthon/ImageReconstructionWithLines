import cv2
import numpy as np
import time

start_time = time.time()

PIXELS_BETWEEN_PEGS = 4
FIRST_PEG_POSITION = (0, 0) # Top left
GRAY_SHADE = 4
THICKNESS = 0
picture_name = "Brno-Cathedral-of-St-Peter.jpg"

def open_picture(filepath):
    """
    Load picture and returning its dimensions.
    """

    image = cv2.imread(filepath)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = gray_image.shape

    return gray_image, height, width

def create_line_image(height, width):
    """
    Create blank picture with proportions of original picture.
    """

    line_image = np.full((height, width), 255, dtype=np.uint8)

    return line_image

def check_position_of_actual_peg(peg_position,height, width):
    """
    Determines whether a node is in a corner or on an edge of the image.
    """
    
    x, y = peg_position

    if x == 0 and y == 0:
        return "top_left_corner"
    elif x == width - 1 and y == 0:
        return "top_right_corner"
    elif x == 0 and y == height - 1:
        return "bottom_left_corner"
    elif x == width - 1 and y == height - 1:
        return "bottom_right_corner"
    
    elif y == 0 and (0 < x < width - 1):
        return "top_edge_pegs"
    elif y == height - 1 and (0 < x < width - 1):
        return "bottom_edge_pegs"
    elif x == 0 and (0 < y < height - 1):
        return "left_edge_pegs"
    elif x == width - 1 and (0 < y < height - 1):
        return "right_edge_pegs"
    
def get_end_peg_positions(initial_peg_position):
    """
    Determines the final edges and corners based on the peg position name.
    """
    
    end_peg_positions = []

    if initial_peg_position == "top_left_corner":
        end_peg_positions = ["bottom_edge_pegs", "right_edge_pegs", "bottom_right_corner"]
    elif initial_peg_position == "top_right_corner":
        end_peg_positions = ["bottom_edge_pegs", "left_edge_pegs", "bottom_left_corner"]
    elif initial_peg_position == "bottom_left_corner":
        end_peg_positions = ["top_edge_pegs", "right_edge_pegs", "top_right_corner"]
    elif initial_peg_position == "bottom_right_corner":
        end_peg_positions = ["top_edge_pegs", "left_edge_pegs", "top_left_corner"]

    elif initial_peg_position == "top_edge_pegs":
        end_peg_positions = ["left_edge_pegs", "right_edge_pegs", "bottom_edge_pegs", "bottom_left_corner", "bottom_right_corner"]
    elif initial_peg_position == "bottom_edge_pegs":
        end_peg_positions = ["left_edge_pegs", "right_edge_pegs", "top_edge_pegs", "top_left_corner", "top_right_corner"]
    elif initial_peg_position == "left_edge_pegs":
        end_peg_positions = ["top_edge_pegs", "right_edge_pegs", "bottom_edge_pegs", "top_right_corner", "bottom_right_corner"]
    elif initial_peg_position == "right_edge_pegs":
        end_peg_positions = ["top_edge_pegs", "left_edge_pegs", "bottom_edge_pegs", "top_left_corner", "bottom_left_corner"]

    return end_peg_positions 

def get_pegs_positions(PIXELS_BETWEEN_PEGS,image_height, image_width):
    """
    Generate peg positions along the edges of an image with uniform spacing, ensuring fixed corner pegs.
    """
    
    # Calculate number of segments (spaces between pegs)
    num_x_segments = max(1, round((image_width - 1) / PIXELS_BETWEEN_PEGS))
    num_y_segments = max(1, round((image_height - 1) / PIXELS_BETWEEN_PEGS))

    top_left_corner = (0, 0)
    top_right_corner = (image_width - 1, 0)
    bottom_left_corner = (0, image_height - 1)
    bottom_right_corner = (image_width - 1, image_height - 1)
    top_edge_pegs = [(int(x), 0) for x in np.linspace(0, image_width - 1, num_x_segments + 1)][1:-1]
    bottom_edge_pegs = [(int(x), image_height - 1) for x in np.linspace(0, image_width - 1, num_x_segments + 1)][1:-1]
    left_edge_pegs = [(0, int(y)) for y in np.linspace(0, image_height - 1, num_y_segments + 1)][1:-1]
    right_edge_pegs = [(image_width - 1, int(y)) for y in np.linspace(0, image_height - 1, num_y_segments + 1)][1:-1]

    return {
        "top_left_corner": top_left_corner,
        "top_right_corner": top_right_corner,
        "bottom_left_corner": bottom_left_corner,
        "bottom_right_corner": bottom_right_corner,
        "top_edge_pegs": top_edge_pegs,
        "bottom_edge_pegs": bottom_edge_pegs,
        "left_edge_pegs": left_edge_pegs,
        "right_edge_pegs": right_edge_pegs,
    }

def bresenham_line_new(start, end, thickness, canvas_size=None):
    """
    Modified Bresenham line algorithm that also accounts for line thickness.
    """

    x0, y0 = start
    x1, y1 = end

    pixels = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        pixels.append((x0, y0))

        if thickness > 0:
            for dx_offset in range(-thickness, thickness + 1):
                for dy_offset in range(-thickness, thickness + 1):
                    if dx_offset**2 + dy_offset**2 <= thickness**2:
                        nx, ny = x0 + dx_offset, y0 + dy_offset
                        if (nx, ny) != (x0, y0):
                            pixels.append((nx, ny))

        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

    if canvas_size is not None:
        height, width = canvas_size
        pixels = [
            (x, y) for (x, y) in pixels
            if 0 <= x < width and 0 <= y < height
        ]
    
    return pixels

def select_necessary_pegs(end_peg_positions, pegs_coordinates):
    """
    Selects all pegs for which a Bresenham line will be constructed.
    """

    pegs = []

    for edge in end_peg_positions:
        if edge in pegs_coordinates:  
            value = pegs_coordinates[edge]
            
            if isinstance(value, tuple):  
                pegs.append(value)
            elif isinstance(value, list): 
                pegs.extend(value)

    return pegs

def get_mean_gray(image,pixels):
    """
    Calculates the mean gray value of the provided pixels.
    """

    gray_values = [image[y, x] for x, y in pixels]
    average_gray_value = np.mean(gray_values)

    return average_gray_value

def add_gray_to_line_image(image,pixels,GRAY_SHADE):
    """
    Adds a gray shade to all provided pixels in the image.
    """

    for pixel in pixels:
        reversed_pixel = (pixel[1], pixel[0])
        current_amount_of_gray = int(image[reversed_pixel])
        new_gray_value = max(0, current_amount_of_gray - GRAY_SHADE)
        image[reversed_pixel] = new_gray_value  

    return image  # Return modified image

    
def subtract_gray_from_gray_image(image,pixels,GRAY_SHADE):
    """
    Subtract a gray shade from all provided pixels in the image.
    """

    for pixel in pixels:
        reversed_pixel = (pixel[1], pixel[0])
        current_amount_of_gray = int(image[reversed_pixel])
        new_gray_value = min(255, current_amount_of_gray + GRAY_SHADE)
        image[reversed_pixel] = new_gray_value  # Update the image pixel

    return image 

def compute_LSE(original_image, line_image):
    squared_error = (original_image.astype(np.float32) - line_image.astype(np.float32)) ** 2
    total_error = np.sum(squared_error)

    # Compute normalization factor
    N = original_image.shape[0] * original_image.shape[1]
    norm_factor = 255**2 * N  # Maximum possible error

    LSE = total_error / norm_factor

    return LSE
    
def main():
    gray_image, height, width = open_picture(picture_name)  
    copied_gray_image = gray_image.copy()
    line_image = create_line_image(height, width)
    start_peg_position = FIRST_PEG_POSITION
    error = 1
    number_of_lines = 0 

    while True:
        positon_of_peg = check_position_of_actual_peg(start_peg_position,height, width)
        end_peg_positions = get_end_peg_positions(positon_of_peg)
        pegs_coordinates = get_pegs_positions(PIXELS_BETWEEN_PEGS,height, width)
        all_pegs = select_necessary_pegs(end_peg_positions, pegs_coordinates)

        max_gray = 255  
        end_point = (0,0)
        pixels_to_change = tuple()

        for peg in all_pegs:
            pixel_in_bresenham_line = bresenham_line_new(start_peg_position, peg, THICKNESS, canvas_size=(height, width))
            mean_gray = get_mean_gray(gray_image,pixel_in_bresenham_line)

            if mean_gray < max_gray:
                max_gray = mean_gray
                end_point = peg
                pixels_to_change = pixel_in_bresenham_line 

        add_gray_to_line_image(line_image,pixels_to_change,GRAY_SHADE)
        subtract_gray_from_gray_image(gray_image,pixels_to_change,GRAY_SHADE)
        least_square_error = compute_LSE(copied_gray_image, line_image)

        if least_square_error < error:
            error = least_square_error
            number_of_lines += 1
            print(f"number_of_lines: {number_of_lines}")
            print(error)
            #if number_of_lines % 100 == 0:
                #cv2.imwrite(f"{picture_name}_PBP-{PIXELS_BETWEEN_PEGS}_GS-{GRAY_SHADE}_LSE-{least_square_error:.3f}_LN-{number_of_lines}_TH-{THICKNESS}.png", line_image)
        else:
            break  

        start_peg_position = end_point

    end_time = time.time()
    elapsed_time = end_time - start_time

    cv2.imshow("Line Image", line_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
                
    cv2.imwrite(f"{picture_name}_PBP-{PIXELS_BETWEEN_PEGS}_GS-{GRAY_SHADE}_LSE-{least_square_error:.3f}_TH-{THICKNESS}_LN-{number_of_lines}_ET-{elapsed_time:.0f}.png", line_image)

if __name__ == "__main__":
    main()

