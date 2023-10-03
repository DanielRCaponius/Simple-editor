#Импорт модулей
import os
import io

from PIL import ImageFilter, ImageQt, Image

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QFileDialog, QMainWindow, QAction, QSizePolicy, QMessageBox, QScrollArea, QSlider
from PyQt5.QtGui import QPixmap, QImage

#Первая итерация импорта модулей
#from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox, QTextEdit, QLineEdit, QListWidget, QListWidgetItem, QInputDialog, QMessageBox, QGroupBox , QFileDialog, QSlider, QScrollArea, QMainWindow, QAction, QSizePolicy

#Список со всеми совершенными действиями.
#actions = []

# Класс "Действие", создаётся действие, его шорткат, заметка о нём,
# к какому разделу привязывается, функция, выполняемая при нажатии.
class action():
    def __init__(self,name,shortcut,tip,bar,function,enable):
        self.name = QAction(name)
        self.shortcut = self.name.setShortcut(shortcut)
        self.tip = self.name.setStatusTip(tip)
        self.bar = bar.addAction(self.name)
        self.function = self.name.triggered.connect(function)
        self.enable = self.name.setEnabled(enable)

# Класс изображения (вторая итерация).
class classimg():
    # Конструктор
    def __init__(self,image,img,qimg,pixmap):
        self.image = image
        self.img = img
        self.qimg = qimg
        self.pixmap = pixmap

    # Открытие изображения
    def open_image(self):
        #Выбор изображения через проводник
        self.image = QFileDialog.getOpenFileName(None,'Open Image',os.path.expanduser('~\OneDrive'),"png files (*.png);;jpg files (*.jpg)")
        #Открытие доступа к кнопкам:
        
        for act in available:
            act.name.setEnabled(True)
        
        #Создания пиксмапа, PILовского изображения и его загрузка, [0] для того, чтобы это был не кортеж.
        self.pixmap = QPixmap(self.image[0])
        self.img = Image.open(self.image[0])
        self.img.load()
        
        #Добавление в список совершенных действий, отображение последнего элемента списка.
        #actions = [self.pixmap]

        #Устанока пиксмапа и подгонка окна под его размер
        Label.setPixmap(self.pixmap)
        Label.resize(Label.pixmap().size())
        
        #Показ ползунков для скролла изображения
        vscroll.setVisible(True)
    # Сохранение изображения
    def save_image(self):
        #Открытие проводника для сохранения изображения.
        filepath, _ = QFileDialog.getSaveFileName(None,'Save Image',os.path.expanduser('~\OneDrive'),"png files (*.png);;jpg files (*.jpg)")
        
        #Сохранение по заданному пути в выбранной папке и прочем.
        self.img.save(filepath)

    # Конвертация PILовского изображения в пиксмап
    def pil2pix(self,function):
        #PILовское изображение приравнивается к редактированному функцией (указывается в function)
        self.img = function
        
        #Сохранение PILовского изображения в битах для загрузки в QImage
        bytesimg = io.BytesIO()
        self.img.save(bytesimg, format='PNG')

        #Создание QImage, в которое загружается сохраненное в битах PILовское изобр.
        self.qimg = QImage()
        self.qimg.loadFromData(bytesimg.getvalue())
        
        #Конвертация QImage в пиксмап
        self.pixmap = QPixmap.fromImage(self.qimg)
        
        #Установка пиксмапа.
        Label.setPixmap(self.pixmap)
        Label.resize(Label.pixmap().size())


        #Добавление пиксмапа в список совершенных действий.

    #Попытка сделать UNDO
    '''def undo(self):
        if len(actions) == 1:
            None
        else:
            actions.pop()
            Label.setPixmap(actions[-1])'''
        
    # Отражение по вертикали
    def mirror_y(self):
        imgobj.pil2pix(self.img.transpose(Image.FLIP_TOP_BOTTOM))

    # Отражение по горизонтали
    def mirror_x(self):
        imgobj.pil2pix(self.img.transpose(Image.FLIP_LEFT_RIGHT))

    # Поворот вправо по заданному в ползунке углу
    def rotate(self,value):
        RotateSlider.show()
        imgobj.pil2pix(self.img.rotate(value))

    # Поворот обратно на 0 градусов.
    def rotate_0(self):
        imgobj.pil2pix(self.img.rotate(0))

    # Повоорот вправо/влево на 15 градусов
    def rotate_15_r(self):
        imgobj.pil2pix(self.img.rotate(15))

    def rotate_15_l(self):
        imgobj.pil2pix(self.img.rotate(-15))

    # Наложение блюра (обычного)
    def blur(self):
        imgobj.pil2pix(self.img.filter(ImageFilter.BLUR))

    # Наложение боксового блюра с заданным радиусом
    def box_blur(self,value): 
        BlurSlider.show()
        BlurSlider.setValue(0)
        imgobj.pil2pix(self.img.filter(ImageFilter.BoxBlur(value)))

    # Наложение гауссовского блюра с заданным радиусом
    def gauss_blur(self,value):    
        BlurSlider.show()
        BlurSlider.setValue(0)
        imgobj.pil2pix(self.img.filter(ImageFilter.GaussianBlur(value)))

    # Конвертировать изображение в чёрно-белое.
    def bw(self):
        imgobj.pil2pix(self.img.convert('L'))

    # Обрезка, не будет реализовано.

