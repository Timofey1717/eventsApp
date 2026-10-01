from datetime import date
from storage.db import Database
from models.User import User, Student, Organizer
from models.Event import Event
from models.Request import Request


class Repository:
    def __init__(self, path="data/database.db"):
        self.db = Database(path)
        self.connection = self.db.connection

    # ---------- Пользователи ----------

    def add_student(self, login, password, full_name, group,
                    contact, direction, participation_form):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO users (login, password, role, full_name, contact,
                               created_at, group_name, direction, participation_form)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (login, password, "Студент", full_name, contact,
              str(date.today()), group, direction, participation_form))
        self.connection.commit()
        return cursor.lastrowid

    def add_organizer(self, login, password, full_name, contact, position=""):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO users (login, password, role, full_name, contact,
                               created_at, position)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (login, password, "Организатор", full_name, contact,
              str(date.today()), position))
        self.connection.commit()
        return cursor.lastrowid

    def get_user(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return self._row_to_user(row)

    def get_user_by_login(self, login):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE login = ?", (login,))
        row = cursor.fetchone()
        if row is None:
            return None
        return self._row_to_user(row)

    def get_all_users(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users ORDER BY id")
        return [self._row_to_user(row) for row in cursor.fetchall()]

    def _row_to_user(self, row):
        if row["role"] == "Студент":
            return Student(
                id=row["id"],
                login=row["login"],
                password=row["password"],
                full_name=row["full_name"],
                group=row["group_name"],
                contact=row["contact"],
                direction=row["direction"],
                participation_form=row["participation_form"],
                created_at=row["created_at"],
            )
        return Organizer(
            id=row["id"],
            login=row["login"],
            password=row["password"],
            full_name=row["full_name"],
            contact=row["contact"],
            position=row["position"] or "",
            created_at=row["created_at"],
        )

    # ---------- Мероприятия ----------

    def add_event(self, title, event_date, place, description=""):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO events (title, event_date, place, description)
            VALUES (?, ?, ?, ?)
        """, (title, event_date, place, description))
        self.connection.commit()
        return cursor.lastrowid

    def get_event(self, event_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return Event(row["id"], row["title"], row["event_date"],
                     row["place"], row["description"])

    def get_all_events(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events ORDER BY id")
        return [Event(r["id"], r["title"], r["event_date"],
                      r["place"], r["description"])
                for r in cursor.fetchall()]

    def delete_event(self, event_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
        self.connection.commit()

    # ---------- Заявки ----------

    def add_request(self, user_id, event_id):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO requests (user_id, event_id, status, updated_at)
            VALUES (?, ?, ?, ?)
        """, (user_id, event_id, "новая", str(date.today())))
        self.connection.commit()
        return cursor.lastrowid

    def get_request(self, request_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM requests WHERE id = ?", (request_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return Request(row["id"], row["user_id"], row["event_id"],
                       row["status"], row["updated_at"])

    def get_all_requests(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM requests ORDER BY id")
        return [Request(r["id"], r["user_id"], r["event_id"],
                        r["status"], r["updated_at"])
                for r in cursor.fetchall()]

    def get_requests_by_event(self, event_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM requests WHERE event_id = ? ORDER BY id",
                       (event_id,))
        return [Request(r["id"], r["user_id"], r["event_id"],
                        r["status"], r["updated_at"])
                for r in cursor.fetchall()]

    def update_status(self, request_id, status):
        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE requests SET status = ?, updated_at = ?
            WHERE id = ?
        """, (status, str(date.today()), request_id))
        self.connection.commit()

    def delete_request(self, request_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM requests WHERE id = ?", (request_id,))
        self.connection.commit()

    # ---------- Поиск и сводка ----------

    def search_requests(self, query, event_id=None):
        cursor = self.connection.cursor()
        sql = """
            SELECT r.* FROM requests r
            JOIN users u ON u.id = r.user_id
            WHERE (u.full_name LIKE ? OR u.group_name LIKE ? OR u.direction LIKE ?)
        """
        params = [f"%{query}%", f"%{query}%", f"%{query}%"]
        if event_id:
            sql += " AND r.event_id = ?"
            params.append(event_id)
        cursor.execute(sql, params)
        return [Request(r["id"], r["user_id"], r["event_id"],
                        r["status"], r["updated_at"])
                for r in cursor.fetchall()]

    def summary(self, event_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM requests WHERE event_id = ?",
                       (event_id,))
        total = cursor.fetchone()[0]

        cursor.execute("""
            SELECT status, COUNT(*) FROM requests
            WHERE event_id = ? GROUP BY status
        """, (event_id,))
        by_status = {row[0]: row[1] for row in cursor.fetchall()}

        cursor.execute("""
            SELECT u.direction, COUNT(*) FROM requests r
            JOIN users u ON u.id = r.user_id
            WHERE r.event_id = ? GROUP BY u.direction
        """, (event_id,))
        by_direction = {row[0]: row[1] for row in cursor.fetchall()}

        return {
            "total": total,
            "by_status": by_status,
            "by_direction": by_direction,
        }

    def close(self):
        self.db.close()