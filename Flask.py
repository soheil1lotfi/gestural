from flask import Flask, render_template, Response, jsonify
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import numpy as np
from mediapipe.framework.formats import landmark_pb2
import threading

app = Flask(__name__)

category_name = ""


def generate_frames():

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    model_path = "C:/Users/DC/Downloads/Gestural/project/gesture_recognizer.task"

    BaseOptions = mp.tasks.BaseOptions
    GestureRecognizer = mp.tasks.vision.GestureRecognizer
    GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        num_hands=2,
        min_hand_detection_confidence=0.75,
        min_hand_presence_confidence=0.75,
    )
    GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
    VisionRunningMode = mp.tasks.vision.RunningMode
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

    with GestureRecognizer.create_from_options(GestureRecognizerOptions) as recognizer:

        # Start the webcam.
        cap = cv2.VideoCapture(0)

        while True:
            # Capture a frame from the webcam.
            ret, frame = cap.read()
            if not ret:
                print("Error capturing frame")
                break

            # Convert the frame to RGB.
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Create a MediaPipe Image object from the frame.
            # image = mp.Image.create_from_array(frame_rgb)
            image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

            # Recognize gestures in the image.
            recognition_result = recognizer.recognize(image)

            for hand_landmarks in recognition_result.hand_landmarks:
                hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
                hand_landmarks_proto.landmark.extend(
                    [
                        landmark_pb2.NormalizedLandmark(
                            x=landmark.x, y=landmark.y, z=landmark.z
                        )
                        for landmark in hand_landmarks
                    ]
                )

                ############## Visualization
                # mp_drawing.draw_landmarks(
                #     frame,
                #     hand_landmarks_proto,
                #     mp_hands.HAND_CONNECTIONS,
                #     mp_drawing_styles.get_default_hand_landmarks_style(),
                #     mp_drawing_styles.get_default_hand_connections_style(),
                # )
            # cv2.imshow("Gesture Recognition", frame)
            ret, buffer = cv2.imencode(".jpg", frame)
            frame_byte = buffer.tobytes()
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame_byte + b"\r\n"
            )

            if recognition_result.gestures:
                # Assuming recognition_result.gestures is your output variable that contains the gesture recognition results
                for gesture_list in recognition_result.gestures:
                    # print(gesture_list)
                    if gesture_list:  # Check if the list is not empty
                        # Accessing the category_name attribute of the first Category object in the list
                        global category_name
                        category_name = str(gesture_list[0].category_name)

                    else:
                        print("No gesture recognized in this frame.")
                        # category_name = "No gesture recognized in this frame."
            else:
                category_name = "No gesture recognized in this frame."
                # print(category_name)

            # Press 'q' to quit.
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break


thread = threading.Thread(target=generate_frames)
thread.daemon = True
thread.start()


@app.route("/")
def index():
    # global category_name  # Access the global variable
    # if category_name:
    #     message = f"Detected gesture: {category_name}"
    # else:
    #     message = "No gesture detected"
    return render_template("index.html")


@app.route("/get_category_name")
def get_category_name():
    global category_name
    print("in client: " + category_name)
    return jsonify(category_name)


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    app.run(debug=True)
