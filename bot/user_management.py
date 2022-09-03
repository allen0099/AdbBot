import json
import os

from core import settings

ALLOWED_USERS_FILE = settings.BASE_DIR / "users.json"

if not os.path.exists(ALLOWED_USERS_FILE):
    with open(ALLOWED_USERS_FILE, "x", encoding="UTF-8") as f:
        f.write('{"user":[]}')


def get_allowed_users() -> list[int]:
    with open(ALLOWED_USERS_FILE, "r", encoding="UTF-8") as f:
        data: dict = json.load(f)
        return data.get("user")


def add_allowed_user(uid: int) -> bool:
    with open(ALLOWED_USERS_FILE, "r+", encoding="UTF-8") as f:
        data: list[int] = get_allowed_users()

        if uid in data:
            return False

        data.append(uid)
        data.sort()

        json.dump({"user": data}, f, ensure_ascii=False, indent=4)
        return True


def remove_allowed_user(uid: int) -> bool:
    data: list[int] = get_allowed_users()

    if uid not in data:
        return False

    data.remove(uid)
    data.sort()

    f = open(ALLOWED_USERS_FILE, "w", encoding="UTF-8")
    json.dump({"user": data}, f, ensure_ascii=False, indent=4)
    f.close()
    return True
