import os

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_path(*args, root_path=ROOT_PATH):
    for dir in args:
        root_path = os.path.join(root_path, dir)
    return root_path
