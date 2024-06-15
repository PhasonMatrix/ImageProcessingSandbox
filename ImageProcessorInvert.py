import math
from PIL import Image
from AbstractImageProcessor import AbstractImageProcessor


class ImageProcessorInvert(AbstractImageProcessor):

    def process_image(self, input: Image.Image)->Image.Image:

        width, height = input.size

        output:Image.Image = Image.new("RGB", (width, height))

        for y in range(0, height):
            for x in range(0, width):

                r, g, b, *a = input.getpixel((x, y))
                inverse_r = 255 - r
                inverse_g = 255 - g
                inverse_b = 255 - b
                output.putpixel((x, y), (inverse_r, inverse_g, inverse_b))
        
        return output
    

    @staticmethod
    def pythagorian_colour_distance(r1, g1, b1, r2, g2, b2):
        return int(math.sqrt((r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2))
