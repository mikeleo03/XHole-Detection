import cv2
import numpy as np
from .constant import *
from .objectdetector import FocalLength, Distance_finder, face_data

# Some Constants
Known_distance = 30  # Inches
Known_width = 5.7  # Inches
thres = 0.5 # Threshold to detect object
nms_threshold = 0.2 # (0.1 to 1) 1 means no suppress, 0.1 means high suppress

font = cv2.FONT_HERSHEY_PLAIN
fonts = cv2.FONT_HERSHEY_COMPLEX
fonts2 = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
fonts3 = cv2.FONT_HERSHEY_COMPLEX_SMALL
fonts4 = cv2.FONT_HERSHEY_TRIPLEX

# Define the net variable at a higher level
weightsPath = CONFIG_PATH + "frozen_inference_graph.pb"
configPath = CONFIG_PATH + "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
face_detector = cv2.CascadeClassifier(CONFIG_PATH + "haarcascade_frontalface_default.xml")

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

def euclidean_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return int(distance)

def generate_frames():
    # Camera Object
    cap = cv2.VideoCapture(0)  # Number According to Camera
    face_model = cv2.CascadeClassifier(CONFIG_PATH + 'haarcascade_frontalface_default.xml')
    Distance_level = 0
    classNames = []
    with open(CONFIG_PATH + 'coco.names','r') as f:
        classNames = f.read().splitlines()
    # print(classNames)
    Colors = np.random.uniform(0, 255, size=(len(classNames), 3))
    
    ref_image = cv2.imread(CONFIG_PATH + "lena.png")

    ref_image_face_width, _, _, _ = face_data(ref_image, False, Distance_level)
    Focal_length_found = FocalLength(Known_distance, Known_width, ref_image_face_width)
    
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            classIds, confs, bbox = net.detect(frame, confThreshold=thres)

            # ... (your existing object detection code)
            bbox = list(bbox)
            confs = list(np.array(confs).reshape(1, -1)[0])
            confs = list(map(float, confs))
            indices = cv2.dnn.NMSBoxes(bbox, confs, thres, nms_threshold)
            
            face_width_in_frame, Faces, FC_X, FC_Y = face_data(frame, True, Distance_level)
            # finding the distance by calling function Distance finder
            if len(classIds) != 0:
                for i in indices:
                    i = i
                    box = bbox[i]
                    confidence = str(round(confs[i], 2))
                    color = Colors[classIds[i] - 1]
                    x, y, w, h = box[0], box[1], box[2], box[3]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness=2)
                    cv2.putText(frame, classNames[classIds[i]- 1] + " " + confidence, (x + 10, y + 20), font, 1, color, 2)

            for (face_x, face_y, face_w, face_h) in Faces:
                if face_width_in_frame != 0:
                    Distance = Distance_finder(Focal_length_found, Known_width, face_width_in_frame)
                    Distance = round(Distance, 2)
                    # Drwaing Text on the screen
                    Distance_level = int(Distance)

                    cv2.putText(frame, f"Distance {Distance} Inches", (face_x-6, face_y-6), fonts, 0.5, (BLACK), 2)

            if cv2.waitKey(1) == ord("q"):
                break

            status, photo = cap.read()
            l = len(bbox)
            frame = cv2.putText(frame, str(len(bbox)) + " Object", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            stack_x = []
            stack_y = []
            stack_x_print = []
            stack_y_print = []
            global D

            if len(bbox) == 0:
                pass
            else:
                for i in range(0, len(bbox)):
                    x1 = bbox[i][0]
                    y1 = bbox[i][1]
                    x2 = bbox[i][0] + bbox[i][2]
                    y2 = bbox[i][1] + bbox[i][3]

                    mid_x = int((x1 + x2) / 2)
                    mid_y = int((y1 + y2) / 2)
                    stack_x.append(mid_x)
                    stack_y.append(mid_y)
                    stack_x_print.append(mid_x)
                    stack_y_print.append(mid_y)

                    frame = cv2.circle(frame, (mid_x, mid_y), 3, [0, 0, 255], -1)
                    frame = cv2.rectangle(frame, (x1, y1), (x2, y2), [0, 0, 255], 2)

                if len(bbox) == 2:
                    point1 = (stack_x.pop(), stack_y.pop())
                    point2 = (stack_x.pop(), stack_y.pop())
                    D = euclidean_distance(point1, point2)
                    frame = cv2.line(frame, (stack_x_print.pop(), stack_y_print.pop()), (stack_x_print.pop(), stack_y_print.pop()), [0, 0, 255], 2)
                else:
                    D = 0

                if D < 250 and D != 0:
                    frame = cv2.putText(frame, "!!MOVE AWAY!!", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, [0, 0, 255], 4)

                frame = cv2.putText(frame, str(D / 10) + " cm", (300, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()