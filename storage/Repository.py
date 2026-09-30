import json

from models.User import User
from models.User import Student
from models.User import Organizer
from models.Event import Event
from models.Request import Request


class Repository:
    def __init__(self, path="data.json"):
        self.path = path
        self.users = []
        self.events = []
        self.requests = []
        self.load()

    def load(self):
        try:
            with open(self.path, encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return

        for u in data.get("users", []):
            if u["role"] == "Студент":
                self.users.append(Student(
                    u["id"], u["login"], u["password"], u["full_name"],
                    u["group"], u["contact"], u["direction"],
                    u["participation_form"], u["created_at"]
                ))
            else:
                self.users.append(Organizer(
                    u["id"], u["login"], u["password"], u["full_name"],
                    u["contact"], u.get("position", ""), u["created_at"]
                ))

        for e in data.get("events", []):
            self.events.append(Event(
                e["id"], e["title"], e["event_date"],
                e["place"], e.get("description", "")
            ))

        for r in data.get("requests", []):
            self.requests.append(Request(
                r["id"], r["user_id"], r["event_id"],
                r["status"], r["updated_at"]
            ))

    def save(self):
        data = {
            "users": [u.to_dict() for u in self.users],
            "events": [e.to_dict() for e in self.events],
            "requests": [r.to_dict() for r in self.requests],
        }
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def next_id(self, items):
        if not items:
            return 1
        return max(i.id for i in items) + 1

    def find_user(self, user_id):
        for u in self.users:
            if u.id == user_id:
                return u
        return None

    def find_event(self, event_id):
        for e in self.events:
            if e.id == event_id:
                return e
        return None

    def add_event(self, title, event_date, place, description=""):
        event = Event(self.next_id(self.events), title, event_date, place, description)
        self.events.append(event)
        self.save()
        return event

    def add_request(self, user_id, event_id):
        request = Request(self.next_id(self.requests), user_id, event_id)
        self.requests.append(request)
        self.save()
        return request

    def update_status(self, request_id, status):
        for r in self.requests:
            if r.id == request_id:
                r.status = status
                self.save()
                return
        raise ValueError("Заявка не найдена")

    def delete_request(self, request_id):
        self.requests = [r for r in self.requests if r.id != request_id]
        self.save()

    def summary(self, event_id):
        by_status = {}
        total = 0
        for r in self.requests:
            if r.event_id == event_id:
                total += 1
                by_status[r.status] = by_status.get(r.status, 0) + 1
        return {"total": total, "by_status": by_status}