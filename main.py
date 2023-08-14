from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
import psycopg2
from db_logic import do_registration
import string
import random
import bcrypt
import requests
from kivy.properties import StringProperty

class WindowManager(ScreenManager):
	pass 

class LoginWindow(Screen):
	# name = 'login'
	# first_name = StringProperty('')
	
	def log_user_in(self):
		email = self.ids.email.text.strip().lower()
		password = self.ids.password.text.strip()

		# validate input
		if email == '' or password == '':
			self.ids.error.text = '[color=ff3333]Provide both email and password to Login![/color]'

		else:
			if '@' in email:
				conn = psycopg2.connect(database = "kvappdb", user = "postgres", password = "password", host = "127.0.0.1", port = "5432")
				cur = conn.cursor()

				sql = "SELECT * FROM MYUSER WHERE email=%s"

				cur.execute(sql,[email])

				u = cur.fetchone() #return a list of one element containg data of the user with the given email
				print(u)
				conn.close()

				if u is not None:
					first_name = u[1]
					print(f'LogIn as {first_name}')
					main_screen = self.manager.get_screen('main')
					self.manager.switch_to(main_screen)
					# MainWindow.username = first_name
					# WindowManager.MainWindow.ids.name.text = first_name
				else:
					self.ids.error.text = '[color=ff3333]No user with the given email!![/color]'

				self.ids.email.text = ''
				self.ids.password.text = ''
			else:
				self.ids.error.text = '[color=ff3333]A valid email is required![/color]'

class RegistrationWindow(Screen):

	def register_user(self):
		fname = self.ids.fname.text.strip()
		lname = self.ids.lname.text.strip()
		email = self.ids.email.text.strip().lower()
		phone = self.ids.phone.text.strip()
		passwrd = self.ids.password.text.strip()
		

		# validate input
		if email == '' or passwrd == '' or lname == '' or fname == '' or phone == '':
			if email == '' and passwrd == '' and lname == '' and fname == '' and phone == '':
				self.ids.error.text = '[color=ff3333]All fields are required![/color]'

			if email == '' and passwrd != '' and lname != '' and fname != '' and phone != '':
				self.ids.error.text = '[color=ff3333]Email is required![/color]'

			if email != '' and passwrd != '' and lname != '' and fname == '' and phone != '':
				self.ids.error.text = '[color=ff3333]Your first name is required![/color]'

			if email != '' and passwrd != '' and lname == '' and fname != '' and phone != '':
				self.ids.error.text = '[color=ff3333]Your last name is required![/color]'

			if email != '' and passwrd == '' and lname != '' and fname != '' and phone != '':
				self.ids.error.text = '[color=ff3333]Provide a password![/color]'

			if email != '' and passwrd != '' and lname != '' and fname != '' and phone == '':
				self.ids.error.text = '[color=ff3333]Provide your phone number.[/color]'
		else:

			if '@' in email:
				# do a proper email validation with regex

				do_registration(first_name=fname,last_name=lname,phone_number=phone,email=email,password=passwrd)

				# clear input fields
				self.ids.fname.text = ''
				self.ids.lname.text = ''
				self.ids.email.text = ''
				self.ids.password.text = ''
				self.ids.phone.text = ''
				
				self.ids.error.text = '[color=11ff33]You have successfully registered.[/color]'
			else:
				self.ids.error.text = '[color=ff3333]Enter a valid email![/color]'

class ForgotPasswordWindow(Screen):
	
	def reset_password(self):

		conn = psycopg2.connect(database = "kvappdb", user = "postgres", password = "password", host = "127.0.0.1", port = "5432")
		cur = conn.cursor()

		email = self.ids.email.text.strip().lower()


		if email == '':
			self.ids.error.text = '[color=ff3333]Provide your email![/color]'
		else:
			if '@' in email:
				self.ids.email.text = ''
				self.ids.error.text = ''

				sql = "SELECT * FROM MYUSER WHERE email=%s"

				cur.execute(sql,[email])

				u = cur.fetchone() #return a list of one element containg data of the user with the given email
				# print(u)

				
				if u is not None:

					# generate password
				    generated_password = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=10))

				    print(generated_password)

				    # hash generated password
				    bytePwd = generated_password.encode('utf-8') #pwd to b-string
				    salt = bcrypt.gensalt() #generate salt
				    hashed_pwd = bcrypt.hashpw(bytePwd,salt) #hashed pwd

				    # print(hashed_pwd)


				    sql = "UPDATE MYUSER SET password = %s WHERE email=%s"
				    cur.execute(sql,[hashed_pwd,email])
				    conn.commit()
				    conn.close()
				 
				    # send new password to users phone
				    endPoint = 'https://api.mnotify.com/api/sms/quick'
				    apiKey = 'R9GpqsNyO1V3yflU7OFhSkjmG'
				    url = endPoint + '?key=' + apiKey

				    first_name = u[1]
				    phone = u[4]

				    data = {
				    	'recipient[]': [phone,],
				    	'sender': 'Kivy App',
				    	'message': f'Hello {first_name}, password reset was successful.\nYour new password is "{generated_password}"\
				    	 without the double quotes.',
				    	 'is_schedule': False,
				    	 'schedule_date': ''
				    }

				    try:
				    	response =requests.post(url,data)
				    	data = response.json()
				    	password_reset_done_screen = self.manager.get_screen('passwordResetDone')
				    	self.manager.switch_to(password_reset_done_screen)

				    # except ConnectionError:
				    # 	print("connect to the internet and try again")
				    except Exception as e:
				    	print(e)

				else:
					self.ids.error.text = '[color=ff3333]No user with that email!![/color]'

			else:
				self.ids.error.text = '[color=ff3333]Enter a valid email![/color]'

		conn.close()

class PasswordResetDoneWindow(Screen):
	def login_redirect(self):
		self.clear_widgets()
		self.add_widget(WindowManager())
			
class MainWindow(Screen):
	username = StringProperty('user')

	
	def logout(self):
		self.clear_widgets()
		self.add_widget(WindowManager())

class MyLayoutTuto(App):
	def build(self):
		self.title = "Basic Management App"
		# sm = ScreenManager()
		# sm.add_widget(LoginWindow(name='login'))
		# sm.add_widget(ForgotPasswordWindow(name='forgotPassword'))
		# sm.add_widget(RegistrationWindow(name='register'))
		# sm.add_widget(PasswordResetDoneWindow(name='passwordResetDone'))
		# sm.add_widget(MainWindow(name='main'))

		# return sm
		return WindowManager()
		
		

if __name__ == '__main__':
	MyLayoutTuto().run()