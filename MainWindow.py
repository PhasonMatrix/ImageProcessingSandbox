import wx
from wx.lib.floatcanvas.FCObjects import ScaledBitmap
from wx.lib.floatcanvas.FloatCanvas import FloatCanvas
import PIL.Image
from AbstractImageProcessor import AbstractImageProcessor
from ImageProcessorBlur import ImageProcessorBlur
from ImageProcessorEdgeDetect import ImageProcessorEdgeDetect
from ImageProcessorGreyScale import ImageProcessorGreyScale
from ImageProcessorInvert import ImageProcessorInvert


class MainWindow(wx.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, size=(1600,900))

        self.SetUpImageProcessors()

        self.previous_mouse_x = 0
        self.previous_mouse_y = 0

        self.SetBackgroundColour("#e8e8e8")
        self.grid_sizer = wx.BoxSizer(wx.HORIZONTAL)

        left_panel = wx.Panel(self)
        left_panel_sizer = wx.BoxSizer(wx.VERTICAL)

        load_image_button = wx.Button(left_panel, label="Load image", size=(150,30))
        self.Bind(wx.EVT_BUTTON, self.OnLoadButtonClick, load_image_button)

        processor_label= wx.StaticText(left_panel, label="Select a process.")
        processor_label.Wrap(150)
        self.processor_combobox = wx.ComboBox(left_panel, value = "", choices=list(self.processors.keys()), style=wx.CB_READONLY)

        process_image_button = wx.Button(left_panel, label="Process", size=(150,30))
        self.Bind(wx.EVT_BUTTON, self.OnProcessButtonClick, process_image_button)

        recycle_label= wx.StaticText(left_panel, label="Recycle the output image (right) back to become input (left) for next process.")
        recycle_label.Wrap(150)
        recycle_image_button = wx.Button(left_panel, label="Input<-Output", size=(150,30))
        self.Bind(wx.EVT_BUTTON, self.OnRecycleButtonClick, recycle_image_button)

        save_result_button = wx.Button(left_panel, label="Save result", size=(150,30))
        self.Bind(wx.EVT_BUTTON, self.OnSaveResultButtonClick, save_result_button)

        left_panel_sizer.Add(load_image_button, proportion=0, flag = wx.EXPAND|wx.ALL, border = 5)
        left_panel_sizer.Add(processor_label, proportion=0, flag = wx.EXPAND|wx.ALL, border = 5)
        left_panel_sizer.Add(self.processor_combobox, proportion=0, flag = wx.EXPAND|wx.ALL, border = 5)
        left_panel_sizer.Add(process_image_button, proportion=0, flag = wx.EXPAND|wx.ALL, border = 5)
        left_panel_sizer.Add(recycle_label, proportion=0, flag = wx.EXPAND|wx.ALL, border = 5)
        left_panel_sizer.Add(recycle_image_button, proportion=0, flag = wx.EXPAND|wx.ALL, border = 5)
        left_panel_sizer.Add(save_result_button, proportion=0, flag = wx.EXPAND|wx.ALL, border = 5)
        left_panel.SetSizer(left_panel_sizer)

        self.left_canvas = FloatCanvas(self)
        self.left_canvas.Draw()
        self.left_canvas.Bind(wx.EVT_MOUSEWHEEL, self.OnWheel)
        self.left_canvas.Bind(wx.EVT_LEFT_DCLICK, self.ZoomToFit)
        self.left_canvas.Bind(wx.EVT_MOTION, self.OnMouseMove)
        
        self.right_canvas = FloatCanvas(self)
        self.right_canvas.Draw()
        self.right_canvas.Bind(wx.EVT_MOUSEWHEEL, self.OnWheel)
        self.right_canvas.Bind(wx.EVT_LEFT_DCLICK, self.ZoomToFit)
        self.right_canvas.Bind(wx.EVT_MOTION, self.OnMouseMove)
    
        self.grid_sizer.Add(left_panel, proportion=0, flag = wx.ALL|wx.EXPAND, border=10)
        self.grid_sizer.Add(self.left_canvas, proportion=1, flag = wx.ALL|wx.EXPAND, border=10)
        self.grid_sizer.Add(self.right_canvas, proportion=1, flag = wx.ALL|wx.EXPAND, border=10)

        self.SetSizer(self.grid_sizer)



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






    def OnWheel(self, event:wx.MouseEvent):

        zoom_amount = 1.1
        if event.GetWheelRotation() < 0:
            zoom_amount = 1 / 1.1 

        self.left_canvas.Zoom(zoom_amount, event.Position,"Pixel", keepPointInPlace=True)
        self.right_canvas.Zoom(zoom_amount, event.Position, "Pixel", keepPointInPlace=True)
    


    def ZoomToFit(self, event):
        self.left_canvas.ZoomToBB()
        self.right_canvas.ZoomToBB()



    def OnMouseMove(self, event:wx.MouseEvent):
        if event.Dragging():
            current_x, current_y = event.GetPosition()
            diff_x = current_x - self.previous_mouse_x 
            diff_y = current_y - self.previous_mouse_y  
            self.left_canvas.MoveImage((-diff_x, -diff_y), "Pixel")
            self.right_canvas.MoveImage((-diff_x, -diff_y), "Pixel")
            self.previous_mouse_x = current_x
            self.previous_mouse_y = current_y
        else:
            self.previous_mouse_x, self.previous_mouse_y = event.GetPosition()


    def OnLoadButtonClick(self, event):
        openFileDialog = wx.FileDialog(
            self, "Open image file", "", "", 
            "Image files (*.bmp;*.png;*.jpg;*.jpeg)|*.bmp;*.png;*.jpg;*.jpeg", 
            wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if openFileDialog.ShowModal() == wx.ID_OK:
            file_path = openFileDialog.GetPath()
            self.left_image:wx.Image = wx.Image(file_path)
            self.DrawLeftImage()
            self.left_canvas.ZoomToBB()
            self.right_canvas.ZoomToBB()
        openFileDialog.Destroy()


    def OnRecycleButtonClick(self, event):
        self.left_image = self.right_image
        self.DrawLeftImage()
        self.left_canvas.ZoomToBB()
        self.right_canvas.ZoomToBB()


    def OnProcessButtonClick(self, event):
        input_image:PIL.Image.Image = self.WxImageToPilImage(self.left_image)
        self.SetCursor(wx.Cursor(wx.CURSOR_WAIT))

        processor_name = self.processor_combobox.GetValue()
        if processor_name != None and processor_name != "":
            processor:AbstractImageProcessor = self.processors[processor_name]
            result_image:PIL.Image.Image = processor.process_image(input_image)

            self.right_image:wx.Image = self.PilImageToWxImage(result_image)
            self.DrawRightImage()

        self.SetCursor(wx.Cursor(wx.CURSOR_DEFAULT))
        self.left_canvas.ZoomToBB()
        self.right_canvas.ZoomToBB()


    def DrawLeftImage(self):
        self.left_canvas.ClearAll()
        self.left_canvas.Refresh()
        w, h = self.left_canvas.GetSize()
        left_scaled_bitmap = ScaledBitmap(self.left_image, (0,0), h, 'cc')
        self.left_canvas.AddObject(left_scaled_bitmap)
        self.left_canvas.Draw()
    

    def DrawRightImage(self):
        self.right_canvas.ClearAll()
        self.right_canvas.Refresh()
        w, h = self.right_canvas.GetSize()
        right_scaled_bitmap = ScaledBitmap(self.right_image, (0,0), h, 'cc')
        self.right_canvas.AddObject(right_scaled_bitmap)
        self.right_canvas.Draw()
    

    def OnSaveResultButtonClick(self, event):
        if self.right_image != None:
            openFileDialog = wx.FileDialog(
                self, "Save image file", "", "", 
                "PNG (*.png)|*.png|JPG (*.jpg)|*.jpg",
                wx.FD_SAVE)
            if openFileDialog.ShowModal() == wx.ID_OK:
                file_path = openFileDialog.GetPath()
                file_type_selection = openFileDialog.GetCurrentlySelectedFilterIndex()
                
                print(file_path, file_type_selection)
                if file_type_selection == 0: # save as png
                    self.right_image.SaveFile(file_path, wx.BITMAP_TYPE_PNG)
                elif file_type_selection == 1: # save as jpg
                    self.right_image.SaveFile(file_path, wx.BITMAP_TYPE_JPEG)

            openFileDialog.Destroy()



    def WxImageToPilImage(self, wxImage:wx.Image) -> PIL.Image.Image:
        myPilImage:PIL.Image.Image = PIL.Image.new('RGB', (wxImage.GetWidth(), wxImage.GetHeight()))
        myPilImage.frombytes(wxImage.GetData())
        return myPilImage


    def PilImageToWxImage(self, pilImage:PIL.Image.Image) -> wx.Image:
        wxImage:wx.Image = wx.EmptyImage(pilImage.size[0], pilImage.size[1])
        wxImage.SetData(pilImage.convert('RGB').tobytes())
        return wxImage


