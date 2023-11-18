from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
import pyrebase
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart  # Add this impor
import random


# class CustomMDTextField(MDTextField):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.hint_text_size = 5  # Set hint text size to 15

#     def get_hint_text_size(self):
#         return self.hint_text_size  # Always return 15
# Gotp = 0
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
        
        # Check if database_data is None or empty
        if not database_data or database_data.each() is None:
            # If no data is present, add the new user directly
            data = {
                "first_name": first_name_input,
                "last_name": last_name_input,
                "organization": organization_input,
                "email": email_input,
                "password": password_input
            }
            self.firebase_manager.db.child(first_name_input).set(data)
            MDApp.get_running_app().root.current = "Login"
        else:
            # Data is present, check if the email already exists
            cond = True
            for single_data in database_data.each():
                dict_data = single_data.val()
                if "email" in dict_data and dict_data["email"] == email_input:
                    cond = False
                    dialog = MDDialog(title="Signup Information", text="User already exists")
                    dialog.open()
        
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
            # print(f"Welcome to the {retrive_organization}")
            dialog = MDDialog(title="Login Successful", text=f"Welcome to the {retrive_organization}")
            dialog.open()
        else:
            # print("No User found")    
            dialog = MDDialog(title="Login Failed", text="No User Found")
            dialog.open()


    def handle_forgot_password(self):
        username = self.ids.username_input.text

        if not username:
            dialog = MDDialog(title="Username Required", text="Please enter your username to proceed.")
            dialog.open()
        else:
            # Send OTP functionality here
            self.send_otp_to_email(username)

    def generate_otp(self):
        return str(random.randint(1000, 9999))        

    def send_otp_to_email(self, username):
        user_data = self.firebase_manager.db.child(username).get()

        if user_data.val():
            email = user_data.val().get("email")
            generated_otp = self.generate_otp() #i want to acces this generated_otp in side OtpVerificationScreen class
            # Gotp = self.generate_otp() #i want to acces this generated_otp in side OtpVerificationScreen class
            # Masking the email
            masked_email = email[0:2] + '*'*(email.index('@')-2) + email[email.index('@'):]
            # Example: if email is "akvsmlavk@gmail.com", masked_email will be "ak******k@gmail.com"

            gmail_user = 'avksmlavk@gmail.com'  # Replace with your Gmail address
            gmail_password = 'kxbg sdom epmp oszh'  # Replace with your Gmail password

            sent_from = gmail_user
            to = email
            subject = 'Your OTP'
            body = f'Your OTP is: {generated_otp}'
            # body = f'Your OTP is: {Gotp}'

            msg = MIMEMultipart()
            msg['From'] = sent_from
            msg['To'] = to
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            try:
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login(gmail_user, gmail_password)
                server.sendmail(sent_from, to, msg.as_string())
                server.close()

                print(f"OTP sent to {to}: {generated_otp}")

                dialog = MDDialog(title="OTP Sent", text=f"An OTP has been sent to your registered {masked_email}")
                dialog.open()

                app = MDApp.get_running_app()
                app.set_generated_otp(generated_otp)
                app.root.current = "OtpVerificationScreen"
            except Exception as e:
                print(f"Failed to send email. Error: {str(e)}")

                dialog = MDDialog(title="Error", text="Failed to send OTP via email.")
                dialog.open()
        else:
            dialog = MDDialog(title="User Not Found", text="Username does not exist.")
            dialog.open()   
        
    
        

        
        



class ForgotPasswordScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.firebase_manager = FirebaseManager()

    def reset_password(self):
        username = self.ids.userid_input.text
        new_password = self.ids.new_password_input.text
        confirm_password = self.ids.cnf_password_input.text

        # Check if new password matches confirm password
        if new_password != confirm_password:
            dialog = MDDialog(title="Password Mismatch", text="Passwords do not match.")
            dialog.open()
            return

        # Retrieve user data from the database
        user_data = self.firebase_manager.db.child(username).get()

        # Check if the user exists
        if user_data.val():
            # Update the password
            self.firebase_manager.db.child(username).update({"password": new_password})
            dialog = MDDialog(title="Password Reset", text="Password updated successfully.")
            dialog.open()

            # Add this line to switch to the login screen after password update
            app = MDApp.get_running_app()
            app.root.current = "Login"

        else:
            dialog = MDDialog(title="User Not Found", text="Username does not exist.")
            dialog.open()

    def check_inputs(self):
        # Additional validation or checks if needed before resetting the password
        self.reset_password()
        
class OtpVerificationScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.generated_otp = None

    # def set_generated_otp(self, otp):
    #     self.generated_otp = otp    

    def check_inputs(self):
        entered_otp = self.ids.otp_input.text  # Get entered OTP from the TextInput
        print(f"inside otpverification {self.generated_otp}")

        app = MDApp.get_running_app()
        generated_otp = app.generated_otp

        # You'd want to fetch the expected OTP sent to the user's email from the previous screen
        expected_otp = "1234"  # Replace this with the expected OTP

        if entered_otp == generated_otp:
            # If entered OTP matches the expected OTP, navigate to ForgotPasswordScreen
            app = MDApp.get_running_app()
            app.root.current = "ForgotPassword"
            
        else:
            dialog = MDDialog(title="Invalid OTP", text="Entered OTP is incorrect. Please try again.")
            dialog.open()
    
    

class WindowManager(ScreenManager):
    pass

class AwesomeApp(MDApp):
    def build(self):
        kv = Builder.load_file('new_window.kv')
        return kv
    def set_generated_otp(self, otp):
        AwesomeApp.generated_otp = otp
if __name__ == "__main__":
    AwesomeApp().run()