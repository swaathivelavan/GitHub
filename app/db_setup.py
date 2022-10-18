
from cred import config
import pyrebase
firebase = pyrebase.initialize_app(config)
db = firebase.database()