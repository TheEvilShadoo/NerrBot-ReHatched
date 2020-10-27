from logging import log
import colorama
colorama.init()

print(colorama.Fore.GREEN + "===================================================NerrBot: RH v0.1.0===================================================" + colorama.Fore.LIGHTBLUE_EX + """


                                    _______________________________________________ 
                                   |____________________       ____________________|
                                   |   ______________   |     |   ______________   |
                                   |  |   ________   |  |_____|  |   ________   |  |
                                   |  |  |   _____|  |   _____   |  |_____   |  |  |
                                   |  |  |  |__      |  |     |  |      __|  |  |  |
                                   |  |  |_____|     |  |     |  |     |_____|  |  |
                                   |  |______________|  |     |  |______________|  |
                                   |____________________|     |____________________|
                                   |   _________________________________________   |
                                   |  |                                         |  |
                                   |  |   ___________________________________   |  |
                                   |  |  |                                   |  |  |
                                   |  |  |___________________________________|  |  |
                                   |  |                                         |  |
                                   |  |_________________________________________|  |
                                   |_______________________________________________|""" + colorama.Fore.LIGHTCYAN_EX + """


  _   _                ____        _       ____  _   _   ___       ____                    _                         
 | \ | | ___ _ __ _ __| __ )  ___ | |_ _  |  _ \| | | | |_ _|___  |  _ \ _   _ _ __  _ __ (_)_ __   __ _             
 |  \| |/ _ \ '__| '__|  _ \ / _ \| __(_) | |_) | |_| |  | |/ __| | |_) | | | | '_ \| '_ \| | '_ \ / _` |            
 | |\  |  __/ |  | |  | |_) | (_) | |_ _  |  _ <|  _  |  | |\__ \ |  _ <| |_| | | | | | | | | | | | (_| |  _   _   _ 
 |_| \_|\___|_|  |_|  |____/ \___/ \__(_) |_| \_\_| |_| |___|___/ |_| \_\\\__,_|_| |_|_| |_|_|_| |_|\__, | (_) (_) (_)
                                                                                                   |___/             """ + colorama.Fore.RESET)

import logging
import json5
from socketIO_client import SocketIO, BaseNamespace

import utilities.counter as counter
import utilities.dice as dice

# Logging Configuration
logging.basicConfig(format = "%(asctime)s: %(levelname)s: %(name)s: %(message)s", datefmt='%m/%d/%Y %H:%M:%S', filename='NerrBot RH.log', filemode='w', level = logging.DEBUG)

# Socketio Connection Events
class Namespace(BaseNamespace):

    def on_connect(self):
        logging.info('A connection with the Digibutter websocket has been established.')
        print('\n> A connection with the Digibutter websocket has been established.')
        Namespace.authenticate(BaseNamespace)
        sio.wait(seconds=.2)
        sio.emit("posts:index", {"topic": False, "room": "db", "topicsOnly": False, "source": "db"}, Namespace.on_all_posts_index_response)
        sio.wait(seconds=.2)
        sio.emit("posts:index", {"topic": False, "room": "nf", "topicsOnly": False, "source": "db"}, Namespace.on_gaming_news_index_response)
        sio.wait(seconds=.2)
        sio.emit("posts:index", {"topic": False, "room": "sidebar", "topicsOnly": False, "source": "db"}, Namespace.on_the_dump_index_response)
        sio.wait(seconds=.2)
        sio.emit("posts:chats", {"room": "sidebar"}, Namespace.on_NerrChat_response)

    def on_authentication(self):
        logging.info("Successfully logged in")
        print("\n> Successfully logged in")

    def on_disconnect(self):
        logging.warning('The Digibutter websocket has closed the connection.')

    def on_all_posts_index_response(self):
        print('\n> Received posts index for room "All Posts"')
        index = json5.loads(str(self))

    def on_gaming_news_index_response(self):
        print('\n> Received posts index for room "Gaming News"')
        index = json5.loads(str(self))

    def on_the_dump_index_response(self):
        print('\n> Received posts index for room "The Dump"')
        index = json5.loads(str(self))

    def on_NerrChat_response(self):
        print('\n> Received chatlog for "NerrChat"')
        index = json5.loads(str(self))

    def authenticate(self):
        logging.info("Attempting to login...")
        print("\n> Attempting to login...")
        sio.emit("ready", Namespace.on_authentication(BaseNamespace))

    def disconnect_if_inactive(self):
        sio.wait(seconds=100)
        sio.disconnect()
        
class room_name_ids:
    All_Posts = "db"
    Gaming_News = "nf"
    The_Dump = "sidebar"
    Nerr_Chat = "posts:chats" 

sio = SocketIO('http://digibutter.nerr.biz', 80, Namespace, cookies={'nerr3': "s:uW83D8OONzshQkshsXgwYiZG.GhLY3EKzpIt6tuZtsLcfiWpfu4ze5QsHkZ8gfQtKDHM"})
Namespace.disconnect_if_inactive(Namespace)