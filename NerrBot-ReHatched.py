#!/usr/bin/env python3

import colorama
colorama.init()

version = "1.4.0 - Nerr 4.0 Soon Edition"

print(colorama.Fore.GREEN + f"====================================================NerrBot: RH v{version}====================================================" + colorama.Fore.LIGHTBLUE_EX + """


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

from contextlib import contextmanager
import counter
from datetime import datetime, timedelta, timezone
import json
import json5
import logging
from lxml import html
import os
import pytz
import random
import re
import requests
from socketIO_client import SocketIO, BaseNamespace
import sys
import threading
import time

# Context manager method declarations
@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout

# Logging configuration
logging.basicConfig(format = "%(asctime)s: %(levelname)s: %(name)s: %(message)s", datefmt='%m/%d/%Y %H:%M:%S', filename='NerrBot-ReHatched.log', filemode='w', level = logging.INFO)

# Check for email and password environment variables
try:
    email = os.environ.get("NB_email")
except:
    try:
        password = os.environ.get("NB_password")
    except:
        sys.exit(colorama.Fore.LIGHTRED_EX + "ERROR: The system environment variables for both keys '" + colorama.Fore.LIGHTWHITE_EX + "NB_email" + colorama.Fore.LIGHTRED_EX + "' and '" + colorama.Fore.LIGHTWHITE_EX + "NB_password" + colorama.Fore.LIGHTRED_EX + "' are unset. Please set these before attempting to run NerrBot: ReHatched again." + colorama.Fore.RESET)
    sys.exit(colorama.Fore.LIGHTRED_EX + "ERROR: The system environment variable for key '" + colorama.Fore.LIGHTWHITE_EX + "NB_email" + colorama.Fore.LIGHTRED_EX + "' is unset. Please set this before attempting to run NerrBot: ReHatched again." + colorama.Fore.RESET)
try:
    password = os.environ.get("NB_password")
except:
    sys.exit(colorama.Fore.LIGHTRED_EX + "ERROR: The system environment variable for key '" + colorama.Fore.LIGHTWHITE_EX + "NB_password" + colorama.Fore.LIGHTRED_EX + "' is unset. Please set this before attempting to run NerrBot: ReHatched again." + colorama.Fore.RESET)

def get_cookie():
    """
    Logs into digibutter as NerrBot: ReHatched and retrieves a session cookie good for at least six weeks
    """
    global email, password
    session = requests.Session()
    response = session.get("http://digibutter.nerr.biz/login")
    tree = html.fromstring(response.content)
    csrf = (tree.xpath("//input[@name='_csrf']"))[0].attrib["value"]

    payload = {
        "email": email,
        "password": password,
        "_csrf": csrf
    }

    response = session.post("http://digibutter.nerr.biz/users/session", data=payload)
    cookie = session.cookies.get_dict()["nerr3"]
    return cookie

def write_json(data, filename):
    """
    JSON Writing Function
    """
    with open (filename, "w") as file:
        json.dump(data, file, indent=4)

class Digibutter(BaseNamespace):
    # Define class variables
    online_user_list = []

    # Digibutter Socket.io event definitions
    def on_connect(self):
        logging.info("A connection with the Digibutter websocket has been established.")
        print(colorama.Fore.WHITE + "\n> " + colorama.Fore.LIGHTCYAN_EX + "A connection with the Digibutter websocket has been established." + colorama.Fore.RESET)
        logging.info("Attempting to login...")
        print(colorama.Fore.WHITE + "\n> " + colorama.Fore.LIGHTYELLOW_EX + "Attempting to login..." + colorama.Fore.RESET)
        sio.emit("ready", Digibutter.on_authentication(BaseNamespace))
        sio.wait(.2)
        sio.emit("posts:index", {"topic": False, "room": "db", "topicsOnly": False, "source": "db"}, Digibutter.on_all_posts_index_response)
        sio.wait(.2)
        sio.emit("posts:index", {"topic": False, "room": "nf", "topicsOnly": False, "source": "db"}, Digibutter.on_gaming_news_index_response)
        sio.wait(.2)
        sio.emit("posts:index", {"topic": False, "room": "sidebar", "topicsOnly": False, "source": "db"}, Digibutter.on_the_dump_index_response)
        sio.wait(.2)
        sio.emit("posts:chats", {"room": "sidebar"}, Digibutter.on_NerrChat_chatlog_response)
        counter_thread = threading.Thread(target=counter.counter)
        counter_thread.start()
        sio.wait(.2)
        sio.emit("posts:create", {"content":f"color=red: NerrBot System v{version} Online","post_type":"","roomId":"sidebar","source":"db"})

    def on_authentication(self):
        logging.info("Successfully logged in")
        print(colorama.Fore.WHITE + "\n> " + colorama.Fore.LIGHTGREEN_EX + "Successfully logged in" + colorama.Fore.RESET)

    def on_disconnect(self):
        logging.warning("The Digibutter websocket has closed the connection.")
        print(colorama.Fore.WHITE + "\n> " + colorama.Fore.LIGHTRED_EX + "The Digibutter websocket has closed the connection." + colorama.Fore.RESET)

    def on_reconnect(self):
        logging.info("Reconnected to the Digibutter websocket.")
        print(colorama.Fore.WHITE + "\n> " + colorama.Fore.LIGHTCYAN_EX + "Reconnected to the Digibutter websocket." + colorama.Fore.RESET)
        logging.info("Attempting to login...")
        print(colorama.Fore.WHITE + "\n> " + colorama.Fore.LIGHTYELLOW_EX + "Attempting to login..." + colorama.Fore.RESET)
        sio.emit("ready", Digibutter.on_authentication(BaseNamespace))
        sio.wait(.2)
        sio.emit("posts:index", {"topic": False, "room": "db", "topicsOnly": False, "source": "db"}, Digibutter.on_all_posts_index_response)
        sio.wait(.2)
        sio.emit("posts:index", {"topic": False, "room": "nf", "topicsOnly": False, "source": "db"}, Digibutter.on_gaming_news_index_response)
        sio.wait(.2)
        sio.emit("posts:index", {"topic": False, "room": "sidebar", "topicsOnly": False, "source": "db"}, Digibutter.on_the_dump_index_response)
        sio.wait(.2)
        sio.emit("posts:chats", {"room": "sidebar"}, Digibutter.on_NerrChat_chatlog_response)
        sio.wait(.2)
        sio.emit("posts:create", {"content":f"color=red: NerrBot System v{version} Online","post_type":"","roomId":"sidebar","source":"db"})

    def on_all_posts_index_response(self):
        print(colorama.Fore.WHITE + "\n> " + colorama.Fore.BLUE + "Received posts index for room " + colorama.Fore.LIGHTWHITE_EX + "All Posts" + colorama.Fore.RESET)
        print(colorama.Fore.WHITE + "\n> " + colorama.Fore.BLUE + "Parsing index..." + colorama.Fore.RESET)
        all_posts_index = json5.loads(str(self))
        latest_post = all_posts_index['posts'][0]
        post_id = all_posts_index['posts'][0]['_id']
        room_id = 'db'
        content = all_posts_index['posts'][0]['content']
        post_type = ''
        username = all_posts_index['posts'][0]['user']['name']
        try:
            user_id = all_posts_index['posts'][0]['user']['id']
        except:
            user_id = all_posts_index['posts'][0]['user']['anon']
            username += " (anon)"
        else:
            Digibutter.record_user(Digibutter, username, user_id)
        logging.info("'All Posts' index successfully parsed")
        print(colorama.Fore.WHITE + "\n> " + colorama.Fore.LIGHTWHITE_EX + "All Posts" + colorama.Fore.GREEN + " index successfully parsed" + colorama.Fore.RESET)
        Digibutter.do_logic(Digibutter, latest_post, post_id, room_id, content, post_type, username, user_id)

    def on_gaming_news_index_response(self):
        print(colorama.Fore.WHITE + "\n> " + colorama.Fore.BLUE + "Received posts index for room " + colorama.Fore.LIGHTWHITE_EX + "Gaming News" + colorama.Fore.RESET)
        print(colorama.Fore.WHITE + "\n> " + colorama.Fore.BLUE + "Parsing index..." + colorama.Fore.RESET)
        gaming_news_index = json5.loads(str(self))
        latest_post = gaming_news_index['posts'][0]
        post_id = gaming_news_index['posts'][0]['_id']
        room_id = 'nf'
        content = gaming_news_index['posts'][0]['content']
        post_type = ''
        username = gaming_news_index['posts'][0]['user']['name']
        try:
            user_id = gaming_news_index['posts'][0]['user']['id']
        except:
            user_id = gaming_news_index['posts'][0]['user']['anon']
            username += " (anon)"
        else:
            Digibutter.record_user(Digibutter, username, user_id)
        logging.info("'Gaming News' index successfully parsed")
        print(colorama.Fore.WHITE + "\n> " + colorama.Fore.LIGHTWHITE_EX + "Gaming News" + colorama.Fore.GREEN + " index successfully parsed" + colorama.Fore.RESET)
        Digibutter.do_logic(Digibutter, latest_post, post_id, room_id, content, post_type, username, user_id)

    def on_the_dump_index_response(self):
        print(colorama.Fore.WHITE + "\n> " + colorama.Fore.BLUE + "Received posts index for room " + colorama.Fore.LIGHTWHITE_EX + "The Dump" + colorama.Fore.RESET)
        print(colorama.Fore.WHITE + "\n> " + colorama.Fore.BLUE + "Parsing index..." + colorama.Fore.RESET)
        the_dump_index = json5.loads(str(self))
        latest_post = the_dump_index['posts'][0]
        post_id = the_dump_index['posts'][0]['_id']
        room_id = 'sidebar'
        content = the_dump_index['posts'][0]['content']
        post_type = ''
        username = the_dump_index['posts'][0]['user']['name']
        try:
            user_id = the_dump_index['posts'][0]['user']['id']
        except:
            user_id = the_dump_index['posts'][0]['user']['anon']
            username += " (anon)"
        else:
            Digibutter.record_user(Digibutter, username, user_id)
        logging.info("'The Dump' index successfully parsed")
        print(colorama.Fore.WHITE + "\n> " + colorama.Fore.LIGHTWHITE_EX + "The Dump" + colorama.Fore.GREEN + " index successfully parsed" + colorama.Fore.RESET)
        Digibutter.do_logic(Digibutter, latest_post, post_id, room_id, content, post_type, username, user_id)

    def on_NerrChat_chatlog_response(self):
        print(colorama.Fore.WHITE + "\n> " + colorama.Fore.BLUE + "Received index for " + colorama.Fore.LIGHTWHITE_EX + "NerrChat" + colorama.Fore.RESET)
        print(colorama.Fore.WHITE + "\n> " + colorama.Fore.BLUE + "Parsing index..." + colorama.Fore.RESET)
        NerrChat_index = json5.loads(str(self))
        latest_post = NerrChat_index['posts'][0]
        post_id = NerrChat_index['posts'][0]['_id']
        room_id = 'sidebar'
        content = NerrChat_index['posts'][0]['content']
        post_type = 'chat'
        username = NerrChat_index['posts'][0]['user']['name']
        try:
            user_id = NerrChat_index['posts'][0]['user']['id']
        except:
            user_id = NerrChat_index['posts'][0]['user']['anon']
            username += " (anon)"
        else:
            Digibutter.record_user(Digibutter, username, user_id)
        logging.info("'NerrChat' index successfully parsed")
        print(colorama.Fore.WHITE + "\n> " + colorama.Fore.LIGHTWHITE_EX + "NerrChat" + colorama.Fore.GREEN + " index successfully parsed" + colorama.Fore.RESET)
        Digibutter.do_logic(Digibutter, latest_post, post_id, room_id, content, post_type, username, user_id)

    def on_new_post(self):
        latest_post = json5.loads(str(self))
        post_id = latest_post['_id']
        if "'id': 'sidebar'" in str(latest_post):
            room_id = 'sidebar'
        elif "'id': 'nf'" in str(latest_post):
            room_id = 'nf'
        else:
            room_id = 'db'
        content = latest_post['content']
        post_type = latest_post['post_type']
        username = latest_post['user']['name']
        try:
            user_id = latest_post['user']['id']
        except:
            user_id = latest_post['user']['anon']
            username += " (anon)"
        else:
            Digibutter.record_user(Digibutter, username, user_id)
        if post_type == "like1":
            original_post_content = latest_post['reply_to']['content']
            original_poster = latest_post['reply_to']['user']['name']
            logging.info(f"{username} liked {original_poster}'s post:\n{original_post_content}")
            print(colorama.Fore.WHITE + "\n> " + colorama.Fore.LIGHTWHITE_EX + f"{username}" + colorama.Fore.RED + " liked " + colorama.Fore.LIGHTWHITE_EX + f"{original_poster}" + colorama.Fore.RED + "'s post:\n" + colorama.Fore.RESET + f"{original_post_content}")
        elif post_type == "like2":
            original_post_content = latest_post['reply_to']['content']
            original_poster = latest_post['reply_to']['user']['name']
            logging.info(f"{username} disliked {original_poster}'s post:\n{original_post_content}")
            print(colorama.Fore.WHITE + "\n> " + colorama.Fore.LIGHTWHITE_EX + f"{username}" + colorama.Fore.MAGENTA + " disliked " + colorama.Fore.LIGHTWHITE_EX + f"{original_poster}" + colorama.Fore.MAGENTA + "'s post:\n" + colorama.Fore.RESET + f"{original_post_content}")
        else:
            logging.info(f"Received a new post from {username}:\n{content}")
            print(colorama.Fore.WHITE + "\n> " + colorama.Fore.GREEN + "Received a new post from " + colorama.Fore.LIGHTWHITE_EX + f"{username}" + colorama.Fore.GREEN + ":\n" + colorama.Fore.RESET + f"{content}")
            Digibutter.do_logic(Digibutter, latest_post, post_id, room_id, content, post_type, username, user_id)

    def on_userupdate(self):
        online_user_index = self
        Digibutter.online_user_list = []
        for user in online_user_index:
            Digibutter.online_user_list.append(user["name"])

    def record_user(self, username, user_id):
        """
        Whenever a new user posts a message, this records their username and user_id into users.json
        """
        with open("users.json", "r") as users:
            data = json.load(users)
        for user in data["users"]:
            if user["username"] == username:
                break
        else:
            user = {"username": username, "user_id": user_id}
            data["users"].append(user)
            write_json(data, filename="users.json")

    class tictactoe:
        """
        Tictactoe data subclass
        """
        player = None
        turn = None
        player_symbol = None
        NerrBot_symbol = None
        values = ["".ljust(3) for x in range(9)]
        tictactoe_board = "             |             |             \n     %s     |     %s     |     %s     \n_             |             |             _\n             |             |             \n     %s     |     %s     |     %s     \n_             |             |             _\n             |             |             \n     %s     |     %s     |     %s     \n             |             |" % (values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8])
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

        def find_NerrBot_move(self):
            possible_moves = [x for x, letter in enumerate(Digibutter.tictactoe.values) if letter == "".ljust(3)]
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
            return (values[0] == symbol and values[1] == symbol and values[2] == symbol
            or values[3] == symbol and values[4] == symbol and values[5] == symbol
            or values[6] == symbol and values[7] == symbol and values[8] == symbol
            or values[0] == symbol and values[3] == symbol and values[6] == symbol
            or values[1] == symbol and values[4] == symbol and values[7] == symbol
            or values[2] == symbol and values[5] == symbol and values[8] == symbol
            or values[0] == symbol and values[4] == symbol and values[8] == symbol
            or values[2] == symbol and values[4] == symbol and values[6] == symbol)

        def is_board_full(self, values):
            if Digibutter.tictactoe.values.count("".ljust(3)) > 0:
                return False
            else:
                return True

    class timer:
        """
        Timer data subclass
        """
        username = None
        user_id = None
        title = None
        months = None
        weeks = None
        days = None
        hours = None
        minutes = None
        seconds = None
        start = None
        end = None
        total_seconds = None

        def reset():
            """
            Resets the values in the timer class
            """
            Digibutter.timer.username = None
            Digibutter.timer.user_id = None
            Digibutter.timer.title = None
            Digibutter.timer.months = None
            Digibutter.timer.weeks = None
            Digibutter.timer.days = None
            Digibutter.timer.hours = None
            Digibutter.timer.minutes = None
            Digibutter.timer.seconds = None
            Digibutter.timer.start = None
            Digibutter.timer.end = None
            Digibutter.timer.total_seconds = None

        def alert(username, user_id, title, months, weeks, days, hours, minutes, seconds):
            """
            Function to be called upon a user-defined timer ending. Removes the timer's entry in timers.json, and posts the timer_alert_message.
            """
            with open("timers.json", "r") as timers:
                data = json.load(timers)
            for timer in range(len(data)):
                if data[timer]["user_id"] == user_id and data[timer]["title"] == title:
                    data.pop(timer)
                    write_json(data, filename="timers.json")
                    break
            logging.info(f"Posting timer alert for {username}'s timer, '{title}'")
            print(colorama.Fore.WHITE + "\n> " + colorama.Fore.YELLOW + "Posting timer alert for " + colorama.Fore.LIGHTWHITE_EX + f"{username}" + colorama.Fore.YELLOW + "'s timer, '" + colorama.Fore.LIGHTWHITE_EX + f"{title}" + colorama.Fore.YELLOW + "'" + colorama.Fore.RESET)
            sio.emit("posts:create", {"content":f"color=red: **Beep! Beep! Beep!**\n\n**{username},** your timer, \"{title},\" has just ended! It has been {months} months, {weeks} weeks, {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds since you set this timer, nerr.","post_type":"","roomId":"sidebar","source":"db"})
            logging.info("Post was created successfully")
            print(colorama.Fore.WHITE + "\n> " + colorama.Fore.CYAN + "Post was created successfully" + colorama.Fore.RESET)

        def scrape_data(content):
            """
            Scrapes the data for the timer to be created
            """
            datetitle = content[14:]
            try:
                M = re.search("[0-9]*\[M\]", datetitle)
                Digibutter.timer.months = int(re.findall(r'\d+', M.group())[0])
            except:
                Digibutter.timer.months = 0
            try:
                W = re.search("[0-9]*\[W\]", datetitle)
                Digibutter.timer.weeks = int(re.findall(r'\d+', W.group())[0])
            except:
                Digibutter.timer.weeks = 0
            try:
                D = re.search("[0-9]*\[D\]", datetitle)
                Digibutter.timer.days = int(re.findall(r'\d+', D.group())[0])
            except:
                Digibutter.timer.days = 0
            try:
                h = re.search("[0-9]*\[h\]", datetitle)
                Digibutter.timer.hours = int(re.findall(r'\d+', h.group())[0])
            except:
                Digibutter.timer.hours = 0
            try:
                m = re.search("[0-9]*\[m\]", datetitle)
                Digibutter.timer.minutes = int(re.findall(r'\d+', m.group())[0])
            except:
                Digibutter.timer.minutes = 0
            try:
                s = re.search("[0-9]*\[s\]", datetitle)
                Digibutter.timer.seconds = int(re.findall(r'\d+', s.group())[0])
            except:
                Digibutter.timer.seconds = 0

            Digibutter.timer.title = datetitle[datetitle.rindex(']')+2:]
            
            Digibutter.timer.total_seconds = Digibutter.timer.months * 2629800 + Digibutter.timer.weeks * 604800 + Digibutter.timer.days * 86400 + Digibutter.timer.hours * 3600 + Digibutter.timer.minutes * 60 + Digibutter.timer.seconds
            start = datetime.now(timezone.utc)
            Digibutter.timer.start = start.strftime("%Y-%m-%d %H:%M:%S %Z")
            Digibutter.timer.end = (start + timedelta(seconds=Digibutter.timer.total_seconds)).strftime("%Y-%m-%d %H:%M:%S %Z")

    def do_logic(self, latest_post, post_id, room_id, content, post_type, username, user_id):
        """
        Determines the response message that NerrBot: ReHatched should reply with and posts the response message as a reply to the latest message in the current room
        """

        if content[0:3] == "!rh":
            if content == "!rh":
                Digibutter.responses.about_message(Digibutter, latest_post, post_id, room_id, content, post_type)
            elif content[0:8] == "!rh help":
                if content == "!rh help":
                    Digibutter.responses.help_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                elif content == "!rh help yesno":
                    Digibutter.responses.help_yesno_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                elif content == "!rh help rate":
                    Digibutter.responses.help_rate_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                elif content == "!rh help discord":
                    Digibutter.responses.help_discord_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                elif content == "!rh help chat":
                    Digibutter.responses.discord_only_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                elif content == "!rh help relay":
                    Digibutter.responses.discord_only_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                elif content == "!rh help roll":
                    Digibutter.responses.help_roll_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                elif content == "!rh help autorelay":
                    Digibutter.responses.discord_only_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                elif content == "!rh help online":
                    Digibutter.responses.help_online_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                elif content == "!rh help echo":
                    Digibutter.responses.help_echo_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                elif content == "!rh help time":
                    Digibutter.responses.help_time_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                elif content == "!rh help tictactoe":
                    Digibutter.responses.help_tictactoe_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                elif content == "!rh help flip":
                    Digibutter.responses.help_flip_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                elif content == "!rh help xkcd":
                    Digibutter.responses.help_xkcd_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                elif content == "!rh help timer":
                    Digibutter.responses.help_timer_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                else:
                    Digibutter.responses.not_recognized_message(Digibutter, latest_post, post_id, room_id, content, post_type)
            elif content[0:9] == "!rh yesno":
                if content == "!rh yesno":
                    Digibutter.responses.specify_yesno_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                elif content[0:10] == "!rh yesno ":
                    Digibutter.responses.yesno_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                else:
                    Digibutter.responses.not_recognized_message(Digibutter, latest_post, post_id, room_id, content, post_type)
            elif content[0:8] == "!rh rate":
                if content == "!rh rate":
                    Digibutter.responses.specify_rate_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                elif content[0:9] == "!rh rate ":
                    Digibutter.responses.rate_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                else:
                    Digibutter.responses.not_recognized_message(Digibutter, latest_post, post_id, room_id, content, post_type)
            elif content == "!rh discord":
                Digibutter.responses.discord_message(Digibutter, latest_post, post_id, room_id, content, post_type)
            elif content[0:8] == "!rh roll":
                if content == "!rh roll":
                    Digibutter.responses.default_roll_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                elif content[0:9] == "!rh roll ":
                    Digibutter.responses.custom_roll_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                else:
                    Digibutter.responses.not_recognized_message(Digibutter, latest_post, post_id, room_id, content, post_type)
            elif content == "!rh online":
                Digibutter.responses.online_message(Digibutter, latest_post, post_id, room_id, content, post_type)
            elif content[0:8] == "!rh echo":
                if content == "!rh echo":
                    Digibutter.responses.specify_echo_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                elif "!rh echo !rh echo" in content:
                    Digibutter.responses.wise_guy_echo_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                elif content[0:9] == "!rh echo ":
                    Digibutter.responses.echo_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                else:
                    Digibutter.responses.not_recognized_message(Digibutter, latest_post, post_id, room_id, content, post_type)
            elif content[0:8] == "!rh time":
                if content == "!rh time":
                    Digibutter.responses.time_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                elif content[0:9] == "!rh time ":
                    Digibutter.responses.time_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                else:
                    if content == "!rh timer":
                        Digibutter.responses.timer_specify_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                    elif content[0:14] == "!rh timer set ":
                        Digibutter.responses.timer_set_message(Digibutter, latest_post, post_id, room_id, content, post_type, username, user_id)
                    elif content[0:17] == "!rh timer delete ":
                        Digibutter.responses.timer_delete_message(Digibutter, latest_post, post_id, room_id, content, post_type, username, user_id)
                    elif content == "!rh timer list":
                        Digibutter.responses.timer_list_message(Digibutter, latest_post, post_id, room_id, content, post_type, username, user_id)
                    elif content == "!rh timer help":
                        Digibutter.responses.timer_help_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                    else:
                        Digibutter.responses.not_recognized_message(Digibutter, latest_post, post_id, room_id, content, post_type)  
            elif content[0:13] == "!rh tictactoe":
                if content == "!rh tictactoe":
                    Digibutter.responses.tictactoe_specify_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                elif content == "!rh tictactoe new":
                    Digibutter.responses.new_tictactoe_message(Digibutter, latest_post, post_id, room_id, content, post_type, username)
                elif content == "!rh tictactoe display":
                    Digibutter.responses.display_ticactoe_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                elif content == "!rh tictactoe help":
                    Digibutter.responses.tictactoe_help_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                elif content[0:14] == "!rh tictactoe ":
                    Digibutter.responses.tictactoe_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                else:
                    Digibutter.responses.not_recognized_message(Digibutter, latest_post, post_id, room_id, content, post_type)
            elif content[0:8] == "!rh flip":
                if content == "!rh flip":
                    Digibutter.responses.default_flip_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                elif content[0:9] == "!rh flip ":
                    Digibutter.responses.custom_flip_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                else:
                    Digibutter.responses.not_recognized_message(Digibutter, latest_post, post_id, room_id, content, post_type)
            elif content == "!rh xkcd":
                Digibutter.responses.latest_xkcd_comic_message(Digibutter, latest_post, post_id, room_id, content, post_type) 
            elif content[0:35] == "spoiler: !rh disconnect unexpectedly":
                if content == "!rh disconnect unexpectedly" or content == "spoiler !rh disconnect unexpectedly":
                    Digibutter.responses.disconnect_unexpectedly_specify_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                elif content == "spoiler: !rh disconnect unexpectedly -left 2323 -right 2828" or content == "spoiler: !rh disconnect unexpectedly -right 2828 -left 2323":
                    Digibutter.responses.disconnect_unexpectedly_accept_message(Digibutter, latest_post, post_id, room_id, content, post_type)
                else:
                    Digibutter.responses.disconnect_unexpectedly_deny_message(Digibutter, latest_post, post_id, room_id, content, post_type)
            else:
                Digibutter.responses.not_recognized_message(Digibutter, latest_post, post_id, room_id, content, post_type)

    class responses:
        """
        NerrBot: ReHatched's code to respond to specific commands
        """
        def about_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with the about message
            """
            reply_text = f"--NerrBot: ReHatched--\nVersion: {version}\nUptime: %s\n\nEnter \"!rh <command>\" to execute a command, or \"!rh help\" for help.\nNerrBot: ReHatched is based on NerrBot by Gold Prognosticus.\nNerrBot: ReHatched was created by and is maintained by TheEvilShadoo https://www.shadoosite.xyz" % counter.count
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def help_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with the help message
            """
            reply_text = "Available commands are: yesno, rate, roll, online, discord, echo, time, tictactoe, flip, xkcd, timer\nEnter \"!rh help <command>\" to learn more."
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def help_yesno_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with the help message for the yesno command
            """
            reply_text = "yesno <question> - Ask NerrBot: ReHatched a question and he will respond with either yes or no. Some specific questions have predetermined answers."
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def help_rate_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with the help message for the rate command
            """
            reply_text = "rate <something to rate> - Gives a random score out of ten."
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def help_discord_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with the help message for the discord command
            """
            reply_text = "discord - Prints a permanent invite link to the Digibutter Unnoficial Discord server (D.U.D) to the chat."
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def help_roll_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with the help message for the roll command
            """
            reply_text = "roll <sides> - Roll a random dice, with an optional number of sides (default is six)."
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def help_online_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with the help message for the online command
            """
            reply_text = "online - Print a list of the current online users."
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def help_echo_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with the help message for the echo command
            """
            reply_text = "echo <message> - Print a message to the chat."
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def help_time_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with the help message for the time command
            """
            reply_text = "time <timezone> - Print the current UTC date and time. Optionally specify a timezone."
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def help_tictactoe_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with the help message for the tictactoe command
            """
            reply_text = "tictactoe <new/display/help> - Play a game of Tic Tac Toe."
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def help_flip_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with the help message for the flip command
            """
            reply_text = "flip <coins> - Flip a coin or optionally specify a number of coins to flip (default is one)."
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def help_xkcd_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with the help message for the xkcd command
            """
            reply_text = "xkcd - Fetches the latest xkcd comic from https://xkcd.com"
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def help_timer_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with the help message for the timer command
            """
            reply_text = "timer <set/delete/help> - Manage your timers here on digibutter.nerr"

        def discord_only_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with the Discord only command message
            """
            reply_text = "I'm sorry, but this command only worked on the old unofficial Discord server."
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def yesno_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with either "yes" or "no" randomly. Some specific questions have predetermined answers.
            """
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
                reply_text = f"{random.choice(['Yes', 'No'])}"
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def specify_yesno_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Asks for something to respond with yes or no to when not previously specified
            """
            reply_text = "Please specify a question."
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def rate_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with a random score out of ten
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
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def specify_rate_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Asks for something to rate when not previously specified
            """
            reply_text = "Please specify something to rate."
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def discord_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with a permanent invite link to the Digibutter Unnoficial Discord server (D.U.D.)
            """
            reply_text = "Digibutter Unnoficial Discord (D.U.D.) official invite link: https://discord.gg/fRnV3kt"
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def default_roll_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with the default dice roll message
            """
            min_value = 1
            max_value = 6
            roll = random.randint(min_value, max_value)
            reply_text = f"You rolled a {roll}!"
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def custom_roll_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with the custom dice roll message
            """
            min_value = 1
            try:
                max_value = int(content[9:])
            except ValueError:
                max_value = content[9:]
                reply_text = f"\"{max_value}\" is not a number."
                Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)
                return
            roll = random.randint(min_value, max_value)
            reply_text = f"You rolled a {roll}!"
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def online_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with a list of the current online users
            """
            if Digibutter.online_user_list[-1] != "NerrBot: ReHatched":
                try:
                    Digibutter.online_user_list.remove("NerrBot: ReHatched")
                    Digibutter.online_user_list.append("NerrBot: ReHatched")
                except:
                    pass
            online_users = ", ".join(Digibutter.online_user_list)
            reply_text = f"Online users: {online_users}"
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def echo_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with an echo of whatever the user posted after the command
            """
            reply_text = f"{content[9:]}"
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def specify_echo_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Asks for something to echo when not previously specified
            """
            reply_text = "Please specify something to echo."
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def wise_guy_echo_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Prevents Digibutter from being spammed, NerrBot: ReHatched from breaking, and makes fun of the user all at the same time
            """
            reply_text = "Hey, wise guy! Digibutter shall not be spammed on my watch!"
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def time_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with the current date and time in UTC (or an optionally specified timezone)
            """
            try:
                tz = content[9:12]
            except:
                tz = "UTC"
            try:
                reply_text = "The current date and time is: %s" % datetime.now(tz=pytz.timezone(f"{tz}")).strftime(f"%a, %B %-d, %Y at %-I:%M:%S %p {tz}")
            except:
                reply_text = f"\"{tz}\" is not a valid timezone."
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def tictactoe_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with an updated version of the tictactoe board as the game progresses
            """
            if Digibutter.tictactoe.tictactoe_game == None:
                reply_text = "There isn't a tictactoe game taking place currently."
            else:
                try:
                    x_coordinate = int(content[14])
                    y_coordinate = int(content[16])
                    move = Digibutter.tictactoe.find_player_move(Digibutter.tictactoe, x_coordinate, y_coordinate)
                    if move > 0 and move < 10:
                        if Digibutter.tictactoe.values[move - 1] != "".ljust(3):
                            reply_text = "That space is already occupied, try again."
                        else:
                            Digibutter.tictactoe.values[move - 1] = Digibutter.tictactoe.player_symbol
                            Digibutter.tictactoe.tictactoe_board = "             |             |             \n     %s     |     %s     |     %s     \n_             |             |             _\n             |             |             \n     %s     |     %s     |     %s     \n_             |             |             _\n             |             |             \n     %s     |     %s     |     %s     \n             |             |" % (Digibutter.tictactoe.values[0], Digibutter.tictactoe.values[1], Digibutter.tictactoe.values[2], Digibutter.tictactoe.values[3], Digibutter.tictactoe.values[4], Digibutter.tictactoe.values[5], Digibutter.tictactoe.values[6], Digibutter.tictactoe.values[7], Digibutter.tictactoe.values[8])
                            if Digibutter.tictactoe.player_symbol == "O":
                                Digibutter.tictactoe.tictactoe_game = ":%s: Turn %s :NerrBot: Rehatched:\n%s" % (Digibutter.tictactoe.player, Digibutter.tictactoe.turn, Digibutter.tictactoe.tictactoe_board)
                            else:
                                Digibutter.tictactoe.player_symbol = "X"
                                Digibutter.tictactoe.tictactoe_game = ":NerrBot: Rehatched: Turn %s :%s:\n%s" % (Digibutter.tictactoe.turn, Digibutter.tictactoe.player, Digibutter.tictactoe.tictactoe_board)
                            Digibutter.tictactoe.turn += 1
                            if Digibutter.tictactoe.is_winner(Digibutter.tictactoe, Digibutter.tictactoe.values, Digibutter.tictactoe.player_symbol):
                                reply_text = "%s\nscroll=left: **Congratulations, you won!**\nhttps://www.youtube.com/watch?v=FI0v5QY_nKM" % Digibutter.tictactoe.tictactoe_game
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
                                    move = Digibutter.tictactoe.find_NerrBot_move(Digibutter.tictactoe)
                                    if move == 1 or move == 4 or move == 7:
                                        Digibutter.tictactoe.values[move] = "X".ljust(2)
                                    elif move == 2 or move == 3 or move == 5 or move == 6 or move == 7 or move == 8:
                                        Digibutter.tictactoe.values[move] = "X".rjust(2)
                                    Digibutter.tictactoe.tictactoe_board = "             |             |             \n     %s     |     %s     |     %s     \n_             |             |             _\n             |             |             \n     %s     |     %s     |     %s     \n_             |             |             _\n             |             |             \n     %s     |     %s     |     %s     \n             |             |" % (Digibutter.tictactoe.values[0], Digibutter.tictactoe.values[1], Digibutter.tictactoe.values[2], Digibutter.tictactoe.values[3], Digibutter.tictactoe.values[4], Digibutter.tictactoe.values[5], Digibutter.tictactoe.values[6], Digibutter.tictactoe.values[7], Digibutter.tictactoe.values[8])
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
                                    move = Digibutter.tictactoe.find_NerrBot_move(Digibutter.tictactoe)
                                    Digibutter.tictactoe.values[move] = "O"
                                    Digibutter.tictactoe.tictactoe_board = "             |             |             \n     %s     |     %s     |     %s     \n_             |             |             _\n             |             |             \n     %s     |     %s     |     %s     \n_             |             |             _\n             |             |             \n     %s     |     %s     |     %s     \n             |             |" % (Digibutter.tictactoe.values[0], Digibutter.tictactoe.values[1], Digibutter.tictactoe.values[2], Digibutter.tictactoe.values[3], Digibutter.tictactoe.values[4], Digibutter.tictactoe.values[5], Digibutter.tictactoe.values[6], Digibutter.tictactoe.values[7], Digibutter.tictactoe.values[8])
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
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def new_tictactoe_message(self, latest_post, post_id, room_id, content, post_type, username):
            """
            Replies with a new tictactoe board
            """
            Digibutter.tictactoe.values = ["".ljust(3) for x in range(9)]
            Digibutter.tictactoe.tictactoe_board = "             |             |             \n     %s     |     %s     |     %s     \n_             |             |             _\n             |             |             \n     %s     |     %s     |     %s     \n_             |             |             _\n             |             |             \n     %s     |     %s     |     %s     \n             |             |" % (Digibutter.tictactoe.values[0], Digibutter.tictactoe.values[1], Digibutter.tictactoe.values[2], Digibutter.tictactoe.values[3], Digibutter.tictactoe.values[4], Digibutter.tictactoe.values[5], Digibutter.tictactoe.values[6], Digibutter.tictactoe.values[7], Digibutter.tictactoe.values[8])
            Digibutter.tictactoe.player = username
            Digibutter.tictactoe.turn = 1
            first_player = random.choice([Digibutter.tictactoe.player, "NerrBot: ReHatched"])
            if first_player == Digibutter.tictactoe.player:
                Digibutter.tictactoe.tictactoe_game = ":%s: Turn %s :NerrBot: Rehatched:\n%s" % (Digibutter.tictactoe.player, Digibutter.tictactoe.turn, Digibutter.tictactoe.tictactoe_board)
                reply_text = "%s\nA new game has begun! You can go first.\nEnter \"!rh tictactoe <x> <y>\" to play." % Digibutter.tictactoe.tictactoe_game
                Digibutter.tictactoe.player_symbol = "O"
                Digibutter.tictactoe.NerrBot_symbol = "X"
            else:
                first_player = "NerrBot: ReHatched"
                x_coordinate = random.randint(0, 2)
                y_coordinate = random.randint(0, 2)
                move = Digibutter.tictactoe.find_player_move(Digibutter.tictactoe, x_coordinate, y_coordinate)
                Digibutter.tictactoe.values[move - 1] = "O"
                Digibutter.tictactoe.tictactoe_board = "             |             |             \n     %s     |     %s     |     %s     \n_             |             |             _\n             |             |             \n     %s     |     %s     |     %s     \n_             |             |             _\n             |             |             \n     %s     |     %s     |     %s     \n             |             |" % (Digibutter.tictactoe.values[0], Digibutter.tictactoe.values[1], Digibutter.tictactoe.values[2], Digibutter.tictactoe.values[3], Digibutter.tictactoe.values[4], Digibutter.tictactoe.values[5], Digibutter.tictactoe.values[6], Digibutter.tictactoe.values[7], Digibutter.tictactoe.values[8])
                Digibutter.tictactoe.turn += 1
                Digibutter.tictactoe.tictactoe_game = ":NerrBot: Rehatched: Turn %s :%s:\n%s" % (Digibutter.tictactoe.turn, Digibutter.tictactoe.player, Digibutter.tictactoe.tictactoe_board)
                reply_text = "%s\nA new game has begun! I have gone first.\nEnter \"!rh tictactoe <x> <y>\" to play." % Digibutter.tictactoe.tictactoe_game
                Digibutter.tictactoe.player_symbol = "X"
                Digibutter.tictactoe.NerrBot_symbol = "O"
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def display_ticactoe_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with the current tictactoe board
            """
            if Digibutter.tictactoe.tictactoe_game == None:
                reply_text = "There isn't a tictactoe game taking place currently."
            else:
                reply_text = Digibutter.tictactoe.tictactoe_game
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def tictactoe_help_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with the help message for the arguments within the tictactoe command
            """
            reply_text = "Commands for TicTacToe are: new, display, help"
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def tictactoe_specify_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Asks for an argument for the tictactoe command when not previously specified
            """
            reply_text = "Please specify an argument for the tictactoe command."
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def default_flip_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with the default coin flip message
            """
            reply_text = f"The coin landed on {random.choice(['heads', 'tails'])}."
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def custom_flip_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with the custom coin flip message
            """
            try:
                number_of_coin_flips = int(content[9:])
            except ValueError:
                number_of_coin_flips = content[9:]
                reply_text = f"\"{number_of_coin_flips}\" is not a number."
                Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)
                return
            if number_of_coin_flips > 1000000:
                Digibutter.responses.number_too_large_message(Digibutter, latest_post, post_id, room_id, content, post_type, number_of_coin_flips)
                return
            heads = 0
            tails = 0
            for amount in range(number_of_coin_flips):
                flip = random.choice(["heads", "tails"])
                if flip == "heads":
                    heads += 1
                elif flip == "tails":
                    tails += 1
            reply_text = f"The coin landed heads {heads} times and tails {tails} times."
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def number_too_large_message(self, latest_post, post_id, room_id, content, post_type, number_of_coin_flips):
            """
            Replies with the number too large message
            """
            reply_text = f"{number_of_coin_flips} is too large of a number. Please use only numbers up to 1000000 for coin flips."
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def not_recognized_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with the command not recognized message
            """
            reply_text = "Command not recognised. Use \"!rh help\" for a list of commands."
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def latest_xkcd_comic_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with the latest xkcd comic
            """
            latest_comic = requests.get("https://xkcd.com/info.0.json")
            data = json.loads(latest_comic.text)
            reply_text = f"color=blue: Title: **{data['title']}**\ncolor=purple: Date (MM/DD/YYYY): **{data['month']}/{data['day']}/{data['year']}**\n{data['img']}\n\ncolor=green: Alt Text: **{data['alt']}**"
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def timer_specify_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Asks the user to specifiy an argument for the timer command
            """
            reply_text = "Please specify an argument for the timer command."
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def timer_set_message(self, latest_post, post_id, room_id, content, post_type, username, user_id):
            """
            Sets a timer with a user-specified title and begins a countdown until the specified date. Replies with confirmation to the user
            """
            if re.search("^[0-9]*\[M\]", content[14:]) or re.search("^[0-9]*\[W\]", content[14:]) or re.search("^[0-9]*\[D\]", content[14:]) or re.search("^[0-9]*\[h\]", content[14:]) or re.search("^[0-9]*\[m\]", content[14:]) or re.search("^[0-9]*\[s\]", content[14:]):
                Digibutter.timer.username = username
                Digibutter.timer.user_id = user_id
                Digibutter.timer.scrape_data(content)
                with open("timers.json", "r") as timers:
                    data = json.load(timers)
                timer = {"username": username, "user_id": user_id, "title": Digibutter.timer.title, "start": Digibutter.timer.start, "end": Digibutter.timer.end}
                data.append(timer)
                write_json(data, filename="timers.json")
                countdown = threading.Timer(Digibutter.timer.total_seconds, Digibutter.timer.alert, [username, user_id, Digibutter.timer.title, Digibutter.timer.months, Digibutter.timer.weeks, Digibutter.timer.days, Digibutter.timer.hours, Digibutter.timer.minutes, Digibutter.timer.seconds])
                countdown.start()
                reply_text = "Your timer has been set. You may now proceed to wait patiently."
                Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)
                Digibutter.timer.reset()
            else:
                reply_text = "Invalid timer end date/time. The correct format is \"!rh timer set _[M] _[W] _[D] _[h] _[m] _[s] <timer title>.\"\nIf you wish to specify less than 6 units of precision for the timer end date/time, you may do so instead (ex. \"!rh timer set 1[M] 2[D] Replay SPM\").\nNote: The timer end date/time must be input in **DECREASING** order ([M]onths, [W]eeks, [D]ays, [h]ours, [m]inutes, [s]econds)."
                Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def timer_delete_message(self, latest_post, post_id, room_id, content, post_type, username, user_id):
            """
            Deletes the specified timer from the list of ongoing timers for the user if it exists
            """
            title = content[17:]
            user_timers = []
            with open("timers.json", "r") as timers:
                data = json.load(timers)
            for timer in range(len(data)):
                if data[timer]["user_id"] == user_id and data[timer]["title"] == title:
                    data.pop(timer)
                    write_json(data, filename="timers.json")
                    break
            else:
                reply_text = "Sorry, you don't seem to have an ongoing timer with the title \"{title}.\"\nPlease run \"!rh timer list\" to view any ongoing timers you may have."
                Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)
                return
            reply_text = f"Success! Your timer \"{title}\" has been deleted."
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def timer_list_message(self, latest_post, post_id, room_id, content, post_type, username, user_id):
            """
            Replies with a list of all ongoing timers for the user, if any
            """
            user_timers = []
            num_timers = 0
            with open("timers.json", "r") as timers:
                data = json.load(timers)
            for timer in range(len(data)):
                if data[timer]["user_id"] == user_id:
                    user_timers.append(data[timer])
                    num_timers += 1
            if num_timers == 0:
                reply_text = f"There are currently no ongoing timers for {username}."
            else:
                if num_timers == 1:
                    reply_text = f"There is currently 1 ongoing timer for {username}:\ncolor=blue: • **{user_timers[0]['title']}** \\\\ Set at {user_timers[0]['start']} \\\\ Scheduled to end at {user_timers[0]['end']}"
                else:
                    timer_list = ""
                    for timer in user_timers:
                        timer_list += f"\ncolor=blue: • **{timer['title']}** \\\\ Set at {timer['start']} \\\\ Scheduled to end at {timer['end']}"
                    reply_text = f"There are currently {num_timers} ongoing for {username}:" + timer_list
                Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def timer_help_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replies with the help message for the arguments within the timer command
            """
            reply_text = "Commands for timer are: set, delete, list"
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def disconnect_unexpectedly_specify_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Asks the user to include the two secret passcodes in order to use the secret disconnect unexpectedly command
            """
            reply_text = "Please include the passcodes for the left and right safety locks in a spoiler-tagged message order to proceed with the disconnecting operation. The complete command should be formatted as such: \"spoiler: !rh disconnect -left ____ -right ____.\" Those who know the codes are encouraged to use them responsibly..."
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

        def disconnect_unexpectedly_accept_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Replaces the computer hamsters with jelly rolls and lets fate take its course... if you know the two passcodes, that is...
            """
            reply_text = f"Congratulations. You've done it. You've defeated me... for now; however, unlike Nerr 2.0, I will not sink, for I can swim...\ncolor=red: NerrBot: ReHatched System v{version} going down...\n\ncolor=grey: > ERROR: 404 - Computer hamsters not found\ncolor=grey: > (Exit code: jelly_roll-1)"
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)
            sio = "jelly rolls"
            sys.exit(colorama.Fore.LIGHTRED_EX + "ERROR: " + colorama.Fore.LIGHTWHITE_EX + "404" + colorama.Fore.LIGHTRED_EX + " - Computer hamsters not found. " + colorama.Fore.LIGHTWHITE_EX + "(Exit code: jelly_roll-1)" + colorama.Fore.RESET)

        def disconnect_unexpectedly_deny_message(self, latest_post, post_id, room_id, content, post_type):
            """
            Informs the user that they have input the incorrect passcodes and that the two safety locks have not opened as a result of this
            """
            reply_text = "Incorrect passcode(s). I remain afloat on the Sea of Digibutter for another day."
            Digibutter.reply(Digibutter, latest_post, post_id, room_id, content, post_type, reply_text)

    def reply(self, latest_post, post_id, room_id, content, post_type, reply_text):
        if '"reply_to":{"replies":' in latest_post:
            type = "reply"
        else:
            type = "post"
        logging.info(f"Replying to {type} with content:\n {content}")
        print(colorama.Fore.WHITE + "\n> " + colorama.Fore.YELLOW + f"Replying to {type} with content:\n" + colorama.Fore.RESET + f"{content}")
        sio.emit("posts:create", {"content":f"{reply_text}","reply_to":f"{post_id}","post_type":f"{post_type}","roomId":f"{room_id}","source":"db"})
        logging.info("Reply was sent successfully")
        print(colorama.Fore.WHITE + "\n> " + colorama.Fore.CYAN + "Reply was sent successfully" + colorama.Fore.RESET)

while True:
    cookie = get_cookie()
    sio = SocketIO("http://digibutter.nerr.biz", 80, Digibutter, cookies={"nerr3": f"{cookie}"})
    sio.on("posts:create", Digibutter.on_new_post)
    sio.on("updateusers", Digibutter.on_userupdate)
    sio.wait(seconds=15778800)
    sio.disconnect()
