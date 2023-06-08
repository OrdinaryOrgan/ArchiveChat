import sys

base = sys.path.append('../src')
import os
print()
from chat import *
ChatClient(port=8000, info=("39.104.207.15", 3000))

while True:
    pass