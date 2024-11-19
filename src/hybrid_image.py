import os
from math import sqrt

import cv2
import numpy as np


class HybridImage:
    def __distance(self, point1, point2):
        return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

    def __gaussian_low_pass(self, cf, imgShape):
        base = np.zeros(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows / 2, cols / 2)
        for i in range(rows):
            for j in range(cols):
                base[i, j] = np.exp(
                    -((self.__distance((i, j), center)) ** 2) / (2 * cf**2)
                )
        return base

    def __gaussian_high_pass(self, cf, imgShape):
        base = np.zeros(imgShape[:2])
        rows, cols = imgShape[:2]
        center = (rows / 2, cols / 2)
        for i in range(rows):
            for j in range(cols):
                base[i, j] = 1 - np.exp(
                    -((self.__distance((i, j), center)) ** 2) / (2 * cf**2)
                )
        return base

    def __process_buffer(self, buffer, image_size):
        # Convert the bytes to a NumPy array
        np_arr = np.frombuffer(buffer, np.uint8)

        # Decode the NumPy array to an image
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, (image_size, image_size))

        return image

    def __create_filtered_image(self, buffer, image_size, cf=10, useHighPass=False):
        image = self.__process_buffer(buffer, image_size)

        filterFunction = (
            self.__gaussian_high_pass if useHighPass else self.__gaussian_low_pass
        )

        # Fourier Transform of the image
        ft = np.fft.fft2(image)

        # Apply Centre Shifting
        center = np.fft.fftshift(ft)

        # Apply Filter
        filteredCenter = center * filterFunction(cf, image.shape)

        # Extract frequency component
        filteredFT = np.fft.ifftshift(filteredCenter)

        # Get image using Inverse FFT
        filteredImage = np.fft.ifft2(filteredFT)

        return np.abs(filteredImage)

    def apply_low_pass_filter(self, buffer, image_size, cf):
        return self.__create_filtered_image(buffer, image_size, cf)

    def apply_high_pass_filter(self, buffer, image_size, cf):
        return self.__create_filtered_image(buffer, image_size, cf, useHighPass=True)

    def create_image_preview(self, buffer, image_size):
        return self.__process_buffer(buffer, image_size)

    def create_hybrid_image(self, image_lp, image_hp, image_size):
        processed_lp = self.__process_buffer(image_lp, image_size)
        processed_hp = self.__process_buffer(image_hp, image_size)

        return np.abs(processed_hp) + np.abs(processed_lp)
