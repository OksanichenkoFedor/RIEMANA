import telebot

bot = telebot.TeleBot("5337445036:AAGQDYKj-MCSfgAIOsUytcUMhySBCdTR0qM")

def print_message(message, tg_id):
    """
    Sends current message to the account
    whose ID is passed to this function.
    For telegram to work successfully, the bot must be activated from this account

    Parameters:
        message: The message that will be sent
        tg_id: The telegram ID of the account to which the message will be sent

    Return:
        None
    """
    bot.send_message(tg_id, message)

def throw_plot(filename, tg_id):
    """
    Sends current file to the account
    whose ID is passed to this function.
    File can be audio, picture, etc.
    For telegram to work successfully, the bot must be activated from this account

    Parameters:
        filename: Relative location of the document file
        tg_id: The telegram ID of the account to which the message will be sent

    Return:
        None
    """
    curr_file = open(filename, 'rb')
    bot.send_document(tg_id, curr_file)