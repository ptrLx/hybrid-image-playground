import os
from math import sqrt

import cv2
import numpy as np


class HybridImage:
    def __init__(self):
        # enum of filter modes
        self.CUT = "cut"
        self.GAUSSIAN = "gaussian"

    def __distance(self, point1, point2):
        return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

    def __gaussian_mask_lp(self, cf, img_shape):
        base = np.zeros(img_shape[:2])
        rows, cols = img_shape[:2]
        center = (rows / 2, cols / 2)
        for i in range(rows):
            for j in range(cols):
                base[i, j] = np.exp(
                    -((self.__distance((i, j), center)) ** 2) / (2 * cf**2)
                )
        return base

    def __gaussian_mask_hp(self, cf, img_shape):
        return 1 - self.__gaussian_mask_lp(cf, img_shape)

    def __cut_mask_lp(self, cf, img_shape):
        mask = np.zeros(img_shape[:2])
        rows, cols = img_shape[:2]
        center = (rows / 2, cols / 2)
        for i in range(rows):
            for j in range(cols):
                mask[i, j] = 1 if self.__distance((i, j), center) < cf else 0
        return mask

    def __cut_mask_hp(self, cf, img_shape):
        return 1 - self.__cut_mask_lp(cf, img_shape)

    def __process_buffer(self, buffer, image_size):
        # Convert the bytes to a NumPy array
        np_arr = np.frombuffer(buffer, np.uint8)

        # Decode the NumPy array to an image
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, (image_size, image_size))

        return image

    def __create_filtered_image(
        self,
        buffer,
        image_size,
        filter_mode,
        cf=10,
        use_high_pass=False,
        is_scale_independent_cf=False,
    ):
        image = self.__process_buffer(buffer, image_size)

        # Resize the cutoff frequency
        if is_scale_independent_cf:
            cf *= image_size / 128

        # Fourier Transform of the image
        ft = np.fft.fft2(image)

        # Apply Center Shifting (Shift the zero-frequency component to the center of the spectrum)
        ft = np.fft.fftshift(ft)

        # Apply Filter
        if filter_mode == self.GAUSSIAN:
            filter_mask = (
                self.__gaussian_mask_hp(cf, image.shape)
                if use_high_pass
                else self.__gaussian_mask_lp(cf, image.shape)
            )
        else:
            filter_mask = (
                self.__cut_mask_hp(cf, image.shape)
                if use_high_pass
                else self.__cut_mask_lp(cf, image.shape)
            )

        filtered_center = ft * filter_mask

        # Extract frequency component
        filtered_ft = np.fft.ifftshift(filtered_center)

        # Get image using Inverse FFT
        filtered_image = np.fft.ifft2(filtered_center)

        return (
            image,
            np.abs(filter_mask),
            np.abs(ft),
            np.abs(filtered_center),
            np.abs(filtered_image),
        )

    def apply_low_pass_filter(
        self, buffer, image_size, filter_mode, cf, is_scale_independent_cf
    ):
        return self.__create_filtered_image(
            buffer=buffer,
            image_size=image_size,
            filter_mode=filter_mode,
            cf=cf,
            use_high_pass=False,
            is_scale_independent_cf=is_scale_independent_cf,
        )

    def apply_high_pass_filter(
        self, buffer, image_size, filter_mode, cf, is_scale_independent_cf
    ):
        return self.__create_filtered_image(
            buffer=buffer,
            image_size=image_size,
            filter_mode=filter_mode,
            cf=cf,
            use_high_pass=True,
            is_scale_independent_cf=is_scale_independent_cf,
        )

    def create_image_preview(self, buffer, image_size):
        return self.__process_buffer(buffer, image_size)

    def create_hybrid_image(self, image_lp, image_hp, image_size):
        processed_lp = self.__process_buffer(image_lp, image_size)
        processed_hp = self.__process_buffer(image_hp, image_size)

        return np.abs(processed_hp) + np.abs(processed_lp)
