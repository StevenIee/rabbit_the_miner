# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 16:07:41 2023

@author: JISU babo
"""
import rpyc
import time

class Connect:
    def __init__(self):
        self.rpy = [];
        
    def check(self):
        try:
            self.rpy = rpyc.connect("localhost", 18861, config = {'allow_all_attrs': True, 'allow_pickle':True})
            return self.rpy
    
        except ConnectionRefusedError:
            print('Please run a servier_APP first!!')
            time.sleep(1)
            empty_rpy = []
            return empty_rpy

