import sys
import os
import RunBfs as BFS
from gifMaker import * 
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import labelStartStop as lb
import shutil
import RunDjikstra as dj
import RunAstar as astar


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
        self.AlgoInfo_group.setGeometry(QRect(1180, 600, 700, 300))
        self.AlgoInfo_group.setText("")
        self.AlgoInfo_group.setFrameShape(QFrame.Panel)
        self.AlgoInfo_group.setFrameShadow(QFrame.Sunken)
        self.AlgoInfo_group.setLineWidth(3)
        
        self.AlgoInfo_Title=QLabel(self)
        self.AlgoInfo_Title.setGeometry(QRect(1185, 610, 300, 20))
        self.AlgoInfo_Title.setText("Solution Info:")
        
        self.AlgoInfo_AlgoRun_l=QLabel(self)
        self.AlgoInfo_AlgoRun_l.setGeometry(QRect(1185, 660, 300, 20))
        self.AlgoInfo_AlgoRun_l.setText("Status:")
        
        self.AlgoInfo_AlgoRun=QLabel(self)
        self.AlgoInfo_AlgoRun.setGeometry(QRect(1485, 660, 400, 50))
        self.AlgoInfo_AlgoRun.setWordWrap(True)
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
        
        self.show_visited_button = QPushButton('Show Visited Nodes', self)
        self.show_visited_button.setToolTip('Show Animation of all visited nodes by algorithm')
        self.show_visited_button.move(840,260)
        self.show_visited_button.clicked.connect(self.show_visited_gif)
        
        self.show_visited_button = QPushButton('Show Solved Path', self)
        self.show_visited_button.setToolTip('Show animation of solved shortest path')
        self.show_visited_button.move(840,320)
        self.show_visited_button.clicked.connect(self.show_solved_path_gif)
        
        self.load_image_button = QPushButton('Load Image', self)
        self.load_image_button.setToolTip('Load Maze Image from device')
        self.load_image_button.move(140,560)
        self.load_image_button.clicked.connect(self.load_image)
        
        self.mark_start_top_button = QPushButton('Mark End at Top Border', self)
        self.mark_start_top_button.setToolTip('Process the input image to put end position on the top')
        self.mark_start_top_button.move(340,560)
        self.mark_start_top_button.clicked.connect(self.label_start_top)
        
        self.mark_start_left_button = QPushButton('Mark End at Left Border', self)
        self.mark_start_left_button.setToolTip('Process the input image to put end position on the left')
        self.mark_start_left_button.move(340,600)
        self.mark_start_left_button.clicked.connect(self.label_start_left)
        
        self.removePaddingTop_button = QPushButton('Remove Padding + Mark Top', self)
        self.removePaddingTop_button.setToolTip('Remove any white padding in the image and make end on top')
        self.removePaddingTop_button.move(340,650)
        self.removePaddingTop_button.clicked.connect(self.remove_pad_label_top)
        
        self.removePaddingLeft_button = QPushButton('Remove Padding + Mark Left', self)
        self.removePaddingLeft_button.setToolTip('Remove any white padding in the image and make end on left')
        self.removePaddingLeft_button.move(340,700)
        self.removePaddingLeft_button.clicked.connect(self.remove_pad_label_left)
        
        self.RunDjikstra_button = QPushButton('Run Djikstra', self)
        self.RunDjikstra_button.setToolTip('Run Djikstra Algorithm on Selected Maze Image')
        self.RunDjikstra_button.move(1200,50)
        self.RunDjikstra_button.clicked.connect(self.run_djikstra)
        
        self.RunAstar_button = QPushButton('Run A* Algorithm', self)
        self.RunAstar_button.setToolTip('Run A* Algorithm on Selected Maze Image')
        self.RunAstar_button.move(1400,50)
        self.RunAstar_button.clicked.connect(self.run_astar)
        
        self.RunBFS_button = QPushButton('Run BFS', self)
        self.RunBFS_button.setToolTip('Run BFS Algorithm on Selected Maze Image')
        self.RunBFS_button.move(1650,50)
        self.RunBFS_button.clicked.connect(self.run_BFS)
        
        
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
    def initialize_temp_fold(self):
        if os.path.exists('test'):
            shutil.rmtree('test')
        if os.path.exists('solved'):
            shutil.rmtree('solved')
                
        if not os.path.exists('test'):
            os.makedirs('test')
        if not os.path.exists('solved'):
            os.makedirs('solved')
            
    def load_image(self):
        self.initialize_temp_fold()
        image_file = QFileDialog.getOpenFileName(self, "Open Maze Image", "~", "Image Files (*.png *.jpg)")
        self.image_chosen=image_file[0]
        self.photo.setPixmap(QPixmap(self.image_chosen))
        self.photo_label.setText("Loaded Maze")
        self.photoInfo_FilePath.setText(self.image_chosen)
        
    def label_start_top(self):
        width,height,pixels=lb.load_img(self.image_chosen, remove_border=False, start_loc='top') 
        self.photo.setPixmap(QPixmap(self.image_chosen+'marked.png'))
        self.image_chosen=self.image_chosen+'marked.png'
        self.photo_label.setText("Start and Destination Marked ")
        self.photoInfo_width.setText(str(width))
        self.photoInfo_height.setText(str(height))
        self.photoInfo_Pixel.setText(str(pixels))
        
    def label_start_left(self):
        width,height,pixels=lb.load_img(self.image_chosen, remove_border=False, start_loc='left') 
        self.photo.setPixmap(QPixmap(self.image_chosen+'marked.png'))
        self.image_chosen=self.image_chosen+'marked.png'
        self.photo_label.setText("Start and Destination Marked ")
        self.photoInfo_width.setText(str(width))
        self.photoInfo_height.setText(str(height))
        self.photoInfo_Pixel.setText(str(pixels))
        
    def remove_pad_label_top(self):
        width,height,pixels=lb.load_img(self.image_chosen, remove_border=True, start_loc='top') 
        self.photo.setPixmap(QPixmap(self.image_chosen+'marked.png'))
        self.image_chosen=self.image_chosen+'marked.png'
        self.photo_label.setText("Start and Destination Marked ")
        self.photoInfo_width.setText(str(width))
        self.photoInfo_height.setText(str(height))
        self.photoInfo_Pixel.setText(str(pixels))
        
    def remove_pad_label_left(self):
        width,height,pixels=lb.load_img(self.image_chosen, remove_border=True, start_loc='left') 
        self.photo.setPixmap(QPixmap(self.image_chosen+'marked.png'))
        self.image_chosen=self.image_chosen+'marked.png'
        self.photo_label.setText("Start and Destination Marked ")
        self.photoInfo_width.setText(str(width))
        self.photoInfo_height.setText(str(height))
        self.photoInfo_Pixel.setText(str(pixels))
    
    def show_visited_gif(self):
        make_searched_gif()
        movie = QMovie("searched_movie.gif")
        self.gif.setMovie(movie)
        movie.start()
    def show_solved_path_gif(self):
        make_solved_gif()
        movie = QMovie("solved_movie.gif")
        self.gif.setMovie(movie)
        movie.start()
        
    def run_djikstra(self):
        self.initialize_temp_fold()
        self.AlgoInfo_AlgoRun.setText("Running Djikstra Algorithm")
        start_time = time.time()
        path_info=dj.run_djikstra(self.image_chosen)
        end_time=time.time()-start_time
        self.AlgoInfo_AlgoRun.setText("Djikstra Successfully Found a Path")
        self.AlgoInfo_SPLength.setText(str(path_info[0]))
        self.AlgoInfo_Total_Nodes.setText(str(path_info[1]))
        self.AlgoInfo_Total_Runtime.setText(str(end_time))
        make_solved_gif()
        movie = QMovie("solved_movie.gif")
        self.gif.setMovie(movie)
        movie.start()
        
    def run_astar(self):
        self.initialize_temp_fold()
        self.AlgoInfo_AlgoRun.setText("Running A* Algorithm")
        start_time = time.time()
        path_info=astar.runAstar(self.image_chosen)
        end_time=time.time()-start_time
        self.AlgoInfo_AlgoRun.setText("A* Algorithm Successfully Found a Path")
        self.AlgoInfo_SPLength.setText(str(path_info[0]))
        self.AlgoInfo_Total_Nodes.setText(str(path_info[1]))
        self.AlgoInfo_Total_Runtime.setText(str(end_time))
        make_solved_gif()
        movie = QMovie("solved_movie.gif")
        self.gif.setMovie(movie)
        movie.start()
        
    def run_BFS(self):
        self.initialize_temp_fold()
        self.AlgoInfo_AlgoRun.setText("Running BFS Algorithm")
        start_time = time.time()
        path_info=BFS.run_BFS(self.image_chosen)
        end_time=time.time()-start_time
        self.AlgoInfo_AlgoRun.setText("Breadth First Search Successfully Found a Path")
        self.AlgoInfo_SPLength.setText(str(path_info[0]))
        self.AlgoInfo_Total_Nodes.setText(str(path_info[1]))
        self.AlgoInfo_Total_Runtime.setText(str(end_time))
        make_solved_gif()
        movie = QMovie("solved_movie.gif")
        self.gif.setMovie(movie)
        movie.start()        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())