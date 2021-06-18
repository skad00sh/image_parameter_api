import numpy as np
from xml.etree import ElementTree as et

def cls_attr_val(cls) -> list:
    """
    Aim of this function is to return the values of the attributes of the class.
    Any attribute which starts with '_' is ignored.

    Parameters
    ----------
    :param cls: Input name of the class. e.g. IMAGE_SIZE, AIA_WAVE
    :return list: Output is a list of the values of the attributes

    Doctests
    --------
    >>> from image_param.IP_CONSTANTS.CONSTANTS import *
    >>> from image_param.helper.helper import cls_attr_val
    >>> print(cls_attr_val(AIA_WAVE))
    ['94', '131', '171', '193', '211', '304', '335', '1600', '1700']
    >>> print(cls_attr_val(IMAGE_SIZE))
    ['2k', '512', '256']
    """
    attr_dict = {k: v for k, v in cls.__dict__.items() if not k.startswith('_')}
    return list(attr_dict.values())


def np_array_3d_to_xml(arr: np.ndarray) -> et:
    """
    A function to convert numpy 3d array to xml
    Sample xml output from the API: 
    http://dmlabdmlab.cs.gsu.edu/dmlabapi/params/SDO/AIA/64/full/?wave=171&starttime=2012-02-13T20:10:00
    ~TODO: write function~
    No need to implement this because API has no xml output discussed on 18/06/2021
    """
    pass