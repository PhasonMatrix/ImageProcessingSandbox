import math
from PIL import Image
from AbstractImageProcessor import AbstractImageProcessor


class ImageProcessorBlur(AbstractImageProcessor):


    def process_image(self, input: Image.Image)->Image.Image:

        width, height = input.size
        output:Image.Image = Image.new("RGB", (width, height))

        for y in range(1, height-1):
            for x in range(1, width-1):

                this_r, this_g, this_b, *this_a = input.getpixel((x, y))
                left_r, left_g, left_b, *left_a = input.getpixel((x-1, y))
                above_r, above_g, above_b, *above_a = input.getpixel((x, y-1))
                right_r, right_g, right_b, *right_a = input.getpixel((x+1, y))
                below_r, below_g, below_b, *below_a = input.getpixel((x, y+1))
                
                
                blured_r = int((this_r + left_r + above_r + right_r + below_r) / 5)
                blured_g = int((this_g + left_g + above_g + right_g + below_g) / 5)
                blured_b = int((this_b + left_b + above_b + right_b + below_b) / 5)
                

                output.putpixel((x, y), (blured_r, blured_g, blured_b))
        
        return output
    

