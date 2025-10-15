"""数据库模块"""
import sqlite3

db_file = '../.data/ai_db.db'
conn = sqlite3.connect(db_file)

class Database:

    def __init__(self): pass