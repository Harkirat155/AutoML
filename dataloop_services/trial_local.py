import dtlpy as dl
import logging
from logging_utils import logginger
logger = logging.getLogger(name=__name__)
from importlib import import_module
import json
import torch


class LocalTrialConnector():

    def __init__(self):
        self.logger = logginger(__name__)

    def run(self, inputs_dict):
        model_name = inputs_dict['model_specs']['name']
        # cls = getattr(import_module('.adapter', 'object_detecter.' + model_name), 'AdapterModel')
        cls = getattr(import_module('.adapter', 'object_detecter'), 'AdapterModel')#TODO: reapropriate the model choosing to networks
        checkpoint_path = 'checkpoint.pt'
        torch.save(inputs_dict, checkpoint_path)
        adapter = cls()
        adapter.load(checkpoint_path=checkpoint_path)
        self.logger.info('commencing training . . . ')
        adapter.train()
        self.logger.info('training finished')
        checkpoint = adapter.get_checkpoint()
        if type(checkpoint['metrics']['val_accuracy']) is not float:
            raise Exception(
                'adapter, get_best_metrics method must return dict with only python floats. '
                'Not numpy floats or any other objects like that')
        return checkpoint
