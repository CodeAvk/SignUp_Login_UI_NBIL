from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivymd.uix.dropdownitem import MDDropDownItem
from kivy.uix.textinput import TextInput
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivymd.uix.button import MDRectangleFlatButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
import os
import base64
import time 
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
        self.current_username_login = None 

    def print(self):
        username = self.ids.username_input.text
        password = self.ids.password_input.text

        user_data = self.firebase_manager.db.child(username).get()
        # print("user_data:", user_data) 0x0000020AD23D2B60
        print("user_data:", user_data.val()["password"]) #0x0000020AD23D2B60
        
        retrive_password=user_data.val()["password"]
        retrive_organization=user_data.val()["organization"]
        if(retrive_password==password):

             # Fetch username from the user data
            retrive_username = user_data.val().get("first_name")
            self.current_username_login = retrive_username 

             # Create a reference to the WelcomeScreen
            welcome_screen = MDApp.get_running_app().root.get_screen("Welcome")

            # Pass the username to the WelcomeScreen
            # welcome_screen.update_username(retrive_username)



            # print(f"Welcome to the {retrive_organization}")
            dialog = MDDialog(title="Login Successful", text=f"Welcome to the{retrive_username} {retrive_organization}")
            dialog.open()
            app = MDApp.get_running_app()
            # app.set_generated_otp(generated_otp)
            app.root.current = "Welcome"

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
    
class WelcomeScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.firebase_manager = FirebaseManager()

    # def on_dropdown_select(self, instance, option):
    #     print(f'Selected option: {option}')
    
    # def update_username(self, username):
    #     # Update the options_button text with the retrieved username
    #     options_button = self.ids.options_button
    #     options_button.text = f"Welcome, {username}" if username else "Options"

    # def get_username(self):
    #     # Fetch the current username from your data or session
    #     return "Current_User"  # Replace this with the actual username
class WindowManager(ScreenManager):
    pass


    # def __init__(self, text="", path="", **kwargs):
    #     super().__init__(text=text, path=path, **kwargs)
    #     self.custom_data = None

