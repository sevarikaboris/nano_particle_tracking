import os
import numpy as np
import scipy
from keras.models import load_model
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import VGG16
from PIL import Image
from scipy.io import loadmat

basepath = "E:\Particle Set 2/" #path where experiments are located
savepath = 'C:/Users/sevar/OneDrive/Radna površina/Data/Fotos/'
model = load_model("C:/Users/sevar\OneDrive\Documents\OneNote\OneDrive\Архив\Research\MIT Project\Microrheology\MPT - new\BorisBoris.h5")
vgg16_model = VGG16(include_top=False, input_shape=(224, 224, 3))

#change this value
dedrift = True

def transpose_matrix(matrix):
    return list(map(list, zip(*matrix)))

for experiment_dir in os.listdir(basepath):
    experiment_dir += "/"
    print("processing: " + experiment_dir)

    for videos_dir in os.listdir(basepath + experiment_dir):
        if(not os.path.isdir(basepath + experiment_dir + videos_dir)):
            continue

        videos_dir += "/"
        print("videos: "  + videos_dir)

        if not dedrift:
            file_name = '/tracked_particles.mat'
        elif dedrift:
            file_name = '/tracked_particles_dedrift.mat'

        mat_file = loadmat(basepath + experiment_dir + file_name)
        concat_ptcl2 = mat_file['concat_ptcl2'] #read the file
        #savename = basepath + experiment_dir + videos_dir
        
        row, col = concat_ptcl2.shape               #get rows and cols of mat_file
        table_with_result = np.zeros(shape=(row,6)) #initializing resulting table. it is faster to fill the array with zeros beforehand, than appending and copying tables
        table_with_result_index = 0                 #navigating index 

        for concat_row in concat_ptcl2:
            picture_number = int(concat_row[2])
            if picture_number <10:
                number = '_000' + str(picture_number)
            elif picture_number <100:
                number = '_00' + str(picture_number)
            else:
                number = '_0' + str(picture_number)

            img2Name = basepath + experiment_dir + videos_dir +  'fov1' +number + '.tif'
            img = Image.open(img2Name)

            #left, up, right, bottom
            heigth = 40
            width = 40
            left = concat_row[0]-(width/2)
            top = concat_row[1]-(heigth/2)
            right = left + width
            bottom =top + heigth
            
            imgSel = img.crop((left, top, right, bottom))
            imgSel = imgSel.resize((224, 224), Image.LANCZOS)
            imgSel = np.asarray(imgSel).reshape(1, 224, 224, 3)
            image = preprocess_input(imgSel)
            
            X_after_vgg = vgg16_model.predict(image)
            X_after_vgg.shape

            
            x = model.predict(X_after_vgg)
            print("particle id: "+ str(concat_row[3]))

            #if x >= 0.9: 
            #    print("is Particle")
            #else : 
            #    print("not a Particle")

            for i in range(5):
                table_with_result[table_with_result_index][i] = concat_row[i]
            table_with_result[table_with_result_index][5] = x
            table_with_result_index += 1
            
            
        scipy.io.savemat('result_mat'+str(concat_row[2])+'.mat',mdict={'concat_ptcl2': table_with_result})
            
            


