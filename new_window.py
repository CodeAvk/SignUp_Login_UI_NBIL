from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.core.window import Window
from kivy.uix.textinput import TextInput


class SignUpScreen(Screen):
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
                    App.get_running_app().root.current = "Login"

   


class LoginScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass
kv=Builder.load_file('new_window.kv')



class AwesomeApp(App):
    def build(self):
        return kv
    

if __name__== "__main__":
    AwesomeApp().run()