class AwesomeApp(MDApp):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.firebase_manager = FirebaseManager()
    def build(self):
        kv = Builder.load_file('new_window.kv')
        return kv
    def set_generated_otp(self, otp):
        AwesomeApp.generated_otp = otp
    def on_option_select(self, text):
        print(f"Selected option: {text}") 
    def save_to_firebase(self, text):
        # firebase_manager = self.root.get_screen("Welcome").firebase_manager
        login_screen = self.root.get_screen("Login")
        
        # Fetch current username from LoginScreen
        current_user = login_screen.current_username_login

        # Create a reference to the current user's node
        user_ref =self.firebase_manager.db.child(current_user)
        timestamp = time.time()
        new_child_name = "GCODES"  # You can use any desired name
        new_child_ref = user_ref.child(new_child_name)

        # Fetch the count of existing work entries for the user
        user_data = user_ref.push({"text": text, "timestamp": timestamp})
        
        


    def open_from_firebase(self):
        login_screen = self.root.get_screen("Login")
            
        # Fetch current username from LoginScreen
        current_user = login_screen.current_username_login

        # Create a reference to the current user's "GCODES" node
        user_ref = self.firebase_manager.db.child(current_user).child("GCODES")
        
        # Fetch all entries under "GCODES" node
        all_entries = user_ref.get()
        
        # Create a BoxLayout to hold the widgets
        content = BoxLayout(orientation='vertical', spacing=10)
        
        if all_entries.each():
            for entry in all_entries.each():
                text = entry.val()  # Get the text directly
                if isinstance(text, dict):
                    text = str(text.get('text', ''))
                
                # Create a Label for text
                text_label = Label(text=str(text))
                
                # Create buttons
                open_button = MDRectangleFlatButton(text="Open")
                delete_button = MDRectangleFlatButton(text="Delete")
                
                # Define button actions
                open_button.bind(on_press=lambda instance, label=text_label.text: self.open_entry(label))
                delete_button.bind(on_press=lambda instance, entry_key=entry.key(): self.delete_entry(current_user, entry_key))
                
                # Add Label and buttons to the layout
                entry_layout = BoxLayout(orientation='horizontal', spacing=10)
                entry_layout.add_widget(text_label)
                entry_layout.add_widget(open_button)
                entry_layout.add_widget(delete_button)
                
                content.add_widget(entry_layout)
        else:
            no_entry_label = Label(text="No entries found.")
            content.add_widget(no_entry_label)

        # Create a Popup to display the entries
        popup = Popup(title='Text Entries', content=content, size_hint=(None, None), size=(500, 500))
        popup.open()

    def open_entry(self, text):
        # Handle opening an entry (e.g., display it in another screen or popup)
        welcome_screen = self.root.get_screen("Welcome")
        text_input = welcome_screen.ids.editor  # Access the TextInput widget

        # Set the text in the TextInput of the WelcomeScreen
        text_input.text = text

        # Change the screen to the WelcomeScreen (if needed)
        self.root.current = "Welcome"

    def delete_entry(self, current_user, entry_key):
        # Handle deleting an entry from Firebase
        user_ref = self.firebase_manager.db.child(current_user).child("GCODES")
        user_ref.child(entry_key).remove()
        # After deletion, you might want to refresh the displayed entries or update the UI accordingly
    def choose_file(self):
        desktop_path = os.path.expanduser("~/Desktop/GCodes")  # Get the path to the desktop directory

        file_chooser = FileChooserListView(path=desktop_path)  # Set the path to the desktop directory
        file_chooser.filters = ['*.gcode']
        file_chooser.bind(on_submit=self.selected)

        popup = Popup(title='Select .gcode file', content=file_chooser, size_hint=(0.9, 0.9))
        popup.open()

    def selected(self, instance, value,*args):
        if value:
            file_path = value[0]
            welcome_screen = self.root.get_screen("Welcome")
            file_path_text = welcome_screen.ids.file_path_text
            file_path_text.text = file_path

            # Here, you can upload 'file_path' to the cloud or perform other operations
             # Upload the selected GCODE file to Firebase
            # self.upload_file(file_path)
    def upload_file(self, file_path):
        firebase_manager = self.firebase_manager
        shared_files_ref = firebase_manager.db.child("SharedFiles")  # Reference to the shared files node

        # Extract the file name from the file path
        file_name = os.path.basename(file_path)
        print(file_name)


        # Convert byte stream to base64 encoded string
        with open(file_path, 'rb') as file:
            file_data = file.read()
            encoded_data = base64.b64encode(file_data).decode('utf-8')

            # Create a dictionary with the file name as key and encoded data as value
        # data_to_push = {file_name.split('.')[0]: encoded_data}  # Using split to remove file extension
        data_to_push = {"name": file_name, "data": encoded_data}  # Using split to remove file extension
        print(data_to_push)

        # Push the dictionary containing file name and encoded data to the shared files node
        shared_files_ref.push(data_to_push)

        dialog = MDDialog(title="Upload Successful", text="File uploaded successfully to shared files.")
        dialog.open()
        
    def show_cloud_files(self):
        firebase_manager = self.firebase_manager
        shared_files_ref = firebase_manager.db.child("SharedFiles")  # Reference to the shared files node

        # Fetch all entries under "SharedFiles" node
        all_files = shared_files_ref.get()

        # Create a BoxLayout to hold the list of files
        content = BoxLayout(orientation='vertical', spacing=10)

        if all_files:
            for file_entry in all_files.each():
                file_name = file_entry.val().get('name')  # Get the file name without extension
                file_data = file_entry.val().get('data')  # Get the file data
                # print(file_name,file_data)
                # Create a BoxLayout to hold the label and button
                file_layout = BoxLayout(orientation='horizontal', spacing=10)

                # Create a label to represent the file entry
                file_label = Label(text=f"File: {file_name}")  # Display filename or any identifier
                file_layout.add_widget(file_label)

                # Create a button to open the file or handle the data
                file_button = Button(text="Open File")

                # Bind button press action to open the file or handle the data
                file_button.bind(
                    on_release=lambda instance, data=(file_name, file_data): self.open_cloud_file(data)
                )
                file_layout.add_widget(file_button)

                # Add the label and button to the layout
                content.add_widget(file_layout)
        else:
            no_file_label = Label(text="No files found.")
            content.add_widget(no_file_label)

        # Create a Popup to display the files
        popup = Popup(title='Cloud Files', content=content, size_hint=(None, None), size=(500, 500))
        popup.open()
            
    def open_cloud_file(self, data):
            # Access the TextInput widget from the WelcomeScreen
        welcome_screen = self.root.get_screen("Welcome")
        text_input = welcome_screen.ids.editor  # Access the TextInput widget

        # Get the file data from the passed data tuple
        file_name, file_data = data

        # Decode the file data from base64 to text
        decoded_data = base64.b64decode(file_data).decode('latin-1')

        # Set the decoded data in the TextInput
        text_input.text = decoded_data

        # Change the screen to the WelcomeScreen
        self.root.current = "Welcome"

        
        





    
        

if __name__ == "__main__":
    AwesomeApp().run()