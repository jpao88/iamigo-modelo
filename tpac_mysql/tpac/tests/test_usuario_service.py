import unittest
from types import SimpleNamespace

from services.usuario_service import UsuarioService


class UsuarioRepositoryFake:
    """Repositório em memória: simula o banco sem precisar do MySQL."""

    def __init__(self):
        self.usuarios = []
        self.proximo_id = 1

    def listar(self):
        return list(self.usuarios)

    def buscar_por_nome(self, nome):
        for usuario in self.usuarios:
            if usuario.nome == nome:
                return usuario
        return None

    def buscar_por_id(self, usuario_id):
        for usuario in self.usuarios:
            if usuario.id == usuario_id:
                return usuario
        return None

    def criar(self, nome, estilo_instrucao, senha_hash=None):
        usuario = SimpleNamespace(
            id=self.proximo_id,
            nome=nome,
            estilo_instrucao=estilo_instrucao,
            senha_hash=senha_hash
        )
        self.proximo_id += 1
        self.usuarios.append(usuario)
        return usuario

    def atualizar(self, usuario_id, nome, estilo_instrucao):
        usuario = self.buscar_por_id(usuario_id)
        usuario.nome = nome
        usuario.estilo_instrucao = estilo_instrucao
        return usuario


class TestUsuarioServiceCriar(unittest.TestCase):
    def setUp(self):
        self.repository = UsuarioRepositoryFake()
        self.service = UsuarioService(repository=self.repository)

    def test_criar_com_dados_validos(self):
        usuario = self.service.criar_usuario("Ana", "direto")

        self.assertEqual(usuario.nome, "Ana")
        self.assertEqual(usuario.estilo_instrucao, "direto")
        self.assertEqual(len(self.repository.usuarios), 1)

    def test_nome_vazio_e_recusado(self):
        with self.assertRaises(ValueError) as contexto:
            self.service.criar_usuario("   ", "direto")

        self.assertEqual(str(contexto.exception), "O nome não pode ficar vazio.")
        self.assertEqual(len(self.repository.usuarios), 0)

    def test_nome_curto_e_recusado(self):
        with self.assertRaises(ValueError) as contexto:
            self.service.criar_usuario("Al", "direto")

        self.assertEqual(
            str(contexto.exception),
            "O nome precisa ter pelo menos 3 caracteres."
        )

    def test_estilo_invalido_e_recusado(self):
        with self.assertRaises(ValueError) as contexto:
            self.service.criar_usuario("Bia", "rapido")

        self.assertEqual(
            str(contexto.exception),
            "O estilo deve ser 'direto' ou 'detalhado'."
        )

    def test_nome_duplicado_e_recusado(self):
        self.service.criar_usuario("Ana", "direto")

        with self.assertRaises(ValueError) as contexto:
            self.service.criar_usuario("Ana", "detalhado")

        self.assertEqual(
            str(contexto.exception),
            "Já existe um perfil com esse nome."
        )
        self.assertEqual(len(self.repository.usuarios), 1)


class TestUsuarioServiceAtualizar(unittest.TestCase):
    def setUp(self):
        self.repository = UsuarioRepositoryFake()
        self.service = UsuarioService(repository=self.repository)

    def test_atualizar_mantendo_o_proprio_nome_e_permitido(self):
        usuario = self.service.criar_usuario("Ana", "direto")

        atualizado = self.service.atualizar_usuario(usuario.id, "Ana", "detalhado")

        self.assertEqual(atualizado.nome, "Ana")
        self.assertEqual(atualizado.estilo_instrucao, "detalhado")


if __name__ == "__main__":
    unittest.main()