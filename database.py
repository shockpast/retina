import sqlite3

sqlite = sqlite3.connect("server.db", check_same_thread=False)
cursor = sqlite.cursor()

def init():
    cursor.execute("CREATE TABLE IF NOT EXISTS shortened_urls ('full' varchar, 'short' varchar, 'clicks' INTEGER)")

def exec(sql: str, params = ...):
	cursor.execute(sql, params)
	sqlite.commit()

	return cursor