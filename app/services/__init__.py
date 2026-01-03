__all__ = ('QuotesService', 'JokesService',
           'AuthorService', 'UsersService',
           'QuotesSchemaPUT', 'QuotesSchemaPOST',
           'QuotesSchemaGET', 'AuthorSchemaPUT',
           'AuthorSchemaPOST', 'AuthorSchemaGET',
           'JokesSchemaGET', 'JokesSchemaPUT', 'JokesSchemaPOST',
           'UsersSchemaGET', 'UsersSchemaPUT', 'UsersSchemaPOST')

from .quotes import (QuotesService, AuthorService,
                     QuotesSchemaPUT, QuotesSchemaPOST,
                     QuotesSchemaGET, AuthorSchemaPUT,
                     AuthorSchemaPOST, AuthorSchemaGET)
from .jokes import JokesService, JokesSchemaGET, JokesSchemaPUT, JokesSchemaPOST
from .users import UsersService, UsersSchemaGET, UsersSchemaPUT, UsersSchemaPOST