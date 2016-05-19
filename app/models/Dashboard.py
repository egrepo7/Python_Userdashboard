from system.core.model import Model
import re
EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')

class Dashboard(Model):
	def __init__(self):
		super(Dashboard, self).__init__()
	
	def delete(self, id):
		query = "DELETE FROM users WHERE users.id = :id"
		data = { 'id': id }
		self.db.query_db(query, data)

	def sign_in(self, info):
		errors = {}
		if not EMAIL_REGEX.match(info['log_email']):
			errors.update({'log_email':'Please enter a valid email address'})
		if len(info['log_password']) < 8:
			errors.update({'log_password':'Password must be at least 8 characters'})
		if len(errors) > 0:
			return errors
		else:
			query = "SELECT * FROM users WHERE email = :email LIMIT 1"
			data = {
				'email': info['log_email']
			}
			user = self.db.query_db(query, data)
			if user == []:
				errors.update({'notreg':'Email is not registered'})
				return errors
			else:
				if self.bcrypt.check_password_hash(user[0]['password'], info['log_password']):
					logged_user = {'logged_user':{'id': user[0]['id'], 'first_name':user[0]['first_name'], 'last_name': user[0]['last_name'], 'email': user[0]['email'], 'description': user[0]['description'], 'created_at': user[0]['created_at'], 'level': user[0]['level']}}
					return logged_user
				else:
					errors.update({'passmatch': 'Password entered does not match registered email'})
					return errors

	def show_wall_user(self, id):
		query = "SELECT * FROM users WHERE users.id = :id"
		data = {
			'id': id
		}
		return self.db.query_db(query, data)


	def show_wall_messages(self, id):
		query = "SELECT first_name, last_name, messages.message as message, users_wallid, messages.id as m_id, messages.created_at as m_created_at FROM users LEFT JOIN messages on messages.user_id = users.id WHERE messages.users_wallid = :id"
		data = {
			'id': id
		}
		return self.db.query_db(query, data)

	def show_wall_comments(self, id):
		query = "SELECT users_wallid, first_name, last_name, comment, comments.message_id as c_m_id, comments.id as c_id, comments.created_at as c_created_at FROM comments LEFT JOIN users on comments.user_id = users.id WHERE comments.users_wallid = :id"
		data = {
			'id': id
		}
		print data
		varia = self.db.query_db(query, data)
		print varia
		print "*" * 50
		return self.db.query_db(query, data)


	def wall_comment(self, info, id):
		query = "INSERT INTO comments (comment, user_id, message_id, users_wallid, created_at) VALUES (:comment, :author, :message_id, :users_wallid, NOW())"
		data = {
			'comment': info['comment'],
			'author': info['author'],
			'message_id': id,
			'users_wallid': info['userid']
		}
		self.db.query_db(query,data)
		return info['userid']

	def wall_message(self, info, id):
		query = "INSERT INTO messages (message, user_id, users_wallid, created_at) VALUES (:message, :author, :users_wallid, NOW())"
		data = {
			'message': info['message'],
			'author': info['author'],
			'users_wallid': id
		}
		self.db.query_db(query, data)
		

	def show_all_users(self):
		query = "SELECT * FROM users ORDER BY level asc"
		return self.db.query_db(query)

	def admin_edit_user(self, id):
		query ="SELECT * FROM users WHERE users.id = :id"
		data = { 'id': id }
		return self.db.query_db(query, data)

	def edit_profile(self, id):
		query = "SELECT * FROM users WHERE users.id = :id"
		data = { 'id': id }
		return self.db.query_db(query, data)

	def update_profile_info(self, info, id):
		query = "UPDATE users SET email = :email, first_name = :first_name, last_name = :last_name WHERE users.id = :id"
		data = {
			'email': info['email'],
			'first_name': info['first_name'],
			'last_name': info['last_name'],
			'id': id
		}
		self.db.query_db(query, data)

	def update_profile_password(self, info, id):
		pw_hash = self.bcrypt.generate_password_hash(info['password'])
		query = "UPDATE users SET password = :password WHERE users.id = :id"
		data = {
			'password': pw_hash,
			'id': id
		}
		self.db.query_db(query, data)

	def update_profile_desc(self, info, id):
		query = "UPDATE users SET description = :description WHERE users.id = :id"
		data = {
			'description': info['description'],
			'id': id
		}
		self.db.query_db(query, data)

	def admin_update_userinfo(self, info, id):
		query = "UPDATE users SET email = :email, first_name = :first_name, last_name = :last_name, level = :user_level WHERE users.id = :id"
		data = {
			'email': info['email'],
			'first_name': info['first_name'],
			'last_name': info['last_name'],
			'user_level': info['user_level'],
			'id': id
		}
		self.db.query_db(query, data)

	def admin_update_password(self, info, id):
		pw_hash = self.bcrypt.generate_password_hash(info['password'])
		query = "UPDATE users SET password = :password WHERE users.id = :id"
		data = {
			'password': pw_hash,
			'id': id
		}
		self.db.query_db(query, data)


	def register_new(self, info):
		errors = {}

		if not info['reg_fname'] or len(info['reg_fname']) < 2:
			errors.update({'fname': 'First name must be at least 2 characters long'})
		if not info['reg_lname'] or len(info['reg_lname']) < 2:
			errors.update({'lname':'Last name must be at least 2 characters long'})
		if not EMAIL_REGEX.match(info['reg_email']):
			errors.update({'email':'Email must be a valid email address'})
		if len(info['reg_password']) < 8:
			errors.update({'password':'Password must be at least 8 characters long'})
		if info['reg_confirm'] != info['reg_password']:
			errors.update({'confirm_password':'Passwords must be matching'})
		if len(errors) > 0:
			return errors
		else:
			pw_hash = self.bcrypt.generate_password_hash(info['reg_password'])
			level = 'Normal'
			query = "INSERT INTO users (first_name, last_name, email, password, level, created_at, updated_at) VALUES (:first_name, :last_name, :email, :password, :level, NOW(), NOW())"
			data = {
				'first_name': info['reg_fname'],
				'last_name':info['reg_lname'],
				'email': info['reg_email'],
				'password': pw_hash,
				'level': level
			}
			self.db.query_db(query, data)
		return 'registered'