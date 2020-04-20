#import the libraries
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardRemove
from telegram import ReplyKeyboardMarkup
from telegram.ext import MessageHandler
import subprocess
import os
import time

abs_path_scripts=os.getenv("HOME")+'/.ServerManagement/Files/Scripts/'
abs_path_resources=os.getenv("HOME")+'/.ServerManagement/Files/Resources/'
case_sensitive=False
show_time=True
INITIAL_CONFIRMATION, FINAL_CONFIRMATION = range(2)
operating_machine = ""
operating_username = ""
SWAP_MACHINE = range(1)


def display_time(bot, update, timei, timef):
	if show_time:
		bot.send_message(chat_id=update.message.chat_id, text="Process executed in: " + str(round(timef-timei)) + " seconds")


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
	timei = time.time()
	file = open(abs_path_resources+'Args/magnetlink.txt', "w+")
	file.write(args[0])
	file.close()
	subprocess.call(abs_path_scripts+'SSH/download.sh', shell=True)
	bot.send_message(chat_id=update.message.chat_id, text="Download link managed correctly")
	timef = time.time()
	display_time(bot, update, timei, timef)


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
			if not case_sensitive:
				if keyword.lower() in show.lower():
					shows.append(show)
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
	substrings=string.split("\n")
	num = int(len(string)/4096)+1
	substringsdef = ['']*num
	substringsdef[0] = ""
	i = 0
	for substring in substrings:
		if len(substringsdef[i])+len(substring) < 4096:
			substringsdef[i] = substringsdef[i] + substring + "\n"
		else:
			i = i+1;
			substringsdef[i] = substringsdef[i] + substring + "\n"
	return substringsdef


def ls(bot, update, args, recursive):
	timei = time.time()
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
	timef = time.time()
	display_time(bot, update, timei, timef)


#when /getup
def getup(bot, update):
	message = bot.send_message(chat_id=update.message.chat_id, text="Can't I have 5 more mins... (Be a little patient)")
	timei = time.time()
	subprocess.call(abs_path_scripts+'StateModification/getup.sh', shell=True) #wakeonlan + ping until success through the script
	timef = time.time()
	bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=message.message_id, text="Ready to rock!") #reply to the 'time to get up' message
	display_time(bot, update, timei, timef)


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
	bot.send_message(chat_id=update.message.chat_id, text=str(update.message.from_user.id))


def parse_machines():
	file = open(abs_path_resources+'/Authentication/Machines/machines.txt', 'r')
	machines = []
	for line in file:
		machines.append(line.split(" ")[0])
	file.close()
	return machines


def establish_connection(bot, update, machine):
	file = open(abs_path_resources+'Authentication/Machines/machines.txt', 'r')
	found = False
	for line in file:
		if line.split(" ")[0] == machine:
			filetmp = open(abs_path_resources+'Authentication/SSH/serveruser.txt', 'w+')
			filetmp.write(line.split(" ")[1])
			filetmp.close()
			filetmp = open(abs_path_resources+'Authentication/SSH/serverip.txt', 'w+')
			filetmp.write(line.split(" ")[2])
			filetmp.close()
			filetmp = open(abs_path_resources+'Authentication/SSH/servermac.txt', 'w+')
			filetmp.write(line.split(" ")[3])
			filetmp.close()
			filetmp = open(abs_path_resources+'Authentication/SSH/serverport.txt', 'w+')
			filetmp.write(line.split(" ")[4])
			filetmp.close()
			found = True
			break
	file.close()
	if found:
		print('connected')
		bot.send_message(chat_id=update.message.chat_id, text="Connection established to "+args[0])
	else:
		bot.send_message(chat_id=update.message.chat_id, text="Cannot connect to "+args[0]+ ", no machine with this given name")


