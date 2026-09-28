from sqlalchemy import text
from config.database import engine

with engine.connect() as conexao:
    print(
        "CONEXAO ORM OK:",
        conexao.execute(text("SELECT 1")).scalar()
    )