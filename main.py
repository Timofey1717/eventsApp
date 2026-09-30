from models.User import Student
from models.User import Organizer
from models.Event import Event
from models.Request import Request


def main():
    # Проверка Student
    print("Student")
    s = Student(1,"ivanov","12345","Иванов И.И.","ИС-21","+79594994939","Математика","Очная")
    print(s.to_dict())

    # Проверка Organizer
    print("\nOrganizer")
    o = Organizer(2,"petrova","admin","Петрова А.С.","+79001112233","Куратор конференции",)
    print(o)
    print(o.to_dict())


    print("\nEvent")
    e = Event(1,"Научная конференция","15.10.2026","Аудитория 305","Ежегодная студенческая конференция")
    print(e.to_dict())

    # Проверка Request
    print("\nRequest")
    r = Request(1,user_id=s.id,event_id=e.id,)
    print(r.to_dict())


if __name__ == "__main__":
    main()