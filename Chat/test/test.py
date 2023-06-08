import sys

base = sys.path.append('../src')
import os
print()
from chat import *

ChatServer("C:/Users/98324/Desktop/Text/Exp8/Chat/res/server")

ChatClient(port=8000, info=('127.0.0.1', 8080))
ChatClient(port=8001, info=('127.0.0.1', 8080))

while True:
    pass