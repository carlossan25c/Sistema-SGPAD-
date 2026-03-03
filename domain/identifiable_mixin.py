import uuid

class IdentifiableMixin:
    """
    Mixin que fornece um identificador único universalmente exclusivo (UUID) para uma classe.
    """
    def __init__(self, *args, **kwargs):
        self._id = str(uuid.uuid4())
        super().__init__(*args, **kwargs)

    @property
    def id(self):
        """
        Retorna o ID único do objeto.
        """
        return self._id
