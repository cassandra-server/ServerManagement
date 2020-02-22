#import of libraries
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
import subprocess

#when /start
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hey there!")


#when /awake
def awake(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Checking, please be patient") #message before executing the script
	script = subprocess.call('pathtothescript/checkifawake.sh', shell=True) #execution of the script to check if the server is awake
	status = open('pathtothefile/status.txt').read().strip() #read the output of the comprobation
	if status == 'awake':
		bot.send_message(chat_id=update.message.chat_id, text="Hello I'm awake :)")
	if status == 'asleep':
		bot.send_message(chat_id=update.message.chat_id, text="I'm sleeping :(")


TOKEN = open('token.txt').read().strip() #initialization of the token specified in token.txt (same directory as this file)


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


#association of the commands with the functions
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('awake', awake))


#initialization of the bot
updater.start_polling()
