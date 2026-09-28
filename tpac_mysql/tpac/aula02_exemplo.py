from controllers.usuario_controller import UsuarioController

controller = UsuarioController()

while True:
    print("\n=== EXEMPLO AULA 02 ===")
    print("1. Listar perfis")
    print("2. Criar perfil")
    print("3. Sair")

    opcao = input("Escolha: ").strip()

    if opcao == "1":
        print("\nPerfis:")
        for nome in controller.listar_perfis():
            print("-", nome)

    elif opcao == "2":
        nome = input("Nome: ").strip()
        print("1. Direto")
        print("2. Detalhado")
        escolha = input("Estilo: ").strip()
        estilo = "detalhado" if escolha == "2" else "direto"
        resposta = controller.criar_perfil(nome, estilo)
        print(resposta["mensagem"])

    elif opcao == "3":
        break
