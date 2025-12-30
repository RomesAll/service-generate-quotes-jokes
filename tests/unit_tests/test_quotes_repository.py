from app.repository import QuotesRepository
from app.models import QuotesOrm

class TestQuotesRepositoryMock:

    def test_db_select_all(self, mocker, get_test_session, get_default_quotes):
        '''
        Тест для вывода записей из тестовой таблицы. Пытался реализовать мокирование объектов.
        Получилось так себе, нечитабельно. Потом исправлю
        '''
        mock_session = mocker.patch.object(get_test_session, 'execute')
        mock_result = mocker.Mock()
        mock_result_scalars = mocker.Mock()

        mock_result_scalars.all.return_value = get_default_quotes
        mock_result.scalars.return_value = mock_result_scalars
        mock_session.execute.return_value = mock_result
        data = QuotesRepository(mock_session).select_all_quotes()
        assert data == get_default_quotes
        mock_result_scalars.all.assert_called_once_with()

    def test_db_select_one_record(self, mocker, get_test_session, get_default_quotes):
        '''
        Тест для вывода записей из тестовой таблицы по id. Пытался реализовать мокирование объектов.
        Получилось так себе, нечитабельно. Потом исправлю
        '''
        mock_session = mocker.patch.object(get_test_session, 'get')
        mock_session.get.return_value = get_default_quotes[0] # id = 1
        assert QuotesRepository(mock_session).select_quotes_by_id(quotes_id=1) == get_default_quotes[0]

class TestQuotesRepositoryTestDB:

    def test_db_create_quotes(self, get_test_session, create_default_quotes_author):
        orm_object = QuotesOrm(id=2, text='hello', author_id=1)
        result = QuotesRepository(get_test_session).create_quotes(orm_object)
        assert isinstance(result, QuotesOrm)

    def test_db_update_quotes(self, get_test_session, create_default_quotes_author):
        orm_object = QuotesOrm(id=2, author_id=1, text='hello wrld')
        result = QuotesRepository(get_test_session).update_quotes(orm_object)
        assert isinstance(result, QuotesOrm)
        assert result.text == 'hello wrld'

    def test_db_delete_quotes(self, get_test_session, create_default_quotes_author):
        result = QuotesRepository(get_test_session).delete_quotes(quotes_id=2)
        assert isinstance(result, QuotesOrm)
        assert result.id == 2
