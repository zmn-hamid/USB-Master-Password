import base64
import os
import pickle
from collections import Counter
from pathlib import Path

import cv2
import face_recognition
import psutil
import pyautogui
import pyperclip
from cryptography.fernet import Fernet, InvalidToken as InvalidPasswordKey
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from config import *
from GetUUID import get_uuid


def get_usb_drive_letter():
    for disk in psutil.disk_partitions():
        if "removable" in disk.opts:
            return disk.device


ENC_MP_BIN = f"{get_usb_drive_letter()}{ENC_MP_BIN}"  # encrypted master password
DEFAULT_ENCODINGS_PATH = Path(DEFAULT_ENCODINGS_PATH)


def face_verificated(face_name: str):
    def _recognize_face(unknown_encoding, loaded_encodings):
        boolean_matches = face_recognition.compare_faces(
            loaded_encodings["encodings"], unknown_encoding
        )
        votes = Counter(
            name
            for match, name in zip(boolean_matches, loaded_encodings["names"])
            if match
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
        pyautogui.alert(text="Couldn't take photo", title="Bro", button="OK")

    if took_pic:
        if recognize_face(CAPTURED_PIC)[0] == face_name:
            return True


def get_master_password():
    def _derive_key(passphrase: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend(),
        )
        return base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))

    with open(ENC_SALT_BIN, "rb") as enc_salt:
        with open(ENC_MP_BIN, "rb") as enc_mp:
            return (
                Fernet(_derive_key(get_uuid(), enc_salt.read()))
                .decrypt(enc_mp.read())
                .decode()
            )


if os.path.exists(ENC_MP_BIN):
    if DO_FACE_RECOGNITION and not face_verificated(FACE_RECOGNITION_USER):
        pyautogui.alert(text="No photo could be taken", title="Bro", button="OK")
    else:
        try:
            pyperclip.copy(get_master_password())
            pyautogui.hotkey("ctrl", "v")
        except InvalidPasswordKey:
            pyautogui.alert(text="password mismatch", title="Bro", button="OK")
