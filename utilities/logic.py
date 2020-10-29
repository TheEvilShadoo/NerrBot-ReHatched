def do_logic(content):
    """
    Performs the logic for NerrBot: ReHatched
    """
    if content[0:3] == "!rh":
        if content == "!rh":
            return "about_message"
        elif content[0:8] == "!rh help":
            if content == "!rh help":
                return "help_message"
            elif content == "!rh help yesno":
                return "not_implemented_yet_message"
            elif content == "!rh help rate":
                return "not_implemented_yet_message"
            elif content == "!rh help chat":
                return "discord_only_message"
            elif content == "!rh help relay":
                return "discord_only message"
            elif content == "!rh help roll":
                return "help_roll_message"
            elif content == "!rh help autorelay":
                return "discord_only message"
            elif content == "!rh help online":
                return "not_implemented_yet_message"
            elif content == "!rh help echo":
                return "help_echo_message"
            elif content == "!rh help time":
                return "not_implemented_yet_message"
            elif content == "!rh help tictactoe":
                return "not_implemented_yet_message"
            elif content == "!rh help flip":
                return "not_implemented_yet_message"
        elif content[0:8] == "!rh roll":
            if content == "!rh roll":
                return "roll_message"
        elif content[0:8] == "!rh echo":
                return "echo_message"
        else:
            return "not_recognized_message"