from system.core.controller import *

class Dashboards(Controller):
	def __init__(self, action):
		super(Dashboards, self).__init__(action)
		self.load_model('Dashboard')
		self.db = self._app.db
   
	def index(self):
		return self.load_view('index.html')

	def signout(self):
		session.clear()
		return redirect('/')

	def show_wall(self, id):
		print id
		user = self.models['Dashboard'].show_wall_user(id)
		messages = self.models['Dashboard'].show_wall_messages(id)
		comments = self.models['Dashboard'].show_wall_comments(id)
		
		
		return self.load_view('wall.html', user = user[0], messages = messages, comments = comments)

	def send_message(self, id):
		message = self.models['Dashboard'].wall_message(request.form, id)
		return self.show_wall(id)

	def send_comment(self, id):
		comment = self.models['Dashboard'].wall_comment(request.form, id)
		return self.show_wall(comment)


	def add_user(self):
		return self.load_view('adminnew.html')

	def signin_page(self):
		return self.load_view('signin.html')

	def user_profile(self, id):
		user = self.models['Dashboard'].edit_profile(id)
		return self.load_view('edituser.html', user = user)

	def admin_edit_page(self, id):
		user = self.models['Dashboard'].admin_edit_user(id)
		return self.load_view('adminedit.html', user = user[0])

	def delete_user(self, id):
		self.models['Dashboard'].delete(id)
		return redirect('/viewusers')

	def update_profileinfo(self, id):
		user = self.models['Dashboard'].update_profile_info(request.form, id)
		return redirect('/viewusers')

	def update_profilepass(self, id):
		user = self.models['Dashboard'].update_profile_password(request.form, id)
		return redirect('/viewusers')

	def update_profiledesc(self, id):
		user = self.models['Dashboard'].update_profile_desc(request.form, id)
		return redirect('viewusers')

	def admin_update_user(self, id):
		self.models['Dashboard'].admin_update_userinfo(request.form, id)
		if session['logged_user']['level'] == 'Admin':
			return redirect('/viewusers')

	def admin_update_password(self, id):
		self.models['Dashboard'].admin_update_password(request.form, id)
		if session['logged_user']['level'] == 'Admin':
			return redirect('/viewusers')

	def signin_user(self):
		signedin = self.models['Dashboard'].sign_in(request.form)
		if 'logged_user' in signedin:
			session['logged_user'] = signedin['logged_user']
			return redirect('/viewusers')
		else:
			session.clear()
			errors = signedin
			flash(errors)
		return redirect('/signin')

	def view_admin_dash(self):
		users = self.models['Dashboard'].show_all_users()
		return self.load_view('adminpage.html', users = users)

	def view_users(self):
		users = self.models['Dashboard'].show_all_users()
		if session['logged_user']['level'] == 'Admin':
			return self.load_view('adminpage.html', users = users)
		elif session['logged_user']['level'] == 'Normal':
			return self.load_view('allusers.html', users = users)


	def register_page(self):
		return self.load_view('register.html')

	def register_user(self):
		newuser = self.models['Dashboard'].register_new(request.form)
		if newuser == 'registered':
			return self.load_view('signin.html')
		else:
			session.clear()
			errors = newuser
			flash(errors)
		return redirect('/registerpage')

	def admin_newuser(self):
		newuser = self.models['Dashboard'].register_new(request.form)
		if newuser == 'registered':
			return self.view_admin_dash()
		else:
			session.clear()
			errors = newuser
			flash(errors)
		return redirect('/addnew')