from typing import ValuesView
from PIL import Image
import numpy as np
import requests
from xml.etree import ElementTree as et
from io import BytesIO
from datetime import datetime, timedelta
from image_param.IP_CONSTANTS import URL_STRINGS
from image_param.IP_CONSTANTS.CONSTANTS import *
from image_param.helper.helper import *

class GetImage:
    """
    This class is used to get single image or batch images.
    Images are returned in the following format:
    * Single Image
        a. PIL.Image
        b. numpy.ndarray
        c. xml #pending
    * Images in batches
        a. dictionary of {timestamps: PIL.Image}
        b. dictionary of {timestamps: numpy.ndarray}
        c. dictionary of {timestamps: xml} #pending

    Methods
    -------

    __init__():
        initializes required values. Some values are mandatory whereas some are optional.
    
    url():
        returns url which will be used to get single image
    
    set_details():
        this method can set mandetory or required values
    
    get_batch():
        returns dictionary of multiple timestamps and respective images/array/xml
    """
    def __init__(self, starttime: datetime,
                 aia_wave: (AIA_WAVE, str),
                 image_size: (IMAGE_SIZE, str),
                 output: (OUTPUT_FMT, str),
                 endtime: datetime = None,
                 step: int = None,
                 limit: int = None):
        """
        This constructor function initializes required values.
        Some parameters are mandatory whereas some are optional.
        Optional parameters will be initialized as `None`.
        Parameters
        ----------
        :param starttime: mandatory -> defines starting time. Input should be in `datetime` format. For get() mehtod, this value will be used.
        :param aia_wave: mandatory -> defines type of wave of the image. It should be one of the AIA_WAIVE class value.
        :param image_size: mandatory -> defines size of the image in pixels. It should be one of the IMAGE_SIZE class value.
        :param output: mandatory -> defines output format of get() and get_batch() methods. It should be one of the OUTPUT_FMT class value.
        :param endtime: optional -> defines ending time when timeperiod will be used. It should be in `datetime` format.
        :param step: optional -> defines step which will be used for getting images in batch. It should be integer.
        :param limit: optional -> defines maximum images which shall be fetched. It should be integer.
        """
        # TODO: Error handling
        self.starttime = starttime
        self.aia_wave = aia_wave
        self.image_size = image_size
        self.output = output
        self.endtime = endtime
        self.step = step
        self.limit = limit

    def url(self) -> str:
        """
        This methods prepares the url to get the single image. 
        :return str: prepared url is returned as a string.
        """
        time_str = datetime.strftime(self.starttime, '%Y-%m-%dT%H:%M:%S')
        # self.time_str = datetime.strftime(self.starttime, '%Y-%m-%dT%H:%M:%S')
        prepared_url = URL_STRINGS.aia_image_jpeg_url.format(self.image_size, self.aia_wave, time_str)
        return prepared_url

    def get(self) -> (Image, np.ndarray):
        """
        To get a single image this method is used.
        :return (PIL.Image or np.ndarray or xml): output of the image.

        """
        if self.output not in cls_attr_val(OUTPUT_FMT):
            raise AttributeError(f'\'OUTPUT_FMT\' has no attribute value \'{self.output}\'.')

        response = requests.get(self.url())
        img = Image.open(BytesIO(response.content))

        if self.output == 'image':
            return img
        elif self.output == 'array':
            return np.asarray(img)
        elif self.output == 'xml':
            # TODO: write a function to convert 3d array to xml in image_param.helper.helper
            pass

        return None
    
    def set_details(self, starttime: datetime = None, 
                 aia_wave: (AIA_WAVE, str) = None,
                 image_size: (IMAGE_SIZE, str) = None,
                 output: (OUTPUT_FMT, str) = None,
                 endtime: datetime = None,
                 step: int = None,
                 limit: int = None):
        """
        Using this method, user can change initialized values.
        If values is already initialized and/or user does not desire to change it; previous values will be preserved.
        
        Parameters
        ----------
        :param starttime: optional -> defines starting time. Input should be in `datetime` format. For get() mehtod, this value will be used.
        :param aia_wave: optional -> defines type of wave of the image. It should be one of the AIA_WAIVE class value.
        :param image_size: optional -> defines size of the image in pixels. It should be one of the IMAGE_SIZE class value.
        :param output: optional -> defines output format of get() and get_batch() methods. It should be one of the OUTPUT_FMT class value.
        :param endtime: optional -> defines ending time when timeperiod will be used. It should be in `datetime` format.
        :param step: optional -> defines step which will be used for getting images in batch. It should be integer.
        :param limit: optional -> defines maximum images which shall be fetched. It should be integer.
        """

        #TODO: self.starttime = starttime if !starttime

        if starttime != None:
            self.starttime = starttime
        
        if aia_wave != None:
            self.aia_wave = aia_wave
        
        if image_size != None:
            self.image_size = image_size

        if endtime != None:
            self.endtime = endtime

        if step != None:
            self.step = step

        if limit != None:
            self.limit = limit

        if output != None:
            self.output = output

    def get_batch(self) -> dict:
        """
        To get images in batches i.e. between starting time and ending time, this method is used.
        :return dict: dictionary with {timestamp: PIL.Image or numpy.ndarray or xml}
        """
        time_diff = (self.endtime - self.starttime).total_seconds() #seconds
        # TODO: Discuss limit and step

        step = int(time_diff / self.limit) #integer values

        img_time = self.starttime #Image will be fetched by this time

        img_dict = {}

        while img_time < self.endtime:
            img_time_str = img_time.strftime('%Y-%m-%dT%H:%M:%S')
            img_dict[img_time_str] = self.get()
            img_time = img_time + timedelta(seconds = step)

        if self.output == 'image':
            return img_dict
        elif self.output == 'array':
            for key in img_dict:
                img_dict[key] = np.asarray(img_dict[key])
            return img_dict
        elif self.output == 'xml':
            # TODO: write a function to convert 3d array to xml in image_param.helper.helper
            pass