# -*- coding: utf-8 -*-

import os
import json
import logging

from pathlib import Path

from media import MediaType
from error import error_handler

class Preference:
    def __init__(self, directory = "", media_type =  MediaType.ANY):
        self.directory = Path(directory)
        self.media_type = media_type
        
    def __repr__(self):
        return "Preference({}, {})".format(self.directory, self.media_type)
        
        
        
        
class PreferenceManager:
    
    @classmethod         
    def loadFrom(cls, path):
        try:
            with open(path, 'r') as f:
                try:
                    preference = json.load(f, object_hook = cls._dico_to_preference)
                except json.JSONDecodeError:
                    preference = Preference()
                    logging.warning("Invalid json file:\n{}".format(error_handler()))
                finally:
                    return preference
        except FileNotFoundError:
            return Preference()
    
    @classmethod     
    def saveTo(cls, path, preference):
        if not path:
            return
        
        directory_path = path.parents[0]
        try:
            os.listdir(str(directory_path))
        except FileNotFoundError:
            try:
                os.makedirs(directory_path)
            except Exception:
                logging.error("Can't create {}\n{}".format(directory_path, error_handler()))
                return
        
        with open(path, 'w') as f:
            data = json.dumps(cls._preference_to_dico(preference), indent = 4)
            print("data: {}".format(data))
            f.write(data)
    
    @staticmethod    
    def _dico_to_preference(dico):
        media_type =  MediaType.ANY
        if dico["media_type"]:
            media_type = MediaType.media_type_from_str(dico["media_type"])
            
        return Preference(dico["directory"], media_type)
    
    @staticmethod    
    def _preference_to_dico(preference):
        dico = dict()
        dico["directory"] = str(preference.directory)
        dico["media_type"] = str(preference.media_type)
        return dico
    
    
    
        