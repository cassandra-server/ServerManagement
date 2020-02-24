#import the libraries
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import Filters
import subprocess

#when /proves
def proves(bot, update):
	message = bot.send_message(chat_id=update.message.chat_id, text="Put your doubious stuff here")


#when /awake
def awake(bot, update):
	message = bot.send_message(chat_id=update.message.chat_id, text="Checking...")
	subprocess.call('./scripts/checkifawake.sh', shell=True) #check the awakeness of the server through the script
	status = open('./resources/status.txt').read().strip() #read the output of the script
	if status == 'awake':
		bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=message.message_id, text="Hello, I'm awake :)") #reply to the checking message
	if status == 'asleep':
		bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=message.message_id, text="I'm sleeping :(") #reply to the checking message


#when /getup
def getup(bot, update):
	message = bot.send_message(chat_id=update.message.chat_id, text="Can't I have 5 more mins... (Be a little patient)")
	subprocess.call('./scripts/getup.sh', shell=True) #wakeonlan + ping until success through the script
	bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=message.message_id, text="Ready to rock!") #reply to the 'time to get up' message


#when /help
def help(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="/awake - displays the current status of the server \n"
	+ "/getup - turns the server on and waits until it's active\n"
	+ "/help - displays this same menu\n"
	+ "/sleep - turns the server off\n"
	+ "/start - turns the bot on\n"
	+ "/wakeup - turns the server on\n")


#when /sleep
def sleep(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Putting on my pajamas...")
	subprocess.call('./scripts/sleep.sh', shell=True) #shutdown -P 0 through the script


#when /start
def start(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="I'm active, now you can start asking")


#when /umountall
def umountall
	bot.send_message(chat_id=update.message.chat_id, text="Looking for some mounted partitions (this may take a while)"
	subprocess.call('./scripts/umount.sh', shell=True) #kill desired process remotely


#when /wakeup
def wakeup(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Clock is ringing...")
	subprocess.call('./scripts/wakeup.sh', shell=True) #wakeonlan through the script


#initialization of the bot through the token pasted on the file
TOKEN = open('./resources/token.txt').read().strip()
#load all the permited ids in the file userIds to a list
with open('./resources/userIds.txt') as file:
	permittedIds = [int(x) for x in file.read().split()]


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


#assign each command to its function
dispatcher.add_handler(CommandHandler('awake', awake, Filters.user(user_id=permittedIds)))
dispatcher.add_handler(CommandHandler('getup', getup, Filters.user(user_id=permittedIds)))
dispatcher.add_handler(CommandHandler('help', help, Filters.user(user_id=permittedIds)))
dispatcher.add_handler(CommandHandler('sleep', sleep, Filters.user(user_id=permittedIds)))
dispatcher.add_handler(CommandHandler('start', start, Filters.user(user_id=permittedIds)))
dispatcher.add_handler(CommandHandler('umountall', umountall, Filter.user(user_id=permittedIds)))
dispatcher.add_handler(CommandHandler('wakeup', wakeup, Filters.user(user_id=permittedIds)))
dispatcher.add_handler(CommandHandler('proves', proves, Filters.user(user_id=permittedIds)))


#start the bot
updater.start_polling()
