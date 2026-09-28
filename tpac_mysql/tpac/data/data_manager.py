from typing import Dict, Any

from config.database import SessionLocal
from models.usuario import Usuario
from models.tarefa import Tarefa
from models.passo import Passo


def carregar_dados() -> Dict[str, Any]:
    """
    Busca os usuários, tarefas e passos no MySQL (via SQLAlchemy) e monta a
    mesma estrutura que antes era lida do arquivo tpac_users.json.

    Estrutura retornada:
    {
        "Nome": {
            "preferencias": {"estilo_instrucao": "direto"},
            "tarefas_diarias": [...],
            "tarefas_educacionais": [...]
        }
    }
    """
    dados = {}

    with SessionLocal() as session:
        usuarios = session.query(Usuario).order_by(Usuario.nome).all()

        for usuario in usuarios:
            dados[usuario.nome] = {
                "preferencias": {
                    "estilo_instrucao": usuario.estilo_instrucao
                },
                "tarefas_diarias": [],
                "tarefas_educacionais": []
            }

            tarefas = (
                session.query(Tarefa)
                .filter(Tarefa.usuario_id == usuario.id)
                .order_by(Tarefa.id)
                .all()
            )

            for tarefa in tarefas:
                tarefa_dict = {
                    "titulo": tarefa.titulo,
                    "descricao": tarefa.descricao,
                    "prioridade": tarefa.prioridade,
                    "prazo": tarefa.prazo.isoformat() if tarefa.prazo else None,
                    "concluida": bool(tarefa.concluida),
                    "passos": []
                }

                passos = (
                    session.query(Passo)
                    .filter(Passo.tarefa_id == tarefa.id)
                    .order_by(Passo.ordem)
                    .all()
                )

                for passo in passos:
                    tarefa_dict["passos"].append({
                        "texto": passo.texto,
                        "concluido": bool(passo.concluido)
                    })

                dados[usuario.nome][tarefa.tipo].append(tarefa_dict)

    return dados


def salvar_dados(dados: Dict[str, Any]) -> None:
    """
    Salva no MySQL (via SQLAlchemy) a estrutura completa do sistema, SEM
    apagar tudo primeiro. Em vez de TRUNCATE + reinsert, compara o que já
    existe no banco com o dicionário recebido e aplica só as diferenças:

    - usuários são identificados pelo nome (único);
    - tarefas são identificadas por (tipo, titulo) dentro de cada usuário;
    - passos são identificados pela posição (ordem) dentro de cada tarefa.

    Isso evita apagar dados criados por outras vias (como a API) que não
    estejam presentes no dicionário em memória da tela de console.
    """
    with SessionLocal() as session:
        try:
            usuarios_existentes = {
                usuario.nome: usuario
                for usuario in session.query(Usuario).all()
            }
            nomes_no_dict = set(dados.keys())

            for nome, info_usuario in dados.items():
                estilo = info_usuario.get("preferencias", {}).get(
                    "estilo_instrucao", "direto"
                )

                usuario = usuarios_existentes.get(nome)

                if usuario is None:
                    usuario = Usuario(nome=nome, estilo_instrucao=estilo)
                    session.add(usuario)
                    session.flush()
                else:
                    usuario.estilo_instrucao = estilo

                tarefas_existentes = {
                    (tarefa.tipo, tarefa.titulo): tarefa
                    for tarefa in session.query(Tarefa)
                    .filter(Tarefa.usuario_id == usuario.id)
                    .all()
                }
                chaves_tarefas_no_dict = set()

                for tipo in ["tarefas_diarias", "tarefas_educacionais"]:
                    for tarefa_info in info_usuario.get(tipo, []):
                        titulo = tarefa_info.get("titulo", "")
                        chave = (tipo, titulo)
                        chaves_tarefas_no_dict.add(chave)

                        tarefa = tarefas_existentes.get(chave)

                        if tarefa is None:
                            tarefa = Tarefa(
                                usuario_id=usuario.id,
                                tipo=tipo,
                                titulo=titulo,
                                descricao=tarefa_info.get("descricao"),
                                prioridade=tarefa_info.get("prioridade", "media"),
                                prazo=tarefa_info.get("prazo"),
                                concluida=bool(tarefa_info.get("concluida", False))
                            )
                            session.add(tarefa)
                            session.flush()
                        else:
                            tarefa.descricao = tarefa_info.get("descricao")
                            tarefa.prioridade = tarefa_info.get("prioridade", "media")
                            tarefa.prazo = tarefa_info.get("prazo")
                            tarefa.concluida = bool(tarefa_info.get("concluida", False))

                        passos_existentes = {
                            passo.ordem: passo
                            for passo in session.query(Passo)
                            .filter(Passo.tarefa_id == tarefa.id)
                            .all()
                        }
                        ordens_no_dict = set()

                        for ordem, passo_info in enumerate(
                            tarefa_info.get("passos", []), start=1
                        ):
                            ordens_no_dict.add(ordem)
                            passo = passos_existentes.get(ordem)

                            if passo is None:
                                passo = Passo(
                                    tarefa_id=tarefa.id,
                                    texto=passo_info.get("texto", ""),
                                    concluido=bool(passo_info.get("concluido", False)),
                                    ordem=ordem
                                )
                                session.add(passo)
                            else:
                                passo.texto = passo_info.get("texto", "")
                                passo.concluido = bool(passo_info.get("concluido", False))

                        for ordem_existente, passo_existente in passos_existentes.items():
                            if ordem_existente not in ordens_no_dict:
                                session.delete(passo_existente)

                for chave_existente, tarefa_existente in tarefas_existentes.items():
                    if chave_existente not in chaves_tarefas_no_dict:
                        session.delete(tarefa_existente)

            for nome_existente, usuario_existente in usuarios_existentes.items():
                if nome_existente not in nomes_no_dict:
                    session.delete(usuario_existente)

            session.commit()

        except Exception:
            session.rollback()
            raise