import sqlite3

db = sqlite3.connect("database.db")

# Create users table
db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")

# Insert default user
db.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")

# Create logs table
db.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, payload TEXT, status TEXT, time TEXT)")

db.commit()
db.close()

print("Database created successfully!")