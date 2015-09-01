import telegram


LAST_UPDATE_ID = None


def main():

    ''' This is the main function that has to be called '''

    global LAST_UPDATE_ID

    # Telegram Bot Authorization Token
    bot = telegram.Bot('Put your token here')

    # This will be our global variable to keep the latest update_id when requesting
    # for updates. It starts with the latest update_id if available.
    try:
        LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
    except IndexError:
        LAST_UPDATE_ID = None

    while True:
        fetch_url(bot)


def list_compare(first_list, second_list):

    ''' Function to compare two list and return the index of first matched index'''

    for word in first_list:
        if word in second_list:
            return second_list.index(word)
    return -1

def fetch_url(bot):
    global LAST_UPDATE_ID

    # Following is a dictionary of commands that the bot can use

    commands = {'/help':"You can add me in any group or text me! I don't have aceess to the group message so you need to call me by my name i.e @lmgtfyou_bot or start your senstence with '/' , I listen to the keyword 'means' ", '/start':'I am always listening to you. Just use magical words'}

    magic_words = ['means','mean','/means','/mean']

    for update in bot.getUpdates(offset=LAST_UPDATE_ID, timeout=10):
        chat_id = update.message.chat_id
        message = update.message.text.encode('utf-8')
        message_list = message.split()

        if(message in commands):
           bot.sendMessage(chat_id=chat_id, text=commands[message])
           LAST_UPDATE_ID = update.update_id + 1

        if ( list_compare(magic_words, message_list)!= -1):
            search = message_list[list_compare(magic_words, message_list)-1]
            url='http://lmgtfy.com/?q='+search
            bot.sendMessage(chat_id=chat_id,text=url)
            LAST_UPDATE_ID = update.update_id + 1


if __name__ == '__main__':
    main()
