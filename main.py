from storage.Repository import Repository

def main():
    repo = Repository("database.db")

    # Добавляем студента
    student_id = repo.add_student(
        login="ivanov",
        password="12345",
        full_name="Иванов И.И.",
        group="ИС-21",
        contact="+79594994939",
        direction="Математика",
        participation_form="Очная",
    )
    print("Студент добавлен, id =", student_id)

    # Добавляем организатора
    organizer_id = repo.add_organizer(
        login="petrova",
        password="admin",
        full_name="Петрова А.С.",
        contact="+79001112233",
        position="Куратор конференции",
    )
    print("Организатор добавлен, id =", organizer_id)

    # Добавляем мероприятие
    event_id = repo.add_event(
        title="Научная конференция",
        event_date="15.10.2026",
        place="Аудитория 305",
        description="Ежегодная студенческая конференция",
    )
    print("Мероприятие добавлено, id =", event_id)

    # Подаём заявку
    request_id = repo.add_request(student_id, event_id)
    print("Заявка добавлена, id =", request_id)

    # Подтверждаем участие
    repo.update_status(request_id, "подтверждена")

    # Ищем
    found = repo.search_requests("Иванов")
    print("Найдено заявок:", len(found))

    # Сводка
    print("Сводка:", repo.summary(event_id))

    # Проверяем загрузку
    print("\nВсе пользователи:")
    for u in repo.get_all_users():
        print(" ", u)

    print("\nВсе заявки:")
    for r in repo.get_all_requests():
        print(" ", r)

    repo.close()


if __name__ == "__main__":
    main()