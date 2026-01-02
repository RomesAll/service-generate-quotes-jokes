__all__ = ('JokesRepository', 'QuotesRepository', 'AuthorRepository', 'UsersRepository')

from .jokes import JokesRepository
from .quotes import QuotesRepository, AuthorRepository
from .users import UsersRepository