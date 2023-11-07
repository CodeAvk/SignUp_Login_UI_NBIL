from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
import pyrebase


class SignUpScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
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
        firebase=pyrebase.initialize_app(firebase_conf)
        self.db=firebase.database() #by using self.db we can acces it in creator function
        data1={"Email":"xyz@gmail1.com","Password":"123"}
        data2={"Email":"xyz@gmail2.com","Password":"123"}
        data3={"Email":"xyz@gmail3.com","Password":"123"}
        # db.child("Parent").push(data) 
        # defining custome key for data
        # db.child("CustomKey1").set(data1)
        # db.child("CustomKey2").set(data2)
        # db.child("CustomKey3").set(data3)
        # reading Data
        # database_data=db.get()
        # print(database_data.val())
        # for s_d in database_data.each():
        #     print(s_d.val())
    def creator(self):
        first_name_input = self.ids.first_name_input.text
        last_name_input = self.ids.last_name_input.text
        organization_input = self.ids.organization_input.text
        email_input = self.ids.email_input.text
        password_input = self.ids.password_input.text
        data = {
        "first_name": first_name_input,
        "last_name": last_name_input,
        "organization": organization_input,
        "email": email_input,
        "password": password_input
    }
        self.db.child(first_name_input).set(data)
        MDApp.get_running_app().root.current = "Login"


    def check_inputs(self):
        # Get references to your TextInput widgets
        first_name_input = self.ids.first_name_input
        last_name_input = self.ids.last_name_input
        organization_input = self.ids.organization_input
        email_input = self.ids.email_input
        password_input = self.ids.password_input

        # Create a list of (TextInput, label) pairs for error messages
        fields = [(first_name_input, "First Name"),
                  (last_name_input, "Last Name"),
                  (organization_input, "Organization/Institution"),
                  (email_input, "Email Address"),
                  (password_input, "Password")]

        missing_fields = []

        # Check if any of the input fields are empty
        for field, label in fields:
            if not field.text:
                missing_fields.append(label)

        if len(missing_fields) == 1:
            # Show an error message specifying which field is required
            error_label = self.ids.error_label
            error_label.text = f"The '{missing_fields[0]}' field is required."
        elif len(missing_fields) > 1:
            # More than one field is missing, show a general error message
            error_label = self.ids.error_label
            error_label.text = "Please fill in all fields"
        else:
            # All fields are filled, so clear the error message
            error_label = self.ids.error_label
            error_label.text = ""

            # Check email format (contains @ symbol)
            if '@' not in email_input.text:
                error_label.text = "Invalid email format."
            else:
                # Check password strength (you can add your own criteria here)
                password = password_input.text
                if not (any(c.isalpha() for c in password) and
                        any(c.isdigit() for c in password) and
                        any(not c.isalnum() for c in password)):
                    error_label.text = "Password must include letters, numbers, and special characters."
                else:
                    
                    # Reset all TextInput fields to default values
                    first_name_input.text = ""
                    last_name_input.text = ""
                    organization_input.text = ""
                    email_input.text = ""
                    password_input.text = ""

                    # Transition to the LoginScreen
                    MDApp.get_running_app().root.current = "Login"

   


class LoginScreen(Screen):
      pass
    

class ForgotPasswordScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass




class AwesomeApp(MDApp):
    def build(self):
        kv=Builder.load_file('new_window.kv')
        


         
        return kv
    

if __name__== "__main__":
    AwesomeApp().run()
