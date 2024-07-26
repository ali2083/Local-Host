from flaskr.db import get_db, init_db

database = get_db()
data = database.execute("SELECT * FROM users").fetchone
for i in data:
    print(i)
