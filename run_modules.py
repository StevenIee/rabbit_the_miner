# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 16:51:30 2023

@author: JAY KIM
"""

import subprocess

def run_modules(modules):
    for module in modules:
        subprocess.run(['python', module])

if __name__ == '__main__':
    modules = ['NF_server_app.py', 'main.py']
    run_modules(modules)