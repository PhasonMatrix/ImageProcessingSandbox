# ImageProcessingSandbox

Image viewer for developing and testing image processing algorithms.

Create your own image procssing class, inheriting from `AbstractImageProcessor`, like this:

```python
class ImageProcessorInvert(AbstractImageProcessor):
    ...
```

Then implement the method `process_image(self, input: Image.Image)->Image.Image`

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


The included image processing algorithms are not designed to be efficient or best-practice. This is simply a sand-box for tring ideas.


----------------------------------
Built with wxPython GUI library.

