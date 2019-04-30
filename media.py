import os
import logging
import random

from pathlib import Path
from enum import Enum

from error import error_handler

# Media
# -> Save basic data from a media file
# -----------------------------------------------------------------------------
class Media:
    def __init__(self, path, name):
        self.name = name
        self.path = Path(path, name)
        
    def __str__(self):
        return str(self.path)
    
    def __repr__(self):
        "Media(name: {}, path: {})".format(self.name, self.path)
        
        
        

# Media type
# -----------------------------------------------------------------------------
class MediaType (Enum):
    ANY = 0
    SOUND = 1 << 0
    VIDEO = 1 << 1


# Librarian
# -> handle media liste (generate media list)
# -----------------------------------------------------------------------------
class Librarian:
    
    @staticmethod
    def generate_media_list(directory_path, media_type = MediaType.ANY, reccurent = False):
        try:
            files = []
            for path_name, dir_names, file_names in os.walk(directory_path, topdown = True, onerror = error_handler):
                for file_name in file_names:
                    file = Media(path_name, file_name)
                    files.append(file)
    
                if not reccurent:
                    break
                
            return files
        except Exception:
            logging.error(error_handler())
            return []
        
    @staticmethod
    def random_media(media_list):
        try:
            return random.choice(media_list)
        except IndexError:
            logging.error(error_handler())
            return []

    @staticmethod
    def random_media_list(media_list, media_nb):
        try:
            return random.choices(media_list, k= media_nb)
        except IndexError:
            logging.error(error_handler())
            return []