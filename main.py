# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 17:33:57 2019

@author: quentin
"""

import os
import logging
from pathlib import Path
import subprocess
from enum import Enum

from media import Librarian, MediaType
from error import error_handler
    
class State (Enum):
    STATE_ASK_MEDIA_TYPE = 0
    STATE_ASK_DIRECTORY = 1
    STATE_GENERATE_LIST = 2
    STATE_ASK_EMPTY = 3
    STATE_ASK_PLAY_OPTION = 4
    STATE_RANDOM_MEDIA = 5
    STATE_GENERATE_SUGGESTION = 6
    STATE_ASK_SUGGESTION = 7
    STATE_PLAY = 8
    STATE_QUIT = 9


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

def ask_option(options, question = "Choose your option: ", default = 0):
    [print("{} - {}".format(i + 1,option)) for i, option in enumerate(options)]
    res = input(question)
    
    if not res:
        option = default
    else:
        option = int(res) - 1
        
    is_valid = (option >= 0 and option < len(options))
    return is_valid, option

def ask_mediatype():
    options = [
            "Audio",
            "Video",
            "Any"
            ]
    
    is_valid, option = ask_option(options, question = "Which media type: ")
    
    media_type = MediaType.ANY
    if is_valid:
        if option == 0:
            media_type = MediaType.SOUND
        elif option == 1:
            media_type = MediaType.VIDEO
        else:
            media_type = MediaType.ANY
        
    return is_valid, media_type

def ask_empty_folder():
    options = [
        "Other media type",
        "Other folder",
        "Quit"
        ]
    
    is_valid, option = ask_option(options, question = "The folder have no desired medias, what do you want: ")
            
    state = State.STATE_ASK_EMPTY
    if is_valid:
        if option == 0:
            state = State.STATE_ASK_MEDIA_TYPE
        elif option == 1:
            state = State.STATE_ASK_DIRECTORY
        else:
            state = State.STATE_QUIT
    return is_valid, state

        
def ask_play_option():
    options = [
            "Read a random media",
            "Suggest media"
            ]
    
    is_valid, option = ask_option(options)
    
    state = State.STATE_ASK_PLAY_OPTION
    if is_valid:
        if option == 0:
            state = State.STATE_RANDOM_MEDIA
        else:
            state = State.STATE_GENERATE_SUGGESTION
            
    return option, state

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
    state = State.STATE_ASK_MEDIA_TYPE
    media_type =  MediaType.ANY
    media_list = []
    suggestions = []
    
    while True:
        if state == State.STATE_ASK_MEDIA_TYPE:
            is_valid, media_type = ask_mediatype()
            if is_valid:
                state = State.STATE_ASK_DIRECTORY
        elif state == State.STATE_ASK_DIRECTORY:
            is_valid, path = ask_directory("Media directory:")
            if is_valid:
                state = State.STATE_GENERATE_LIST
        elif state == State.STATE_GENERATE_LIST:
            media_list = Librarian.generate_media_list(path, media_type = media_type, reccurent = True)
            if not media_list:
                state = State.STATE_ASK_EMPTY
            else:
                state = State.STATE_ASK_PLAY_OPTION
        elif state == State.STATE_ASK_EMPTY:
            is_valid, state = ask_empty_folder()
        elif state == State.STATE_ASK_PLAY_OPTION:
            is_valid, state = ask_play_option()
        elif state == State.STATE_RANDOM_MEDIA:
            media = Librarian.random_media(media_list)
            state = State.STATE_PLAY
        elif state == State.STATE_GENERATE_SUGGESTION:
            suggestions = Librarian.random_media_list(media_list, 3) # TODO: retake can have many time the same media
            state = State.STATE_ASK_SUGGESTION
        elif state == State.STATE_ASK_SUGGESTION:
            is_valid, option = aks_suggestion(suggestions)
            if is_valid:
                media = suggestions[option]
                state = State.STATE_PLAY
        elif state == State.STATE_PLAY:
                if media:
                    open_file(media)
                break;
        else:
            break;
    

if __name__=="__main__":
    main()