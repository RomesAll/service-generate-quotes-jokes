__all__ = ('QuotesService', 'JokesService', 'AuthorService', 'UsersService')

from .quotes import QuotesService, AuthorService
from .jokes import JokesService
from .users import UsersService