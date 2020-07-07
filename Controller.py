import cheroot
from webpy import web
from Models import RegisterModel, LoginModel, Posts
from pymongo import MongoClient

web.config.debug = False

urls = (
    "/", 'Home',
    '/register', 'Register',
    '/login', 'Login',
    '/logout', 'Logout',
    '/postregistration', 'PostRegistration',
    '/check-login', 'CheckLogin',
    '/discover', 'Discover',
    '/post-activity', 'PostActivity',
    '/settings', 'UserSettings',
    '/update-settings', 'UpdateSettings',
    '/profile/(.*)', 'UserProfile'
)

app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore("sessions"), initializer={"user": None})
session_data = session._initializer

render = web.template.render("Views/Templates", base="MainLayout",
                             globals={'session': session_data, 'current_user': session_data["user"]})


# Classes/Routes
class Home:
    def GET(self):
        data = type('obj', (object,), {"username": "ali1", "password": "bones"})

        login = LoginModel.LoginModel()
        isCorrect = login.check_user(data)

        if isCorrect:
            session_data["user"] = isCorrect

        post_model = Posts.Posts()
        posts = post_model.get_all_posts()
        return render.Home(posts)


class Discover:
    def GET(self):
        return render.Discover()


class Register:
    def GET(self):
        return render.Register()


class Login:
    def GET(self):
        return render.Login()


class CheckLogin:
    def POST(self):
        data = web.input()
        login = LoginModel.LoginModel()
        isCorrect = login.check_user(data)

        if isCorrect:
            session_data["user"] = isCorrect
            return isCorrect

        return "error"

class PostActivity:
    def POST(self):
        data = web.input()
        data.username = session_data['user']['username']

        post_model = Posts.Posts()
        post_model.insert_post(data)
        return "success"

class PostRegistration:
    def POST(self):
        data = web.input()
        reg_model = RegisterModel.RegisterModel()
        reg_model.add_user(data)

        return data.username

class UpdateSettings:
    def POST(self):
        data = web.input()
        data.username = session_data["user"]["username"]
        settings_model = LoginModel.LoginModel()
        if settings_model.update_info(data):
            return "success"
        else:
            return "An error occurred"




class Logout:
    def GET(self):
        session['user'] = None
        session_data['user'] = None
        session.kill()
        return "success"


if __name__ == "__main__":
    app.run()
