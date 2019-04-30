# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 17:33:57 2019

@author: quentin
"""

import os
import logging
from pathlib import Path
import subprocess

from media import Librarian
from error import error_handler




def open_file(file):
    try:
        subprocess.run([str(file.path)], shell = True)
    except subprocess.CalledProcessError:
        logging.error(error_handler())
    except FileNotFoundError:
        logging.error(error_handler())
        logging.error("File Not Found: {}".format(str(file.path)))
    except OSError:
        logging.error(error_handler())
        
def ask_directory(ask_mess):
    str_res = input(ask_mess)
    path =  Path(str(str_res))        
    try:
        os.listdir(str(path))            
        return True, path
    except FileNotFoundError:
        print("Directory \"{}\" is not valid, please enter a valid path: ".format(str(path)))
    except OSError:
        logging.error(error_handler())
        
    return False, ""
        
def ask_option(options, default = 0):
    [print("{} - {}".format(i + 1,option)) for i, option in enumerate(options)]
    res = input("Choose your option: ")
    
    if not res:
        option = default
    else:
        option = int(res) - 1
        
    is_valid = (option >= 0 and option < len(options))
    return is_valid, option

def aks_suggestion(media_list, default = 0):
    [print("{} - {}".format(i + 1, media.name)) for i, media in enumerate(media_list)]
    res = input("Choose your media: ")
    if not res:
        option = default
    else:
        option = int(res) - 1
        
    is_valid = (option >= 0 and option < len(media_list))
    return is_valid, option
    
def main():
    
    is_valid = False
    path = Path()
    
    while not is_valid :
        is_valid, path = ask_directory("Media directory:")
        media_list = Librarian.generate_media_list(path, reccurent = True)
        if not media_list:
            print("No media in folder, please chose another directory.")
            is_valid = False
            
    options = [
            "Read a random media",
            "Suggest media"
            ]
    
    is_valid = False
    while not is_valid :
        is_valid, option = ask_option(options)
    
    if option == 0:
        media = Librarian.random_media(media_list)
    else:
        medias = Librarian.random_media_list(media_list, 3)
        is_valid = False
        while not is_valid:
            is_valid, option = aks_suggestion(medias)
        media = medias[option]

    if media:
        open_file(media)
    

if __name__=="__main__":
    main()