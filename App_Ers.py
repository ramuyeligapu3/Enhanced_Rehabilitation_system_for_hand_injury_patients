import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import mediapipe as mp
import HandExercise  # Import custom module
import serial.tools.list_ports
from cvzone.SerialModule import SerialObject


# Initialize hand detector
hand_detector = HandExercise.Hand_Excerises_Detection()

# Define the CameraApp class
class CameraApp:
    def __init__(self, parent):
        self.parent = parent
        self.cam_window = tk.Toplevel(parent)  # Create a new window
        self.cam_window.geometry("1200x600")  # Set window size
        self.cam_window.title("Camera App")  # Set window title
        self.cam_window.resizable(False,False)
        self.cam_window.configure(bg='#3A7FF6') 
        self.imgtk = None  # Initialize PhotoImage variable

        # port connect button
        self.connect_button = tk.Button(self.cam_window, width=15, text='Connect port', bg='red',fg='white',command=self.find_available_port)  
        self.connect_button.place(x=970, y=40)

        # Left Frame for featured buttons
        left_frame = tk.Frame(self.cam_window, bg='#3A7FF6', highlightbackground="white", highlightthickness=2)
        left_frame.place(x=40, y=80, width=270, height=500)

        # Right Frame for camera label/ feed
        self.right_frame = tk.Frame(self.cam_window, bg='#3A7FF6', highlightbackground="white", highlightthickness=2)
        self.right_frame.place(x=320, y=80, width=630, height=500)

        # Rest Frame for finger status
        self.rest_frame = tk.Frame(self.cam_window, bg='#3A7FF6', highlightbackground="white", highlightthickness=2)
        self.rest_frame.place(x=960, y=80, width=200, height=500)

        # Label to display camera feed
        self.camera_label = tk.Label(self.right_frame,text="Camera Label",font=('Arial', 20, 'bold'),fg="white",bg='#3A7FF6')
        self.camera_label.pack()

        # Label for system description
        self.system_label = tk.Label(self.cam_window, text="With each exercise, you regain your strength", font=('Arial', 20, 'bold'), bg='#3A7FF6', fg='white')
        self.system_label.place(x=300,y=20)

        # Label for finger status heading
        self.finger_status_heading = tk.Label(self.rest_frame, text="Finger Status", font=('Arial', 12, 'bold'), bg='white', fg='#3A7FF6')
        self.finger_status_heading.pack(side="top", fill="x", padx=5, pady=5)

        # Text widget to display finger status
        self.finger_status_text = tk.Text(self.rest_frame, wrap="none")
        self.finger_status_text.pack(side="left", fill="y")

        # Scrollbar for finger status text
        self.scrollbar = ttk.Scrollbar(self.rest_frame, orient="vertical", command=self.finger_status_text.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.finger_status_text.config(yscrollcommand=self.scrollbar.set)

        # Initialize MediaPipe Hands module
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()

        # Buttons for different functionalities

        self.Live_button = tk.Button(left_frame, width=25, text='Live Exercise', bg='white',activebackground="#3A7FF6",activeforeground="white",fg="#3A7FF6",state='disabled', command=self.start_live_feed)
        self.Live_button.pack(pady=20)

        self.Video_button = tk.Button(left_frame, width=25, text='Recorded Exercises', bg='white',activebackground="#3A7FF6",activeforeground="white",fg="#3A7FF6",state='disabled', command=self.enable_button)
        self.Video_button.pack(pady=20)

        self.v1_button = tk.Button(left_frame, width=25, text='Video 1', state='disabled',activebackground="#3A7FF6",activeforeground="white",fg="#3A7FF6", bg='white', command=self.start_video_feed)
        self.v1_button.pack(pady=20)

        self.v2_button = tk.Button(left_frame, width=25, text='Video 2', bg='white',activebackground="#3A7FF6",activeforeground="white",fg="#3A7FF6", state='disabled')
        self.v2_button.pack(pady=20)

        self.v3_button = tk.Button(left_frame, width=25, text='Video 3', bg='white',activebackground="#3A7FF6",activeforeground="white",fg="#3A7FF6", state='disabled')
        self.v3_button.pack(pady=20)

        self.stop_button = tk.Button(left_frame, width=25, text='Start Exercise', bg='white',fg="black",state='disabled', command=self.stop_camera)
        self.stop_button.pack(pady=20)

        self.exit_button = tk.Button(left_frame, width=25, text='Exit', bg='white',activebackground="#3A7FF6",activeforeground="white",fg="#3A7FF6", command=self.exit_camera)
        self.exit_button.pack(pady=20)

        self.cap = None  # Initialize VideoCapture object
    
    # Method to find available ports
    def find_available_port(self):
        def check():
            available_ports = serial.tools.list_ports.comports()
            for port in available_ports:
                if "COM" in port.device:
                    return port.device
            return None

        port = check()

        if port:
            self.My_Serial = SerialObject(port, 9600, 1)  
            messagebox.showinfo("Port Connected", f"Connected to port: {port}",parent=self.cam_window)
            self.Live_button.config(state='normal')
            self.Video_button.config(state='normal')
            self.stop_button.config(state='normal')
            self.connect_button.config(bg='green',text='Port connected')
            self.stop_button.config(bg='green',fg='white')
            
        else:
            messagebox.showerror("Port Error", "No COM port available. Check your connections.",parent=self.cam_window)
            self.connect_button.config(bg='red',text='connect Port')
        

    # Method to start live camera feed
    def start_live_feed(self):
        self.stop_button.config(text='stop',bg="red",fg='white')
        if self.cap is not None:
            self.cap.release()  # Release any existing VideoCapture object
        self.cap = cv2.VideoCapture(0)
        self.display_camera_feed()
        
    # Method to start video feed
    def start_video_feed(self):
        self.stop_button.config(text='stop',bg="red",fg='white')
        if self.cap is not None:
            self.cap.release()  # Release any existing VideoCapture object
        video_path = r'C:\Users\2024au\OneDrive\Desktop\Python(3)\EnhancedRehabilitationGloveSystem\videos\hand_test.mp4'
        #video_path = resource_path('videos\\hand_test.mp4')
        self.cap = cv2.VideoCapture(video_path)
        self.display_camera_feed()
    
    
    # Method to display camera feed
    def display_camera_feed(self):
        ret, frame_ = self.cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame_, cv2.COLOR_BGR2RGB)
            results, finger_status = hand_detector.find_handgeasures(frame_) #obtain the data from custom module

            self.My_Serial.sendData(finger_status)

            # Update finger status text
            self.finger_status_text.insert("end", str(finger_status) + "\n")
            self.finger_status_text.see("end")

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.draw_hand_landmarks(frame_rgb, hand_landmarks)

            img = Image.fromarray(frame_rgb)
            img = img.resize((640, 480), Image.LANCZOS)
            self.imgtk = ImageTk.PhotoImage(image=img)  # Store the PhotoImage object in the instance variable

            self.camera_label.imgtk = self.imgtk  # Use the stored PhotoImage object
            self.camera_label.config(image=self.imgtk)
            self.camera_label.after(10, self.display_camera_feed)

    # Method to draw hand landmarks on frame
    def draw_hand_landmarks(self, frame, landmarks):
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing.draw_landmarks(frame, landmarks, self.mp_hands.HAND_CONNECTIONS)
        

    # Method to enable video buttons
    def enable_button(self):
        self.v1_button.config(state='normal')
        self.v2_button.config(state='normal')
        self.v3_button.config(state='normal')
    

    # Method to stop camera 
    def stop_camera(self):
        if self.cap is not None:
            self.cap.release()
        self.stop_button.config(text='Start Exercise',bg="green",fg='white')
        self.camera_label.config(text="Camera Label",font=('Arial', 20, 'bold'),fg="white",bg='#3A7FF6')
         

    # Method to close camera App window
    def exit_camera(self):
        if self.cap is not None:
            self.cap.release()
        self.cam_window.destroy()

