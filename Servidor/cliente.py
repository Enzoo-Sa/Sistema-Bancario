class Cliente:

    __slots__ = ['_nome', '_cpf']

    def __init__(self, nome, cpf):
        self._nome = nome
        self._cpf = cpf

        @property
        def nome(self):
            return self._nome

        @nome.setter
        def nome(self, nome):
            self._nome = nome

        @property
        def cpf(self):
            return self._cpf

        @cpf.setter
        def cpf(self, cpf):
            self._cpf = cpf
