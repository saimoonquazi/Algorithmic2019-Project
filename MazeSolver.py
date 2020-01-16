import sys
import os
import imageio
import glob
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PIL import Image, ImageChops
import numpy as np
import labelStartStop as lb


class App(QWidget):
    
    def __init__(self):
        super().__init__()
        self.title = 'Maze Solver'
        self.left = 10
        self.top = 10
        self.width = 1960
        self.height = 1260
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.image_chosen=None
                
        self.button_group_label=QLabel(self)
        self.button_group_label.setGeometry(QRect(1320, 5, 400, 40))
        self.button_group_label.setText("Choose Algorithm to Run")
        
        self.button_group=QLabel(self)
        self.button_group.setGeometry(QRect(1180, 40, 600, 70))
        self.button_group.setText("")
        self.button_group.setFrameShape(QFrame.Panel)
        self.button_group.setFrameShadow(QFrame.Sunken)
        self.button_group.setLineWidth(3)
        
        self.photoInfo_group=QLabel(self)
        self.photoInfo_group.setGeometry(QRect(60, 750, 640, 300))
        self.photoInfo_group.setText("")
        self.photoInfo_group.setFrameShape(QFrame.Panel)
        self.photoInfo_group.setFrameShadow(QFrame.Sunken)
        self.photoInfo_group.setLineWidth(3)
        
        self.photoInfo_title=QLabel(self)
        self.photoInfo_title.setGeometry(QRect(65, 755, 600, 20))
        self.photoInfo_title.setText("Loaded Image Information:")
        
        self.photoInfo_height_l=QLabel(self)
        self.photoInfo_height_l.setGeometry(QRect(65, 785, 600, 30))
        self.photoInfo_height_l.setText("Image Height:")
        
        self.photoInfo_height=QLabel(self)
        self.photoInfo_height.setGeometry(QRect(365, 785, 600, 20))
        self.photoInfo_height.setText("")
        
        self.photoInfo_width_l=QLabel(self)
        self.photoInfo_width_l.setGeometry(QRect(65, 815, 600, 30))
        self.photoInfo_width_l.setText("Image Width:")
        
        self.photoInfo_width=QLabel(self)
        self.photoInfo_width.setGeometry(QRect(365, 815, 600, 20))
        self.photoInfo_width.setText("")
        
        self.photoInfo_Pixel_l=QLabel(self)
        self.photoInfo_Pixel_l.setGeometry(QRect(65, 845, 600, 20))
        self.photoInfo_Pixel_l.setText("Total Number of Pixels:")
        
        self.photoInfo_Pixel=QLabel(self)
        self.photoInfo_Pixel.setGeometry(QRect(365, 845, 600, 20))
        self.photoInfo_Pixel.setText("")
        
        self.photoInfo_FilePath_l=QLabel(self)
        self.photoInfo_FilePath_l.setGeometry(QRect(65, 895, 600, 20))
        self.photoInfo_FilePath_l.setText("File Path:")
        
        self.photoInfo_FilePath=QLabel(self)
        self.photoInfo_FilePath.setGeometry(QRect(200, 875, 400, 150))
        self.photoInfo_FilePath.setWordWrap(True)
        self.photoInfo_FilePath.setText("")
        
        self.AlgoInfo_group=QLabel(self)
        self.AlgoInfo_group.setGeometry(QRect(1180, 600, 600, 300))
        self.AlgoInfo_group.setText("")
        self.AlgoInfo_group.setFrameShape(QFrame.Panel)
        self.AlgoInfo_group.setFrameShadow(QFrame.Sunken)
        self.AlgoInfo_group.setLineWidth(3)
        
        self.AlgoInfo_Title=QLabel(self)
        self.AlgoInfo_Title.setGeometry(QRect(1185, 610, 300, 20))
        self.AlgoInfo_Title.setText("Solution Info:")
        
        self.AlgoInfo_AlgoRun_l=QLabel(self)
        self.AlgoInfo_AlgoRun_l.setGeometry(QRect(1185, 660, 300, 20))
        self.AlgoInfo_AlgoRun_l.setText("Algorithm Ran:")
        
        self.AlgoInfo_AlgoRun=QLabel(self)
        self.AlgoInfo_AlgoRun.setGeometry(QRect(1535, 660, 300, 20))
        self.AlgoInfo_AlgoRun.setText("")
        
        self.AlgoInfo_SPLength_l=QLabel(self)
        self.AlgoInfo_SPLength_l.setGeometry(QRect(1185, 720, 300, 30))
        self.AlgoInfo_SPLength_l.setText("Shortest Path Length:")
        
        self.AlgoInfo_SPLength=QLabel(self)
        self.AlgoInfo_SPLength.setGeometry(QRect(1535, 720, 300, 20))
        self.AlgoInfo_SPLength.setText("")
        
        self.AlgoInfo_Total_Nodes_l=QLabel(self)
        self.AlgoInfo_Total_Nodes_l.setGeometry(QRect(1185, 780, 300, 30))
        self.AlgoInfo_Total_Nodes_l.setText("Total Nodes Visited:")
        
        self.AlgoInfo_Total_Nodes=QLabel(self)
        self.AlgoInfo_Total_Nodes.setGeometry(QRect(1535, 780, 300, 20))
        self.AlgoInfo_Total_Nodes.setText("")
        
        self.AlgoInfo_Total_Runtime_l=QLabel(self)
        self.AlgoInfo_Total_Runtime_l.setGeometry(QRect(1185, 840, 300, 30))
        self.AlgoInfo_Total_Runtime_l.setText("Total Runtime (s):")
        
        self.AlgoInfo_Total_Runtime=QLabel(self)
        self.AlgoInfo_Total_Runtime.setGeometry(QRect(1535, 840, 300, 30))
        self.AlgoInfo_Total_Runtime.setText("")
        
        
        self.load_image_button = QPushButton('Load Image', self)
        self.load_image_button.setToolTip('This is an example button')
        self.load_image_button.move(140,560)
        self.load_image_button.clicked.connect(self.load_image)
        
        self.mark_start_top_button = QPushButton('Mark Start at Top Border', self)
        self.mark_start_top_button.setToolTip('This is an example button')
        self.mark_start_top_button.move(340,560)
        self.mark_start_top_button.clicked.connect(self.label_start_top)
        
        self.mark_start_left_button = QPushButton('Mark Start at Left Border', self)
        self.mark_start_left_button.setToolTip('This is an example button')
        self.mark_start_left_button.move(340,600)
        self.mark_start_left_button.clicked.connect(self.load_image)
        
        self.removePaddingTop_button = QPushButton('Remove Padding + Mark Top', self)
        self.removePaddingTop_button.setToolTip('This is an example button')
        self.removePaddingTop_button.move(340,650)
        self.removePaddingTop_button.clicked.connect(self.load_image)
        
        self.removePaddingLeft_button = QPushButton('Remove Padding + Mark Left', self)
        self.removePaddingLeft_button.setToolTip('This is an example button')
        self.removePaddingLeft_button.move(340,700)
        self.removePaddingLeft_button.clicked.connect(self.load_image)
        
        self.RunDjikstra_button = QPushButton('Run Djikstra', self)
        self.RunDjikstra_button.setToolTip('This is an example button')
        self.RunDjikstra_button.move(1200,50)
        self.RunDjikstra_button.clicked.connect(self.run_djikstra)
        
        self.RunAstar_button = QPushButton('Run A* Algorithm', self)
        self.RunAstar_button.setToolTip('This is an example button')
        self.RunAstar_button.move(1400,50)
        self.RunAstar_button.clicked.connect(self.load_image)
        
        self.RunBFS_button = QPushButton('Run BFS', self)
        self.RunBFS_button.setToolTip('This is an example button')
        self.RunBFS_button.move(1650,50)
        self.RunBFS_button.clicked.connect(self.load_image)
        
        
        
        self.gif = QLabel(self)
        self.gif.setGeometry(QRect(1180, 120, 600, 400))
        self.gif.setText("")
        self.gif.setFrameShape(QFrame.Panel)
        self.gif.setFrameShadow(QFrame.Sunken)
        self.gif.setLineWidth(3)
        self.gif.setScaledContents(True)
        self.gif.setObjectName("Animation")
        self.gif_label = QLabel(self)
        self.gif_label.setGeometry(QRect(1370, 520, 200, 40))
        self.gif_label.setText("Solution Window")
        
        
        self.photo = QLabel(self)
        self.photo.setGeometry(QRect(60, 20, 640, 480))
        self.photo.setText("")
        self.photo.setFrameShape(QFrame.Panel)
        self.photo.setFrameShadow(QFrame.Sunken)
        self.photo.setLineWidth(3)
