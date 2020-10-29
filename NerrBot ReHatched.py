from utilities.logic import do_logic
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

from utilities import counter, dice
from utilities.logic import do_logic

# Logging Configuration
logging.basicConfig(format = "%(asctime)s: %(levelname)s: %(name)s: %(message)s", datefmt='%m/%d/%Y %H:%M:%S', filename='NerrBot RH.log', filemode='w', level = logging.DEBUG)

class Digibutter(BaseNamespace):
    """
    Digibutter Socketio Event Definitions
    """

    def on_connect(self):
        logging.info('A connection with the Digibutter websocket has been established.')
        print('\n> A connection with the Digibutter websocket has been established.')
        Digibutter.authenticate(BaseNamespace)
        sio.wait(seconds=.2)
        sio.emit("posts:index", {"topic": False, "room": "db", "topicsOnly": False, "source": "db"}, Digibutter.on_all_posts_index_response)
        sio.wait(seconds=.2)
        sio.emit("posts:index", {"topic": False, "room": "nf", "topicsOnly": False, "source": "db"}, Digibutter.on_gaming_news_index_response)
        sio.wait(seconds=.2)
        sio.emit("posts:index", {"topic": False, "room": "sidebar", "topicsOnly": False, "source": "db"}, Digibutter.on_the_dump_index_response)
        sio.wait(seconds=.2)
        sio.emit("posts:chats", {"room": "sidebar"}, Digibutter.on_NerrChat_chatlog_response)

    def on_authentication(self):
        logging.info("Successfully logged in")
        print("\n> Successfully logged in")

    def on_disconnect(self):
        logging.warning('The Digibutter websocket has closed the connection.')
        print('\n> The Digibutter websocket has closed the connection.')

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
            print('\n> Index successfully parsed')
        except:
            logging.error('Failed to parse index')
            print('\n> ERROR: Failed to parse index')
            index = None
            latest_post = None
            id = None
            room_id = None
            content = None
            post_type = None
        response_type = do_logic(content)
        if response_type == "about_message":
            Digibutter.responses.about_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "help_message":
            Digibutter.responses.help_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "not_implemented_yet_message":
            Digibutter.responses.not_implemented_yet_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "discord_only_message":
            Digibutter.responses.discord_only_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "help_roll_message":
            Digibutter.responses.help_roll_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "help_echo_message":
            Digibutter.responses.help_echo_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "roll_message":
            Digibutter.responses.roll_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "echo_message":
            Digibutter.responses.echo_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "not_recognized_message":
            Digibutter.responses.not_recognized_message(Digibutter, latest_post, id, room_id, content, post_type)

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
            print('\n> Index successfully parsed')
        except:
            logging.error('Failed to parse index')
            print('\n> ERROR: Failed to parse index')
            index = None
            latest_post = None
            id = None
            room_id = None
            content = None
            post_type = None
        response_type = do_logic(content)
        if response_type == "about_message":
            Digibutter.responses.about_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "help_message":
            Digibutter.responses.help_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "not_implemented_yet_message":
            Digibutter.responses.not_implemented_yet_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "discord_only_message":
            Digibutter.responses.discord_only_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "help_roll_message":
            Digibutter.responses.help_roll_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "help_echo_message":
            Digibutter.responses.help_echo_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "roll_message":
            Digibutter.responses.roll_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "echo_message":
            Digibutter.responses.echo_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "not_recognized_message":
            Digibutter.responses.not_recognized_message(Digibutter, latest_post, id, room_id, content, post_type)

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
            print('\n> Index successfully parsed')
        except:
            logging.error('Failed to parse index')
            print('\n> ERROR: Failed to parse index')
            index = None
            latest_post = None
            id = None
            room_id = None
            content = None
            post_type = None
        response_type = do_logic(content)
        if response_type == "about_message":
            Digibutter.responses.about_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "help_message":
            Digibutter.responses.help_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "not_implemented_yet_message":
            Digibutter.responses.not_implemented_yet_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "discord_only_message":
            Digibutter.responses.discord_only_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "help_roll_message":
            Digibutter.responses.help_roll_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "help_echo_message":
            Digibutter.responses.help_echo_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "roll_message":
            Digibutter.responses.roll_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "echo_message":
            Digibutter.responses.echo_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "not_recognized_message":
            Digibutter.responses.not_recognized_message(Digibutter, latest_post, id, room_id, content, post_type)

    def on_NerrChat_chatlog_response(self):
        print('\n> Received chatlog for "NerrChat"')
        print('\n> Parsing index...')
        try:
            index = json5.loads(str(self))
            latest_post = index['posts'][0]
            id = index['posts'][0]['_id']
            room_id = 'sidebar'
            content = index['posts'][0]['content']
            post_type = 'chat'
            print('\n> Index successfully parsed')
        except:
            logging.error('Failed to parse index')
            print('\n> ERROR: Failed to parse chatlog')
            index = None
            latest_post = None
            id = None
            room_id = None
            content = None
            post_type = None
        response_type = do_logic(content)
        if response_type == "about_message":
            Digibutter.responses.about_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "help_message":
            Digibutter.responses.help_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "not_implemented_yet_message":
            Digibutter.responses.not_implemented_yet_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "discord_only_message":
            Digibutter.responses.discord_only_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "help_roll_message":
            Digibutter.responses.help_roll_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "help_echo_message":
            Digibutter.responses.help_echo_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "roll_message":
            Digibutter.responses.roll_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "echo_message":
            Digibutter.responses.echo_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "not_recognized_message":
            Digibutter.responses.not_recognized_message(Digibutter, latest_post, id, room_id, content, post_type)

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
            print('    ' + content)
        except:
            logging.error('Failed to parse post content')
            print('\n> ERROR: Failed to parse post content')
            latest_post = None
            id = None
            room_id = None
            content = None
            post_type = None
        response_type = do_logic(content)
        if response_type == "about_message":
            Digibutter.responses.about_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "help_message":
            Digibutter.responses.help_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "not_implemented_yet_message":
            Digibutter.responses.not_implemented_yet_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "discord_only_message":
            Digibutter.responses.discord_only_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "help_roll_message":
            Digibutter.responses.help_roll_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "help_echo_message":
            Digibutter.responses.help_echo_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "roll_message":
            Digibutter.responses.roll_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "echo_message":
            Digibutter.responses.echo_message(Digibutter, latest_post, id, room_id, content, post_type)
        elif response_type == "not_recognized_message":
            Digibutter.responses.not_recognized_message(Digibutter, latest_post, id, room_id, content, post_type)

    def authenticate(self):
        logging.info("Attempting to login...")
        print("\n> Attempting to login...")
        sio.emit("ready", Digibutter.on_authentication(BaseNamespace))

    # NerrBot: ReHatched's code to respond to specific commands
    class responses:
        """
        NerrBot: ReHatched's code to respond to specific commands
        """
        def about_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts the about message to the latest topic in the current room
            """
            reply_text = "--NerrBot: Rehatched--\nVersion: 0.1 Alpha\nUptime: %s\n\nEnter '!rh <command>' to execute a command, or '!rh help' for help.\nNerrBot: ReHatched is based on NerrBot by Gold Prognosticus" % counter.count
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def roll_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts the dice roll message to the latest topic in the current room
            """
            reply_text = "You rolled a %s!" % dice.default_roll
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
            Posts an echo of whatever the user posted after the command to the latest topic in the current room
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

        def help_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts the help message to the latest topic in the current room
            """
            reply_text = "Available commands are: yesno, rate, roll, online, echo, time, tictactoe, flip\nEnter '!rh help <command>' to learn more."
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
            Posts the roll command help message to the latest topic in the current room
            """
            reply_text = "roll <sides> - Roll a random dice, with an optional number of sides (default is six) (currently only the default number of sides is supported)."
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
            Posts the echo command help message to the latest topic in the current room
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

        def discord_only_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts the Discord pnly command message to the latest topic in the current room
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

        def not_implemented_yet_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts the not implemented yet message to the latest topic in the current room
            """
            reply_text = "I'm sorry, but this command has not been programmed back into my robot brain yet."
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
            Posts the command not recognized message to the latest topic in the current room
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
sio.wait()
