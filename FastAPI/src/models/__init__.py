from .conta_model import Conta
from .transacao_model import Transacao
from .token_blocklist import TokenBlocklist

# Isso garante que ambas as classes estejam registradas no Base.metadata
__all__ = ["Conta", "Transacao", 'TokenBlocklist']
