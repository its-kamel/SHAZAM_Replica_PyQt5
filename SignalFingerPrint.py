# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'songRecognition.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import ntpath
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog,QApplication,QFileDialog
from PyQt5.uic import loadUi
import os
from librosa.feature.spectral import mfcc
from numpy import disp, float16
from scipy.io import wavfile
from scipy.signal import spectrogram
import librosa
import matplotlib.pyplot as plt
import PIL as Image
import imagehash
from imagehash import hex_to_hash
import glob
from glob import glob
import librosa.display
from PIL import Image
import imagehash
from imagehash import hex_to_hash
import numpy as np



class Ui_MainWindow( QDialog):
    def setupUi(self, MainWindow):
        
        self.inserted_song_1=''
        self.inserted_song_2=''
        self.inserted_song_1_data=''
        self.inserted_song_2_data=''
        self.inserted_song_1_sample_rate=''
        self.inserted_song_2_sample_rate=''
        self.inserted_song_hash1=0
        self.inserted_song_hash2=0
        self.filePath='./Songs_wav'
        self.comparison_difference=[]
        self.comparison_difference_mixer=[]
        self.similiraties = []
        self.similiraties_mixer=[]
        self.listSongsPaths=[]
        self.full_songs_hash=[]
        self.displayed_mix_index=[]
        self.displayed_mix_path=[]
        self.displayed_index=[]
        self.displayed_path=[]
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(685, 405)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Song1_FileName = QtWidgets.QLineEdit(self.centralwidget)
        self.Song1_FileName.setGeometry(QtCore.QRect(10, 30, 251, 20))
        self.Song1_FileName.setObjectName("Song1_FileName")
        self.Song1_Browse = QtWidgets.QPushButton(self.centralwidget)
        self.Song1_Browse.setGeometry(QtCore.QRect(280, 30, 101, 23))
        self.Song1_Browse.setObjectName("Song1_Browse")
        self.Song2_FileName = QtWidgets.QLineEdit(self.centralwidget)
        self.Song2_FileName.setGeometry(QtCore.QRect(10, 70, 251, 20))
        self.Song2_FileName.setObjectName("Song2_FileName")
        self.Song2_Browse = QtWidgets.QPushButton(self.centralwidget)
        self.Song2_Browse.setGeometry(QtCore.QRect(280, 70, 101, 23))
        self.Song2_Browse.setObjectName("Song2_Browse")
        self.Song2_Percentage = QtWidgets.QSlider(self.centralwidget)
        self.Song2_Percentage.setGeometry(QtCore.QRect(490, 70, 181, 22))
        self.Song2_Percentage.setOrientation(QtCore.Qt.Horizontal)
        self.Song2_Percentage.setObjectName("Song2_Percentage")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(30, 140, 600, 201))
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableWidget.setRowCount(10)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(350)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setVisible(True)
        self.Mix_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Mix_Button.setGeometry(QtCore.QRect(540, 100, 75, 23))
        self.Mix_Button.setObjectName("Mix_Button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 685, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.Song1_Browse.clicked.connect(lambda:self.browsefiles(self.Song1_Browse))
        self.Song2_Browse.clicked.connect(lambda:self.browsefiles(self.Song2_Browse))
        self.Mix_Button.clicked.connect(self.reading_and_hashing)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def browsefiles(self,button):
        fname=QFileDialog.getOpenFileName(self, 'Open file',self.filePath)
        if button==self.Song1_Browse:
            self.Song1_FileName.setText(fname[0])
            self.inserted_song_1 = fname[0]
        else:
            self.Song2_FileName.setText(fname[0])
            self.inserted_song_2 = fname[0]
            

    def reading_and_hashing(self):
        #reading songs
        self.folderSongsPaths() 
        # print('Reading Songs')
        
        self.reading_input_songs()
# 
        # self.folder_songs_hash_spec()
        # print('Finished Hash/Spec extraction')
        
        self.read_from_txt()

        if self.inserted_song_2 != '':
            self.mixer()
            self.display_data_mixer()
        else:
            self.compare_similiarities()
            self.display_data()
            
        # self.hash_to_txt()
        # self.read_from_txt()
        self.restart()
        
    #file iteration
    def folderSongsPaths(self):
        for song in os.listdir(self.filePath):
            self.listSongsPaths.append(os.path.join(self.filePath,song))
        return 0
    
    def reading_input_songs(self):
        #new song 1
        self.inserted_song_1_data,self.inserted_song_1_sample_rate=librosa.load(self.inserted_song_1 , duration = 60)
        mfccs1 = librosa.feature.mfcc(self.inserted_song_1_data, sr=self.inserted_song_1_sample_rate)
        self.inserted_song_hash1 = self.Hash(mfccs1)
        if self.inserted_song_2 != '':
            #new song 2
            self.inserted_song_2_data,self.inserted_song_2_sample_rate=librosa.load(self.inserted_song_2 , duration = 60)
            mfccs2 = librosa.feature.mfcc(self.inserted_song_2_data, sr=self.inserted_song_2_sample_rate)
            self.inserted_song_hash2 = self.Hash(mfccs2)
        
        
    def folder_songs_hash_spec(self):    
       
        count =0
        for song in self.listSongsPaths:
            
            data,sample_rate=librosa.load(song, duration = 60)
            mfccs = librosa.feature.mfcc(data, sr=sample_rate)
            
            X = librosa.stft(data)
            Xdb = librosa.amplitude_to_db(abs(X))
            plt.figure(figsize=(14, 5))
            librosa.display.specshow(Xdb, sr=sample_rate, x_axis='time', y_axis='hz') 
            # If to pring log of frequencies  
            librosa.display.specshow(Xdb, sr=sample_rate, x_axis='time', y_axis='log')
            plt.colorbar()
            plt.savefig('./Spectrogram1/F1_Song1_'+str(count).zfill(3) +'.png')
            
            
            librosa.display.specshow(mfccs)
            plt.savefig('./Feature1/F1_Song1_'+str(count).zfill(3) +'.png')
            count+=1
        
            
            self.full_songs_hash.append(self.Hash(mfccs))
            print('Loading ', count)
        
        

        
    def compare_similiarities(self):
        for song_number in range(len(self.listSongsPaths)):
            self.comparison_difference.append(hex_to_hash(self.inserted_song_hash1) - hex_to_hash(self.full_songs_hash[song_number]))
            self.similiraties.append((1 - self.maps(self.comparison_difference[song_number], 0, 255, 0, 1) )* 100)


    def mixer(self):
        
        sliderRatio = self.Song2_Percentage.value()/100
        self.outputSong = self.inserted_song_1_data * sliderRatio + self.inserted_song_2_data * (1-sliderRatio)
        mfccs = librosa.feature.mfcc(self.outputSong, sr=self.inserted_song_1_sample_rate)
        
        out = self.Hash(mfccs)
        for song_number in range(len(self.listSongsPaths)):
            self.comparison_difference_mixer.append(hex_to_hash(out) - hex_to_hash(self.full_songs_hash[song_number]))
            self.similiraties_mixer.append((1 - self.maps(self.comparison_difference_mixer[song_number], 0, 255, 0, 1) )* 100)
        
        self.displayed_mix_index, self.displayed_mix_path = zip(*sorted(zip(self.similiraties_mixer, self.listSongsPaths), reverse=True))

        
        
    def hash_to_txt(self):
        
        number = 0
        for hash in range(len(self.listSongsPaths)):
            
            f = open('hashes/'+os.path.splitext(os.path.basename(self.listSongsPaths[number]))[0]+'.txt','w')
            f.write(str(self.full_songs_hash[hash]))
            number +=1
        f.close()

            
            
    def read_from_txt(self):
        for filename in os.listdir('hashes'):
            f = open('hashes/'+ filename,'r') 
            self.full_songs_hash.append(f.read())  
        f.close()    
                
    def restart(self):
        self.comparison_difference.clear()
        self.comparison_difference_mixer.clear()
        self.similiraties.clear()
        self.similiraties_mixer.clear()
        self.listSongsPaths.clear()
        self.full_songs_hash.clear()

    def Hash(self,data):
        image=Image.fromarray(data)
        return imagehash.phash(image, hash_size=16).__str__()

    
    def maps(self, inputValue: float, inMin: float, inMax: float, outMin: float, outMax: float):
        slope = (outMax-outMin) / (inMax-inMin)
        return outMin + slope*(inputValue-inMin)

    def display_data_mixer(self):  
        y = []
        for value in range(len(self.displayed_mix_path)):
            y.append(ntpath.basename(self.displayed_mix_path[value]))
        GUITable= np.column_stack((y , self.displayed_mix_index))
        row,column = GUITable.shape
        for r in range(row):
            for c in range(column):
                self.tableWidget.setItem(r ,c ,QtWidgets.QTableWidgetItem(GUITable[r][c]))
     
    def display_data(self):  
        self.displayed_index, self.displayed_path = zip(*sorted(zip(self.similiraties, self.listSongsPaths), reverse=True))

        y = []
        for value in range(len(self.displayed_path)):
            y.append(ntpath.basename(self.displayed_path[value]))
        GUITable= np.column_stack((y , self.displayed_index))
        row,column = GUITable.shape
        for r in range(row):
            for c in range(column):
                self.tableWidget.setItem(r ,c ,QtWidgets.QTableWidgetItem(GUITable[r][c]))


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Song1_Browse.setText(_translate("MainWindow", "Song1_Browse"))
        self.Song2_Browse.setText(_translate("MainWindow", "Song2_Browse"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "             Song-Name                  Similarity-Index"))
        self.Mix_Button.setText(_translate("MainWindow", "Mix"))
        self.tableWidget. setHorizontalHeaderLabels(["Song Name", "Similarity index"])
        



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())




