from curses.panel import top_panel
from email.mime import base
import math
import os
from turtle import left, right
import numpy as np
import tensorflow as tf
from keras.models import load_model
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import VGG16
from PIL import Image
from scipy.io import loadmat

basepath = "C:/Users/Jerome's Laptop/Desktop/Hauptordner/" #path where experiments are located
savepath = 'C:/Users/sevar/OneDrive/Radna površina/Data/Fotos/'

dedrift = False

def transpose_matrix(matrix):
    return list(map(list, zip(*matrix)))

for experiment_dir in os.listdir(basepath):
    for videos_dir in os.listdir(basepath + experiment_dir):
        if not dedrift:
            file_name = 'Tracked_Particles.mat'
        elif dedrift:
            file_name = 'Tracked_Particles_Dedrift.mat'
        mat_file = loadmat(basepath + experiment_dir + file_name)
        concat_ptcl2 = mat_file['concat_ptcl2']
        transposed_concat_ptcl2 = transpose_matrix(concat_ptcl2)

    print("Download completed. Done!")
    savename = basepath + experiment_dir + videos_dir
    
    #remember, python starts with 0 --> transposed_concat_ptcl2[5] is empty
    min_of_series = int(min(transposed_concat_ptcl2[4])) # would be 1
    max_of_series = int(max(transposed_concat_ptcl2[4])) # would be 10
    
    #make a 2D list of all fovs with index
    fov_index_list = [[] for y in range(max_of_series)]
    for index, value in enumerate(transposed_concat_ptcl2[4]):
        fov_index_list[int(value)-1].append(index)

    

    #add 1 to max because range wouldn't go to 10
    FOV = list()
    for fov in fov_index_list:
        for index in fov:
            FOV.append(concat_ptcl2[index])        
            FOV_tr = transpose_matrix(FOV)

        particleid_index = [[] for y in range(int(max(FOV_tr[3])))]
        before = -1
        for index, particleid in enumerate(FOV_tr[3]):
            if(before == particleid):
                particleid_index[int(particleid)].append(index)
            before = particleid



        # for fov = 1:max(concat_ptcl2(:,5))
        #     index = find(concat_ptcl2(:,5)==fov);
        #     FOV = concat_ptcl2(index(1):index(end),:);

        #     for particleid = min((FOV(:,4))):max(FOV(:,4))
        #         index = find(FOV(:,4)==particleid);
        #         trnconcat = FOV(index(1):index(end),:);

               
        #         for pos = 1:size(trnconcat,1)
        #             if fov == 1
        #                 fovIMG = 1;
        #             elseif fov == 2
        #                 fovIMG = 10;
        #             else
        #                 fovIMG = fov-1;
        #             end
                    

        #              if trnconcat(pos,3) <10
        #                 img2Name = [basepath folder{j}{i} '\fov' int2str(fovIMG) '\fov' int2str(fovIMG) '_000' int2str(trnconcat(pos,3)) '.tif'];
        #             else if trnconcat(pos,3) <100
        #                 img2Name = [basepath folder{j}{i} '\fov' int2str(fovIMG) '\fov' int2str(fovIMG) '_00' int2str(trnconcat(pos,3)) '.tif'];
        #             else
        #                 img2Name = [basepath folder{j}{i} '\fov' int2str(fovIMG) '\fov' int2str(fovIMG) '_0' int2str(trnconcat(pos,3)) '.tif'];
        #             end
                    

                    img = Image.open(img2Name);

                    #left, up, right, bottom
                    left = trnconcat(pos,1)-20
                    top = trnconcat(pos,2)-20
                    right = left + 40
                    bottom =top + 40
                    
                    imgSel = img.crop(left, top, right, bottom)
                    imgSel = imgSel.resize(224, 224)
                    imgSel = np.asarray(imgSel).reshape(1, 224, 224, 3)
                    
                    image = preprocess_input(image)

                    #image.shape
                    vgg16_model = VGG16(include_top=False, input_shape=(224, 224, 3))

                    X_after_vgg = vgg16_model.predict(image)

                    X_after_vgg.shape

                    model = load_model("C:/Users/Jerome's Laptop/Desktop/Boris_KI/particle.h5")
                    x = model.predict(X_after_vgg)
                    print(x)

                    if x >= 0.9: 
                        print("is Particle")
                        is_particle = True
                    else : 
                        print("not a Particle")
                        is_particle = False

                    
                    #write to file (it is not possible to alter a specific line or row)
                    #so you have to read all, change a specific line with this and overwrite the file
                    #completely

                    filename = "table.txt"
                    with open(filename, 'r') as file:
                        file_lines = file.readlines()

                    line_position_of_table = 3      #I dont know
                    file_lines[1] = x+'\n'          #'\n' means newline

                    # and write everything back
                    with open(filename, 'w') as file:
                        file.writelines(file_lines)

                    #label = predict(net, X_after_vgg);
                    #text(10, 20, char(label),'Color','white')                        



