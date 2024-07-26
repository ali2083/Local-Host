# Local Host

## Description
[I think it would be very interesting if I could send my files to all devices on the local network without intermediary programs, and in this project I did this with some additional features.]

## Prerequisites

* Python 3.8+
* Flask
* psutil
* pyautogui
* numpy
* opencv
* pytest
* aiortc

## Installation
1. Install the prerequisites, you can also use the virtual environment
2. First, initialize the database <br>```bash flask --app flaskr init-db```
3. Then run the program on local network <br>```bash flask --app flaskr run --host=0.0.0.0```

> [!WARNING]
> Note that you have given the necessary permissions for the firewall