#import the libraries
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import Filters
import subprocess

abs_path_scripts='path_to_home/.ServerManagement/Files/Scripts/'
abs_path_resources='path_to_home/.ServerManagement/Files/Resources/'
case_sensitive=False

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


#when /cases
def cases(bot, update, args):
	global case_sensitive
	if args[0].lower() == 'on':
		case_sensitive = True
		bot.send_message(chat_id=update.message.chat_id, text="Arguments are now case sensitive")
	elif args[0].lower() == 'off':
		case_sensitive = False
		bot.send_message(chat_id=update.message.chat_id, text="Arguments are no longer case sensitive")
	elif args[0].lower() == 'status':
		if case_sensitive == False:
			bot.send_message(chat_id=update.message.chat_id, text="The sensitivity is off")
		if case_sensitive == True:
			bot.send_message(chat_id=update.message.chat_id, text="The sensitivity is on")
	else:
		bot.send_message(chat_id=update.message.chat_id, text="Please write On/Off/Status")


#when /download
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
			if case_sensitive:
				if keyword in show:
					shows.append(show)
#					shows = shows + show
			if not case_sensitive:
				if keyword.lower() in show.lower():
					shows.append(show)
#					shows = shows + show
		if len(shows) == 0:
			bot.send_message(chat_id=update.message.chat_id, text="Nothing found :(")
		else:
			str=""
			for show in shows:
				str = str+show
			bot.send_message(chat_id = update.message.chat_id, text=str)


#when /list
def list (bot, update, args):
	ls(bot, update, args, False)


def split_string(string):
	args = []
	for k in range(0, len(string), 4096):
		args.append(string[0+k:4096+k])
	return args


def ls(bot, update, args, recursive):
	file = open(abs_path_resources+'Args/dir.txt', 'w+')
	if case_sensitive:
		file.write(args[0])
	elif not case_sensitive:
		args[0] == args[0].lower()
		args_no_case = '*'
		for i in args[0]:
			args_no_case = args_no_case+'['+i.lower()+i.upper()+']'
		args_no_case = args_no_case+'*'
		file.write(args_no_case)
	file.close()
	if not recursive:
		subprocess.call(abs_path_scripts+'SSH/list.sh', shell=True)
	elif recursive:
		subprocess.call(abs_path_scripts+'SSH/search.sh', shell=True)
	if len(args)==1:
		list = open(abs_path_resources+'Outputs/list.txt', 'r').read().strip()
		if len(list) > 4096:
			messages = split_string(list)
			for message in messages:
				bot.send_message(chat_id=update.message.chat_id, text=message)
		else:
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
							      "/cases (On/Off/Status) - Modify the case sensitivity of the commands\n"+
							      "/help - Print this message of help\n"+
							      "/list (folder)[filters] - List data with filters\n"+
							      "/mount - Access the folder containing the autofs\n"+
							      "/start - Initializes the bot\n")


#when /superhelp
def superhelp(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="/awake - Check the status of the server\n"+
							      "/cases (On/Off/Status) - Modify the case sensitivity of the commands\n"+
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


def parse_machines():
	file = open(abs_path_resources+'/Authentication/Machines/machines.txt', 'r')
	machines = []
	for line in file:
		machines.append(line.split(" ")[0])
	file.close()
#	print(machines)
	return machines


def machines(bot, update, args):
	machines = parse_machines()
	if len(args) == 0:
		list = ""
		for machine in machines:
			list = list+machine+"\n"
		bot.send_message(chat_id=update.message.chat_id, text=list)
	if len(args) > 0:
		str = ""
		if len(args) == 1:
			for machine in machines:
				if args[0] in machine:
					str = str+machine+"\n"
			bot.send_message(chat_id=update.message.chat_id, text=str)
		if len(args) == 2:
			if args[1] == 'swap':
				file = open(abs_path_resources+'Authentication/Machines/machines.txt', 'r')
				found = False
				for line in file:
					if line.split(" ")[0] == args[0]:
						filetmp = open(abs_path_resources+'Authentication/SSH/serveruser.txt', 'w+')
						filetmp.write(line.split(" ")[1])
						filetmp.close()
						filetmp = open(abs_path_resources+'Authentication/SSH/serverip.txt', 'w+')
						filetmp.write(line.split(" ")[2])
						filetmp.close()
						filetmp = open(abs_path_resources+'Authentication/SSH/servermac.txt', 'w+')
						filetmp.write(line.split(" ")[3])
						filetmp.close()
						found = True
						break
				file.close()
				if found:
					bot.send_message(chat_id=update.message.chat_id, text="Machine swapped to "+args[0])
				if not found:
					bot.send_message(chat_id=update.message.chat_id, text="No machine named "+args[0])


#when /migrate
def migrate(bot, update):
	message = bot.send_message(chat_id=update.message.chat_id, text="Heading towards Unformatted")
	subprocess.call(abs_path_scripts+'SSH/migrate.sh', shell=True)
	bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=message.message_id, text="Destination reached")


#when /mount
def mount(bot, update):
	subprocess.call(abs_path_scripts+'Local/mount.sh', shell=True) #cd on the directory (only because there is the autofs)
	bot.send_message(chat_id=update.message.chat_id, text="Like it was your home")


#when /reboot
def reboot(bot, update):
	message = bot.send_message(chat_id=update.message.chat_id, text='Gonna take a nap')
	subprocess.call(abs_path_scripts+'StateModification/reboot.sh', shell=True)
	bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=message.message_id, text="Already woken up")


#when /search
def search(bot, update, args):
	ls(bot, update, args, True)


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
TOKEN = open(abs_path_resources+'Authentication/Functioning/token.txt').read().strip()
#load all the permited ids in the file userIds to a list
with open(abs_path_resources+'Authentication/Functioning/userIds.txt') as file:
	users = [int(x) for x in file.read().split()]
with open(abs_path_resources+'Authentication/Functioning/superuserIds.txt') as file:
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
dispatcher.add_handler(CommandHandler('cases', cases, Filters.user(user_id=users), pass_args=True))
dispatcher.add_handler(CommandHandler('search', search, Filters.user(user_id=users), pass_args=True))
dispatcher.add_handler(CommandHandler('machines', machines, Filters.user(user_id=superusers), pass_args=True))

#start the bot
updater.start_polling()
