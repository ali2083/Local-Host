# Local Host

## Description
I think it would be very interesting if I could send my files to all devices on the local network without intermediary programs, and in this project I did this with some additional features.

## Prerequisites
You can use 
```bash
pip install -r requirements.txt
```
or install separately:

* Python 3.8+ (https://www.python.org/downloads/)
* Flask (https://flask.palletsprojects.com/en/2.3.x/installation/#install-flask)
* psutil (https://pypi.org/project/psutil/)
* pyautogui (https://pypi.org/project/PyAutoGUI/)
* numpy (https://pypi.org/project/numpy/)
* opencv (https://pypi.org/project/opencv-python/)
* pytest (https://pypi.org/project/pytest/)
* aiortc (https://pypi.org/project/aiortc/)

## Installation
1. Install the prerequisites, you can also use the virtual environment
2. First, initialize the database <br>
```bash 
flask --app flaskr init-db
```
3. Then run the program on local network <br>
```bash 
flask --app flaskr run --host=0.0.0.0
```

> [!WARNING]
> Note that you have given the necessary permissions for the firewall