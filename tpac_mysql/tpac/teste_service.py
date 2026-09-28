from services.usuario_service import UsuarioService

service = UsuarioService()

# Caso válido
try:
    usuario = service.criar_usuario("Ana_Teste", "detalhado")
    print("✅ Criado:", usuario.nome, usuario.estilo_instrucao)
except ValueError as erro:
    print("❌ Não deveria falhar aqui:", erro)

# Caso que deve ser recusado (nome duplicado)
try:
    service.criar_usuario("Rafa_Aula02", "direto")
    print("❌ Não deveria ter criado, isso é um erro!")
except ValueError as erro:
    print("✅ Recusado corretamente:", erro)