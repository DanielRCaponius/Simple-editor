#Modules import
import os
import io

from PIL import ImageFilter, ImageQt, Image

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QFileDialog, QMainWindow, QAction, QSizePolicy, QMessageBox, QScrollArea, QSlider
from PyQt5.QtGui import QPixmap, QImage

#All actions list (a try to make undo fucntion)
#actions = []

# Class actions , it's name, shortcut, tip for it, in which bar located, function, enability
class action():
    def __init__(self,name,shortcut,tip,bar,function,enable):
        self.name = QAction(name)
        self.shortcut = self.name.setShortcut(shortcut)
        self.tip = self.name.setStatusTip(tip)
        self.bar = bar.addAction(self.name)
        self.function = self.name.triggered.connect(function)
        self.enable = self.name.setEnabled(enable)

# Image class
class classimg():
    # Class constructor
    def __init__(self,image,img,qimg,pixmap):
        self.image = image
        self.img = img
        self.qimg = qimg
        self.pixmap = pixmap

    # Image opening
    def open_image(self):
        # Choose image through file explorer
        self.image = QFileDialog.getOpenFileName(None,'Open Image',os.path.expanduser('~\OneDrive'),"png files (*.png);;jpg files (*.jpg)")
        # Making all buttons available after opening image
        
        for act in available:
            act.name.setEnabled(True)
        
        #Creating pixmap, PIL image and loading it.
        self.pixmap = QPixmap(self.image[0])
        self.img = Image.open(self.image[0])
        self.img.load()
        
        #Part of undo function, list of all pixmaps
        #actions = [self.pixmap]

        #Setting pixmap with correct size
        Label.setPixmap(self.pixmap)
        Label.resize(Label.pixmap().size())
        
        #Setting scrolls visible
        vscroll.setVisible(True)
    # Saving image
    def save_image(self):
        #Saving image through file explorer
        filepath, _ = QFileDialog.getSaveFileName(None,'Save Image',os.path.expanduser('~\OneDrive'),"png files (*.png);;jpg files (*.jpg)")
        
        #Saving image by filepath
        self.img.save(filepath)

    # Conversion of PILimage to QPixmap
    def pil2pix(self,function):
        #PILimage equalts to redacted one by function
        self.img = function
        
        #Saving PILimage as bytes for conversion in QImage
        bytesimg = io.BytesIO()
        self.img.save(bytesimg, format='PNG')

        #Creating QImage, then we load bytes in it.
        self.qimg = QImage()
        self.qimg.loadFromData(bytesimg.getvalue())
        
        #Convert QImage to pixmap
        self.pixmap = QPixmap.fromImage(self.qimg)
        
        #Setting pixmap
        Label.setPixmap(self.pixmap)
        Label.resize(Label.pixmap().size())

    #Try to make undo
    '''def undo(self):
        if len(actions) == 1:
            None
        else:
            actions.pop()
            Label.setPixmap(actions[-1])'''
        
    # Mirror by vertical
    def mirror_y(self):
        imgobj.pil2pix(self.img.transpose(Image.FLIP_TOP_BOTTOM))

    # Mirror by horizontal
    def mirror_x(self):
        imgobj.pil2pix(self.img.transpose(Image.FLIP_LEFT_RIGHT))

    # Rotate image by slider (It's works cursed ._.)
    def rotate(self,value):
        RotateSlider.show()
        imgobj.pil2pix(self.img.rotate(value))

    # Rotate to 0 (doesn't work as expected)
    def rotate_0(self):
        imgobj.pil2pix(self.img.rotate(0))

    # Rotate right/left by 15 dergrees.
    def rotate_15_r(self):
        imgobj.pil2pix(self.img.rotate(15))

    def rotate_15_l(self):
        imgobj.pil2pix(self.img.rotate(-15))

    # Regular blur
    def blur(self):
        imgobj.pil2pix(self.img.filter(ImageFilter.BLUR))

    # Box blur with radius on slider (same thing...)
    def box_blur(self,value): 
        BlurSlider.show()
        BlurSlider.setValue(0)
        imgobj.pil2pix(self.img.filter(ImageFilter.BoxBlur(value)))

    # Gauss blur with radius on slider.
    def gauss_blur(self,value):    
        BlurSlider.show()
        BlurSlider.setValue(0)
        imgobj.pil2pix(self.img.filter(ImageFilter.GaussianBlur(value)))

    # Black and white
    def bw(self):
        imgobj.pil2pix(self.img.convert('L'))


