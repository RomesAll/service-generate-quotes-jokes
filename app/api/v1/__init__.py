__all__ = ('router_jokes', 'router_quotes', 'router_author', 'router_users', 'router_auth')
from .jokes import router as router_jokes
from .quotes import router as router_quotes
from .author import router as router_author
from .users import router as router_users
from .auth import router as router_auth