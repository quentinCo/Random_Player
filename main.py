# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 17:33:57 2019

@author: quentin
"""

import logging
import sys
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
        
    
def main():
    if  len(sys.argv) < 2:
        print("Add a directory")
        return
    
    path =  Path(str(sys.argv[1]))
    files = Librarian.generate_media_list(path, reccurent = True)
    if files:
        #[print("file: {}".format(file)) for file in files]
        file = Librarian.random_media(files)
        if file:
            open_file(file)
    else:
        print("No listed files")
    

if __name__=="__main__":
    main()