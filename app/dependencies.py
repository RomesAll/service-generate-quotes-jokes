from app.database import session_maker
from app.core import settings

def get_session():
    try:
        session = session_maker()
        yield session
    finally:
        session.close()

