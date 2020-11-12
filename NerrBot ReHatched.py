import colorama
colorama.init()

print(colorama.Fore.GREEN + "====================================================NerrBot: RH v0.2====================================================" + colorama.Fore.LIGHTBLUE_EX + """


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

from utilities import counter, dice, yesno

# Logging Configuration
logging.basicConfig(format = "%(asctime)s: %(levelname)s: %(name)s: %(message)s", datefmt='%m/%d/%Y %H:%M:%S', filename='NerrBot RH.log', filemode='w', level = logging.DEBUG)

class Digibutter(BaseNamespace):
    """
    Digibutter Socket.io Event Definitions
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
        sio.emit("posts:create", {"content":"Ready.","post_type":"","roomId":"sidebar","source":"db"})

    def on_authentication(self):
        logging.info("Successfully logged in")
        print("\n> Successfully logged in")

    def on_disconnect(self):
        logging.warning('The Digibutter websocket has closed the connection.')
        print('\n> The Digibutter websocket has closed the connection.')

    def on_reconnect(self):
        logging.warning('Reconnected to the Digibutter websocket.')
        print('\n> Reconnected to the Digibutter websocket.')
        sio.emit("posts:create", {"content":"I disconnected unexpectedly there, sorry!","post_type":"","roomId":"sidebar","source":"db"})

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
        Digibutter.do_logic(Digibutter, latest_post, id, room_id, content, post_type)

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
            print('    ' + content)
        except:
            logging.error('Failed to parse post content')
            print('\n> ERROR: Failed to parse post content')
            latest_post = None
            id = None
            room_id = None
            content = None
            post_type = None
        Digibutter.do_logic(Digibutter, latest_post, id, room_id, content, post_type)

    def authenticate(self):
        logging.info("Attempting to login...")
        print("\n> Attempting to login...")
        sio.emit("ready", Digibutter.on_authentication(BaseNamespace))

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
                    Digibutter.responses.not_implemented_yet_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content == "!rh help chat":
                    Digibutter.responses.discord_only_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content == "!rh help relay":
                    Digibutter.responses.discord_only_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content == "!rh help roll":
                    Digibutter.responses.help_roll_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content == "!rh help autorelay":
                    Digibutter.responses.discord_only_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content == "!rh help online":
                    Digibutter.responses.not_implemented_yet_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content == "!rh help echo":
                    Digibutter.responses.help_echo_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content == "!rh help time":
                    Digibutter.responses.not_implemented_yet_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content == "!rh help tictactoe":
                    Digibutter.responses.not_implemented_yet_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content == "!rh help flip":
                    Digibutter.responses.not_implemented_yet_message(Digibutter, latest_post, id, room_id, content, post_type)
            elif content[0:9] == "!rh yesno":
                Digibutter.responses.yesno_message(Digibutter, latest_post, id, room_id, content, post_type)
            elif content[0:8] == "!rh roll":
                if content == "!rh roll":
                    Digibutter.responses.default_roll_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content[0:9] == "!rh roll ":
                    try:
                        max_value = int(content[9:])
                        Digibutter.responses.custom_roll_message(Digibutter, latest_post, id, room_id, content, post_type, max_value)
                    except ValueError:
                        max_value = content[9:]
                        Digibutter.responses.roll_NaN_error_message(Digibutter, latest_post, id, room_id, content, post_type, max_value)
            elif content[0:8] == "!rh echo":
                if content == "!rh echo":
                    Digibutter.responses.specify_echo_message(Digibutter, latest_post, id, room_id, content, post_type)
                elif content[0:] == "!rh echo !rh echo":
                    Digibutter.responses.wise_guy_echo_message(Digibutter, latest_post, id, room_id, content, post_type)
                else:
                    Digibutter.responses.echo_message(Digibutter, latest_post, id, room_id, content, post_type)
            else:
                Digibutter.responses.not_recognized_message(Digibutter, latest_post, id, room_id, content, post_type)

    # NerrBot: ReHatched's code to respond to specific commands
    class responses:
        """
        NerrBot: ReHatched's code to respond to specific commands
        """
        def about_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts the about message as a reply to the latest message in the current room
            """
            reply_text = "--NerrBot: ReHatched--\nVersion: 0.1 Alpha\nUptime: %s\n\nEnter '!rh <command>' to execute a command, or '!rh help' for help.\nNerrBot: ReHatched is based on NerrBot by Gold Prognosticus.\nNerrBot: ReHatched was created by and is maintained by TheEvilShadoo." % counter.count
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

        def help_yesno_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts the help message for the yesno command as a reply to the latest topic in the current room
            """
            reply_text = "yesno <question> - Ask NerrBot: ReHatched a question and he will respond with either yes or no."
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

        def not_implemented_yet_message(self, latest_post, id, room_id, content, post_type):
            """
            Posts the not implemented yet message as a reply to the latest message in the current room
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
            Posts either "yes" or "no" randomly in response to the the latest message in the current room
            """
            reply_text = "%s" % yesno.random_odds()
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
            reply_text = "You rolled a %s!" % dice.default_roll()
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def custom_roll_message(self, latest_post, id, room_id, content, post_type, max_value):
            """
            Posts the custom dice roll message as a reply to the latest message in the current room
            """
            reply_text = "You rolled a %s!" % dice.custom_roll(max_value)
            if '"reply_to":{"replies":' in latest_post:
                type = "reply"
            else:
                type = "post"
            logging.info('Replying to %s with content: "%s"' % (type, content))
            print('\n> Replying to %s with content: "%s"' % (type, content))
            sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
            logging.info("Message was sent successfully")
            print("\n> Message was sent successfully")

        def roll_NaN_error_message(Digibutter, latest_post, id, room_id, content, post_type, max_value):
            """
            Posts a NaN error message as a reply to the latest topic in the current room
            """
            reply_text = f'"{max_value}" is not a number.'
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
sio.wait()
