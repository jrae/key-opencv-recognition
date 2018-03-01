# Code re used from tutorial

# https://pythonprogramming.net/haar-cascade-object-detection-python-opencv-tutorial/

import urllib.request
import cv2
import numpy as np
import os
import pdb

def store_raw_images():
    # neg_images_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n04146050'
    # neg_images_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n02802544'
    neg_images_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n03541923'
    neg_image_urls = urllib.request.urlopen(neg_images_link).read().decode()
    # pic_num = 1
    pic_num = len(os.listdir('neg/')) + 1

    if not os.path.exists('neg'):
        os.makedirs('neg')

    for i in neg_image_urls.split('\n'):
        try:
            print(i)
            urllib.request.urlretrieve(i, "neg/"+str(pic_num)+".jpg")
            img = cv2.imread("neg/"+str(pic_num)+".jpg",cv2.IMREAD_GRAYSCALE)
            # should be larger than samples / pos pic (so we can place our image on it)
            resized_image = cv2.resize(img, (100, 100))
            cv2.imwrite("neg/"+str(pic_num)+".jpg",resized_image)
            pic_num += 1

        except Exception as e:
            print(str(e))

# store_raw_images()

def crop_image_to_threshold():

    # load image
    for img in os.listdir('pos'):
        try:
            print(img)
            current_image_path = 'pos/'+str(img)
            read_img = cv2.imread(current_image_path, cv2.IMREAD_GRAYSCALE)

            # Copied from here https://stackoverflow.com/questions/44383209/how-to-detect-edge-and-crop-an-image-in-python

            # threshold to get just the key
            retval, thresh_gray = cv2.threshold(read_img, thresh=100, maxval=250, type=cv2.THRESH_BINARY)

            # find where the signature is and make a cropped region
            points = np.argwhere(thresh_gray==0) # find where the black pixels are
            points = np.fliplr(points) # store them in x,y coordinates instead of row,col indices
            x, y, w, h = cv2.boundingRect(points) # create a rectangle around those points
            # x, y, w, h = x-10, y-10, w+20, h+20 # make the box a little bigger
            crop = read_img[y:y+h, x:x+w] # create a cropped region of the gray image

            # get the thresholded crop
            # retval, thresh_crop = cv2.threshold(crop, thresh=200, maxval=255, type=cv2.THRESH_BINARY)

            resized_image = cv2.resize(crop, (50, 50))
            cv2.imwrite(current_image_path, resized_image)

        except Exception as e:
            print(str(e))

# crop_image_to_threshold()

def reorder_pos_images():
    pic_num = 1

    for img in os.listdir('pos'):
        try:
            print(img)
            current_image_path = 'pos/'+str(img)
            os.rename(current_image_path, 'pos/'+str(pic_num)+".jpg")
            pic_num += 1
        except Exception as e:
            print(str(e))

# reorder_pos_images()



# def resize_pos_images():
#     for img in os.listdir('pos'):
#         try:
#             print(img)
#             current_image_path = 'pos/'+str(img)
#             read_img = cv2.imread(current_image_path, cv2.IMREAD_GRAYSCALE)
#             resized_image = cv2.resize(read_img, (50, 50))
#             cv2.imwrite(current_image_path, resized_image)

#         except Exception as e:
#             print(str(e))

# resize_pos_images()

def find_uglies():
    for img in os.listdir('neg'):
        for ugly in os.listdir('uglies'):
            try:
                current_image_path = 'neg/'+str(img)
                ugly = cv2.imread('uglies/'+str(ugly))
                question = cv2.imread(current_image_path)
                if ugly.shape == question.shape and not(np.bitwise_xor(ugly,question).any()):
                    print('That is one ugly pic! Deleting!')
                    print(current_image_path)
                    os.remove(current_image_path)
            except Exception as e:
                print(str(e))

# find_uglies()


def create_pos_n_neg():
    for file_dir in ['neg', 'pos']:

        for img in os.listdir(file_dir):

            if file_dir == 'pos':
                line = file_dir+'/'+img+' 1 0 0 50 50\n'
                with open('info.dat','a') as f:
                    f.write(line)
            elif file_dir == 'neg':
                line = file_dir+'/'+img+'\n'
                with open('bg.txt','a') as f:
                    f.write(line)

# create_pos_n_neg()
