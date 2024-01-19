
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
# from .face_recognition import music
import os
import av
import cv2 
import numpy as np 
import mediapipe as mp 
from keras.models import load_model
import keyboard
import psutil

PREFIX = f"/ml/v1"


current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'face_recognition', 'model.h5')
model = load_model(model_path)
label = np.load(os.path.join(current_dir, 'face_recognition', 'labels.npy'))
holistic = mp.solutions.holistic
hands = mp.solutions.hands
holis = holistic.Holistic()
#drawing = mp.solutions.drawing_utils

def recording():
    data_size = 0
    cap =cv2.VideoCapture(0)
    pred = None
    while True:
        print("heeee")
        _, frm = cap.read()
        frm = cv2.flip(frm, 1)

        res = holis.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))
        
        lst = []
            
        if res.face_landmarks:
            for i in res.face_landmarks.landmark:
                lst.append(i.x - res.face_landmarks.landmark[1].x)
                lst.append(i.y - res.face_landmarks.landmark[1].y)

            data_size = data_size+1
        print(data_size)
    
        lst = np.array(lst).reshape(1,-1)

        pred = label[np.argmax(model.predict(lst))]

        print(pred)
        cv2.putText(frm, pred, (50,50),cv2.FONT_ITALIC, 1, (255,0,0),2)

                
        #drawing.draw_landmarks(frm, res.face_landmarks, holistic.FACEMESH_TESSELATION,
        #                           landmark_drawing_spec=drawing.DrawingSpec(color=(0,0,255), thickness=-1, circle_radius=1),
        #                            connection_drawing_spec=drawing.DrawingSpec(thickness=1))


        cv2.imshow("window",frm)

        if cv2.waitKey(1) == 27 or data_size >29:
            break
    cv2.destroyAllWindows()
    cap.release()
    return pred
    
app = FastAPI(
    openapi_url=f"{PREFIX}/openapi.json",
    docs_url=f"{PREFIX}/docs",
    redoc_url=f"{PREFIX}/redoc",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/face_recognition") 
async def read_face_recognition():
    return recording()
