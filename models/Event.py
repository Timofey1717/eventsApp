class Event:
    def __init__(self, id, title, event_date, place, description=""):
        self.id = id
        self.title = title
        self.event_date = event_date
        self.place = place
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "event_date": self.event_date,
            "place": self.place,
            "description": self.description,
        }