#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals 

import pathlib
import sys
import warnings

from .core import RTDCBase
from .config import Configuration
from .util import hashfile
from . import fmt_dict, fmt_tdms, fmt_hierarchy

if sys.version_info[0] == 2:
    str_classes = (str, unicode)
else:
    str_classes = str


def new_dataset(data, identifier=None):
    """Initialize a new RT-DC data set
    
    Parameters
    ----------
    data:
        can be one of the following:
        - dict
        - .tdms file
        - subclass of `RTDCBase`
          (will create a hierarchy child)
    identifier: str
        A unique identifier for this data set. If set to `None`
        an identifier will be generated.
    
    Returns
    -------
    dataset: subclass of `RTDCBase`
        A new dataset instance
    """
    if isinstance(data, dict):
        return fmt_dict.RTDC_Dict(data, identifier=identifier)
    elif isinstance(data, (str_classes)):
        return fmt_tdms.RTDC_TDMS(data, identifier=identifier)
    elif isinstance(data, pathlib.Path):
        return fmt_tdms.RTDC_TDMS(str(data), identifier=identifier)
    elif isinstance(data, RTDCBase):
        return fmt_hierarchy.RTDC_Hierarchy(data, identifier=identifier)
    else:
        msg = "data type not supported: {}".format(data.__class__)
        raise NotImplementedError(msg)
