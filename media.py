# -*- coding: utf-8 -*-

import os
import logging
import random

from pathlib import Path
from enum import Flag

from error import error_handler

import magic

# Media type
# -----------------------------------------------------------------------------
class MediaType (Flag):
    UNKNOWN = 1 << 0
    SOUND = 1 << 1
    VIDEO = 1 << 2
    ANY = 0xFF


# Media
# -> Save basic data from a media file
# -----------------------------------------------------------------------------
class Media:
    # Python functions
    def __init__(self, path, name):
        self.name = name
        self.path = Path(path, name)
        self.__init_mime()
        self.__init_type()
                
    def __str__(self):
        return str(self.path)
    
    def __repr__(self):
        "Media(name: {}, path: {})".format(self.name, self.path)
        
    # Private functions
    def __init_mime(self):
        try:
            file = open(self.path, 'rb')
            try:
                self.mime = magic.from_buffer(file.read(1024), mime = True)
            except Exception:
                self.mime = ""
            finally:
                file.close()
        except Exception:
            self.mime = ""
            
    def __init_type(self):
        self.type = MediaType.UNKNOWN
        if not self.mime:
            return
            
        type_end = self.mime.find("/")
        if type_end < 0:
            return
            
        type_str = self.mime[:type_end]        
        if type_str == "audio":
            self.type = MediaType.SOUND
        elif type_str == "video":
            self.type = MediaType.VIDEO
        

# Librarian
# -> handle media liste (generate media list)
# -----------------------------------------------------------------------------
class Librarian:
    
    @staticmethod
    def generate_media_list(directory_path, media_type = MediaType.ANY, reccurent = False):
        try:
            medias = []
            for path_name, dir_names, file_names in os.walk(directory_path, topdown = True, onerror = error_handler):
                for file_name in file_names:
                    media = Media(path_name, file_name)
                    if media.type & media_type:
                        medias.append(media)
                        print("Media: {}".format(media.name))
    
                if not reccurent:
                    break
                
            return medias
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