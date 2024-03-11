# USB Master Password

I created this project so I can use a USB drive to automatically type in my master password in my password manager.

#### Security & Features

- Your password is encrypted and saved into the flash drive. unless someone doesn't have access to your pc, it can't be decrypted.
- To enhance your password even more, the app also does some face recognition using Open-CV to verify it's you who's using this app and flash drive. You can turn this option off.

## Getting Started

#### Prerequisites

- python 3.8 or higher idk

### Installation

- **Installing prerequisities**

  1. `pip install -r requirements.txt`
     **Note:** If you are on windows, you most probably won't be able to install `dlib` library like this. To solve the problem, follow [this tutorial](https://www.geeksforgeeks.org/how-to-install-dlib-library-for-python-in-windows-10/) or search up the internet, then run the command above again untill every library is installed

- **Create encrypted password and key**

  1. run `python CreatePassword.py`, enter your master password and press enter. two files would be created: `enc_salt.bin` and `enc_mp.bin`.
  2. Move `enc_mp.bin` To the flash drive (in the directory you specified in the [config.py](/config.py) file. default: root)
     **Note:** Don't copy it. You want to seperate these two so your security would increase.

- **Training the AI**

  1. Change your name in the config file, using the `FACE_RECOGNITION_USER` variable. The name must be folder-name-friendly.
  2. Take multiple images of your face, put them all in a folder under trainting (the more pictures the better). The name of the folder must be the same string you specified for `FACE_RECOGNITION_USER`.
     The structure would look like this:

  ```
  USB-Master-Password
  ├── training
  │   └── hamid
  │       ├── img1.jpg
  │       ├── img2.jpg
  │       ├   ...
  ```

  **Note:** If you want to reset the training module, just delete the file `encodings.pkl` (or by the variable in config: `DEFAULT_ENCODINGS_PATH`)

  3. In th root directory, run `python train.py`
  4. Once trained, you can validate it using `python validate.py`. It should print out your name and the location of your face in the picture it took.

- **Make executable file**
  In the root directory make `detect.bat` file, open it with your editor, and type this:

  ```
  cd "/path/to/USB-Master-Password/"
  start pythonw detect.pyw
  ```

  (change that path accordingly)

- **Add Scheduled Task**
  1. Enable the Operational Log and create your custom view. You can use [this tutorial](https://www.techrepublic.com/article/how-to-track-down-usb-flash-drive-usage-in-windows-10s-event-viewer/) (you can only use 2003 as the ID since we only need to detect when a USB is plugged in)
  2. Create an scheduled task. There is [this tutorial](https://stackoverflow.com/a/32927488/22502140) for it. For the action, just copy the path to the bat file and paste it in the `Program/Script` field.

**Note:** if you have multiple webcams, you can increase `CAM_PORT` in config, to reach the webcam you want

#### Usage

1. Open your password manager
2. Plug in your USB while you're in front of the camera
3. Instantly click on the password field so it will paste it there for you. If you failed to do it on time, you can manually paste it from the clipboard.

## License

MIT License

This project is free and open-source. You can use, modify, and distribute it without any restrictions. Any credits is appreciated doe

## Contact

- zmn-hamid@proton.me
- [Telegram](https://t.me/hamid1780)
- [GitHub Issues](https://github.com/zmn-hamid/USB-Master-Password/issues)
