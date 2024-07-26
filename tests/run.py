import os


def start():
    os.system("cls")
    # os.system("pip install -r requirements.txt")
    os.system("flask --app flaskr run --host=0.0.0.0")


if __name__ == "__main__":
    start()
