import json

def login(username,password):

    with open("users.json","r") as f:
        user=json.load(f)

    return (
        username==user["username"]
        and
        password==user["password"]
    )
