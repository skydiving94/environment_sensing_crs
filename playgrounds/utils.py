import os.path
import sys


def add_src_to_sys_path():
    playground_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    root_path = os.path.join(playground_root, '..')
    sys.path.append(root_path)

