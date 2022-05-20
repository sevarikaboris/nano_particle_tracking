clc; close all; clear all;
addpath functions
set(0,'recursionLimit',10000);


net = importKerasLayers("C:\Users\sevar\OneDrive\Documents\OneNote\OneDrive\Архив\Research\MIT Project\Microrheology\MPT - new\BorisBoris.h5");

%% USER INPUT

dedrift = false;

basepath = 'E:\Fotos\'; %path where experiments are located
savepathS = 'C:\Users\sevar\OneDrive\Radna površina\Data\Fotos\';

folder{01} = {'C2 000 - M5AC 1,0 - 1'};

for j = 1:size(folder,2)
    for  i = 1:size(folder{j},2)
        if ~dedrift
            load([basepath '\' folder{j}{i} '\' 'Tracked_Particles.mat']);
            concat_ptcl2 = concat_ptcl;
        elseif dedrift
            load([basepath '\' folder{j}{i} '\' 'Tracked_Particles_Dedrift.mat']);
        end
py.print("Download completed. Done!")
        savename = folder{j}{i};

        for fov = 1:max(concat_ptcl2(:,5))
            index = find(concat_ptcl2(:,5)==fov);
            FOV = concat_ptcl2(index(1):index(end),:);

            for particleid = min((FOV(:,4))):max(FOV(:,4))
                index = find(FOV(:,4)==particleid);
                trnconcat = FOV(index(1):index(end),:);

                if(trnconcat(1,7)) == 1
                    for pos = 1:size(trnconcat,1)
                        if fov == 1
                            fovIMG = 1;
                        elseif fov == 2
                            fovIMG = 10;
                        else
                            fovIMG = fov-1;
                        end

                        if trnconcat(pos,3) <10
                            img2Name = [basepath folder{j}{i} '\fov' int2str(fovIMG) '\fov' int2str(fovIMG) '_000' int2str(trnconcat(pos,3)) '.tif'];
                        elseif trnconcat(pos,3) <100
                            img2Name = [basepath folder{j}{i} '\fov' int2str(fovIMG) '\fov' int2str(fovIMG) '_00' int2str(trnconcat(pos,3)) '.tif'];
                        else
                            img2Name = [basepath folder{j}{i} '\fov' int2str(fovIMG) '\fov' int2str(fovIMG) '_0' int2str(trnconcat(pos,3)) '.tif'];
                        end

                        img = ((imread(img2Name)));

                        imgSel = imcrop(img,[(trnconcat(pos,1)-20) (trnconcat(pos,2)-20) 40 40]);
                        imgSel = imresize(imgSel,[224 224]);
                        imgSel = reshape(imgSel,224,224,3);
                        
                        X_after_vgg = predict(vgg16_model,imgSel);
                        X_after_vgg = reshape(X_after_vgg,[7 7 512]);

                        imgSel = reshape(imgSel,[7,7,512]);
                        
                        label = predict(net, X_after_vgg);
                        text(10, 20, char(label),'Color','white')                        
                    end
                end
            end
        end
    end
end