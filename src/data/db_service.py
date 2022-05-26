from src.models.user_db import UserDB

def get_db_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserDB(**user_dict)