# Define the App class
class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1500x900")  # Set window size
        self.root.title("ERS")  # Set window title

        # Load background image
        self.bg_image = Image.open('C:/Users/2024au/OneDrive/Desktop/Python(3)/EnhancedRehabilitationGloveSystem/images/HomePage.png')

        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        # Create label for background image
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Animated text label
        self.txt = "Enhanced Rehabilitation Glove System"
        self.count = 0
        self.text = ''
        self.Animated_label = tk.Label(self.root, text=self.txt, font=('Arial', 40, "bold"), fg='black')
        self.Animated_label.pack(pady=(100, 0))

        # Call slider method to animate text
        self.slider()

        # Display label
        self.display_label = tk.Label(self.root, text='Click on continue button to open exercise window', font=('Arial', 15, "bold"), fg='green')
        self.display_label.pack(pady=(20, 0))

        # Continue button
        self.continue_button = tk.Button(self.root, text='Continue', width=12, height=1, font=('Arial', 15), background='green', command=self.open_next_window)
        self.continue_button.pack(pady=(330, 20))


    # Method to animate text
    def slider(self):
        if self.count < len(self.txt):
            self.text += self.txt[self.count]
            self.Animated_label.config(text=self.text)
            self.count += 1
            self.root.after(100, self.slider)

    # Method to open next window
    def open_next_window(self):
        app = CameraApp(self.root)

# Create root window
root = tk.Tk()
# Create instance of App class
app = App(root)
root.mainloop()  # Start the Tkinter event loop
