from flask_login import LoginManager

login_manager = LoginManager()

setattr(login_manager, "login_view", "admin.sign_in")
setattr(login_manager, "login_message_category", "info")
