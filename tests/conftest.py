import os
import sys

# Set the path to your Python module
path_to_module = "../"

# Add the path to the system path
sys.path.insert(0, os.path.abspath(path_to_module))

# Set the PYTHONPATH environment variable
os.environ["PYTHONPATH"] = os.pathsep.join(sys.path)
