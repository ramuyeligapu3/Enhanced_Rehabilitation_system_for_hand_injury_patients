import cv2
import mediapipe as mp
#from cvzone.SerialModule import SerialObject

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
class Hand_Excerises_Detection:

    # Convert the image to RGB
    def find_handgeasures(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame
        results = hands.process(rgb_frame)
        finger_status = [0, 0, 0, 0, 0]  # Initialize finger status


        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                finger_status = [0, 0, 0, 0, 0]  # Initialize finger status
                
                # Thumb finger
                if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x:
                    finger_status[0] = 1 

                # Index finger
                if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y:
                    finger_status[1] = 1

                # Middle finger
                if hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y:
                    finger_status[2] = 1

                # Ring finger
                if hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y:
                    finger_status[3] = 1

                # Little finger
                if hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y:
                    finger_status[4] = 1

                # Print finger status
                print(finger_status)
                #send data to arduino
                #My_Serial.sendData(finger_status)

        return results,finger_status
Hand_Excerises_Detection()

