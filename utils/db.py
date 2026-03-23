import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "agentic_chain.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    # Table for blockchain ledger
    c.execute('''
        CREATE TABLE IF NOT EXISTS ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            milestone TEXT,
            data_hash TEXT,
            tx_id TEXT
        )
    ''')
    # Table for app state (key-value store)
    c.execute('''
        CREATE TABLE IF NOT EXISTS app_state (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_ledger_entry(entry):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO ledger (timestamp, milestone, data_hash, tx_id)
        VALUES (?, ?, ?, ?)
    ''', (entry["Timestamp"], entry["Milestone"], entry["Data Hash"], entry["Transaction ID"]))
    conn.commit()
    conn.close()

def load_ledger():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT timestamp, milestone, data_hash, tx_id FROM ledger ORDER BY id ASC')
    rows = c.fetchall()
    conn.close()
    return [{"Timestamp": r[0], "Milestone": r[1], "Data Hash": r[2], "Transaction ID": r[3]} for r in rows]

def save_state(key, value):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO app_state (key, value)
        VALUES (?, ?)
    ''', (key, json.dumps(value)))
    conn.commit()
    conn.close()

def load_state(key, default=None):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT value FROM app_state WHERE key = ?', (key,))
    row = c.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return default
