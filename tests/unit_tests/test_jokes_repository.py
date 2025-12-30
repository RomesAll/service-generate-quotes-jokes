from app.repository import JokesRepository
from app.models import JokesOrm
from pytest_mock import mocker

class TestJokesRepositoryMock:

    def test_db_select_all(self, mocker, get_test_session, get_default_jokes):
        '''
        Тест для вывода записей из тестовой таблицы. Пытался реализовать мокирование объектов.
        Получилось так себе, нечитабельно. Потом исправлю
        '''
        mock_session = mocker.patch.object(get_test_session, 'execute')
        mock_result = mocker.Mock()
        mock_result_scalars = mocker.Mock()

        mock_result_scalars.all.return_value = get_default_jokes
        mock_result.scalars.return_value = mock_result_scalars
        mock_session.execute.return_value = mock_result
        data = JokesRepository(mock_session).select_all_jokes()
        assert data == get_default_jokes
        mock_result_scalars.all.assert_called_once_with()

    def test_db_select_one_record(self, mocker, get_test_session, get_default_jokes):
        '''
        Тест для вывода записей из тестовой таблицы по id. Пытался реализовать мокирование объектов.
        Получилось так себе, нечитабельно. Потом исправлю
        '''
        mock_session = mocker.patch.object(get_test_session, 'get')
        mock_session.get.return_value = get_default_jokes[0] # id = 1
        assert JokesRepository(mock_session).select_jokes_by_id(jokes_id=1) == get_default_jokes[0]

class TestJokesRepositoryTestDB:

    def test_db_create_joke(self, get_test_session):
        orm_object = JokesOrm(text='hello')
        result = JokesRepository(get_test_session).create_jokes(orm_object)
        assert isinstance(result, JokesOrm)

    def test_db_update_joke(self, get_test_session, create_default_jokes):
        orm_object = JokesOrm(id=1, text='hello wrld')
        result = JokesRepository(get_test_session).update_jokes(orm_object)
        assert isinstance(result, JokesOrm)
        assert result.text == 'hello wrld'

    def test_db_delete_joke(self, get_test_session, create_default_jokes):
        result = JokesRepository(get_test_session).delete_jokes(jokes_id=1)
        assert isinstance(result, JokesOrm)
        assert result.id == 1
