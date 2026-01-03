__all__ = ('JokesRepository', 'QuotesRepository',
           'AuthorRepository', 'UsersRepository',
           'JokesOrm','QuotesOrm',
           'AuthorOrm','UsersOrm')

from .jokes import JokesRepository, JokesOrm
from .quotes import QuotesRepository, AuthorRepository, QuotesOrm, AuthorOrm
from .users import UsersRepository, UsersOrm