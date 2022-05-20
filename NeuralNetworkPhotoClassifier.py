from email.mime import base
import math
import os
import numpy as np
import tensorflow as tf
from keras.models import load_model
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import VGG16
from PIL import Image

basepath = 'E:/Fotos/' #path where experiments are located
savepathS = 'C:/Users/sevar/OneDrive/Radna površina/Data/Fotos/'

dedrift = False;

#get list of all folders
#folder{01} = {'C2 000 - M5AC 1,0 - 1'};

def count_files(path):
    return len([name for name in os.listdir(path) if os.path.isfile()])

size_of_folder = count_files(basepath)
for j in range(size_of_folder):
    size_of_second_folder = 2
    for i in range (size_of_second_folder):
        if not dedrift:
            file_content = open(basepath + "/" + file).read()
            #load([basepath '\' folder{j}{i} '\' 'Tracked_Particles.mat']);
            concat_ptcl2 = open(basepath + "/" + file).read()
            #concat_ptcl2 = concat_ptcl;
        elif dedrift:
            file_content = open(basepath + "/" + file).read()
            # load([basepath '\' folder{j}{i} '\' 'Tracked_Particles_Dedrift.mat']);
        
    print("Download completed. Done!")
        savename = folder{j}{i};

        for fov = 1:max(concat_ptcl2(:,5))
            index = find(concat_ptcl2(:,5)==fov);
            FOV = concat_ptcl2(index(1):index(end),:);

            for particleid = min((FOV(:,4))):max(FOV(:,4))
                index = find(FOV(:,4)==particleid);
                trnconcat = FOV(index(1):index(end),:);

                if(trnconcat(1,7)) == 1:
                    for pos = 1:size(trnconcat,1)
                        if fov == 1:
                            fovIMG = 1;
                        elif fov == 2:
                            fovIMG = 10;
                        else:
                            fovIMG = fov-1;
                        

                        if trnconcat(pos,3) <10:
                            img2Name = [basepath folder{j}{i} '\fov' int2str(fovIMG) '\fov' int2str(fovIMG) '_000' int2str(trnconcat(pos,3)) '.tif'];
                        elif trnconcat(pos,3) <100:
                            img2Name = [basepath folder{j}{i} '\fov' int2str(fovIMG) '\fov' int2str(fovIMG) '_00' int2str(trnconcat(pos,3)) '.tif'];
                        else:
                            img2Name = [basepath folder{j}{i} '\fov' int2str(fovIMG) '\fov' int2str(fovIMG) '_0' int2str(trnconcat(pos,3)) '.tif'];
                        

                        img = ((imread(img2Name)));

                        imgSel = imcrop(img,[(trnconcat(pos,1)-20) (trnconcat(pos,2)-20) 40 40]);
                        imgSel = imresize(imgSel,[224 224]);
                        imgSel = reshape(imgSel,224,224,3);
                        
                        X_after_vgg = predict(vgg16_model,imgSel);
                        X_after_vgg = reshape(X_after_vgg,[7 7 512]);

                        imgSel = reshape(imgSel,[7,7,512]);
                        
                        label = predict(net, X_after_vgg);
                        text(10, 20, char(label),'Color','white')                        



