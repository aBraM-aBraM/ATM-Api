import json
import uuid
import user



accounts_dict = {}
database_path = 'data.txt'

BAD_AUTH = "Bad authentication"

def init():
	# initalizes the database
	
	global accounts_dict
	
	json_dict = load_data()
	for key,value in json_dict.items():
		accounts_dict[key] = user.User(uid=value["uid"],password=value["password"], balance=int(value["balance"]))
	if not accounts_dict:
		accounts_dict = {}

def load_data(data_path=database_path):
	# returns data from file as a dictionary
	raw_data = open(data_path,'r').read()
	if not raw_data:
		return raw_data
	return json.loads(raw_data)

def save_data(data_path=database_path):
	# saves data appropriately as json
	data = {}
	account_list = list(accounts_dict.values())
	for i in range(len(account_list)):
		data[account_list[i].uid] = account_list[i].__dict__
	open(data_path,'w+').write(json.dumps(data))

def create_account(password):
	# creates an account
	try:
		if not password:
			raise ValueError
		uid = str(uuid.uuid4())
		
		global accounts_dict
		accounts_dict[uid] = user.User(uid,password,0)
		return uid
	except ValueError:
		print("password is required to be at least one character")

def authenticate(uid, password):
	# returns true is password matches uid false otherwise
	try:
		if not accounts_dict.get(uid):
			raise TypeError
		return accounts_dict[uid].password == password
	except TypeError:
		# user doesn't exist
		return False

def change_password(uid, old_pass,new_pass):
	# changes password of a user's account
	try:
		if not authenticate(uid, old_pass):
			raise TypeError
		global accounts_dict
		accounts_dict[uid].password = new_pass
	except TypeError:
		print("User doesn't exist is database or password doesn't match userID")
		return BAD_AUTH

def get_balance(uid, password):
	# returns balance if user is authenticated
	if not authenticate(uid, password):
		return BAD_AUTH
	return accounts_dict[uid].balance

def withdraw(uid, password, amount):
	# withdraws money if user is authenticated
	if not authenticate(uid,password):
		return BAD_AUTH
	global accounts_dict
	accounts_dict[uid].balance -= amount
	return accounts_dict[uid].balance
	
def deposit(uid, password, amount):
	# withdraws money if user is authenticated
	if not authenticate(uid,password):
		return BAD_AUTH
	global accounts_dict
	accounts_dict[uid].balance += amount
	return accounts_dict[uid].balance


