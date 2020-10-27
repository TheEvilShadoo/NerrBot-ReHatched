print("=====================================================NerrBot v1.0.0=====================================================")

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import time
import utilities.counter as counter
import utilities.dice as dice

# Sets Up the Chrome Webdriver to run in headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=chrome_options)

#List Urls
login_url = "http://digibutter.nerr.biz/login"
all_posts_url = "http://digibutter.nerr.biz/posts"
the_dump_url = "http://digibutter.nerr.biz/posts/room/sidebar"

class navigation:
    def all_posts(self):
        #Changes the current channel to All Posts
        driver.get(all_posts_url)
        print("\nConnected to All Posts")

    def the_dump(self):
        #Changes the current channel to The Dump
        driver.get(the_dump_url)
        print("\nConnected to The Dump")

class interactions:
    def login(self):
        #Go to /login Page
        driver.get(login_url)

        #Define Credentials
        email = "nb@nerrbot.com"
        password = "BeepBoopBot-18"

        #Perform Login
        print("\nLogging in...")
        email_textbox = driver.find_element_by_id("email")
        email_textbox.send_keys(email)

        password_textbox = driver.find_element_by_id("password")
        password_textbox.send_keys(password)

        login_button = driver.find_element_by_class_name("btn-primary")
        login_button.submit()
        print("\nDone.")

        username = driver.find_element_by_id("name")
        username = username.get_attribute("value")
        print("\nWelcome, %s." % username)

        def show_more(self):
            #Finds all show more buttons and clicks them
            show_replies_buttons = driver.find_elements_by_css_selector(".btn-showreplies")
            for show_replies_button in show_replies_buttons:
                if show_replies_button.text == "...":
                    show_replies_button.click()

    def post_ready_message(self):
        #Posts "Ready." to the current channel.
        post_text = "Ready."
        post_textbox = driver.find_element_by_id("textarea-message")
        post_textbox.send_keys(post_text)
        print("\nPosting...")
        send_button = driver.find_element_by_xpath("//*[@id='mdl-content']/div/div/main/div/div/div/div[2]/div/div[3]/button")
        send_button.click()
        print("\nDone.")

