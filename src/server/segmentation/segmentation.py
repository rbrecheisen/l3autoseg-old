import os
import pydicom
import numpy as np

from barbell2light.dicom import get_pixels
from django.conf import settings


def load_model():
    import tensorflow as tf
    return tf.keras.models.load_model(settings.TENSORFLOW_MODEL_DIR, compile=False)


def segment_image(image_file_path):
    model = load_model()
    segmentation = Segmentation(model, image_file_path)
    return segmentation.predict_labels()


class Segmentation:

    def __init__(self, model, image_file_path):
        self.model = model
        self.image_file_path = image_file_path

    @staticmethod
    def normalize(img, min_bound, max_bound):
        img = (img - min_bound) / (max_bound - min_bound)
        img[img > 1] = 0
        img[img < 0] = 0
        c = (img - np.min(img))
        d = (np.max(img) - np.min(img))
        img = np.divide(c, d, np.zeros_like(c), where=d != 0)
        return img

    def predict_labels(self):
        p = pydicom.read_file(self.image_file_path)
        img1 = get_pixels(p, normalize=True)
        img1 = self.normalize(img1, -200, 200)  # TODO: put this in params.json
        img1 = img1.astype(np.float32)
        img2 = np.expand_dims(img1, 0)
        img2 = np.expand_dims(img2, -1)
        pred = self.model.predict([img2])
        pred_squeeze = np.squeeze(pred)
        pred_max = pred_squeeze.argmax(axis=-1)
        pred_file_name = os.path.split(self.image_file_path)[1]
        pred_file_name = os.path.splitext(pred_file_name)[0] + '_pred.npy'
        pred_file_path = os.path.join(os.path.split(self.image_file_path)[0], pred_file_name)
        np.save(pred_file_path, pred_max)
        print('Predicted labels for {}'.format(self.image_file_path))
        return pred_file_name, pred_file_path
