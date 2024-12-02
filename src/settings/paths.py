import os

path_raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

path_data = os.path.join(path_raiz, "data")
path_doc = os.path.join(path_raiz, "doc")
path_json = os.path.join(path_raiz, "json")
path_temp = os.path.join(path_raiz, "temp")
path_src = os.path.join(path_raiz, "src")
path_log = os.path.join(path_raiz, "log")
