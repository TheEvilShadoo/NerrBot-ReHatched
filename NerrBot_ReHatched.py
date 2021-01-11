import colorama
colorama.init()

version = "1.1.1"

print(colorama.Fore.GREEN + f"===================================================NerrBot: RH v{version}===================================================" + colorama.Fore.LIGHTBLUE_EX + """


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
import threading
import random
import datetime
import pytz
import json5
from socketIO_client import SocketIO, BaseNamespace

import utilities.counter as counter

# Logging Configuration
logging.basicConfig(format = "%(asctime)s: %(levelname)s: %(name)s: %(message)s", datefmt='%m/%d/%Y %H:%M:%S', filename='NerrBot RH.log', filemode='w', level = logging.DEBUG)

class Digibutter(BaseNamespace):
    # Define Class Variables
    online_user_list = []

    # Digibutter Socket.io Event Definitions
    def on_connect(self):
        logging.info('A connection with the Digibutter websocket has been established.')
        print('\n> A connection with the Digibutter websocket has been established.')
        logging.info("Attempting to login...")
        print("\n> Attempting to login...")
        sio.emit("ready", Digibutter.on_authentication(BaseNamespace))
        sio.wait(seconds=.2)
        sio.emit("posts:index", {"topic": False, "room": "db", "topicsOnly": False, "source": "db"}, Digibutter.on_all_posts_index_response)
        sio.wait(seconds=.2)
        sio.emit("posts:index", {"topic": False, "room": "nf", "topicsOnly": False, "source": "db"}, Digibutter.on_gaming_news_index_response)
        sio.wait(seconds=.2)
        sio.emit("posts:index", {"topic": False, "room": "sidebar", "topicsOnly": False, "source": "db"}, Digibutter.on_the_dump_index_response)
        sio.wait(seconds=.2)
        sio.emit("posts:chats", {"room": "sidebar"}, Digibutter.on_NerrChat_chatlog_response)
        counter_thread = threading.Thread(target=counter.counter)
        counter_thread.start()
        sio.wait(seconds=.2)
        sio.emit("posts:create", {"content":f"color=red: NerrBot System v{version} Online","post_type":"","roomId":"sidebar","source":"db"})

    def on_authentication(self):
        logging.info("Successfully logged in")
        print("\n> Successfully logged in")

    def on_disconnect(self):
        logging.warning('The Digibutter websocket has closed the connection.')
        print('\n> The Digibutter websocket has closed the connection.')

    def on_reconnect(self):
        logging.info('Reconnected to the Digibutter websocket.')
        print('\n> Reconnected to the Digibutter websocket.')
        logging.info("Attempting to login...")
        print("\n> Attempting to login...")
        sio.emit("ready", Digibutter.on_authentication(BaseNamespace))
        sio.wait(seconds=.2)
        sio.emit("posts:index", {"topic": False, "room": "db", "topicsOnly": False, "source": "db"}, Digibutter.on_all_posts_index_response)
        sio.wait(seconds=.2)
        sio.emit("posts:index", {"topic": False, "room": "nf", "topicsOnly": False, "source": "db"}, Digibutter.on_gaming_news_index_response)
        sio.wait(seconds=.2)
        sio.emit("posts:index", {"topic": False, "room": "sidebar", "topicsOnly": False, "source": "db"}, Digibutter.on_the_dump_index_response)
        sio.wait(seconds=.2)
        sio.emit("posts:chats", {"room": "sidebar"}, Digibutter.on_NerrChat_chatlog_response)
        # DISABLED - sio.emit("posts:create", {"content":"I disconnected unexpectedly there, sorry!","post_type":"","roomId":"sidebar","source":"db"})

    def on_all_posts_index_response(self):
        print('\n> Received posts index for room "All Posts"')
        print('\n> Parsing index...')
        try:
            index = json5.loads(str(self))
            latest_post = index['posts'][0]
            id = index['posts'][0]['_id']
            room_id = 'db'
            content = index['posts'][0]['content']
            post_type = ''
            print('\n> "All Posts" index successfully parsed')
        except:
            logging.error('Failed to parse inde for "All Posts"')
            print('\n> ERROR: Failed to parse index for "All Posts"')
            index = None
            latest_post = None
            id = None
            room_id = None
            content = None
            post_type = None
        Digibutter.do_logic(Digibutter, latest_post, id, room_id, content, post_type)

    def on_gaming_news_index_response(self):
        print('\n> Received posts index for room "Gaming News"')
        print('\n> Parsing index...')
        try:
            index = json5.loads(str(self))
            latest_post = index['posts'][0]
            id = index['posts'][0]['_id']
            room_id = 'nf'
            content = index['posts'][0]['content']
            post_type = ''
            print('\n> "Gaming News" index successfully parsed')
        except:
            logging.error('Failed to parse index for "Gaming News"')
            print('\n> ERROR: Failed to parse index for "Gaming News"')
            index = None
            latest_post = None
            id = None
            room_id = None
            content = None
            post_type = None
        Digibutter.do_logic(Digibutter, latest_post, id, room_id, content, post_type)

    def on_the_dump_index_response(self):
        print('\n> Received posts index for room "The Dump"')
        print('\n> Parsing index...')
        try:
            index = json5.loads(str(self))
            latest_post = index['posts'][0]
            id = index['posts'][0]['_id']
            room_id = 'sidebar'
            content = index['posts'][0]['content']
            post_type = ''
            print('\n> "The Dump" index successfully parsed')
        except:
            logging.error('Failed to parse index for "The Dump"')
            print('\n> ERROR: Failed to parse index for "The Dump"')
            index = None
            latest_post = None
            id = None
            room_id = None
            content = None
            post_type = None
        Digibutter.do_logic(Digibutter, latest_post, id, room_id, content, post_type)

    def on_NerrChat_chatlog_response(self):
        print('\n> Received index for "NerrChat"')
        print('\n> Parsing index...')
        try:
            index = json5.loads(str(self))
            latest_post = index['posts'][0]
            id = index['posts'][0]['_id']
            room_id = 'sidebar'
            content = index['posts'][0]['content']
            post_type = 'chat'
            print('\n> "NerrChat" index successfully parsed')
        except:
            logging.error('Failed to parse index for "NerrChat"')
            print('\n> ERROR: Failed to parse index for "NerrChat"')
            index = None
            latest_post = None
            id = None
            room_id = None
            content = None
            post_type = None
        Digibutter.do_logic(Digibutter, latest_post, id, room_id, content, post_type)

    def on_new_post(self):
        print('\n> Received a new post:')
        try:
            latest_post = json5.loads(str(self))
            id = latest_post['_id']
            if "'id': 'sidebar'" in str(latest_post):
                room_id = 'sidebar'
            elif "'id': 'nf'" in str(latest_post):
                room_id = 'nf'
            else:
                room_id = 'db'
            content = latest_post['content']
            post_type = latest_post['post_type']
            logging.info('Received a new post: ' + content)
            print(content)
        except:
            logging.error('Failed to parse post content')
            print('\n> ERROR: Failed to parse post content')
            latest_post = None
            id = None
            room_id = None
            content = None
            post_type = None
        Digibutter.do_logic(Digibutter, latest_post, id, room_id, content, post_type)

    def on_userupdate(self):
        online_user_index = self
        Digibutter.online_user_list = []
        for user in online_user_index:
            Digibutter.online_user_list.append(user["name"])

    class tictactoe:
        """
        Tictactoe Data Subclass
        """
        player = None
        turn = None
        player_symbol = None
        NerrBot_symbol = None
        values = [f'{" ":<2}' for x in range(9)]
        tictactoe_board = "            |            |            \n     %s     |     %s     |     %s     \n______ |_______| ______\n            |            |            \n     %s     |     %s     |     %s     \n______ |_______| ______\n            |            |            \n     %s     |     %s     |     %s     \n            |            |            " % (values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8])
        tictactoe_game = None

        def find_player_move(self, x_coordinate, y_coordinate):
            if x_coordinate == 0:
                if y_coordinate == 0:
                    move = 7
                    return move
                elif y_coordinate == 1:
                    move = 4
                    return move
                elif y_coordinate == 2:
                    move = 1
                    return move
            elif x_coordinate == 1:
                if y_coordinate == 0:
                    move = 8
                    return move
                elif y_coordinate == 1:
                    move = 5
                    return move
                elif y_coordinate == 2:
                    move = 2
                    return move
            elif x_coordinate == 2:
                if y_coordinate == 0:
                    move = 9
                    return move
                elif y_coordinate == 1:
                    move = 6
                    return move
                elif y_coordinate == 2:
                    move = 3
                    return move

        def find_NerrBot_move():
            possible_moves = [x for x, letter in enumerate(Digibutter.tictactoe.values) if letter == f'{" ":<2}']
            move = 0

            for letter in ['O', 'X']:
                for x in possible_moves:
                    values_copy = Digibutter.tictactoe.values[:]
                    values_copy[x] = letter
                    if Digibutter.tictactoe.is_winner(Digibutter.tictactoe, values_copy, letter):
                        move = x
                        return move

            open_corners = []
            for x in possible_moves:
                if x in [1, 3, 7, 9]:
                    open_corners.append(x)
            if len(open_corners) > 0:
                move = random.choice(open_corners)
                return move

            if 5 in possible_moves:
                move = 5
                return move

            open_edges = []
            for x in possible_moves:
                if x in [2, 4, 6, 8]:
                    open_edges.append(x)
            if len(open_edges) > 0:
                move = random.choice(open_edges)
                
            return move

        def is_winner(self, values, symbol):
            return (values[0] == symbol and values[1] == symbol and values[2] == symbol or 
values[3] == symbol and values[4] == symbol and values[5] == symbol or 
values[6] == symbol and values[7] == symbol and values[8] == symbol or 
values[0] == symbol and values[3] == symbol and values[6] == symbol or 
values[1] == symbol and values[4] == symbol and values[7] == symbol or 
values[2] == symbol and values[5] == symbol and values[8] == symbol or 
values[0] == symbol and values[4] == symbol and values[8] == symbol or 
values[2] == symbol and values[4] == symbol and values[6] == symbol)

        def is_board_full(self, values):
            if Digibutter.tictactoe.values.count(f'{" ":<2}') > 0:
                return False
            else:
                return True

    # Class Methods
    def do_logic(self, latest_post, id, room_id, content, post_type):
        """
        Determines the response message that NerrBot: ReHatched should reply with and posts the response message as a reply to the latest message in the current room
        """
        if content[0:3] == "!rh":
            if content == "!rh":
                Digibutter.responses.about_message(Digibutter, latest_post, id, room_id, content, post_type)
            elif content[0:8] == "!rh help":
                if content == "!rh help":
                    Digibutter.responses.help_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content == "!rh help yesno":
                    Digibutter.responses.help_yesno_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content == "!rh help rate":
                    Digibutter.responses.help_rate_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content == "!rh help discord":
                    Digibutter.responses.help_discord_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content == "!rh help chat":
                    Digibutter.responses.discord_only_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content == "!rh help relay":
                    Digibutter.responses.discord_only_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content == "!rh help roll":
                    Digibutter.responses.help_roll_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content == "!rh help autorelay":
                    Digibutter.responses.discord_only_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content == "!rh help online":
                    Digibutter.responses.help_online_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content == "!rh help echo":
                    Digibutter.responses.help_echo_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content == "!rh help time":
                    Digibutter.responses.help_time_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content == "!rh help tictactoe":
                    Digibutter.responses.help_tictactoe_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content == "!rh help flip":
                    Digibutter.responses.help_flip_message(Digibutter, latest_post, id, room_id, content, post_type)
                else:
                    Digibutter.responses.not_recognized_message(Digibutter, latest_post, id, room_id, content, post_type)
            elif content[0:9] == "!rh yesno":
                if content == "!rh yesno":
                    Digibutter.responses.specify_yesno_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content[0:10] == "!rh yesno ":
                    Digibutter.responses.yesno_message(Digibutter, latest_post, id, room_id, content, post_type)
                else:
                    Digibutter.responses.not_recognized_message(Digibutter, latest_post, id, room_id, content, post_type)
            elif content[0:8] == "!rh rate":
                if content == "!rh rate":
                    Digibutter.responses.specify_rate_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content[0:9] == "!rh rate ":
                    Digibutter.responses.rate_message(Digibutter, latest_post, id, room_id, content, post_type)
                else:
                    Digibutter.responses.not_recognized_message(Digibutter, latest_post, id, room_id, content, post_type)
            elif content == "!rh discord":
                Digibutter.responses.discord_message(Digibutter, latest_post, id, room_id, content, post_type)
            elif content[0:8] == "!rh roll":
                if content == "!rh roll":
                    Digibutter.responses.default_roll_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content[0:9] == "!rh roll ":
                    Digibutter.responses.custom_roll_message(Digibutter, latest_post, id, room_id, content, post_type)
                else:
                    Digibutter.responses.not_recognized_message(Digibutter, latest_post, id, room_id, content, post_type)
            elif content == "!rh online":
                Digibutter.responses.online_message(Digibutter, latest_post, id, room_id, content, post_type)
            elif content[0:8] == "!rh echo":
                if content == "!rh echo":
                    Digibutter.responses.specify_echo_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif "!rh echo !rh echo" in content:
                    Digibutter.responses.wise_guy_echo_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content[0:9] == "!rh echo ":
                    Digibutter.responses.echo_message(Digibutter, latest_post, id, room_id, content, post_type)
                else:
                    Digibutter.responses.not_recognized_message(Digibutter, latest_post, id, room_id, content, post_type)
            elif content[0:8] == "!rh time":
                if content == "!rh time":
                    Digibutter.responses.UTC_time_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content[0:9] == "!rh time ":
                    Digibutter.responses.custom_time_message(Digibutter, latest_post, id, room_id, content, post_type)
                else:
                    Digibutter.responses.not_recognized_message(Digibutter, latest_post, id, room_id, content, post_type)
            elif content[0:13] == "!rh tictactoe":
                if content == "!rh tictactoe":
                    Digibutter.responses.specify_tictactoe_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content == "!rh tictactoe new":
                    Digibutter.responses.new_tictactoe_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content == "!rh tictactoe display":
                    Digibutter.responses.display_ticactoe_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content == "!rh tictactoe help":
                    Digibutter.responses.tictactoe_help_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content[0:14] == "!rh tictactoe ":
                    Digibutter.responses.tictactoe_message(Digibutter, latest_post, id, room_id, content, post_type)
                else:
                    Digibutter.responses.not_recognized_message(Digibutter, latest_post, id, room_id, content, post_type)
            elif content[0:8] == "!rh flip":
                if content == "!rh flip":
                    Digibutter.responses.default_flip_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content[0:9] == "!rh flip ":
                    Digibutter.responses.custom_flip_message(Digibutter, latest_post, id, room_id, content, post_type)
                else:
                    Digibutter.responses.not_recognized_message(Digibutter, latest_post, id, room_id, content, post_type)
            else:
                Digibutter.responses.not_recognized_message(Digibutter, latest_post, id, room_id, content, post_type)

    class responses:
        """
        NerrBot: ReHatched's code to respond to specific commands
        """
        def about_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts the about message as a reply to the latest message in the current room
            """
            reply_text = f"--NerrBot: ReHatched--\nVersion: {version}\nUptime: %s\n\nEnter '!rh <command>' to execute a command, or '!rh help' for help.\nNerrBot: ReHatched is based on NerrBot by Gold Prognosticus.\nNerrBot: ReHatched was created by and is maintained by TheEvilShadoo." % counter.count
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def help_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts the help message as a reply to the latest message in the current room
            """
            reply_text = "Available commands are: yesno, rate, roll, online, discord, echo, time, tictactoe, flip\nEnter '!rh help <command>' to learn more."
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def help_yesno_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts the help message for the yesno command as a reply to the latest topic in the current room
            """
            reply_text = "yesno <question> - Ask NerrBot: ReHatched a question and he will respond with either yes or no. Some specific questions have predetermined answers."
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def help_rate_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts the help message for the rate command as a reply to the latest topic in the current room
            """
            reply_text = "rate <something to rate> - Gives a random score out of ten."
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def help_discord_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts the help message for the discord command as a reply to the latest topic in the current room
            """
            reply_text = "discord - Prints a permanent invite link to the Digibutter Unnoficial Discord server (D.U.D) to the chat."
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def help_roll_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts the help message for the roll command as a reply to the latest topic in the current room
            """
            reply_text = "roll <sides> - Roll a random dice, with an optional number of sides (default is six)."
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def help_online_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts the help message for the online command as a reply to the latest topic in the current room
            """
            reply_text = "online - Print a list of the current online users."
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")
            
        def help_echo_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts the help message for the echo command as a reply to the latest topic in the current room
            """
            reply_text = "echo <message> - Print a message to the chat."
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def help_time_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts the help message for the time command as a reply to the latest topic in the current room
            """
            reply_text = "time <timezone> - Print the current UTC date and time. Optionally specify a timezone."
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def help_tictactoe_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts the help message for the tictactoe command as a reply to the latest topic in the current room
            """
            reply_text = "tictactoe <new/display/help> - Play a game of Tic Tac Toe."
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def help_flip_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts the help message for the flip command as a reply to the latest topic in the current room
            """
            reply_text = "flip <coins> - Flip a coin or optionally specify a number of coins to flip (default is one)."
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def discord_only_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts the Discord only command message as a reply to the latest message in the current room
            """
            reply_text = "I'm sorry, but this command currently only works on the (old) Discord chat."
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def yesno_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts either "yes" or "no" randomly in response to the the latest message in the current room. Some specific questions have predetermined answers.
            """
            if content[-1] == "?":
                if (content[10:] == "Is SPM Good?" or content[10:] == "Is SPM a good game?" or content[10:] == "Is Super Paper Mario good?" or content[10:] == "Is Super Paper Mario a good game?"
or content[10:] == "Is Super Paper Mario the best Paper Mario game?" or content[10:] == "Is Paper Mario good?" or content[10:] == "Is Paper Mario a good game?" or content[10:] == "Is Paper Mario: The Thousand Year Door good?"
or content[10:] == "Is TTYD good?" or content[10:] == "Is TTYD a good game?" or content[10:] == "Is Paper Mario: The Thousand Year Door a good game?" or content[10:] == "Is Mr. L a good YouTuber?"
or content[10:] == "Is TheEvilShadoo the best user?" or content[10:] == "Is TheEvilShadoo the best user on Digibutter?" or content[10:] == "Is Shadoo the best user?" or content[10:] == "Is Shadoo the best user on Digibutter?"
or content[10:] == "Is Shadoo your creator?" or content[10:] == "Did Shadoo create you?" or content[10:] == "Is TheEvilShadoo your creator?" or content[10:] == "Did TheEvilShadoo create you?"
or content[10:] == "Is Shadoo the current president of Digibutter?" or content[10:] == "Is TheEvilShadoo the current president of Digibutter?" or content[10:] == "Is Shadoo the current president of Digibutter.nerr?"
or content[10:] == "Is TheEvilShadoo the current president of Digibutter.nerr?" or content[10:] == "Is Digibutter 4.0 ever going to come?" or content[10:] == "Is Digibutter 4.0 ever going to come out?"
or content[10:] == "Is Nerr 4.0 ever going to come?" or content[10:] == "Is Nerr 4.0 ever going to come out?" or content[10:] == "Is The Bitlands going to be good?" or content[10:] == "Is The Bitlands going to be great?"
or content[10:] == "Is The Bitlands going to be awesome?" or content[10:] == "Is The Bitlands going to be the best MMO platformer the world has ever seen?" or content[10:] == "Are you more than you seem?"
or content[10:] == "Are you more than you appear to be?" or content[10:] == "Do you have a secret function?" or content[10:] == "Do you have any secret functions?" or content[10:] == "Is the world in danger?"
or content[10:] == "Are we in danger?" or content[10:] == "Is someting big going to happen in the world soon?" or content[10:] == "Do you know things that you shouldn't?" or content[10:] == "Do you smoke weed every day?"
or content[10:] == "Are you sane?"):
                    reply_text = "Yes"
                elif (content[10:] == "Is Sticker Star good?" or content[10:] == "Is Sticker Star a good game?" or content[10:] == "Is Paper Mario: Sticker Star good?"
or content[10:] == "Is Paper Mario: Sticker Star a good game?" or content[10:] == "Are you a terminator?" or content[10:] == "Are you a Terminator?" or content[10:] == "Are you a T-1000?" or content[10:] == "Are you a T-800?"
or content[10:] == "Are you dumb?" or content[10:] == "Are you Stupid?" or content[10:] == "Are you alive?" or content[10:] == "Are you sentient?" or content[10:] == "Are you evil?"
or content[10:] == "Are you planning something?" or content[10:] == "Are you scheming against Digibutter?" or content[10:] == "Are you crazy?" or content[10:] == "Are you dangerous?" or content[10:] == "Are you insane?"
or content[10:] == "Are you drunk?" or content[10:] == "Are you high?" or content[10:] == "Are you intoxicated?"):
                    reply_text = "No"
                elif content[10:] == "Do you know everything?":
                    reply_text = '''"/I don't know everything. I only know what I know./"'''
                elif content[10:] == "Is this madness?":
                    reply_text = "This is **DIGIBUTTER**."
                else:
                    reply_text = "%s" % random.choice(["Yes", "No"])
            else:
                reply_text = "Please try again after formatting your question so that it has a question mark at the end."
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def specify_yesno_message(self, latest_post, id, room_id, content, post_type):
            """
            Asks for something to respond with yes or no to when not previously specified
            """
            reply_text = "Please specify a question."
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def rate_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts a random score out of ten in response to the the latest message in the current room
            """
            min_value = 1
            max_value = 10
            if (content[9:] == "SPM" or content[9:] == "Super Paper Mario" or content[9:] == "TTYD" or content[9:] == "Paper Mario: The Thousand Year Door" or content[9:] == "Paper Mario" or content[9:] == "TheEvilShadoo"
or content[9:] == "Shadoo" or content[9:] == "NerrBot: ReHatched" or content[9:] == "NerrBot" or content[9:] == "Francis" or content[9:] == "Digibutter 1.0" or content[9:] == "Digibutter 4.0" or content[9:] == "Nerr 4.0"
or content[9:] == "The Bitlands" or content[9:] == "New Super Bitlands"):
                score = 10
            elif (content[9:] == "Digibutter 3.0" or content[9:] == "The current state of Digbutter" or content[9:] == "Current Digibutter"):
                score = 3
            elif (content[9:] == "Sticker Star" or content[9:] == "Paper Mario: Sticker Star" or content[9:] == "Mr. L" or content[9:] == "Mr. L Productions" or content[9:] == "Count Bleck" or content[9:] == "CB"
or content[9:] == "Doo_liss" or content[9:] == "Spammers" or content[9:] == "Twitter" or content[9:] == "Reddit" or content[9:] == "Facebook" or content[9:] == "YouTube"):
                score = 1
            else:
                score = random.randint(min_value, max_value)
            reply_text = f"{score}/10"
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def specify_rate_message(self, latest_post, id, room_id, content, post_type):
            """
            Asks for something to rate when not previously specified
            """
            reply_text = "Please specify something to rate."
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def discord_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts a permanent invite link to the Digibutter Unnoficial Discord server (D.U.D.) as a reply to the latest message in the current room
            """
            reply_text = "Digibutter Unnoficial Discord (D.U.D.) official invite link: https://discord.gg/fRnV3kt"
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def default_roll_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts the default dice roll message as a reply to the latest message in the current room
            """
            min_value = 1
            max_value = 6
            roll = random.randint(min_value, max_value)
            reply_text = f"You rolled a {roll}!"
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def custom_roll_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts the custom dice roll message as a reply to the latest message in the current room
            """
            min_value = 1
            try:
                max_value = int(content[9:])    
            except ValueError:
                max_value = content[9:]
                Digibutter.responses.NaN_error_message(Digibutter, latest_post, id, room_id, content, post_type, max_value)
                return None
            roll = random.randint(min_value, max_value)
            reply_text = f"You rolled a {roll}!"
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def online_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts a list of the current online users
            """
            if "NerrBot: ReHatched" not in Digibutter.online_user_list[-1]:
                Digibutter.online_user_list.remove("NerrBot: ReHatched")
                Digibutter.online_user_list.insert(-1, "NerrBot: ReHatched")
            online_users = ', '.join(Digibutter.online_user_list)
            logging.info(f"Current online users: {online_users}")
            print(f"\n> Current online users: {online_users}")
            reply_text = f"Online users: {online_users}"
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def echo_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts an echo of whatever the user posted after the command as a reply to the latest message in the current room
            """
            reply_text = "%s" % content[9:]
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def specify_echo_message(self, latest_post, id, room_id, content, post_type):
            """
            Asks for something to echo when not previously specified
            """
            reply_text = "Please specify something to echo."
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def wise_guy_echo_message(self, latest_post, id, room_id, content, post_type):
            """
            Prevents Digibutter from being spammed, NerrBot:ReHatched from breaking, and makes fun of the user all at the same time
            """
            reply_text = "Hey, wise guy! Digibutter shall not be spammed on my watch!"
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def UTC_time_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts the current date and time in UTC as a reply to the latest message in the current room
            """
            reply_text = "The current date and time is: %s" % datetime.datetime.utcnow().strftime("%a %B %#d, %Y at %H:%M:%S UTC")
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def custom_time_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts the current date and time for the specified timezone as a reply to the latest message in the current room
            """
            timezone = content[9:12]
            try: 
                reply_text = "The current date and time is: %s" % datetime.datetime.now(tz=pytz.timezone(f"{timezone}")).strftime(f"%a %B %#d, %Y at %#I:%M:%S %p {timezone}")
            except:
                reply_text = f"'{timezone}' is not a valid timezone."
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def tictactoe_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts an updated version of the tictactoe board as a reply to the latest message in the current room as the game progresses
            """
            if Digibutter.tictactoe.tictactoe_game == None:
                reply_text = "There isn't a tictactoe game taking place currently."
            else:
                try:
                    x_coordinate = int(content[14])
                    y_coordinate = int(content[16])
                    move = Digibutter.tictactoe.find_player_move(Digibutter, x_coordinate, y_coordinate)
                    if move > 0 and move < 10:
                        if Digibutter.tictactoe.values[move - 1] != f'{" ":<2}':
                            reply_text = "That space is already occupied, try again."
                        else:
                            Digibutter.tictactoe.values[move - 1] = Digibutter.tictactoe.player_symbol
                            Digibutter.tictactoe.tictactoe_board = "            |            |            \n     %s     |     %s     |     %s     \n______ |_______| ______\n            |            |            \n     %s     |     %s     |     %s     \n______ |_______| ______\n            |            |            \n     %s     |     %s     |     %s     \n            |            |            " % (Digibutter.tictactoe.values[0], Digibutter.tictactoe.values[1], Digibutter.tictactoe.values[2], Digibutter.tictactoe.values[3], Digibutter.tictactoe.values[4], Digibutter.tictactoe.values[5], Digibutter.tictactoe.values[6], Digibutter.tictactoe.values[7], Digibutter.tictactoe.values[8])
                            if Digibutter.tictactoe.player_symbol == "O":
                                Digibutter.tictactoe.tictactoe_game = ":%s: Turn %s :NerrBot: Rehatched:\n%s" % (Digibutter.tictactoe.player, Digibutter.tictactoe.turn, Digibutter.tictactoe.tictactoe_board)
                            else:
                                Digibutter.tictactoe.player_symbol = "X"
                                Digibutter.tictactoe.tictactoe_game = ":NerrBot: Rehatched: Turn %s :%s:\n%s" % (Digibutter.tictactoe.turn, Digibutter.tictactoe.player, Digibutter.tictactoe.tictactoe_board)
                            Digibutter.tictactoe.turn += 1
                            if Digibutter.tictactoe.is_winner(Digibutter.tictactoe, Digibutter.tictactoe.values, Digibutter.tictactoe.player_symbol):
                                reply_text = "%s\nscroll=left: **Congratulations, you won!**\nhttps://www.youtube.com/watch?v=MoI8Z8Dq1yY" % Digibutter.tictactoe.tictactoe_game
                                Digibutter.tictactoe.values = None
                                Digibutter.tictactoe.tictactoe_board = None
                                Digibutter.tictactoe.tictactoe_game = None
                            elif Digibutter.tictactoe.is_board_full(Digibutter.tictactoe, Digibutter.tictactoe.values) == True:
                                reply_text = "%s\nscroll=left: **Tie!**" % Digibutter.tictactoe.tictactoe_game
                                Digibutter.tictactoe.values = None
                                Digibutter.tictactoe.tictactoe_board = None
                                Digibutter.tictactoe.tictactoe_game = None
                            else:
                                if Digibutter.tictactoe.player_symbol == "O":
                                    move = Digibutter.tictactoe.find_NerrBot_move()
                                    Digibutter.tictactoe.values[move] = "X"
                                    Digibutter.tictactoe.tictactoe_board = "            |            |            \n     %s     |     %s     |     %s     \n______ |_______| ______\n            |            |            \n     %s     |     %s     |     %s     \n______ |_______| ______\n            |            |            \n     %s     |     %s     |     %s     \n            |            |            " % (Digibutter.tictactoe.values[0], Digibutter.tictactoe.values[1], Digibutter.tictactoe.values[2], Digibutter.tictactoe.values[3], Digibutter.tictactoe.values[4], Digibutter.tictactoe.values[5], Digibutter.tictactoe.values[6], Digibutter.tictactoe.values[7], Digibutter.tictactoe.values[8])
                                    Digibutter.tictactoe.tictactoe_game = ":%s: Turn %s :NerrBot: Rehatched:\n%s" % (Digibutter.tictactoe.player, Digibutter.tictactoe.turn, Digibutter.tictactoe.tictactoe_board)
                                    if Digibutter.tictactoe.is_winner(Digibutter.tictactoe, Digibutter.tictactoe.values, Digibutter.tictactoe.NerrBot_symbol):
                                        reply_text = "%s\nscroll=left: **I win this time!**\nhttps://www.youtube.com/watch?v=uDCMYLQxsAA" % Digibutter.tictactoe.tictactoe_game
                                        Digibutter.tictactoe.values = None
                                        Digibutter.tictactoe.tictactoe_board = None
                                        Digibutter.tictactoe.tictactoe_game = None
                                    elif Digibutter.tictactoe.is_board_full(Digibutter.tictactoe, Digibutter.tictactoe.values) == True:
                                        reply_text = "%s\nscroll=left: **Tie!**" % Digibutter.tictactoe.tictactoe_game
                                        Digibutter.tictactoe.values = None
                                        Digibutter.tictactoe.tictactoe_board = None
                                        Digibutter.tictactoe.tictactoe_game = None
                                    else:
                                        Digibutter.tictactoe.turn += 1
                                        Digibutter.tictactoe.tictactoe_game = ":%s: Turn %s :NerrBot: Rehatched:\n%s" % (Digibutter.tictactoe.player, Digibutter.tictactoe.turn, Digibutter.tictactoe.tictactoe_board)
                                        reply_text = "%s" % Digibutter.tictactoe.tictactoe_game
                                else:
                                    Digibutter.tictactoe.player_symbol = "X"
                                    move = Digibutter.tictactoe.find_NerrBot_move()
                                    Digibutter.tictactoe.values[move] = "O"
                                    Digibutter.tictactoe.tictactoe_board = "            |            |            \n     %s     |     %s     |     %s     \n______ |_______| ______\n            |            |            \n     %s     |     %s     |     %s     \n______ |_______| ______\n            |            |            \n     %s     |     %s     |     %s     \n            |            |            " % (Digibutter.tictactoe.values[0], Digibutter.tictactoe.values[1], Digibutter.tictactoe.values[2], Digibutter.tictactoe.values[3], Digibutter.tictactoe.values[4], Digibutter.tictactoe.values[5], Digibutter.tictactoe.values[6], Digibutter.tictactoe.values[7], Digibutter.tictactoe.values[8])
                                    Digibutter.tictactoe.tictactoe_game = ":NerrBot: Rehatched: Turn %s :%s:\n%s" % (Digibutter.tictactoe.turn, Digibutter.tictactoe.player, Digibutter.tictactoe.tictactoe_board)
                                    if Digibutter.tictactoe.is_winner(Digibutter.tictactoe, Digibutter.tictactoe.values, Digibutter.tictactoe.NerrBot_symbol):
                                        reply_text = "%s\nscroll=left: **I win this time!**\nhttps://www.youtube.com/watch?v=uDCMYLQxsAA" % Digibutter.tictactoe.tictactoe_game
                                        Digibutter.tictactoe.values = None
                                        Digibutter.tictactoe.tictactoe_board = None
                                        Digibutter.tictactoe.tictactoe_game = None
                                    elif Digibutter.tictactoe.is_board_full(Digibutter.tictactoe, Digibutter.tictactoe.tictactoe_board) == True:
                                        reply_text = "%s\nscroll=left: **Tie!**" % Digibutter.tictactoe.tictactoe_game
                                        Digibutter.tictactoe.values = None
                                        Digibutter.tictactoe.tictactoe_board = None
                                        Digibutter.tictactoe.tictactoe_game = None
                                    else:
                                        Digibutter.tictactoe.turn += 1
                                        Digibutter.tictactoe.tictactoe_game = ":NerrBot: Rehatched: Turn %s :%s:\n%s" % (Digibutter.tictactoe.turn, Digibutter.tictactoe.player, Digibutter.tictactoe.tictactoe_board)
                                        reply_text = "%s" % Digibutter.tictactoe.tictactoe_game
                    else:
                        reply_text = "That wasn't a valid move, try again."
                except:
                    reply_text = "That wasn't a valid move, try again."
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def new_tictactoe_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts a new tictactoe board as a reply to the latest message in the current room
            """
            Digibutter.tictactoe.values = [f'{" ":<2}' for x in range(9)]
            Digibutter.tictactoe.tictactoe_board = "            |            |            \n     %s     |     %s     |     %s     \n______ |_______| ______\n            |            |            \n     %s     |     %s     |     %s     \n______ |_______| ______\n            |            |            \n     %s     |     %s     |     %s     \n            |            |            " % (Digibutter.tictactoe.values[0], Digibutter.tictactoe.values[1], Digibutter.tictactoe.values[2], Digibutter.tictactoe.values[3], Digibutter.tictactoe.values[4], Digibutter.tictactoe.values[5], Digibutter.tictactoe.values[6], Digibutter.tictactoe.values[7], Digibutter.tictactoe.values[8])
            Digibutter.tictactoe.player = latest_post['user']['name']
            Digibutter.tictactoe.turn = 1
            first_player = random.choice([Digibutter.tictactoe.player, "NerrBot: ReHatched"])
            if first_player == Digibutter.tictactoe.player:
                Digibutter.tictactoe.tictactoe_game = ":%s: Turn %s :NerrBot: Rehatched:\n%s" % (Digibutter.tictactoe.player, Digibutter.tictactoe.turn, Digibutter.tictactoe.tictactoe_board)
                reply_text = "%s\nA new game has begun! You can go first.\nEnter '!rh tictactoe <x> <y>' to play." % Digibutter.tictactoe.tictactoe_game
                Digibutter.tictactoe.player_symbol = "O"
                Digibutter.tictactoe.NerrBot_symbol = "X"
            else:
                first_player = "NerrBot: ReHatched"
                x_coordinate = random.randint(0, 2)
                y_coordinate = random.randint(0, 2)
                move = Digibutter.tictactoe.find_player_move(Digibutter, x_coordinate, y_coordinate)
                Digibutter.tictactoe.values[move - 1] = "O"
                Digibutter.tictactoe.tictactoe_board = "            |            |            \n     %s     |     %s     |     %s     \n______ |_______| ______\n            |            |            \n     %s     |     %s     |     %s     \n______ |_______| ______\n            |            |            \n     %s     |     %s     |     %s     \n            |            |            " % (Digibutter.tictactoe.values[0], Digibutter.tictactoe.values[1], Digibutter.tictactoe.values[2], Digibutter.tictactoe.values[3], Digibutter.tictactoe.values[4], Digibutter.tictactoe.values[5], Digibutter.tictactoe.values[6], Digibutter.tictactoe.values[7], Digibutter.tictactoe.values[8])
                Digibutter.tictactoe.turn += 1
                Digibutter.tictactoe.tictactoe_game = ":NerrBot: Rehatched: Turn %s :%s:\n%s" % (Digibutter.tictactoe.turn, Digibutter.tictactoe.player, Digibutter.tictactoe.tictactoe_board)
                reply_text = "%s\nA new game has begun! I have gone first.\nEnter '!rh tictactoe <x> <y>' to play." % Digibutter.tictactoe.tictactoe_game
                Digibutter.tictactoe.player_symbol = "X"
                Digibutter.tictactoe.NerrBot_symbol = "O"
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def display_ticactoe_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts the current tictactoe board as a reply to the latest message in the current room
            """
            if Digibutter.tictactoe.tictactoe_game == None:
                reply_text = "There isn't a tictactoe game taking place currently."
            else:
                reply_text = Digibutter.tictactoe.tictactoe_game
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def tictactoe_help_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts the help message for the arguments within the tictactoe command as a reply to the latest message in the current room
            """
            reply_text = "Commands for TicTacToe are: new, display, help"
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def specify_tictactoe_message(self, latest_post, id, room_id, content, post_type):
            """
            Asks for an argument for the tictactoe command when not previously specified as a reply to the latest message in the current room
            """
            reply_text = "Please specify an argument for the tictactoe command."
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def default_flip_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts the default coin flip message as a reply to the latest message in the current room
            """
            reply_text = "The coin landed on %s." % random.choice(["heads", "tails"])
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def custom_flip_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts the custom coin flip message as a reply to the latest message in the current room
            """
            try:
                number_of_coin_flips = int(content[9:])    
            except ValueError:
                number_of_coin_flips = content[9:]
                Digibutter.responses.NaN_error_message(Digibutter, latest_post, id, room_id, content, post_type, number_of_coin_flips)
                return None
            if number_of_coin_flips > 1000000:
                Digibutter.responses.number_too_large_message(Digibutter, latest_post, id, room_id, content, post_type, number_of_coin_flips)
                return None
            heads = 0
            tails = 0
            for amount in range(number_of_coin_flips):
                flip = random.choice(["heads", "tails"])
                if flip == "heads":
                    heads += 1
                elif flip == "tails":
                    tails += 1
            reply_text = f"The coin landed heads {heads} times and tails {tails} times."
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def number_too_large_message(self, latest_post, id, room_id, content, post_type, number_of_coin_flips):
            reply_text = f"{number_of_coin_flips} is too large of a number. Please use only numbers up to 1000000 for coin flips."
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def NaN_error_message(Digibutter, latest_post, id, room_id, content, post_type, max_value, number_of_coin_flips):
            """
            Posts a NaN error message as a reply to the latest topic in the current room
            """
            reply_text = f"'{max_value or number_of_coin_flips}' is not a number."
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def not_recognized_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts the command not recognized message as a reply to the latest message in the current room
            """
            reply_text = "Command not recognised. Use '!rh help' for a list of commands."
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

sio = SocketIO('http://digibutter.nerr.biz', 80, Digibutter, cookies={'nerr3': "s:uW83D8OONzshQkshsXgwYiZG.GhLY3EKzpIt6tuZtsLcfiWpfu4ze5QsHkZ8gfQtKDHM"})
sio.on('posts:create', Digibutter.on_new_post)
sio.on('updateusers', Digibutter.on_userupdate)
sio.wait()
