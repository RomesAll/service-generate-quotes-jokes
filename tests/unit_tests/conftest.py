from app.models import JokesOrm, QuotesOrm
import pytest
from app.database import Base, engine
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

test_engine = create_engine(url=f'postgresql+psycopg://postgres:qwerty@localhost:5432/db_app_generate_jokes_test')

@pytest.fixture(scope="class")
def get_default_jokes():
    joke_1 = JokesOrm(id=1, text='ha-ha-ha', count_likes=0, count_dislikes=30)
    joke_2 = JokesOrm(id=2, text='ho-ho-ho', count_likes=530, count_dislikes=64)
    joke_3 = JokesOrm(id=3, text='aboba', count_likes=43, count_dislikes=10)
    return [joke_1, joke_2, joke_3]

@pytest.fixture(scope="class")
def get_default_quotes():
    quote_1 = QuotesOrm(id=1, author_id=1, text='ha-ha-ha', count_likes=0, count_dislikes=30)
    quote_2 = QuotesOrm(id=2, author_id=1, text='ho-ho-ho', count_likes=530, count_dislikes=64)
    quote_3 = QuotesOrm(id=3, author_id=1, text='aboba', count_likes=43, count_dislikes=10)
    return [quote_1, quote_2, quote_3]

@pytest.fixture(scope="function")
def get_default_joke():
    joke_1 = JokesOrm(id=4, text='ha-ha-ha', count_likes=50, count_dislikes=30)
    return joke_1

@pytest.fixture(scope="function")
def get_test_session():
    test_session = Session(test_engine)
    yield test_session
    test_session.close()

#-----------------------------------------------------------------------------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)
    yield

@pytest.fixture(scope="session")
def create_default_jokes():
    with test_engine.connect() as connection:
        connection.execute(text("INSERT INTO jokes_orm (id, text, count_likes, count_dislikes) "
                                "VALUES (1, 'hello world', 0, 0)"))
        connection.commit()

@pytest.fixture(scope="session")
def create_default_quotes_author():
    with test_engine.connect() as connection:
        connection.execute(text("INSERT INTO author_orm (id, fio) "
                                "VALUES (1, 'test author')"))
        connection.execute(text("INSERT INTO quotes_orm (id, author_id, text, count_likes, count_dislikes) "
                                "VALUES (1, 1, 'hello world', 0, 0)"))
        connection.commit()