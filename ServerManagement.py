#import the libraries
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import Filters
import subprocess

abs_path_scripts='path_to_home/.ServerManagement/Files/Scripts/'
abs_path_resources='path_to_home/.ServerManagement/Files/Resources/'


#when /proves
def proves(bot, update, args):
	saying = " ".join(args)
	message = bot.send_message(chat_id=update.message.chat_id, text=saying)
	#message = bot.send_message(chat_id=update.message.chat_id, text="Put your doubious stuff here")


#when /awake
def awake(bot, update):
	message = bot.send_message(chat_id=update.message.chat_id, text="Checking...")
	subprocess.call(abs_path_scripts+'StateModification/checkifawake.sh', shell=True) #check the awakeness of the server through the script
	status = open(abs_path_resources+'Outputs/status.txt').read().strip() #read the output of the script
	if status == 'awake':
		bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=message.message_id, text="Hello, I'm awake :)") #reply to the checking message
	if status == 'asleep':
		bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=message.message_id, text="I'm sleeping :(") #reply to the checking message


def download(bot, update, args):
	file = open(abs_path_resources+'Args/magnetlink.txt', "w+")
	file.write(args[0])
	file.close()
	subprocess.call(abs_path_scripts+'SSH/download.sh', shell=True)
	bot.send_message(chat_id=update.message.chat_id, text="Download link managed correctly")


def filter(bot, update, args):
	if len(args) > 1:
		shows = []
		keyword = []
		for k in range(1,len(args)):
			keyword.append(args[k])
		keyword = " ".join(keyword)
		list = open(abs_path_resources+'Outputs/list.txt')
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
		subprocess.call(abs_path_scripts+'SSH/listfilms.sh', shell=True)
		if len(args) == 1:
			list = open(abs_path_resources+'Outputs/list.txt').read().strip()
			bot.send_message(chat_id=update.message.chat_id, text=list)
		else:
			filter(bot, update, args)
	elif args[0] == "series":
		subprocess.call(abs_path_scripts+'SSH/listseries.sh', shell=True)
		if len(args) == 1:
			list = open(abs_path_resources+'Outputs/list.txt').read().strip()
			bot.send_message(chat_id=update.message.chat_id, text=list)
		else:
			filter(bot, update, args)


#when /getup
def getup(bot, update):
	message = bot.send_message(chat_id=update.message.chat_id, text="Can't I have 5 more mins... (Be a little patient)")
	subprocess.call(abs_path_scripts+'StateModification/getup.sh', shell=True) #wakeonlan + ping until success through the script
	bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=message.message_id, text="Ready to rock!") #reply to the 'time to get up' message


#when /help
def help(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="/awake - Check the status of the server\n"+
							      "/help - Print this message of help\n"+
							      "/list (folder)[filters] - List data with filters\n"+
							      "/mount - Access the folder containing the autofs\n"+
							      "/start - Initializes the bot\n")


def superhelp(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="/awake - Check the status of the server\n"+
							      "/download (magnetlink) - Downloads the torrent from the magnetlink\n"+
							      "/getup - Turns the server on and waits for a response\n"+
							      "/help - Displays the basic help\n"+
							      "/list (folder)[filters] - List data with filters\n"+
							      "/migrate - Move the files from downloads to the films folder\n"+
							      "/mount - Access the folder containing the autofs\n"+
							      "/reboot - Restarts the server\n"+
							      "/sleep - Turns off the server\n"+
							      "/start - Initializes the bot\n"+
							      "/superhelp - Displays this message of help\n"+
							      "/wakeup - Just turns the server on")


def migrate(bot, update):
	message = bot.send_message(chat_id=update.message.chat_id, text="Heading towards Unformatted")
	subprocess.call(abs_path_scripts+'SSH/migrate.sh', shell=True)
	bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=message.message_id, text="Destination reached")


def mount(bot, update):
	subprocess.call(abs_path_scripts+'Local/mount.sh', shell=True) #cd on the directory (only because there is the autofs)
	bot.send_message(chat_id=update.message.chat_id, text="Like it was your home")


def reboot(bot, update):
	subprocess.call(abs_path_scripts+'StateModification/reboot.sh', shell=True)
	bot.send_message(chat_id=update.message.chat_id, text="Gonna take a nap")


#when /sleep
def sleep(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Putting on my pajamas...")
	subprocess.call(abs_path_scripts+'StateModification/sleep.sh', shell=True) #shutdown -P 0 through the script


#when /start
def start(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="I'm active, now you can start asking")


#when /wakeup
def wakeup(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Clock is ringing...")
	subprocess.call(abs_path_scripts+'StateModification/wakeup.sh', shell=True) #wakeonlan through the script


#initialization of the bot through the token pasted on the file
TOKEN = open(abs_path_resources+'Authentication/token.txt').read().strip()
#load all the permited ids in the file userIds to a list
with open(abs_path_resources+'Authentication/userIds.txt') as file:
	users = [int(x) for x in file.read().split()]
with open(abs_path_resources+'Authentication/superuserIds.txt') as file:
	superusers = [int(x) for x in file.read().split()]


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


#assign each command to its function
dispatcher.add_handler(CommandHandler('awake', awake, Filters.user(user_id=users)))
dispatcher.add_handler(CommandHandler('getup', getup, Filters.user(user_id=superusers)))
dispatcher.add_handler(CommandHandler('help', help, Filters.user(user_id=users)))
dispatcher.add_handler(CommandHandler('sleep', sleep, Filters.user(user_id=superusers)))
dispatcher.add_handler(CommandHandler('start', start, Filters.user(user_id=users)))
dispatcher.add_handler(CommandHandler('wakeup', wakeup, Filters.user(user_id=superusers)))
dispatcher.add_handler(CommandHandler('proves', proves, Filters.user(user_id=superusers), pass_args=True))
dispatcher.add_handler(CommandHandler('mount', mount, Filters.user(user_id=users)))
dispatcher.add_handler(CommandHandler('list', list, Filters.user(user_id=users), pass_args=True))
dispatcher.add_handler(CommandHandler('migrate', migrate, Filters.user(user_id=superusers)))
dispatcher.add_handler(CommandHandler('download', download, Filters.user(user_id=superusers), pass_args=True))
dispatcher.add_handler(CommandHandler('reboot', reboot, Filters.user(user_id=superusers)))
dispatcher.add_handler(CommandHandler('superhelp', superhelp, Filters.user(user_id=superusers)))

#start the bot
updater.start_polling()