def machines(bot, update, args):
	timei = time.time()
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
				establish_connection(bot, update, args[0])
			if args[1] == 'info':
				file = open(abs_path_resources+'Authentication/Machines/machines.txt', 'r')
				found = False
				str = "Name: " + args[0] + "\n"
				for line in file:
					if line.split(" ")[0] == args[0]:
						str = str + "Username: " + line.split(" ")[1] + "\nIP Address: " + line.split(" ")[2] + "\nMAC Address: " + line.split(" ")[3] + "\nPort: " + line.split(" ")[4]
						found = True
						break
				file.close()
				if found:
					bot.send_message(chat_id=update.message.chat_id, text=str)
				else:
					bot.send_message(chat_id=update.message.chat_id, text="No machine found with name " + args[0])
	timef=time.time()
	display_time(bot, update, timei, timef)


#when /migrate
def migrate(bot, update):
	timei = time.time()
	message = bot.send_message(chat_id=update.message.chat_id, text="Heading towards Unformatted")
	subprocess.call(abs_path_scripts+'SSH/migrate.sh', shell=True)
	bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=message.message_id, text="Destination reached")
	timef = time.time()
	display_time(bot, update, timei, timef)


#when /mount
def mount(bot, update):
	subprocess.call(abs_path_scripts+'Local/mount.sh', shell=True) #cd on the directory (only because there is the autofs)
	bot.send_message(chat_id=update.message.chat_id, text="Like it was your home")


#when /reboot
def reboot(bot, update):
	message = bot.send_message(chat_id=update.message.chat_id, text='Gonna take a nap')
	timei=time.time()
	subprocess.call(abs_path_scripts+'StateModification/reboot.sh', shell=True)
	timef=time.time()
	bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=message.message_id, text="Already woken up")
	display_time(bot, update, timei, timef)


#when /search
def search(bot, update, args):
	ls(bot, update, args, True)


