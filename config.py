import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "development-only-change-me")
    DATABASE = os.environ.get("DATABASE_PATH", "instance/expenses.sqlite")
