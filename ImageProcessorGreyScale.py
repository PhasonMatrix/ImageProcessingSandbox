from PIL import Image
from AbstractImageProcessor import AbstractImageProcessor


class ImageProcessorGreyScale(AbstractImageProcessor):

    def process_image(self, input: Image.Image)->Image.Image:

        width, height = input.size
        output:Image.Image = Image.new("RGB", (width, height))

        for y in range(0, height):
            for x in range(0, width):

                r, g, b, *a = input.getpixel((x, y))
                
                # calculate grey level
                grey:int = int((r + g + b) / 3)

                output.putpixel((x, y), (grey, grey, grey))
        
        return output