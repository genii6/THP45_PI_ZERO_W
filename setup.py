import sqlite3

def create_database():
    conn = sqlite3.connect('THP45.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blockout_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            setting_name TEXT NOT NULL,
            setting_start_hour INT NOT NULL,
            setting_end_hour INT NOT NULL,
            active BOOLEAN DEFAULT 0
        )
    ''')
    cursor.execute(
        "INSERT INTO blockout_settings (setting_name, setting_start_hour, setting_end_hour, active) VALUES (?, ?, ?, ?)",
            ("disabled", 00, 00, 1) # Disabled setting
    )
    cursor.execute(
        "INSERT INTO blockout_settings (setting_name, setting_start_hour, setting_end_hour, active) VALUES (?, ?, ?)",
            ("peak", 16, 21, 0) # peak blockout setting
    )
    cursor.execute(
        "INSERT INTO blockout_settings (setting_name, setting_start_hour, setting_end_hour, active) VALUES (?, ?, ?)",
            ("overnight", 22, 10, 0) # overnight blockout setting
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()