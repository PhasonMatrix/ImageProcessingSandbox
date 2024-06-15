import math
from PIL import Image
from AbstractImageProcessor import AbstractImageProcessor


class ImageProcessorEdgeDetect(AbstractImageProcessor):


    def process_image(self, input: Image.Image)->Image.Image:

        width, height = input.size
        output:Image.Image = Image.new("RGB", (width, height))

        for y in range(0, height-1):
            for x in range(0, width-1):

                this_r, this_g, this_b, *this_a = input.getpixel((x, y))
                right_r, right_g, right_b, *right_a = input.getpixel((x+1, y))
                below_r, below_g, below_b, *below_a = input.getpixel((x, y+1))
                
                horizontal_diff = self.pythagorian_colour_distance(this_r, this_g, this_b, right_r, right_g, right_b)
                vertical_diff = self.pythagorian_colour_distance(this_r, this_g, this_b, below_r, below_g, below_b)


                output.putpixel((x, y), (horizontal_diff, vertical_diff, 0))
        
        return output
    

    @staticmethod
    def pythagorian_colour_distance(r1, g1, b1, r2, g2, b2):
        return int(math.sqrt((r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2))
