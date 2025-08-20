import sqlite3

def create_database():
    conn = sqlite3.connect('THP45.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blockout_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            setting_name TEXT NOT NULL,
            setting_start_hour INT NOT NULL,
            setting_end_hour INT NOT NULL
        )
    ''')
    cursor.execute(
        "INSERT INTO blockout_settings (setting_name, setting_start_hour, setting_end_hour) VALUES (?, ?, ?)",
            ("default_setting", 00, 00) # Default setting
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()