# Creating app

app = QApplication([])

# Creating window
main_window0 = QMainWindow()
main_window0.setWindowTitle('Photoshop...')
main_window0.resize(1280,720)

# Error message box
error = QMessageBox()
error.setWindowTitle('Ошибка')
error.hide()

# QLabel for image.
Label = QLabel('Image')

# Scoll image
vscroll = QScrollArea()
vscroll.setWidget(Label)
vscroll.setVisible(False)
main_window0.setCentralWidget(vscroll)
vscroll.show()
# Image object
imgobj = classimg(None,None,None,None)

# Blur slider
BlurSlider = QSlider(Qt.Horizontal)

BlurSlider.setMinimum(0)
BlurSlider.setMaximum(100)
BlurSlider.setValue(0)
BlurSlider.setTickPosition(QSlider.TicksBelow)
BlurSlider.setTickInterval(10)

BlurSlider.hide()

BlurSlider.valueChanged.connect(imgobj.gauss_blur)
BlurSlider.valueChanged.connect(imgobj.box_blur)

#Rotate slider

RotateSlider = QSlider(Qt.Horizontal)

RotateSlider.setMinimum(0)
RotateSlider.setMaximum(60)
RotateSlider.setTickPosition(QSlider.TicksBelow)
RotateSlider.setTickInterval(30)

RotateSlider.setValue(0)
RotateSlider.hide()

RotateSlider.valueChanged.connect(imgobj.rotate)

#Menubars
menubar = main_window0.menuBar()
filemenu = menubar.addMenu('File')
view = menubar.addMenu('View')
filters = menubar.addMenu('Filters')
blurmenu = filters.addMenu('Blur')
colormenu = filters.addMenu('Color')

# Creating actions
# Exit applicaton , open file, save file as
exitapp = action('&Quit','Ctrl+Q','Exit application',filemenu,app.quit,True)
openfile = action('&Open file','Ctrl+O','Open existing file',filemenu,imgobj.open_image,True)
savefile = action('&Save file as','Ctrl+S','Save this file',filemenu,imgobj.save_image,False)

#undo = action('Undo','Ctrl+Z','Return back',filemenu,imgobj.undo,False)

# Blursbar
# Normal, gauss, box
normal = action('&Normal','Alt+N','Use normal blur',blurmenu,imgobj.blur,False)
gauss = action('&Gaussian','Alt+G','Use gaussian blur',blurmenu,imgobj.gauss_blur,False)
box = action('&Box','Alt+B','Use box blur',blurmenu,imgobj.box_blur,False)

# Colorsbar
# Blackandwhite
bw = action('Black and white','Shift+B','Use black and white filter',colormenu,imgobj.bw,False)

# Image view
# Mirror by h/v, rortate, rotate15r/l, return to 0
mirrorx = action('Mirror(x)','M','Mirror by x axis',view,imgobj.mirror_x,False)
mirrory = action('Mirror(y)','Shift+M','Mirror by y axis',view,imgobj.mirror_y,False)
rotateright = action('Rotate','R','Rotate by value',view,imgobj.rotate,False)
rotate15r = action('Rotate right (15)','6','Rotate right by 15 degrees',view,imgobj.rotate_15_r,False)
rotate15l = action('Rotate left (15)','4','Rotate left by 15 degrees',view,imgobj.rotate_15_l,False)
#return_pos = action('Rotate back','5','Rotate back to 0 degrees',view,imgobj.rotate_0,False)
#All bar parts
available = [exitapp,openfile,savefile,normal,gauss,box,bw,mirrorx,mirrory,rotateright,rotate15l,rotate15r]


#Launch
main_window0.show()
app.exec_()

