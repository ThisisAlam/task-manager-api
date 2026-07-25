from app.database import engine, SessionLocal

print(engine)

session = SessionLocal()
print(session)
session.close()