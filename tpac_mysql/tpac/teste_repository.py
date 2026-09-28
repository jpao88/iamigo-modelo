from repositories.usuario_repository import UsuarioRepository

repo = UsuarioRepository()
print("ANTES:", [u.nome for u in repo.listar()])
if repo.buscar_por_nome("Rafa_Aula02") is None:
    repo.criar("Rafa_Aula02", "direto")
print("DEPOIS:", [u.nome for u in repo.listar()])