# Создание приложения.

app = QApplication([])

# Создания окна.
main_window0 = QMainWindow()
main_window0.setWindowTitle('Photoshop...')
main_window0.resize(1280,720)

# Месседж бокс с ошибкой
error = QMessageBox()
error.setWindowTitle('Ошибка')
error.hide()

# QLabel для изображения.
Label = QLabel('Image')

# Прокрутка изображения
vscroll = QScrollArea()
vscroll.setWidget(Label)
vscroll.setVisible(False)
main_window0.setCentralWidget(vscroll)
vscroll.show()
# Объект изображения
imgobj = classimg(None,None,None,None)

#Ползунок для блюра.
BlurSlider = QSlider(Qt.Horizontal)

BlurSlider.setMinimum(0)
BlurSlider.setMaximum(100)
BlurSlider.setValue(0)
BlurSlider.setTickPosition(QSlider.TicksBelow)
BlurSlider.setTickInterval(10)

BlurSlider.hide()

BlurSlider.valueChanged.connect(imgobj.gauss_blur)
BlurSlider.valueChanged.connect(imgobj.box_blur)

#Ползунок для поворота.

RotateSlider = QSlider(Qt.Horizontal)

RotateSlider.setMinimum(0)
RotateSlider.setMaximum(60)
RotateSlider.setTickPosition(QSlider.TicksBelow)
RotateSlider.setTickInterval(30)

RotateSlider.setValue(0)
RotateSlider.hide()

RotateSlider.valueChanged.connect(imgobj.rotate)

#Создание менюшек для последующего добавления опций
menubar = main_window0.menuBar()
filemenu = menubar.addMenu('File')
view = menubar.addMenu('View')
filters = menubar.addMenu('Filters')
blurmenu = filters.addMenu('Blur')
colormenu = filters.addMenu('Color')

#Создание действий
# Выход, открытие файла, сохранение файла как
exitapp = action('&Quit','Ctrl+Q','Exit application',filemenu,app.quit,True)
openfile = action('&Open file','Ctrl+O','Open existing file',filemenu,imgobj.open_image,True)
savefile = action('&Save file as','Ctrl+S','Save this file',filemenu,imgobj.save_image,False)

#undo = action('Undo','Ctrl+Z','Return back',filemenu,imgobj.undo,False)

#Меню с наложением блюра.
# Нормальный, гауссовский, боксовый
normal = action('&Normal','Alt+N','Use normal blur',blurmenu,imgobj.blur,False)
gauss = action('&Gaussian','Alt+G','Use gaussian blur',blurmenu,imgobj.gauss_blur,False)
box = action('&Box','Alt+B','Use box blur',blurmenu,imgobj.box_blur,False)

#Меню с сменой цвета
# Чёрно-белый
bw = action('Black and white','Shift+B','Use black and white filter',colormenu,imgobj.bw,False)

# Меню с видом изображения
# Отражение по горизонтали/вертикали, поворот направо/налево/обратно
mirrorx = action('Mirror(x)','M','Mirror by x axis',view,imgobj.mirror_x,False)
mirrory = action('Mirror(y)','Shift+M','Mirror by y axis',view,imgobj.mirror_y,False)
rotateright = action('Rotate','R','Rotate by value',view,imgobj.rotate,False)
rotate15r = action('Rotate right (15)','6','Rotate right by 15 degrees',view,imgobj.rotate_15_r,False)
rotate15l = action('Rotate left (15)','4','Rotate left by 15 degrees',view,imgobj.rotate_15_l,False)
#return_pos = action('Rotate back','5','Rotate back to 0 degrees',view,imgobj.rotate_0,False)

available = [exitapp,openfile,savefile,normal,gauss,box,bw,mirrorx,mirrory,rotateright,rotate15l,rotate15r]


#Launch
main_window0.show()
app.exec_()