#        self.photo.setPixmap(QtGui.QPixmap("20 by 20 orthogonal maze.png"))
        self.photo.setScaledContents(True)
        self.photo.setObjectName("photo")
        
        self.photo_label = QLabel(self)
        self.photo_label.setGeometry(QRect(310, 495, 500, 40))
        self.photo_label.setText("")
        
        self.show()
    @pyqtSlot()
    def load_image(self):
        image_file = QFileDialog.getOpenFileName(self, "Open Maze Image", "~", "Image Files (*.png *.jpg)")
        self.image_chosen=image_file[0]
        self.photo.setPixmap(QPixmap(self.image_chosen))
        self.photo_label.setText("Loaded Maze")
        self.photoInfo_FilePath.setText(self.image_chosen)
    def label_start_top(self):
        width,height,pixels=lb.load_img(self.image_chosen, remove_border=False, start_loc='top') 
        self.photo.setPixmap(QPixmap(self.image_chosen+'marked.png'))
        self.photo_label.setText("Start and Destination Marked ")
        self.photoInfo_width.setText(str(width))
        self.photoInfo_height.setText(str(height))
        self.photoInfo_Pixel.setText(str(pixels))
    def run_djikstra(self):
        movie = QMovie("Materials/searched_movie.gif")
        self.gif.setMovie(movie)
        movie.start()
        self.AlgoInfo_AlgoRun.setText("Djikstra")
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())