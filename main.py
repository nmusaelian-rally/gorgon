import sys, os
from app import app


#HOST = 'localhost'
PORT = 4444


if __name__ == '__main__':
    print("about to run the app...")
    app.app.run(port=PORT)