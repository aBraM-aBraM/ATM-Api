"""
Interface Module used to allow to use the atm humanely
init() is the main function and the only one you should call publically
made by Eyal Abramovitch 03/02/2021
"""


import atm as atm
import os

QUIT_VALUE = -1

menu_str = ["ATM","===","Create Account [0]","Check Balance [1]","Deposit [2]","Withdraw [3]",
"Change Password [4]","Exit [" + str(QUIT_VALUE) + "]"]
acc_menu_str = ["Create An Account", "=================",
"Password (Required to be at least one character long","Exit [" + str(QUIT_VALUE) + "]"]
auth_menu_str = ["Authentication", "Enter ID"]
action_login_str = ["User ID: ", "Password: "]
action_str = ["Password: ","","Deposit Amount: ", "Withdraw Amount: ", "New Password: "]
bad_auth_str = "Your login info is incorrect"

def init():
	# initialization function used as MAIN FUNCTION
	atm.init()
	menu_ui()

def cls():
	# wrapper for easy clear screen
	os.system('cls')

def create_account_ui():
	# user interface for creating an account
	cls()
	print('\n'.join(acc_menu_str))
	input_pass = ''
	while input_pass == '':
		input_pass = input("Password: ")
		if input_pass == str(QUIT_VALUE):
			break
		elif input_pass:
			uid = atm.create_account(input_pass)
			print("Thanks for Joining!\n Your ID is [0]", uid)
			input("Press enter to return to the main menu")
			break

def auth_action_ui(action_index):
	# user interface for an action which requires authenticating
	cls()
	print('\n'.join(auth_menu_str))
	
	user_data = []
	
	input_data = ''
	login_step = 0
	
	while True:
		input_data = input(action_login_str[login_step])
		if input_data == str(QUIT_VALUE):
			# return False upon user choice to not authenticate
			return False
		elif input_data:
			user_data.append(input_data)
			login_step += 1
		if len(user_data) == 2:
			response = None
			addition_val = ''
			if action_index == 1:
				response = atm.get_balance(user_data[0], user_data[1])
			if action_index > 1:
				while True:
					addition_val = input(action_str[action_index])
					if addition_val == str(QUIT_VALUE):
						# return False upon user choice to not authenticate
						return False
					if addition_val:
						if action_index == 4 or (action_index < 4 and addition_val.isdigit()):
							break
				if action_index == 2:
					response = atm.deposit(user_data[0], user_data[1], int(addition_val))
				if action_index == 3:
					response = atm.withdraw(user_data[0], user_data[1], int(addition_val))
				if action_index == 4:					
					response = atm.change_password(user_data[0], user_data[1], addition_val)

			if response == atm.BAD_AUTH:
				# bad authentication, retry
				user_data = []
				login_step = 0
				cls()
				print('\n'.join(auth_menu_str))
				print(bad_auth_str)
			else:
				if action_index == 1:
					print("Your Balance = " + str(response))
				if action_index == 2:
					print("You Deposited " + str(addition_val))
				if action_index == 3:
					print("You Withdrawn " + str(addition_val))
				if action_index == 4:
					print("Password Successfully changed")
				input("Press enter to return to the main menu")
				return response
	# return False upon user choice to not authenticate
	return False
	

def menu_ui():
	# menu user interface function
	while True:
		cls()
		print('\n'.join(menu_str))
		
		input_data = input()
		
		
		if input_data == str(QUIT_VALUE):
			atm.save_data()
			break
		
		if not input_data.isdigit():
			continue
		
		input_data = int(input_data)
		
		if input_data == 0:
			create_account_ui()
		else:
			if input_data > 0 and input_data < 5:
				# check for correct input
				auth_action_ui(input_data)
	
init()
