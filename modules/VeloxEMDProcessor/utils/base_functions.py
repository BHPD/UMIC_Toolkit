import os, math, gc, traceback

import hyperspy.api as hs
import numpy as np
import tifffile as tf
import matplotlib.pyplot as plt

from skimage.filters import gaussian

def normalizeImg(img, lower, upper):
    img = (img - lower) / (upper - lower)
    img = np.clip(img, 0, 1)
    return img

def processSingleNormal(file, export_path, invert, norm, norm_min, norm_max, blur, blur_sigma, dtype):
    # Initialize arguments
    norm_min = 0.5 if norm_min == "" else float(norm_min)
    norm_max = 99.5 if norm_max =="" else float(norm_max)
    blur_sigma = 1.0 if blur_sigma == "" else float(blur_sigma)
    dtype = (65535, 'uint16') if dtype == "16-bit" else (255, 'uint8')
    
    # Try to process a single .emd file
    try:
        s = hs.load(
            file, 
            reader = 'emd', 
            select_type = 'images', 
            load_SI_image_stack = True)

        for j in range(len(s)):
            element = s[j].metadata.General.title

            if element == "HAADF":
                img = np.asarray(s[j])[-1,:,:].astype(dtype = 'uint16')
                if invert == 1:
                    img = np.invert(img)
            else:
                img = np.asarray(s[j])#.astype(dtype = 'uint16')
            
            if blur == 1:
                if not element == "HAADF":
                    img = gaussian(
                        img, 
                        blur_sigma)
                
                img = normalizeImg(
                    img,
                    np.percentile(img, norm_min),
                    np.percentile(img, norm_max)
                )
                img = (img*dtype[0]).astype(dtype[1])
            
            else:
                if norm == 1:
                    img= normalizeImg(
                        img,
                        np.percentile(img, norm_min),
                        np.percentile(img, norm_max)
                    )
                    img = (img*dtype[0]).astype(dtype[1])               
            
            tf.imwrite(os.path.join(export_path, f'{os.path.basename(file[:-4])} - {element}.tiff'), img)
            del img
            gc.collect()
        del s
        gc.collect()

    except Exception as e:
        print('Error:', e)
        traceback.print_exc()
        gc.collect()
        
def processMosaicNormal(folder, export_path, invert, norm, norm_min, norm_max, blur, blur_sigma, dtype):
    # Initialize arguments
    norm_min = 0.5 if norm_min == "" else float(norm_min)
    norm_max = 99.5 if norm_max =="" else float(norm_max)
    blur_sigma = 1.0 if blur_sigma == "" else float(blur_sigma)
    dtype = (65535, 'uint16') if dtype == "16-bit" else (255, 'uint8')
    
    # Index files
    files = [i for i in os.listdir(folder) if i.endswith(".emd")]
    file_paths = [os.path.join(folder, i) for i in files]
    
    # Define and try to make export path
    export_path = os.path.join(export_path, 'Exports')
    try:
        os.mkdir(export_path)
    except:
        pass

    # Load the first .emd file for initalization purposes
    s = hs.load(file_paths[0], select_type = 'images')
    elements = [s[i].metadata.General.title for i in range(len(s))]
    del s
    gc.collect()

    # Try to make element export folders
    for i in elements:
        try:
            os.mkdir(os.mkdir(os.path.join(export_path, i)))
        except:
            pass
    try:
        for i in file_paths:
            s = hs.load(i, select_type = 'images', load_SI_image_stack = True)
            for j in range(len(s)):
                element = s[j].metadata.General.title
                if element == "HAADF":
                    img = np.asarray(s[j])[-1,:,:].astype('uint16')
                    if invert == 1:
                        img = np.invert(img)
                else:
                    img = np.asarray(s[j])
                tf.imwrite(os.path.join(export_path,
                                        element,
                                        os.path.basename(i[:-4]) + ".tiff"),
                                        img)
            del s
            gc.collect()

    except Exception as e:
        print('Error:', e)
        traceback.print_exc()
        gc.collect()

    try:
        for i in elements:
            files = os.listdir(os.path.join(export_path, i))
            file_paths = [os.path.join(export_path, i, j) for j in files]
            imgs = []
            for j in file_paths:
                imgs.append(tf.imread(j))
            imgs = np.asarray(imgs)
            if blur == 1:
                if not i == "HAADF":
                    for j in range(imgs.shape[0]):
                        imgs[j,:,:,] = gaussian(
                            imgs[j,:,:],
                            blur_sigma
                            )
                imgs = normalizeImg(
                    imgs,
                    np.percentile(imgs, norm_min),
                    np.percentile(imgs, norm_max)
                )
                imgs = (imgs*dtype[0]).astype(dtype[1])
            else:
                if norm == 1:             
                    imgs = normalizeImg(
                        imgs,
                        np.percentile(imgs, norm_min),
                        np.percentile(imgs, norm_max)
                        )
                    imgs = (imgs*dtype[0]).astype(dtype[1])
            for j in range(imgs.shape[0]):
                tf.imwrite(file_paths[j], imgs[j,:,:])
            del imgs
            gc.collect()
    except Exception as e:
        print('Error:', e)
        traceback.print_exc()
        gc.collect()
            

    
##### Old stuff f'{os.path.basename(file[:-4])} - {element}.tiff'), img)
            
    #         else:
    #             if norm == 1:
    #                 img= normalizeImg(
    #                     img,
    #                     np.percentile(img, norm_min),
    #                     np.percentile(img, norm_max)
    #                 )
    #                 img = (img*dtype[0]).astype(dtype[1])               
            
    #         tf.imwrite(os.path.join(export_path, f'{os.path.basename(file[:-4])} - {element}.tiff'), img)
    #         del img
    #         gc.collect()
    #     del s
    #     gc.collect()

    # except Exception as e:
    #     print('Error:', e)
    #     traceback.print_exc()
    #     gc.collect()