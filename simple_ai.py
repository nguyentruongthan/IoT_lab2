from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np


# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_Model.h5", compile=False)

# Load the labels
class_names = ["Không có người", "Không mang khẩu trang", "Mang khẩu trang"]

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0)

def image_detector():
    # Grab the webcamera's image.
    ret, image = camera.read()

    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Show the image in a window
    cv2.imshow("Webcam Image", image)

    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predicts the model
    prediction = model.predict(image)
    index = np.argmax(prediction)

     # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        return -1
    
    return index


counter_mask = 0
counter_no_mask = 0
counter_no_people = 0
def reset_detect_many_times():
  global counter_mask 
  global counter_no_mask 
  global counter_no_people 

  counter_mask = 0
  counter_no_mask = 0
  counter_no_people = 0



def image_detector_many_times():
  global counter_mask 
  global counter_no_mask 
  global counter_no_people 

  result = image_detector()
  if result == 0:
    counter_mask = 0
    counter_no_mask = 0
    counter_no_people += 1
  elif result == 1:
    counter_mask = 0
    counter_no_mask += 1
    counter_no_people = 0
  elif result == 2:
    counter_mask += 1
    counter_no_mask = 0
    counter_no_people = 0
  elif result == -1:
    return -1
  
  if(counter_mask >= 3):
    return 2
  elif(counter_no_mask >= 3):
    return 1
  elif(counter_no_people >= 3):
    return 0