class responses:
    def about_message(self):
        #Posts the about message to the latest topic in the current channel
        reply_buttons = driver.find_elements_by_xpath("//*[@title='OPEN']")
        reply_buttons[-2].click()
        time.sleep(1)
        reply_textbox = driver.find_element_by_id("textarea-message")
        reply_text = "--NerrBot: Rehatched--\nVersion: 0.1.0\nUptime: %s\n\nEnter '!nb <command>' to execute a command, or '!nb help' for help.\nFor questions or concerns please contact TheEvilShadoo." % counter.count
        reply_textbox.send_keys(reply_text)
        print("\nReplying...")
        send_button = driver.find_element_by_xpath("//*[@id='mdl-content']/div/div/main/div/div/div/div[2]/div/div[3]/button")
        send_button.click()
        print("\nDone.")
        driver.back

    def roll_message(self):
        #Posts the about message to the latest topic in the current channel
        reply_buttons = driver.find_elements_by_xpath("//*[@title='OPEN']")
        reply_buttons[-2].click()
        time.sleep(1)
        reply_textbox = driver.find_element_by_id("textarea-message")
        reply_text = "You rolled a %s!" % dice.default_roll
        reply_textbox.send_keys(reply_text)
        print("\nReplying...")
        send_button = driver.find_element_by_xpath("//*[@id='mdl-content']/div/div/main/div/div/div/div[2]/div/div[3]/button")
        send_button.click()
        print("\nDone.")
        driver.back

    def help_message(self):
        #Posts the help message to the latest topic in the current channel
        reply_buttons = driver.find_elements_by_xpath("//*[@title='OPEN']")
        reply_buttons[-2].click()
        time.sleep(1)
        reply_textbox = driver.find_element_by_id("textarea-message")
        reply_text = "Available commands are: yesno, rate, roll, online, echo, time, tictactoe, flip\nEnter '!nb help <command>' to learn more."
        reply_textbox.send_keys(reply_text)
        print("\nReplying...")
        send_button = driver.find_element_by_xpath("//*[@id='mdl-content']/div/div/main/div/div/div/div[2]/div/div[3]/button")
        send_button.click()
        print("\nDone.")
        driver.back

    def help_roll_message(self):
        #Posts the roll command help message to the latest topic in the current channel
        reply_buttons = driver.find_elements_by_xpath("//*[@title='OPEN']")
        reply_buttons[-2].click()
        time.sleep(1)
        reply_textbox = driver.find_element_by_id("textarea-message")
        reply_text = "roll <sides> - Roll a random dice, with an optional number of sides (default is six) (currently only the default number of sides is supported)."
        reply_textbox.send_keys(reply_text)
        print("\nReplying...")
        send_button = driver.find_element_by_xpath("//*[@id='mdl-content']/div/div/main/div/div/div/div[2]/div/div[3]/button")
        send_button.click()
        print("\nDone.")
        driver.back

    def discord_only_message(self):
        #Posts the Discord Only command message to the latest topic in the current channel
        reply_buttons = driver.find_elements_by_xpath("//*[@title='OPEN']")
        reply_buttons[-2].click()
        time.sleep(1)
        reply_textbox = driver.find_element_by_id("textarea-message")
        reply_text = "I'm sorry, but this command currently only works on the Discord chat."
        reply_textbox.send_keys(reply_text)
        print("\nReplying...")
        send_button = driver.find_element_by_xpath("//*[@id='mdl-content']/div/div/main/div/div/div/div[2]/div/div[3]/button")
        send_button.click()
        print("\nDone.")
        driver.back

    def not_implemented_yet_message(self):
        #Posts the not implemented yet message to the latest topic in the current channel
        reply_buttons = driver.find_elements_by_xpath("//*[@title='OPEN']")
        reply_buttons[-2].click()
        time.sleep(1)
        reply_textbox = driver.find_element_by_id("textarea-message")
        reply_text = "I'm sorry, but this command has not been programmed back into my robot brain yet."
        reply_textbox.send_keys(reply_text)
        print("\nReplying...")
        send_button = driver.find_element_by_xpath("//*[@id='mdl-content']/div/div/main/div/div/div/div[2]/div/div[3]/button")
        send_button.click()
        print("\nDone.")
        driver.back

    def not_recognized_message(self):
        #Posts the command not recognized message to the latest topic in the current channel
        reply_buttons = driver.find_elements_by_xpath("//*[@title='OPEN']")
        reply_buttons[-2].click()
        time.sleep(1)
        reply_textbox = driver.find_element_by_id("textarea-message")
        reply_text = "Command not recognised. Use '!nb help' for a list of commands."
        reply_textbox.send_keys(reply_text)
        print("\nReplying...")
        send_button = driver.find_element_by_xpath("//*[@id='mdl-content']/div/div/main/div/div/div/div[2]/div/div[3]/button")
        send_button.click()
        print("\nDone.")
        driver.back

    def test_response(self):
        #The testing reply function
        reply_buttons = driver.find_elements_by_xpath("//*[@title='OPEN']")
        reply_buttons[-2].click()
        time.sleep(1)
        reply_textbox = driver.find_element_by_id("textarea-message")
        reply_text = "test response"
        reply_textbox.send_keys(reply_text)
        print("\nReplying...")
        send_button = driver.find_element_by_xpath("//*[@id='mdl-content']/div/div/main/div/div/div/div[2]/div/div[3]/button")
        send_button.click()
        print("\nDone.")
        driver.back()

#The main program code which scans for and handles user commands
interactions.login(interactions)
time.sleep(1)

navigation.the_dump(navigation)
time.sleep(1)

interactions.show_more(interactions)
time.sleep(1)

interactions.post_ready_message(interactions)

scan_for_command = True
while scan_for_command == True:
    time.sleep(1)
    topics = driver.find_elements_by_class_name("postcontent")
    latest_topic = topics[-1].text
    if latest_topic[0:3] == "!nb":
        if latest_topic == "!nb":
            responses.about_message(responses)
        elif latest_topic[0:8] == "!nb help":
            if latest_topic == "!nb help":
                responses.help_message(responses)
            elif latest_topic == "!nb help yesno":
                responses.not_implemented_yet_message(responses)
            elif latest_topic == "!nb help rate":
                responses.not_implemented_yet_message(responses)
            elif latest_topic == "!nb help chat":
                responses.discord_only_message(responses)
            elif latest_topic == "!nb help relay":
                responses.discord_only_message(responses)
            elif latest_topic == "!nb help roll":
                responses.help_roll_message(responses)
            elif latest_topic == "!nb help autorelay":
                responses.discord_only_message(responses)
            elif latest_topic == "!nb help online":
                responses.not_implemented_yet_message(responses)
            elif latest_topic == "!nb help echo":
                responses.not_implemented_yet_message(responses)
            elif latest_topic == "!nb help time":
                responses.not_implemented_yet_message(responses)
            elif latest_topic == "!nb help tictactoe":
                responses.not_implemented_yet_message(responses)
            elif latest_topic == "!nb help flip":
                responses.not_implemented_yet_message(responses)
        elif latest_topic[0:8] == "!nb roll":
            if latest_topic == "!nb roll":
                responses.roll_message(responses)
        else:
            responses.not_recognized_message(responses)
    else:
        driver.refresh()
