from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivymd.uix.textfield import MDTextField
import pyrebase
import json


# class CustomMDTextField(MDTextField):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.hint_text_size = 5  # Set hint text size to 15

#     def get_hint_text_size(self):
#         return self.hint_text_size  # Always return 15

class FirebaseManager:
    def __init__(self):
        firebase_conf = {
            "apiKey": "AIzaSyDKvwq5IpvotqYPhynB-_G_ReY_Mylg254",
            "authDomain": "niyantranam-backend.firebaseapp.com",
            "databaseURL": "https://niyantranam-backend-default-rtdb.firebaseio.com",
            "projectId": "niyantranam-backend",
            "storageBucket": "niyantranam-backend.appspot.com",
            "messagingSenderId": "715506007512",
            "appId": "1:715506007512:web:0efbc6d8fe1817c69ac6ad",
            "measurementId": "G-8QKM6T52XY"
        }
        self.firebase = pyrebase.initialize_app(firebase_conf)
        self.db = self.firebase.database()

class SignUpScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.firebase_manager = FirebaseManager()

    def creator(self):
        cond=True
        first_name_input = self.ids.first_name_input.text
        last_name_input = self.ids.last_name_input.text
        organization_input = self.ids.organization_input.text
        email_input = self.ids.email_input.text
        password_input = self.ids.password_input.text
        
        database_data=self.firebase_manager.db.get()
        for single_data in database_data.each():
            dict = single_data.val()
            if "email" in dict and dict["email"] == email_input:
                cond = False
                self.ids.error_label.text = "User already exists"
        
        if cond==True:
            data = {
                "first_name": first_name_input,
                "last_name": last_name_input,
                "organization": organization_input,
                "email": email_input,
                "password": password_input
            }
            self.firebase_manager.db.child(first_name_input).set(data)
            MDApp.get_running_app().root.current = "Login"





class LoginScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.firebase_manager = FirebaseManager()

    def print(self):
        username = self.ids.username_input.text
        password = self.ids.password_input.text

        user_data = self.firebase_manager.db.child(username).get()
        # print("user_data:", user_data) 0x0000020AD23D2B60
        print("user_data:", user_data.val()["password"]) #0x0000020AD23D2B60
        
        retrive_password=user_data.val()["password"]
        retrive_organization=user_data.val()["organization"]
        if(retrive_password==password):
            print(f"Welcome to the {retrive_organization}")
        else:
            print("No User found")    
        
        

        

        
        



class ForgotPasswordScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class AwesomeApp(MDApp):
    def build(self):
        kv = Builder.load_file('new_window.kv')
        return kv

if __name__ == "__main__":
    AwesomeApp().run()