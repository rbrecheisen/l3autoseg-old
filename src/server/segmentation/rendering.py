import os
import pydicom
import numpy as np
import matplotlib.pyplot as plt

from barbell2light.dicom import get_pixels


def create_png(image):
    image_file_path = image.file_obj.path
    image_file_dir = os.path.split(image_file_path)[0]
    image_id = os.path.splitext(os.path.split(image_file_path)[1])[0]
    prediction_file_name = '{}_pred.npy'.format(image_id)
    prediction_file_path = os.path.join(image_file_dir, prediction_file_name)
    if not os.path.isfile(prediction_file_path):
        return None
    prediction = np.load(prediction_file_path)
    image = pydicom.read_file(image_file_path)
    image = get_pixels(image, normalize=True)
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 2, 1)
    plt.imshow(image, cmap='gray')
    ax.axis('off')
    ax = fig.add_subplot(1, 2, 2)
    plt.imshow(prediction, cmap='viridis')
    ax.axis('off')
    png_file_name = '{}.png'.format(image_id)
    png_file_path = os.path.join(image_file_dir, png_file_name)
    plt.savefig(png_file_path, bbox_inches='tight')
    plt.close('all')
    return png_file_name, png_file_path
