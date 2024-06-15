# ImageProcessingSandbox

Image viewer for developing and testing image processing algorithms. Side-by-side viewer for before-and-after images. Zoom and pan for inspecting details. Chain processes together by swapping the output image back into the input for the next process.

![ImageProcessingSandboxScreenshot](https://github.com/PhasonMatrix/ImageProcessingSandbox/assets/37615629/1a0702c2-7d66-41e8-b561-7dc02d42f2ca)


Create your own image processing class, inheriting from `AbstractImageProcessor`, like this:

```python
class ImageProcessorInvert(AbstractImageProcessor):
    ...
```

Then implement the method `process_image()`

Then, add it to the list of selectable processors in `MainWindow.SetUpImageProcessors()`

```python
    def SetUpImageProcessors(self):

        self.processors:dict = {}

        #-----------------------------------------------------------------------#
        #                                                                       #
        #  Add your custom image processor here to make it available in the UI  #
        #                                                                       #
        #-----------------------------------------------------------------------#

        processor_name_greyscale = "Greyscale"
        self.processors[processor_name_greyscale] = ImageProcessorGreyScale()

        processor_name_edge_detect = "Edge detect"
        self.processors[processor_name_edge_detect] = ImageProcessorEdgeDetect()

        processor_name_invert = "Invert"
        self.processors[processor_name_invert] = ImageProcessorInvert()

        processor_name_blur = "Blur"
        self.processors[processor_name_blur] = ImageProcessorBlur()


```


The included image processing algorithms are not designed to be efficient or best-practice. This is simply a sand-box for trying ideas.


----------------------------------
Built with wxPython GUI library.

