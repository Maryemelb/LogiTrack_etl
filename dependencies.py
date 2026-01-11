from app.database import sessionLocal

def getdb():
    db = sessionLocal()     
    try:
      yield db
    finally:
      db.close()