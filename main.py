# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 17:33:57 2019

@author: quentin
"""

import os
import logging
import sys
from pathlib import Path
import random
import subprocess

from media import Media

def error_handler():
    info = sys.exc_info()
    return "{}. {}, line {}".format(info[0], info[1], info[2].tb_lineno)


def generate_file_list(path, reccurent = False):
    try:
        files = []
        for path_name, dir_names, file_names in os.walk(path, topdown = True, onerror = error_handler):
            for file_name in file_names:
                file = Media(path_name, file_name)
                files.append(file)

            if not reccurent:
                break
            
        return files
    except Exception as e:
        logging.error(error_handler())
        return []
                
def random_file(files):
    try:
        return random.choice(files)
    except IndexError as e:
        logging.error(error_handler())
        return []
        
    
def random_files(files, nb_selected):
    try:
        return random.choices(files, k= nb_selected)
    except IndexError as e:
        logging.error(error_handler())
        return []

def open_file(file):
    try:
        subprocess.run([str(file.path)], shell = True)
    except subprocess.CalledProcessError as e:
        logging.error(error_handler())
    except FileNotFoundError as e:
        logging.error(error_handler())
        logging.error("File Not Found: {}".format(str(file.path)))
    except OSError as e:
        logging.error(error_handler())
        
    
def main():
    if  len(sys.argv) < 2:
        print("Add a directory")
        return
    
    path =  Path(str(sys.argv[1]))
    files = generate_file_list(path, True)
    if files:
        #[print("file: {}".format(file)) for file in files]
        file = random_file(files)
        open_file(file)
    else:
        print("No listed files")
    

if __name__=="__main__":
    main()