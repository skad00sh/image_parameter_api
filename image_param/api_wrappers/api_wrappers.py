from PIL import Image
import numpy as np
import requests
from xml.etree import ElementTree as et
from io import BytesIO
from datetime import datetime
from image_param.IP_CONSTANTS import URL_STRINGS
from image_param.IP_CONSTANTS.CONSTANTS import *


class GetImage:
    """
    To get a single image
    Doc pending :/
    """
    def __init__(self,
                 starttime: datetime,
                 aia_wave: (AIA_WAVE, list),
                 image_size: (IMAGE_SIZE, str)):
        self.starttime = starttime
        self.aia_wave = aia_wave
        self.image_size = image_size

    def prepare_url(self) -> str:
        time_str = datetime.strftime(self.starttime, '%Y-%m-%dT%H:%M:%S')
        # self.time_str = datetime.strftime(self.starttime, '%Y-%m-%dT%H:%M:%S')
        prepared_url = URL_STRINGS.aia_image_jpeg_url.format(self.image_size, self.aia_wave, time_str)
        return prepared_url

    def get_image(self) -> Image:
        response = requests.get(self.prepare_url())
        img = Image.open(BytesIO(response.content))
        return img

class GetImageParameter:
    """
    To get parameters of single image
    Doc pending :/
    """

    def __init__(self,
                 starttime: datetime,
                 aia_wave: (AIA_WAVE, list),
                 image_size: (IMAGE_SIZE, str),
                 param_id: (IMAGE_PARAM, str)):
        self.starttime = starttime
        self.aia_wave = aia_wave
        self.image_size = image_size
        self.param_id = param_id

    def prepare_url(self) -> str:
        time_str = datetime.strftime(self.starttime, '%Y-%m-%dT%H:%M:%S')
        # self.time_str = datetime.strftime(self.starttime, '%Y-%m-%dT%H:%M:%S')
        prepared_url = URL_STRINGS.aia_imageparam_jpeg_url.format(self.image_size, self.aia_wave, time_str,
                                                                  self.param_id)
        return prepared_url

    def get_image(self) -> Image:
        response = requests.get(self.prepare_url())
        img = Image.open(BytesIO(response.content))
        return img
    