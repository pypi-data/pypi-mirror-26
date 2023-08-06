# -*- coding: utf-8 -*-
"""
    femagtools
    ~~~~~~~~~~

    Python bindings for FEMAG

    :copyright: 2016 Semafor Informatik & Energie AG, Basel
    :license: BSD, see LICENSE for more details.
"""
napshot_title__ = 'femagtools'
__version__ = '0.3.2'
__author__ = 'Ronald Tanner'
__license__ = 'BSD'
__copyright__ = 'Copyright 2016 SEMAFOR Informatik & Energie AG'

from .bch import Reader
from .model import MachineModel
from .fsl import Builder
from .magnet import Magnet
from .femag import Femag, ZmqFemag


def read_bchfile(filename):
    """Read BCH/BATCH results from file *filename*."""
    import io
    bchresults = Reader()
    with io.open(filename, encoding='latin1', errors='ignore') as f:
        bchresults.read(f.readlines())
    return bchresults


def create_fsl(machine,
               operatingconditions={},
               magnetmat=[]):
    """create FSL command list from model parameters
    :param: machine dict with parameters
    :param: operatuîngConditions dict with parameters
    :param: magnetmat list fo dict with parameters
"""
    model = MachineModel(machine)
    
    builder = Builder()
    magnets = []
    if magnetmat:
        magnets = Magnet(magnetmat)
    if operatingconditions:
            return builder.create(model, operatingconditions, magnets)
    return builder.create_model(model, magnets) + ['save_model(cont)']
    
