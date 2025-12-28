from app.database import session_maker

def get_session():
    try:
        session = session_maker()
        yield session
    finally:
        session.close()