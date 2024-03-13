import logging

import numpy as np
import matplotlib.pyplot as plt
import cv2

from tab_extractor.loader import Loader


class Processor:
    def __init__(self, loader: Loader):
        self.loader = loader
        self.unique_images = []
        self.diff_threshold = 10
        self.full_image = None

    def build_unique_images(self):
        self.unique_images = [self.loader.images[0]]
        for i, img in enumerate(self.loader.images[1:]):
            diff = np.mean((img - self.unique_images[-1]) ** 2)
            logging.debug('MSE between current frame and last unique frame is {}.'.format(diff))
            if diff > self.diff_threshold:
                self.unique_images.append(img)

    def stitch_unique_images(self):
        self.full_image = np.concatenate(self.unique_images, axis=0)

    def run(self):
        self.build_unique_images()
        self.stitch_unique_images()

    def save_stitched(self, path):
        cv2.imwrite(path, self.full_image)
