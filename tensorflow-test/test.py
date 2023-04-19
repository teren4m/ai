from file_storage import file_storage as fs
import numpy as np
import json

value = json.dumps('good')
print(value)

value = json.loads(value)
print(type(value))
