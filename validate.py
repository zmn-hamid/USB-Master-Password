import pickle
from collections import Counter
from pathlib import Path

import cv2
import face_recognition
import pyautogui

from config import *


DEFAULT_ENCODINGS_PATH = Path(DEFAULT_ENCODINGS_PATH)


def _recognize_face(unknown_encoding, loaded_encodings):
    boolean_matches = face_recognition.compare_faces(
        loaded_encodings["encodings"], unknown_encoding
    )
    votes = Counter(
        name for match, name in zip(boolean_matches, loaded_encodings["names"]) if match
    )
    if votes:
        return votes.most_common(1)[0][0]


def recognize_face(
    image_location: str,
    model: str = "hog",
    encodings_location: Path = DEFAULT_ENCODINGS_PATH,
) -> None:
    with encodings_location.open(mode="rb") as f:
        loaded_encodings = pickle.load(f)

    input_image = face_recognition.load_image_file(image_location)

    input_face_locations = face_recognition.face_locations(input_image, model=model)
    input_face_encodings = face_recognition.face_encodings(
        input_image, input_face_locations
    )

    for bounding_box, unknown_encoding in zip(
        input_face_locations, input_face_encodings
    ):
        name = _recognize_face(unknown_encoding, loaded_encodings)
        if not name:
            name = "Unknown"
        return name, bounding_box


# take a screenshot
took_pic = False
cam = cv2.VideoCapture(CAM_PORT)
result, image = cam.read()
if result:
    cv2.imshow("Capture Window", image)
    cv2.imwrite(CAPTURED_PIC, image)
    cv2.waitKey(1)
    cv2.destroyWindow("Capture Window")
    took_pic = True
else:
    pyautogui.alert(text="No face detected", title="Bro", button="OK")

if took_pic:
    print(recognize_face(CAPTURED_PIC))
