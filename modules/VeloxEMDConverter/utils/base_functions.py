from importlib.metadata import metadata
import os, math, gc, traceback, json

import hyperspy.api as hs
import numpy as np
import tifffile as tf
import matplotlib.pyplot as plt
import ome_types as ot

from skimage.filters import gaussian
from skimage.transform import pyramid_gaussian

excluded_titles = ['a']

def normalizeImg(img, lower, upper):
    img = (img - lower) / (upper - lower)
    img = np.clip(img, 0, 1)
    return img

def pixelSizeInCentimeter(pixel_size, unit):
    unit_dict = {
        'nm': 1e-7,
        'µm': 1e-4,
        'um': 1e-4,
        'mm': 1e-1,
        'cm': 1,
        'm': 1e2}
    return pixel_size * unit_dict[unit]

def pixelSizeInMicrometer(pixel_size, unit):
    unit_dict = {
        'nm': 1e-3,
        'µm': 1,
        'um': 1,
        'mm': 1e2,
        'cm': 1e4,
        'm': 1e6}
    return pixel_size * unit_dict[unit]

def flattenMD(md, parent_key='', sep='.'):
    items = []
    for k, v in md.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flattenMD(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def processSingleNormal(master, file, export_path, invert, norm, norm_min, norm_max, blur, blur_sigma, dtype):
    # Initialize arguments
    master.popup.configure(text='Initializing...')
    norm_min = 0.5 if norm_min == "" else float(norm_min)
    norm_max = 99.5 if norm_max =="" else float(norm_max)
    blur_sigma = 1.0 if blur_sigma == "" else float(blur_sigma)
    dtype = (65535, 'uint16') if dtype == "16-bit" else (255, 'uint8')
    
    # Try to process a single .emd file
    try:
        master.popup.configure(text=f'Processing {os.path.basename(file)}\n[Loading]...')
        s = hs.load(file, reader = 'emd', select_type = 'images', load_SI_image_stack = True)
        md = s[0].original_metadata.as_dictionary()

        for j in range(len(s)):
            element = s[j].metadata.General.title
            if element in excluded_titles:
                continue
            master.popup.configure(text=f'{element}\n[Post-processing]...')
            if element == "HAADF":
                img = np.asarray(s[j])[-1,:,:].astype(dtype = 'uint16')
                if invert == 1:
                    img = np.invert(img)
            else:
                img = np.asarray(s[j])
            
            if blur == 1:
                if not element == "HAADF":
                    img = gaussian(
                        img, 
                        blur_sigma)

            if norm == 1:
                img= normalizeImg(
                    img,
                    np.percentile(img, norm_min),
                    np.percentile(img, norm_max)
                )
                img = (img*dtype[0])               
            master.popup.configure(text=f'{element}\n[Writing]...')
            
            tf.imwrite(os.path.join(export_path, f'{os.path.basename(file[:-4])} - {element}.tiff'), 
                       img.astype(dtype[1]),
                       description=json.dumps(md))
            del img
            gc.collect()
        del s
        gc.collect()

    except Exception as e:
        print('Error:', e)
        traceback.print_exc()   
    master.popup.configure(text='Done!')
        
def processMosaicNormal(master, folder, export_path, invert, norm, norm_min, norm_max, haadf_norm, blur, blur_sigma, dtype):
    # Initialize arguments
    master.popup.configure(text='Initializing...')
    norm_min = 0.5 if norm_min == "" else float(norm_min)
    norm_max = 99.5 if norm_max =="" else float(norm_max)
    blur_sigma = 1.0 if blur_sigma == "" else float(blur_sigma)
    dtype = (65535, 'uint16') if dtype == "16-bit" else (255, 'uint8')
    
    # Index files
    files = [i for i in os.listdir(folder) if i.endswith(".emd")]
    file_paths = [os.path.join(folder, i) for i in files]

    # Load the first .emd file for initalization purposes
    s = hs.load(file_paths[0], select_type = 'images')
    elements = [s[i].metadata.General.title 
                for i in range(len(s))
                if s[i].metadata.General.title not in excluded_titles]

    del s
    gc.collect()

    # Try to make element export folders
    master.popup.configure(text=f'Making export folders...')
    for i in elements:
        try:
            os.mkdir(os.mkdir(os.path.join(export_path, i)))
        except:
            pass
    
    # Try to process each .emd file and write the raw images it contains as .tiff files       
    for i in file_paths:
        master.popup.configure(text=f'Processing {os.path.basename(i)}\n[Loading]...')
        s = hs.load(i, select_type = 'images', load_SI_image_stack = True)
        md = s[0].original_metadata.as_dictionary()
        for j in range(len(s)):
            element = s[j].metadata.General.title
            if element in excluded_titles:
                continue
            elif element == "HAADF":
                img = np.asarray(s[j])[-1,:,:].astype('uint16')
                if invert == 1:
                    img = np.invert(img)
            else:
                img = np.asarray(s[j])
            master.popup.configure(text=f'Processing {os.path.basename(i)}\n[Writing]...')
            tf.imwrite(os.path.join(export_path,
                                    element,
                                    os.path.basename(i[:-4]) + ".tiff"),
                                    img,
                                    description=json.dumps(md))
        del s
        gc.collect()
    
    # Post-process each element folder
    for i in elements:
        master.popup.configure(text=f'{i} images\n[Loading]...')
        files = os.listdir(os.path.join(export_path, i))
        file_paths = [os.path.join(export_path, i, j) for j in files]
        imgs = []
        mds = []
        for j in file_paths:
            imgs.append(tf.imread(j))
            with tf.TiffFile(j) as f:
                md = json.loads(f.pages[0].description)
            mds.append(md)
        imgs = np.asarray(imgs)
        
        master.popup.configure(text=f'{i} images\n[Post-processing]...')
        if blur == 1:
            if not i == "HAADF":
                for j in range(imgs.shape[0]):
                    imgs[j,:,:,] = gaussian(
                        imgs[j,:,:],
                        blur_sigma)
        if norm == 1:
            if i == "HAADF" and haadf_norm == "Local HAADF normalization":
                print(imgs.shape)
                imgs = imgs.astype('float32')
                for j in range(imgs.shape[0]):
                    print(np.percentile(imgs[j,:,:], norm_min))
                    print(np.percentile(imgs[j,:,:], norm_max))
                    imgs[j,:,:] = normalizeImg(
                        imgs[j,:,:],
                        np.percentile(imgs[j,:,:], norm_min),
                        np.percentile(imgs[j,:,:], norm_max))
            else:
                imgs = normalizeImg(
                    imgs,
                    np.percentile(imgs, norm_min),
                    np.percentile(imgs, norm_max))
            imgs = (imgs*dtype[0])

        master.popup.configure(text=f'{i} images\n[Writing]...')

        for j in range(imgs.shape[0]):
            tf.imwrite(file_paths[j], 
                       imgs[j,:,:].astype(dtype[1]),
                       description=json.dumps(mds[j]))
        del imgs
        gc.collect()
    master.popup.configure(text='Done!')

def tiffFolderToOmeTiff(master, folder, export_path, name, metadata_tiff):
    master.popup.configure(text='Initializing...')

    with tf.TiffFile(metadata_tiff) as f:
        md = json.loads(f.pages[0].description)
    
    images = []
    files = os.listdir(folder)
    if files[0].endswith(".tiff"):
        channels = [i[:-5] for i in files if i.endswith(".tiff")]
    elif files[0].endswith(".tif"):
        channels = [i[:-4] for i in files if i.endswith(".tif")]

    for c, file in enumerate(files):
        master.popup.configure(text=f'Processing {channels[c]}\n[Loading]...')
        ds_imgs = []
        img = tf.imread(os.path.join(folder, file))
        levels = int(math.log((np.max(img.shape) / 256), 2) +1)
        master.popup.configure(text=f'Processing {channels[c]}\n[Generating pyramid]...')
        ds_img_gen = pyramid_gaussian(img, levels, preserve_range= True)
        for ds_img in range(levels):
            ds_imgs.append(np.asarray(next(ds_img_gen), dtype = 'uint8'))
        images.append(ds_imgs)
        del img, ds_imgs, ds_img
        gc.collect()
    
    master.popup.configure(text=f'Writing OME-TIFF\n[Starting]...')
    with tf.TiffWriter(os.path.join(export_path, name + '.ome.tiff'), bigtiff=True) as tif:
        pixel_size_um = pixelSizeInMicrometer(float(md['BinaryResult']['PixelSize']['width']), 
                                              md['BinaryResult']['PixelUnitX'])
        pixel_size_cm = pixelSizeInCentimeter(float(md['BinaryResult']['PixelSize']['width']), 
                                              md['BinaryResult']['PixelUnitX'])
        metadata = {
            "axes": "CYX",
            "SignificantBits": 8,
            "PhysicalSizeX": pixel_size_um,
            "PhysicalSizeXUnit": 'µm',
            "PhysicalSizeY": pixel_size_um,
            "PhysicalSizeYUnit": 'µm',
            "Channel": {"Name": channels},
        }
        options = dict(
            photometric="MINISBLACK",
            tile=(256, 256),
            resolutionunit="CENTIMETER",
            maxworkers=2,
        )

        master.popup.configure(text=f'Writing OME-TIFF\n[Writing level 0]...')
        pixels_per_cm = 1.0 / pixel_size_cm
        img = np.asarray([images[c][0] for c in range(len(channels))])
        tif.write(
            img,
            subifds=levels-1,
            resolution=(pixels_per_cm, pixels_per_cm),
            metadata=metadata,
            **options)
        
        for level in range(levels-1):
            master.popup.configure(text=f'Writing OME-TIFF\n[Writing level {level+1}]...')
            mag = 2 ** (level + 1)
            ds_img = np.asarray([images[c][level+1] for c in range(len(channels))])
            tif.write(
                ds_img,
                subfiletype=1,
                resolution=(
                    pixels_per_cm / mag,
                    pixels_per_cm / mag),
                **options)
    
    master.popup.configure(text='Populating OME-TIFF with OME-XML metadata...')
    flat_md = flattenMD(md)

    manufacturer_md = ot.model.Microscope(
        manufacturer = md['Instrument']['Manufacturer'],
        model = md['Instrument']['InstrumentClass'],
        serial_number = md['Instrument']['InstrumentId'])
    
    instrument = ot.model.Instrument(
        id = 'Instrument:0',
        microscope = manufacturer_md)
    
    ome_xml = tf.tiffcomment(os.path.join(export_path, name + '.ome.tiff'))
    ome = ot.from_xml(ome_xml)
    ome.instruments.append(instrument)
    ome.images[0].instrument_ref = ot.model.InstrumentRef(id="Instrument:0")
    
    master.popup.configure(text='Populating OME-TIFF with original_metadata as StructuredAnnotations...')
    annotations = []
    for i, (k, v) in enumerate(flat_md.items()):
        ann = ot.model.MapAnnotation(
            id = f'Annotation:{i}',
            namespace = 'emd:original_metadata',
            value = {"k" : k, "value": str(v)})
        annotations.append(ann)
    
    # mapped_annotations = ot.model.MapAnnotation(
    #     id = 'StructuredAnnotations:0',
    #     namespace = 'emd:original_metadata',
    #     value = [{"k" : k, "value": str(v)} for k, v in flat_md.items()])
    if ome.structured_annotations is None:
        ome.structured_annotations = ot.model.StructuredAnnotations()

    for ann in annotations:
        ome.structured_annotations.map_annotations.append(ann)
        ome.images[0].annotation_refs.append(ann.id)
    # ome.structured_annotations.map_annotations.append(mapped_annotations)
    # ome.images[0].annotation_refs.append(mapped_annotations.id)

    tf.tiffcomment(os.path.join(export_path, name + '.ome.tiff'),
                   #('<?xml version="1.0" encoding="UTF-8"?>' + ome.to_xml()).encode())
                     ome.to_xml().encode())