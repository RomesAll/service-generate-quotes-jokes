__all__ = ('QuotesSchemaPOST', 'QuotesSchemaGET', 'QuotesSchemaPUT',
           'AuthorSchemaPOST','AuthorSchemaGET','AuthorSchemaPUT',
           'JokesSchemaPOST','JokesSchemaGET','JokesSchemaPUT', 'AuthorSchemaRel', 'QuotesSchemaRel',
           'UsersSchemaGET', 'UsersSchemaPOST', 'UsersSchemaPUT', 'SearchJokesSchema', 'PaginationJokesSchema')

from .jokes import JokesSchemaPOST, JokesSchemaPUT, JokesSchemaGET
from .quotes import (QuotesSchemaGET, QuotesSchemaPUT, QuotesSchemaPOST, AuthorSchemaPUT,
                     AuthorSchemaPOST, AuthorSchemaGET, QuotesSchemaRel, AuthorSchemaRel)
from .users import UsersSchemaPOST, UsersSchemaGET, UsersSchemaPUT
from .base import SearchJokesSchema, PaginationJokesSchema