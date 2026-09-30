from datetime import date


class Request:
    def __init__(self, id, user_id, event_id, status="новая", updated_at=None):
        self.id = id
        self.user_id = user_id
        self.event_id = event_id
        self.status = status
        self.updated_at = updated_at if updated_at else str(date.today())

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "event_id": self.event_id,
            "status": self.status,
            "updated_at": self.updated_at,
        }