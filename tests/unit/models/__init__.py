import os
import sys

import package
print(os.path.abspath(package.__file__))
sys.path.append(os.path.abspath(package.__file__))
