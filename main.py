import sys, os
from app import app


if __name__ == '__main__':
    print("about to run the app...")
    app.app.run(port=os.environ['PORT'])