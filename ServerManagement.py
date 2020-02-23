#import of libraries
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
import subprocess

def awake(bot, update): #when /awake
	bot.send_message(chat_id=update.message.chat_id, text="Checking")
	subprocess.call('./scripts/checkifawake.sh', shell=True) #ping using the script
	status = open('./resources/status.txt').read().strip() #read the output of the comprobation
	if status == 'awake':
		bot.send_message(chat_id=update.message.chat_id, text="Hello, I'm awake :)")
	if status == 'asleep':
		bot.send_message(chat_id=update.message.chat_id, text="I'm sleeping :(")


def getup(bot, update): #when /getup
	bot.send_message(chat_id=update.message.chat_id, text="Time to get up...")
	subprocess.call('./scripts/getup.sh', shell=True) #wakeonlan + wait using the script
	bot.send_message(chat_id=update.message.chat_id, text="Ready to rock!")


def help(bot, update): #when /help
	bot.send_message(chat_id=update.message.chat_id, text="/awake - displays the current status of the server \n"
	+ "/getup - turns the server on and waits until it's active\n"
	+ "/help - displays this same menu\n"
	+ "/sleep - turns the server off\n"
	+ "/wakeup - turns the server on\n")


def sleep(bot, update): #when /sleep
	bot.send_message(chat_id=update.message.chat_id, text="Time to go to bed...")
	subprocess.call('./scripts/sleep.sh', shell=True) #shutdown using the script


def wakeup(bot, update): #when /wakeup
	bot.send_message(chat_id=update.message.chat_id, text="Clock is ringing...")
	subprocess.call('./scripts/wakeup.sh', shell=True) #wakeonlan using the script


TOKEN = open('./resources/token.txt').read().strip() #initialize with the token in ./resources/token.txt


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


#association of the commands with the functions
dispatcher.add_handler(CommandHandler('awake', awake))
dispatcher.add_handler(CommandHandler('getup', getup))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('sleep', sleep))
dispatcher.add_handler(CommandHandler('wakeup', wakeup))


#initialization of the bot
updater.start_polling()
