# -*- coding: utf-8 -*-
"""
Created on  Feb 14 1:22 PM 2017

@author: aeloyq
"""
import nnbuilder.main
from basic import base
from nnbuilder.main import mainloop


class ex(base):
    def __init__(self, kwargs):
        base.__init__(self, kwargs)
        self.window = None
        self.isload=False
        self.scale=1

    def init(self):
        base.init(self)
        if not self.window: self.window = nnbuilder.main.config.batch_size * self.scale

    def before_epoch(self):
        if self.kwargs['iter'] == 0:
            if self.isload==False:
                self.kwargs['minibatches'] = mainloop.get_minibatches(self.kwargs['datas'], True, self.window)
                self.logger("Shuffled Data At Epoch {} part {} With Window {}".format(self.kwargs['n_epoch']+1,self.kwargs['n_part']+1,self.window),1,1)
            else:
                self.isload=False

    def save_(self,dict):
        pass
    def load_(self,dict):
        self.isload=True


config = ex({})
instance=config
