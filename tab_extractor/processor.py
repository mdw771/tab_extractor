import logging

import numpy as np
from PIL import Image
import cv2

from tab_extractor.loader import Loader


class Processor:
    def __init__(self, loader: Loader, page_aspect_ratio=(11, 8.5)):
        """
        The constructor.

        :param loader: Loader.
        :param page_aspect_ratio: tuple[float]. The desired page aspect ratio in (height, width). This will determine
                                  the number of lines to place in each page.
        """
        self.loader = loader
        self.unique_images = []
        self.diff_threshold = 10
        self.pages = []
        self.page_aspect_ratio = page_aspect_ratio

    def build_unique_images(self):
        self.unique_images = [self.loader.images[0]]
        for i, img in enumerate(self.loader.images[1:]):
            diff = np.mean((img - self.unique_images[-1]) ** 2)
            logging.debug('MSE between current frame and last unique frame is {}.'.format(diff))
            if diff > self.diff_threshold:
                self.unique_images.append(img)

    def find_num_lines_per_page(self):
        image_shape = self.loader.images[0].shape
        n = int(np.floor(image_shape[1] / self.page_aspect_ratio[1] * self.page_aspect_ratio[0] / image_shape[0]))
        return n

    def stitch_unique_images(self):
        lines_per_page = self.find_num_lines_per_page()
        n_pages = int(np.ceil(len(self.unique_images) / lines_per_page))
        i_page = 0
        while i_page < n_pages:
            ind_st = i_page * lines_per_page
            ind_end = min((i_page + 1) * lines_per_page, len(self.unique_images))
            page = np.concatenate(self.unique_images[ind_st:ind_end], axis=0)
            self.pages.append(page)
            i_page += 1
        max_shape = [np.max([p.shape[0] for p in self.pages]), np.max([p.shape[1] for p in self.pages])]
        if len(self.pages[0].shape) == 3:
            max_shape.append(self.pages[0].shape[-1])
        for i in range(n_pages):
            page = np.full(max_shape, fill_value=255)
            img = self.pages[i]
            ys = 0
            xs = max_shape[1] // 2 - img.shape[1] // 2
            page[ys:ys + img.shape[0], xs:xs + img.shape[1]] = img
            self.pages[i] = page

    def run(self):
        self.build_unique_images()
        self.stitch_unique_images()

    def save_pages(self, path):
        image_list = [Image.fromarray(p.astype('uint8')) for p in self.pages]
        image_list[0].save(
            path, "PDF", resolution=100.0, save_all=True, append_images=image_list[1:]
        )
