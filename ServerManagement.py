#import the libraries
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import Filters
import subprocess


#when /awake
def awake(bot, update):
	message = bot.send_message(chat_id=update.message.chat_id, text="Checking...")
	subprocess.call('absolute_path/scripts/checkifawake.sh', shell=True) #check the awakeness of the server through the script
	status = open('absolute_path/resources/status.txt').read().strip() #read the output of the script
	if status == 'awake':
		bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=message.message_id, text="Hello, I'm awake :)") #reply to the checking message
	if status == 'asleep':
		bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=message.message_id, text="I'm sleeping :(") #reply to the checking message


#find if there is a matching between the arguments and the list of series/movies
def filter(bot, update, args):
	bot.send_message(chat_id=update.message.chat_id, text="Inside the method")
	if len(args) > 1:
		shows = []
		keyword = []
		for k in range(1,len(args)):
			keyword.append(args[k])
		keyword = " ".join(keyword)
		list = open('absolute_path/resources/list.txt')
		for show in list:
			if keyword.lower() in show.lower():
				shows.append(show)
		if len(shows) == 0:
			bot.send_message(chat_id=update.message.chat_id, text="Nothing found :(")
		else:
			shows="- " + "- ".join(shows)
			bot.send_message(chat_id = update.message.chat_id, text=shows)


#when /list
def list(bot, update, args):
	if args[0] == "films":
		subprocess.call('absolute_path/scripts/listfilms.sh', shell=True)
		if len(args) == 1:
			list = open('absolute_path/resources/list.txt').read().strip()
			bot.send_message(chat_id=update.message.chat_id, text=list)
		else:
			filter(bot, update, args)
	elif args[0] == "series":
		subprocess.call('absolute_path/scripts/listseries.sh', shell=True)
		if len(args) == 1:
			list = open('absolute_path/resources/list.txt').read().strip()
			bot.send_message(chat_id=update.message.chat_id, text=list)
		else:
			filter(bot, update, args)


#when /getup
def getup(bot, update):
	message = bot.send_message(chat_id=update.message.chat_id, text="Can't I have 5 more mins... (Be a little patient)")
	subprocess.call('absolute_path/scripts/getup.sh', shell=True) #wakeonlan + ping until success through the script
	bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=message.message_id, text="Ready to rock!") #reply to the 'time to get up' message


#when /help
def help(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="/awake - displays the current status of the server \n"
	+ "/getup - turns the server on and waits until it's active\n"
	+ "/help - displays this same menu\n"
	+ "/sleep - turns the server off\n"
	+ "/start - turns the bot on\n"
	+ "/wakeup - turns the server on\n")


def migrate(bot, update):
	message = bot.send_message(chat_id=update.message.chat_id, text="Heading towards Unformmated")
	subprocess.call('absolute_path/scripts/migrate.sh', shell=True)
	bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=message.message_id, text="Destination reached")


def mount(bot, update):
	subprocess.call('absolute_path/scripts/mount.sh', shell=True) #cd on the directory (only because there is the autofs)
	bot.send_message(chat_id=update.message.chat_id, text="Like it was your home")


#when /sleep
def sleep(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Putting on my pajamas...")
	subprocess.call('absolute_path/scripts/sleep.sh', shell=True) #shutdown -P 0 through the script


#when /start
def start(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="I'm active, now you can start asking")


#when /umountall
def umountall(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Looking for some mounted partitions (this may take a while)")
	subprocess.call('absolute_path/scripts/umount.sh', shell=True) #kill desired process remotely
	pidsunf = open('absolute_path/resources/mountedServers.txt').readline()
	pids = pidsunf.split()
	if pids[0] != 'Connection':
		bot.send_message(chat_id=update.message.chat_id, text="The partition was found")
		file = open('absolute_path/resources/mountedServers.txt')
		for pid in pids:
			file.write(pid)
		file.close()
	if pids[0] == 'Connection':
		bot.send_message(chat_id=update.message.chat_id, text="There wasn't any remote partition")

#when /wakeup
def wakeup(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Clock is ringing...")
	subprocess.call('absolute_path/scripts/wakeup.sh', shell=True) #wakeonlan through the script


#initialization of the bot through the token pasted on the file
TOKEN = open('absolute_path/resources/token.txt').read().strip()
#load all the permited ids in the file userIds to a list
with open('absolute_path/resources/userIds.txt') as file:
	permittedIds = [int(x) for x in file.read().split()]


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


#assign each command to its function
dispatcher.add_handler(CommandHandler('awake', awake, Filters.user(user_id=permittedIds)))
dispatcher.add_handler(CommandHandler('getup', getup, Filters.user(user_id=permittedIds)))
dispatcher.add_handler(CommandHandler('help', help, Filters.user(user_id=permittedIds)))
dispatcher.add_handler(CommandHandler('sleep', sleep, Filters.user(user_id=permittedIds)))
dispatcher.add_handler(CommandHandler('start', start, Filters.user(user_id=permittedIds)))
dispatcher.add_handler(CommandHandler('umountall', umountall, Filters.user(user_id=permittedIds)))
dispatcher.add_handler(CommandHandler('wakeup', wakeup, Filters.user(user_id=permittedIds)))
dispatcher.add_handler(CommandHandler('proves', proves, Filters.user(user_id=permittedIds), pass_args=True))
dispatcher.add_handler(CommandHandler('mount', mount, Filters.user(user_id=permittedIds)))
dispatcher.add_handler(CommandHandler('list', list, Filters.user(user_id=permittedIds), pass_args=True))
dispatcher.add_handler(CommandHandler('migrate', migrate, Filters.user(user_id=permittedIds)))

#start the bot
updater.start_polling()
