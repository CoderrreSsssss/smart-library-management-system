import json
import bcrypt

USERS_FILE = "data/users.json"

def load_users():

    with open(USERS_FILE) as f:
        return json.load(f)

def save_users(users):

    with open(USERS_FILE,"w") as f:
        json.dump(users,f,indent=2)

def register(username,password):

    users = load_users()

    if username in users:
        return False

    hashed = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()

    users[username] = {
        "password":hashed,
        "role":"student"
    }

    save_users(users)

    return True

def login(username,password):

    users = load_users()

    if username not in users:
        return False,None

    hashed = users[username]["password"].encode()

    if bcrypt.checkpw(password.encode(),hashed):

        return True,users[username]["role"]

    return False,None
