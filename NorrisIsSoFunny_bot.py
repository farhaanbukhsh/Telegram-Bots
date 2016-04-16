import telegram


LAST_UPDATE_ID = None


def main():

    ''' This is the main function that has to be called '''

    global LAST_UPDATE_ID

    # Telegram Bot Authorization Token
    bot = telegram.Bot('put your token here')

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

    commands = {'/help':"Jokes are what I am made for, my speciality is Chuck Norris", '/start':'I am here to give you more jokes about Chuck Norris, because he is the best'}

    magic_words = ['more','More','/more','/More']

    for update in bot.getUpdates(offset=LAST_UPDATE_ID, timeout=10):
        chat_id = update.message.chat_id
        message = update.message.text.encode('utf-8')
        message_list = message.split()

        if(message in commands):
           bot.sendMessage(chat_id=chat_id, text=commands[message])
           LAST_UPDATE_ID = update.update_id + 1
        # Name of my bot is NorrisIsFunny_bot replace your bot name with this
        if ( list_compare(magic_words, message_list)!= -1 or message == '/more@NorrisIsSoFunny_bot'):
            import requests 
            import json
            url = 'http://api.icndb.com/jokes/random'
            myResponse = requests.get(url)
            if (myResponse.ok):
                jData = json.loads(myResponse.content)
                jValue = jData.get('value')
                jJoke = str(jValue.get('joke'))
                bot.sendMessage(chat_id=chat_id,text=jJoke)
                LAST_UPDATE_ID = update.update_id + 1
         
if __name__ == '__main__':
    main()
