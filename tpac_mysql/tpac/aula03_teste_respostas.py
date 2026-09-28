from controllers.usuario_controller import UsuarioController

controller = UsuarioController()

casos = [
    ("Rafa03", "direto"),
    ("Al", "direto"),
    ("Rafa03", "direto"),
    ("Bia", "rapido"),
]

for nome, estilo in casos:
    print(controller.criar_perfil(nome, estilo))