import logging

import cv2
import matplotlib.pyplot as plt
import numpy as np
import tqdm


class Loader:

    def __init__(self, path):
        self.source_path = path
        self.images = []


class VideoLoader(Loader):
    def __init__(self, path):
        super().__init__(path)
        self.fps = 0
        self.vidcap = None
        self.images = []

    def get_start_end_step_in_frames(self, start_s=None, end_s=None, step_s=1):
        if start_s is None:
            start_s = 0
        if end_s is None:
            end_s = self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT) / self.fps
        start_f, end_f, step_f = [int(np.round(x * self.fps)) for x in (start_s, end_s, step_s)]
        return start_f, end_f, step_f

    def load(self, start_s=None, end_s=None, step_s=None):
        logging.info('Loading video...')
        self.images = []
        self.vidcap = cv2.VideoCapture(self.source_path)
        self.fps = self.vidcap.get(cv2.CAP_PROP_FPS)
        start_f, end_f, step_f = self.get_start_end_step_in_frames(start_s, end_s, step_s)

        i_frame = 0
        pbar = tqdm.tqdm(total=end_f)
        while i_frame < end_f:
            _, image = self.vidcap.read()
            if i_frame > start_f and (i_frame - start_f) % step_f == 0:
                self.images.append(image)
            i_frame += 1
            pbar.update(1)
        self.images = np.stack(self.images)
