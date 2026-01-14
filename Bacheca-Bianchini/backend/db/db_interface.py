from bson import ObjectId
from datetime import datetime

class DatabaseInterface:
    def __init__(self, db):
        self._users = db["users"]
        self._messages = db["messages"]

    # ---------- USERS ----------
    async def get_user_by_email(self, email = None):
        return await self._users.find_one({"email": email})

    async def create_user(self, email, hashed_password):
        return await self._users.insert_one({
            "email": email,
            "password": hashed_password
        })

    # ---------- MESSAGES ----------
    async def get_messages_by_user(self, user_id: str):
        cursor = self._messages.find({"user_id": ObjectId(user_id)})
        return [t async for t in cursor]

    async def get_messages_for_all(self):
        cursor = self._messages.find()
        return [t async for t in cursor]

    async def create_message(self, user_id: str, text: str, email: str):
        return await self._messages.insert_one({
            "user_id": ObjectId(user_id),
            "email": email,
            "text": text,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    async def delete_message_by_user(self, message_id: str, user_id: str):
        return await self._messages.delete_one({
            "_id": ObjectId(message_id),
            "user_id": ObjectId(user_id)
        })