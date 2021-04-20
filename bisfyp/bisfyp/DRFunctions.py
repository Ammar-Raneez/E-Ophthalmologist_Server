import numpy as np
import cv2
import logging
from urllib.request import urlopen

class DRFunctions:
    def get_pad_width(self, image, new_shape, is_rgb=True):
        #Pad image to get same sizing
        pad_diff = new_shape - image.shape[0], new_shape - image.shape[1]
        t, b = math.floor(pad_diff[0]/2), math.ceil(pad_diff[0]/2)
        l, r = math.floor(pad_diff[1]/2), math.ceil(pad_diff[1]/2)
        if is_rgb:
            pad_width = ((t,b), (l,r), (0, 0))
        else:
            pad_width = ((t,b), (l,r))
        return pad_width
    
    def crop_image_from_gray(self, image, tol=7):
        #Crop images to obtain section of only eye
        if image.ndim == 2:
            mask = image > tol
            return image[np.ix_(mask.any(1), mask.any(0))]
        elif image.ndim == 3:
            gray_img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            mask = gray_img > tol

            check_shape = image[:, :, 0][np.ix_(mask.any(1), mask.any(0))].shape[0]
            #If the image was too dark, don't do anything to the original one
            if (check_shape == 0):
                return image 
            else:
                img1=image[:, :, 0][np.ix_(mask.any(1), mask.any(0))]
                img2=image[:, :, 1][np.ix_(mask.any(1), mask.any(0))]
                img3=image[:, :, 2][np.ix_(mask.any(1), mask.any(0))]
                image = np.stack([img1, img2, img3], axis=-1)
            return image

    def load_ben_color(self, image, sigmaX):
        #convert image color to rgb
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = self.crop_image_from_gray(image)
        image = cv2.addWeighted(image, 4, cv2.GaussianBlur(image, (0,0), sigmaX),-4, 128)
        return image

    def preprocess_image(self, image_path, desired_size = 224):
        # req = urlopen(image_path)
        # arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        # image = cv2.imdecode(arr, -1)
        # logging.info(image)
        image = cv2.imdecode(image_path, cv2.IMREAD_UNCHANGED)
        image = self.load_ben_color(image, sigmaX = 30)
        image = cv2.resize(image, (desired_size, desired_size))
        image[:, :, 0] = image[:, :, 1]
        image[:, :, 2] = image[:, :, 1]
        return image
    
    def preprocess(self, image):
        image_array = np.empty((1, 224, 224, 3), dtype=np.uint8)
        image_array[0, :, :, :] = self.preprocess_image(image)
        return image_array