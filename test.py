MDBoxLayout:
        id: main_layout_forgotpassword
        orientation: 'horizontal'
        # size_hint: .7, 1
        # size: self.size[0] * 2, self.size[1] * 2
        canvas.before:
            Color:
                rgba: 4/255, 7/255, 30/255,  1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                # size: self.size[0] * 2, self.size[1] * 2

        MDBoxLayout:
            id: left_layout_forgotpassword
            orientation: 'vertical'
            size_hint: .5, .5

            Image:
                source: './UI niyantranam.jpg'  # Replace with the path to your image
                size: 400, 600
                allow_stretch: True
                keep_ratio: False

        RelativeLayout:
            id: right_layout_forgotpassword
            MDBoxLayout:
                orientation: 'vertical'
                size_hint: None, None
                width: "470dp"
                height: self.minimum_height
                center_x: self.parent.center_x
                top: self.parent.top - 10
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                spacing: 10 

                # Additional BoxLayout for Labels, TextInputs, and Button
                MDBoxLayout:
                    id: sub_layout_forgotpassword
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height * 1.1
                    center_x: self.parent.center_x
                    padding: [10, 0]
                    spacing: 10 
                    # size_hint: 1, 1                    
                    canvas.before:
                        Color:
                            rgba: 36/255, 29/255, 58/255,  1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [30, 30, 30, 30]
                            # color: 1, 0, 0, 1
                            # color: 0.7, 0.7, 0.7, 1
                    MDLabel:
                        text: 'Forgot Password ?'
                        size_hint: None, None
                        size: "500dp", "30dp"
                        halign: "center"
                        # pos_hint: {'center_x': 0.5,'center_y': 0.5}
                        font_size:24
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1  # White color (R, G, B, A)

                    # MDLabel:
                    #     text: 'New member?Create a new account. Sign Up!'
                    #     size_hint: None, None
                    #     size: "500dp", "30dp"
                    #     halign: "center"
                    #     theme_text_color: "Custom"
                    #     text_color: 1, 1, 1, 1  # White color (R, G, B, A)
                    MDLabel:
                        text: ''
                        size_hint: None, None
                        size: "500dp", "20dp"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                    # MDBoxLayout:
                    #     orientation: 'horizontal'
                    #     size_hint_y: None
                    #     height: 30  # Adjust the height as needed
                    #     center_x: self.parent.center_x
                    #     padding: 33.5, 0
                    #     spacing: 10 
                    #     TextInput:
                    #         id: first_name_input  # Add the ID
                    #         hint_text: 'Firstname'
                    #         # input_filter: "str,regex=[a-zA-Z]+"
                    #         foreground_color: (1, 1, 1, 1)
                    #         size_hint: None, None
                    #         size: 245, 40
                    #         pos_hint: {'center_x': 0.5}
                    #         font_size:20
                    #         bold: True  # Adjust the width as needed
                    #         hint_text_color: 1, 1, 1, 1
                    #         background_color: 0, 0, 0, 1  # Fully transparent background                            
                    #     TextInput:
                    #         id: last_name_input  # Add the ID
                    #         foreground_color: (1, 1, 1, 1)
                    #         hint_text: 'Secondname'
                    #         # input_filter: "str,max_length=20"
                    #         size_hint: None, None
                    #         size: 245, 40
                    #         pos_hint: {'center_x': 0.5}
                    #         hint_text_color: 1, 1, 1, 1
                    #         background_color: 0, 0, 0, 1
                    #         font_size:20
                    #         bold: True  # Adjust the width as needed

                    MDTextField:
                        id: userid_input
                        hint_text: 'Username'
                        icon_right: 'account'
                        # required:True
                        # theme_text_color: "Secondary"
                        hint_text_color_normal: "white"
                        icon_right_color_normal: "white"
                        hint_text_color: 1, 1, 1, 1
                        background_color: 0, 0, 0, 1
                        foreground_color: 1,1,1,1
                        size_hint: None, None
                        size: 500, 40
                        pos_hint: {'center_x': 0.5}
                        font_size: 20
                        bold: True
                        write_tab:False
                        # background_color: 0, 0, 0, 0.5
                        
                    MDTextField:
                        id: newpassword_input
                        
                        hint_text: 'New Password'
                        icon_right:'eye-off'
                        password:True
                        hint_text_color_normal: "white"
                        icon_right_color_normal: "white"
                        # input_filter: "str,regex=[a-zA-Z0-9@.]+"
                        foreground_color: (1, 1, 1, 1)
                        size_hint: None, None
                        size: 500, 40
                        pos_hint: {'center_x': 0.5}
                        font_size:20
                        bold: True
                        hint_text_color: 1, 1, 1, 1
                        background_color: 0, 0, 0, 1
                        write_tab:False
                    MDTextField:
                        id: cnfpassword_input
                        
                        hint_text: 'Confirm Password'
                        icon_right:'eye-off'
                        password:True
                        hint_text_color_normal: "white"
                        icon_right_color_normal: "white"
                        # input_filter: "str,regex=[a-zA-Z0-9@.]+"
                        foreground_color: (1, 1, 1, 1)
                        size_hint: None, None
                        size: 500, 40
                        pos_hint: {'center_x': 0.5}
                        font_size:20
                        bold: True
                        hint_text_color: 1, 1, 1, 1
                        background_color: 0, 0, 0, 1
                        write_tab:False    
                    # BoxLayout:
                    #     size_hint:.85,None
                    #     height:"50dp"
                    #     pos_hint: {'center_x': 0.5,'center_y':0.4}
                    #     # spacing:"5dp" #Not need this time
                    #     MDCheckbox:
                    #         id:cb
                    #         size_hint:None,None
                    #         pos_hint: {'center_x': 0.5,'center_y':0.5}
                    #         height:"30dp"  
                    #         width:"30dp"
                    #         on_press:
                    #             password_input.password=False if password_input.password == True else True

                    #     MDLabel:
                    #         text:"Show Password"
                    #         foreground_color:1,1,1,1
                    #         markup:True
                    #         pos_hint: {'center_x': 0.5,'center_y':0.5}
                    #         on_ref_press:
                    #             cb.active= False if cb.active == True else True
                    #             password_input.password=False if password_input.password == True else True

                        

                    BoxLayout:
                        # orientation:"horizontal"
                        size_hint:.25,None
                        # height:"20dp"
                        pos_hint: {'center_x': 0.5,'center_y':0.3}
                        spacing:"10dp"


                        # orientation: 'horizontal'
                        # size_hint_y: None
                        # height: 30  # Adjust the height as needed
                        # center_x: self.parent.center_x
                        # padding: 60, 0
                        # spacing: 10 
                        
                            
                        # MDFlatButton:
                        #     text:"SIGN IN"
                        #     font_size:"22dp"
                        #     size_hint: None, None
                        #     size: 200, 40
                        #     md_bg_color:"#FFFFFF"
                        # MDFlatButton:
                        #     text:"SIGN UP"
                        #     font_size:"22dp"
                        #     size_hint_x:.3
                        MyButton:
                            text: 'RESET'
                            size_hint: None, None
                            size: 200, 40
                            pos_hint: {'center_x': 0.5}
                            font_size:20
                            bold: True
                            on_release: root.check_inputs()
                        # MyButton:
                        #     text: 'Forgot Password'
                        #     size_hint: None, None
                        #     size: 200, 40
                        #     pos_hint: {'center_x': 0.5}
                        #     font_size:20
                        #     bold: True
                        #     on_release: app.root.current="ForgotPassword" # Dont Delete this 
 
                        # MyButton:
                        #     text: 'SIGN UP'
                        #     size_hint: None, None
                        #     size: 200, 40
                        #     pos_hint: {'center_x': 0.5}
                        #     font_size:20
                        #     bold: True
                        #     on_release: root.check_inputs()            
                            
                    # MyButton:
                    #     text: 'LOGIN'
                    #     size_hint: None, None
                    #     size: 200, 40
                    #     pos_hint: {'center_x': 0.5}
                    #     font_size:20
                    #     bold: True
                    #     on_release: root.check_inputs()
                    Label:
                        text: ''
                        size_hint: None, None
                        size: 200, 5
                        pos_hint: {'center_x': 0.5}
                        font_size:20
                        bold: True

                    Label:
                        id: error_label
                        text: ''
                        size_hint: None, None
                        size: 200, 5
                        pos_hint: {'center_x': 0.5}
                        font_size: 16
                        color: 1, 0, 0, 1  # Red color for error messages
                    