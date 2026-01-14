import tornado.escape

from backend.db.db import db_interface
from .base import BaseHandler
from backend.db.db_interface import DatabaseInterface

class MessagesHandler(BaseHandler):
    async def get(self):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)

        messages = await db_interface.get_messages_for_all()

        out = [{
            "id": str(t["_id"]),
            "email": t["email"],
            "text": t["text"],
            "time": t["time"]
            #"isOwner": t["email"] == user["email"]
            # ^^^ #se currentUser non funziona prova questo
        } for t in messages]

        return self.write_json({"items": out, "current_user": user})

    async def post(self):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)

        body = tornado.escape.json_decode(self.request.body)
        text = body.get("text", "").strip()

        if not text:
            return self.write_json({"error": "Testo obbligatorio"}, 400)

        result = await db_interface.create_message(user["id"], text, user["email"])
        return self.write_json({"id": str(result.inserted_id)}, 201)

class MessageDeleteHandler(BaseHandler):
    async def delete(self, message_id):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)

        await db_interface.delete_message_by_user(message_id, user["id"])
        return self.write_json({"message": "Eliminato"})