#when /sleep
def sleep(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Putting on my pajamas...")
	subprocess.call(abs_path_scripts+'StateModification/sleep.sh', shell=True) #shutdown -P 0 through the script


def check_permissions(bot, update, username):
	file = open(abs_path_resources+'Authentication/Machines/machines.txt', 'r')
	print ("inside4")
	machines = []
	print ("inside5")
	for line in file:
		print ("inside6")
		users = line.split(' ')[5].split(',')
		print ("inside7")
		if username in users:
			print ("inside8")
			machines.append(line.split(' ')[0])
			print ("inside9")
	file.close()
	print (machines)
	print ("inside10")
	return machines


def getdata(bot, update):
	print ('getdata')
	print (update.message.text)
	ConversationHandler.END


def abort(bot, update):
	ConversationHandler.END


def swapping(bot, update):
	print("inside")
	global operating_machine
	global operating_username
	print ("inside2")
	operating_username=str(update.message.from_user.id)
	print ("inside3")
	machines_user = check_permissions(bot, update, operating_username)
	print ("inside2")
	a = []
	for index in machines_user:
		a.append([index])
	reply_keyboard = a
	choice = update.message.reply_text("Please get one of the machines that's available for you", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
	return SWAP_MACHINE


def start (bot, update):
	print ('start')
	swapping(bot, update)
#	getdata(bot, update)


def times(bot, update, args):
	global show_time
	if args[0].lower() == 'on':
		show_time = True
		bot.send_message(chat_id=update.message.chat_id, text="Execution times are now on")
	elif args[0].lower() == 'off':
		show_time = False
		bot.send_message(chat_id=update.message.chat_id, text="Execution times are now off")
	elif args[0].lower() == 'status':
		if show_time:
			bot.send_message(chat_id=update.message.chat_id, text="Execution times are on")
		else:
			bot.send_message(chat_id=update.message.chat_id, text="Execution times are off")
	else:
		bot.send_message(chat_id=update.message.chat_id, text="Please write On/Off/Status")


#when /wakeup
def wakeup(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Clock is ringing...")
	subprocess.call(abs_path_scripts+'StateModification/wakeup.sh', shell=True) #wakeonlan through the script


def uninstall(bot, update):
	reply_keyboard = [['Continue'],['Cancel']]
	update.message.reply_text("You're about to uninstall everything in respect to the server manager, make sure this is the option you want to execute befor continuing", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
	return INITIAL_CONFIRMATION


def uninstall_confirmation(bot, update):
	reply_keyboard = [['Yes'],['No']]
	update.message.reply_text("Do you want to uninstall everything?", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
	return FINAL_CONFIRMATION


def uninstall_cancel(bot, update):
	update.message.reply_text("Cancelled", reply_markup=ReplyKeyboardRemove())
	return ConversationHandler.END


def uninstall_final(bot, update):
	update.message.reply_text("Uninstalling daemon...")
	subprocess.call(abs_path_scripts+"Uninstall/daemon.sh", shell=True)
	update.message.reply_text("Removing permissions from sudoers...")
	subprocess.call(abs_path_scripts+"Uninstall/visudo.sh", shell=True)
	update.message.reply_text("Uninstalling directory...")
	subprocess.call(abs_path_scripts+"Uninstall/directory.sh", shell=True)
	update.message.reply_text("Uninstalled successfully", reply_markup=ReplyKeyboardRemove())
	return ConversationHandler.END


confirmations = ConversationHandler(entry_points=[CommandHandler('uninstall', uninstall)],
	states={
		INITIAL_CONFIRMATION: [MessageHandler(Filters.regex('Continue'), uninstall_confirmation), MessageHandler(Filters.regex('Cancel'), uninstall_cancel)],
		FINAL_CONFIRMATION: [MessageHandler(Filters.regex('Cancel'), uninstall_final), MessageHandler(Filters.regex('No'), uninstall_cancel)]
	}, fallbacks=[CommandHandler('cancel', uninstall_cancel)])


initialization = ConversationHandler(entry_points=[swapping],
	states={
		SWAP_MACHINE: [MessageHandler(Filters.regex('elliot'), getdata)]
	}, fallbacks=[CommandHandler('cancel', abort)])


#initialization of the bot through the token pasted on the file
TOKEN = open(abs_path_resources+'Authentication/Functioning/token.txt').read().strip()
#load all the permited ids in the file userIds to a list
with open(abs_path_resources+'Authentication/Functioning/userIds.txt') as file:
	users = [int(x) for x in file.read().split()]
with open(abs_path_resources+'Authentication/Functioning/superuserIds.txt') as file:
	superusers = [int(x) for x in file.read().split()]


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
file = open(abs_path_resources+'Authentication/Machines/Users/users.txt', 'r')
username = []
id = []
for line in file:
	username.append(line.split(":")[0])
	id.append(line.split(":")[1])
usernames, ids = username, id


#assign each command to its function
dispatcher.add_handler(CommandHandler('awake', awake, Filters.user(user_id=users)))
dispatcher.add_handler(CommandHandler('getup', getup, Filters.user(user_id=superusers)))
dispatcher.add_handler(CommandHandler('help', help, Filters.user(user_id=users)))
dispatcher.add_handler(CommandHandler('sleep', sleep, Filters.user(user_id=superusers)))
dispatcher.add_handler(CommandHandler('start', start, Filters.user(user_id=users)))
dispatcher.add_handler(CommandHandler('wakeup', wakeup, Filters.user(user_id=superusers)))
dispatcher.add_handler(CommandHandler('mount', mount, Filters.user(user_id=users)))
dispatcher.add_handler(CommandHandler('list', list, Filters.user(user_id=users), pass_args=True))
dispatcher.add_handler(CommandHandler('migrate', migrate, Filters.user(user_id=superusers)))
dispatcher.add_handler(CommandHandler('download', download, Filters.user(user_id=superusers), pass_args=True))
dispatcher.add_handler(CommandHandler('reboot', reboot, Filters.user(user_id=superusers)))
dispatcher.add_handler(CommandHandler('superhelp', superhelp, Filters.user(user_id=superusers)))
dispatcher.add_handler(CommandHandler('cases', cases, Filters.user(user_id=users), pass_args=True))
dispatcher.add_handler(CommandHandler('search', search, Filters.user(user_id=users), pass_args=True))
dispatcher.add_handler(CommandHandler('machines', machines, Filters.user(user_id=superusers), pass_args=True))
dispatcher.add_handler(CommandHandler('times', times, Filters.user(user_id=users), pass_args=True))
dispatcher.add_handler(CommandHandler('check', check_permissions, Filters.user(user_id=superusers), pass_args=True))

dispatcher.add_handler(confirmations)
dispatcher.add_handler(initialization)
#start the bot
updater.start_polling()
