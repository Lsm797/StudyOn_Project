# Versão com JSON + extras: prioridades, pesquisas e relatório diário
import time
import sys
import json
import os

DADOS_ARQUIVO = "dados.json"

# ----------------- Funções JSON -----------------

def carregar_dados():
    """Carrega dados do arquivo JSON. Se não existir, cria com admin padrão."""
    if os.path.exists(DADOS_ARQUIVO):
        try:
            with open(DADOS_ARQUIVO, "r", encoding="utf-8") as f:
                dados = json.load(f)
            # garantir chaves existentes
            if "usuarios" not in dados:
                dados["usuarios"] = [["admin", "admin@sistema.com", "123456", True]]
            if "solicitacoes" not in dados:
                dados["solicitacoes"] = []
            if "usuarios_dados" not in dados:
                dados["usuarios_dados"] = {}
            return dados
        except (json.JSONDecodeError, IOError):
            # arquivo corrompido: sobrescrever com padrão
            return {
                "usuarios": [["admin", "admin@sistema.com", "123456", True]],
                "solicitacoes": [],
                "usuarios_dados": {}
            }
    else:
        return {
            "usuarios": [["admin", "admin@sistema.com", "123456", True]],
            "solicitacoes": [],
            "usuarios_dados": {}
        }

def salvar_dados(dados):
    """Salva o dicionário completo no arquivo JSON."""
    with open(DADOS_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

# ----------------- Inicialização -----------------

dados = carregar_dados()
usuarios = dados["usuarios"]          # lista de listas: [nome, email, senha, is_admin]
solicitacoes = dados["solicitacoes"]  # lista de dicionários
usuarios_dados = dados["usuarios_dados"]  # cada usuário/email gera dicionário -> {metas, matriz_cronograma, anotacoes, lembretes, horarios, dias}

# função utilitária para garantir estrutura por usuário como acima /\
def garantir_estrutura_usuario(email):
    if email not in usuarios_dados:
        usuarios_dados[email] = {
            "metas": [],
            "cronograma": [],   # legado/backup
            "horarios": [       # horários padrão
                '07:00 - 08:00',
                '08:00 - 09:00',
                '09:00 - 10:00',
                '10:00 - 11:00',
                '11:00 - 12:00',
                '14:00 - 16:00',
                '16:00 - 17:00',
                '17:00 - 18:00'
            ],
            "dias": ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'],
            "matriz_cronograma": [],  # criada a partir de horarios x dias
            "anotacoes": [],
            "lembretes": []
        }
    # garantir matriz_cronograma coerente
    u = usuarios_dados[email]
    if "matriz_cronograma" not in u or not u["matriz_cronograma"]:
        u["matriz_cronograma"] = []
        for _ in range(len(u["horarios"])):
            u["matriz_cronograma"].append([''] * len(u["dias"]))

# util: encontra usuario por email (retorna a lista)
def encontrar_usuario_por_email(email):
    for u in usuarios:
        if u[1].lower() == email.lower():
            return u
    return None

# util: checar estrutura e salvar
def salvar_tudo():
    dados["usuarios"] = usuarios
    dados["solicitacoes"] = solicitacoes
    dados["usuarios_dados"] = usuarios_dados
    salvar_dados(dados)

# ----------------- Programa principal (menu) -----------------

while True:
    print("=== Sistema de Menu ===")
    print("1. Criar conta")
    print("2. Fazer login")
    print("3. Recuperar senha")
    print("0. Encerrar programa")

    opcao = input("Escolha uma opção: ").strip()

    if opcao == '0':
        print("Encerrando o programa...")
        salvar_tudo()
        sys.exit()

    elif opcao == '1':
        print("\n=== Criação de Conta ===")

        while True:
            nome_usuario = input("Digite o nome de usuário desejado (ou 'sair' para cancelar): ")
            if nome_usuario.lower() == 'sair':
                print("Você cancelou a criação da conta. Retornando ao menu principal.\n")
                break
            elif nome_usuario == "":
                print("O nome de usuário não pode ser vazio. Tente novamente.")
                continue
            break

        if nome_usuario.lower() == 'sair':
            continue

        while True:
            email = input("Digite seu email: ")
            if email.lower() == 'sair':
                print("Você cancelou a criação da conta. Retornando ao menu principal.\n")
                break
            elif email == "":
                print("O email não pode ser vazio. Tente novamente.")
                continue
            elif "@" not in email or "." not in email:
                print("Estrutura de e-mail inválida. Tente novamente.")
                continue

            existe_o_email = False
            for usuario in usuarios:
                if usuario[1].lower() == email.lower():
                    existe_o_email = True
                    break
            if existe_o_email:
                print("Este e-mail já está cadastrado. Tente novamente.")
                continue
            break

        if email.lower() == 'sair':
            continue

        while True:
            senha = input("Digite sua senha (mínimo 6 caracteres e pelo menos 1 número): ")
            if senha.lower() == 'sair':
                print("Você cancelou a criação da conta. Retornando ao menu principal.\n")
                break
            elif senha == "":
                print("A senha não pode ser vazia. Tente novamente.")
                continue
            elif len(senha) < 6:
                print("A senha deve ter pelo menos 6 caracteres. Tente novamente.")
                continue

            numeros = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            temnumero = False
            for caractere in senha:
                if caractere in numeros:
                    temnumero = True
                    break
            if not temnumero:
                print("A senha deve conter pelo menos 1 número. Tente novamente.")
                continue
            break

        if senha.lower() == 'sair':
            continue

        usuarios.append([nome_usuario, email, senha, False])
        garantir_estrutura_usuario(email)
        salvar_tudo()
        print(f"Conta criada com sucesso! Bem-vindo(a), {nome_usuario}!\n")

    elif opcao == '2':
        print("\n=== Login ===")

        cancel_login = False
        while True:
            email_login = input("Digite seu e-mail (ou 'sair' para cancelar): ")
            if email_login.lower() == 'sair':
                print("Você cancelou o login. Retornando ao menu principal.\n")
                cancel_login = True
                break
            elif email_login == "":
                print("O e-mail não pode ser vazio. Tente novamente.")
                continue
            elif "@" not in email_login or "." not in email_login:
                print("Estrutura de e-mail inválida. Tente novamente.")
                continue

            existe_o_email = False
            for user in usuarios:
                if user[1].lower() == email_login.lower():
                    existe_o_email = True
                    break
            if not existe_o_email:
                print("Este e-mail não está cadastrado. Tente novamente.\n")
                continue

            break

        if cancel_login:
            continue

        while True:
            senha_login = input("Digite sua senha (ou 'sair' para cancelar): ")
            if senha_login.lower() == 'sair':
                print("Você cancelou o login. Retornando ao menu principal.\n")
                cancel_login = True
                break
            elif senha_login == "":
                print("A senha não pode ser vazia. Tente novamente.")
                continue

            usuario_encontrado = None
            for usuario in usuarios:
                if usuario[1].lower() == email_login.lower() and usuario[2] == senha_login:
                    usuario_encontrado = usuario
                    break

            if usuario_encontrado:
                print(f"Login bem-sucedido! Bem-vindo(a) de volta, {usuario_encontrado[0]}!")
                break
            else:
                print('Senha incorreta! Tente novamente.')

        if cancel_login:
            continue

        # garante estrutura do usuário logado
        garantir_estrutura_usuario(usuario_encontrado[1])

        # ------------------- Área do Admin -------------------
        if usuario_encontrado[3] == True:
            print('Entrando na área do administrador...\n')

            while True:
                print('\n=== ÁREA DO ADMIN ===')
                print('1. Ver solicitações de suporte')
                print('2. Responder solicitação')
                print('0. Sair')

                opcao_admin = input('Escolha: ').strip()

                if opcao_admin == '1':
                    print('\n=== SOLICITAÇÕES DE SUPORTE ===')

                    if len(solicitacoes) == 0:
                        print('Nenhuma solicitação encontrada.\n')
                    else:
                        for i, s in enumerate(solicitacoes):
                            print(f'\nSolicitação {i+1}')
                            print(f'Usuário: {s["usuario"]}')
                            print(f'E-mail: {s["email"]}')
                            print(f'Dúvida: {s["duvida"]}')
                            print(f'Status: {"Respondida" if s["respondida"] else "Pendente"}')
                            if s["respondida"]:
                                print(f'Resposta: {s["resposta"]}')
                    print()

                elif opcao_admin == '2':
                    if len(solicitacoes) == 0:
                        print('Nenhuma solicitação encontrada.\n')
                    else:
                        print('=== Responder solicitação ===')

                        for i, s in enumerate(solicitacoes, start=1):
                            print(f'{i}. {s["usuario"]} - {s["duvida"]} ({"Respondida" if s["respondida"] else "Pendente"})')

                        try:
                            escolha = int(input("Digite o número da solicitação para responder: "))
                            if 1 <= escolha <= len(solicitacoes):
                                idx = escolha - 1
                                resposta = input("Digite sua resposta: ").strip()
                                solicitacoes[idx]["resposta"] = resposta
                                solicitacoes[idx]["respondida"] = True
                                salvar_tudo()
                                print("Solicitação marcada como respondida!\n")
                            else:
                                print("Número fora do intervalo.\n")
                        except ValueError:
                            print("Entrada inválida, digite um número.\n")

                elif opcao_admin == '0':
                    print('Saindo...\n')
                    break
                else:
                    print('Opção inválida!\n')

        # ------------------- Área do Usuário Comum -------------------
        else:
            email_logado = usuario_encontrado[1]
            # carrega dados locais
            user_data = usuarios_dados[email_logado]
            dias = user_data["dias"]
            horarios = user_data["horarios"]
            cronograma = user_data["matriz_cronograma"]
            metas = user_data["metas"]
            anotacoes = user_data["anotacoes"]
            lembretes = user_data["lembretes"]

            # loop principal do usuário
            while True:
                print('\n=== BEM VINDO AO STUDYON ===')
                print('  --- Menu Principal ---  ')
                print('1. Metas')
                print('2. Cronograma')
                print('3. Anotações')
                print('4. Lembretes')
                print('5. Cronômetro Pomodoro')
                print('6. Suporte')
                print('0. Sair')
                escolha = input ('Escolha uma opção: ').strip()

                # ---------- Metas ----------
                if escolha == '1':
                    def mostrar_barra_progresso(porcentagem):
                        barras = int(porcentagem // 5)
                        espacos = 20 - barras
                        print(f"[{'█' * barras}{' ' * espacos}] {porcentagem:.1f}%")

                    while True:
                        print("\n--- Minhas Metas ---")
                        print("1. Adicionar meta")
                        print("2. Ver metas")
                        print("3. Gerenciar submetas de uma meta")
                        print("4. Progresso geral das metas")
                        print("5. Marcar meta como concluída")
                        print("6. Editar/Excluir meta")
                        print("0. Voltar ao menu principal")

                        opc = input("Escolha uma opção: ").strip()

                        if opc == '1':
                            nome = input("\nDigite o nome da meta: ").strip()
                            if nome:
                                prioridade = input("Escolha a prioridade da meta (alta, média ou baixa): ").strip().lower()
                                if prioridade not in ["alta", "media", "baixa"]:
                                    prioridade = "media"
                                metas.append({
                                    "nome": nome,
                                    "submetas": [],
                                    "concluida": False,
                                    "prioridade": prioridade
                                })
                                salvar_tudo()
                                print("Meta adicionada com sucesso!")
                            else:
                                print("Você não digitou nenhuma meta.")

                        elif opc == '2':
                            if not metas:
                                print("Nenhuma meta cadastrada.")
                            else:
                                print("\nMetas:")
                                for i, meta in enumerate(metas, 1):
                                    if meta.get("concluida", False):
                                        status = "✓ CONCLUÍDA"
                                        total = 100
                                    else:
                                        submetas = meta["submetas"]
                                        if submetas:
                                            total = sum(s.get("progresso", 0) for s in submetas) / len(submetas)
                                        else:
                                            total = 0
                                        status = "em andamento"
                                    prior = meta.get("prioridade", "media")
                                    print(f"{i}. {meta['nome']} | Prioridade: {prior} | {status} - {total:.1f}%")

                        elif opc == '3':
                            if not metas:
                                print("Nenhuma meta cadastrada.")
                                continue

                            print("\nEscolha a meta que deseja gerenciar:")
                            for i, meta in enumerate(metas, 1):
                                print(f"{i}. {meta['nome']}")

                            escolha_meta = input("Número da meta: ").strip()

                            if not escolha_meta.isdigit() or not (1 <= int(escolha_meta) <= len(metas)):
                                print("Número inválido.")
                                continue

                            meta = metas[int(escolha_meta) - 1]

                            while True:
                                print(f"\n--- Submetas da meta: {meta['nome']} ---")
                                print("1. Adicionar submeta")
                                print("2. Ver submetas")
                                print("3. Editar progresso de uma submeta")
                                print("4. Renomear submeta")
                                print("5. Excluir submeta")
                                print("6. Marcar submeta como concluída")
                                print("0. Voltar")

                                subopc = input("Escolha: ").strip()

                                if subopc == '1':
                                    nome_sub = input("\nNome da submeta: ").strip()
                                    if nome_sub:
                                        meta["submetas"].append({"nome": nome_sub, "progresso": 0, "concluida": False})
                                        salvar_tudo()
                                        print("Submeta adicionada!")
                                    else:
                                        print("Você não digitou nada.")

                                elif subopc == '2':
                                    if not meta["submetas"]:
                                        print("Nenhuma submeta cadastrada.")
                                    else:
                                        print("\nSubmetas:")
                                        for i, s in enumerate(meta["submetas"], 1):
                                            status = "✓" if s.get("concluida", False) else ""
                                            print(f"{i}. {s['nome']} - {s['progresso']}% {status}")

                                elif subopc == '3':
                                    if not meta["submetas"]:
                                        print("Nenhuma submeta cadastrada.")
                                        continue

                                    for i, s in enumerate(meta["submetas"], 1):
                                        print(f"{i}. {s['nome']} - {s['progresso']}%")

                                    idx = input("Escolha a submeta: ").strip()
                                    if not idx.isdigit() or not (1 <= int(idx) <= len(meta["submetas"])):
                                        print("Número inválido.")
                                        continue

                                    nova = input("Novo progresso (0 – 100): ").strip()
                                    if nova.isdigit() and 0 <= int(nova) <= 100:
                                        meta["submetas"][int(idx) - 1]["progresso"] = int(nova)
                                        if int(nova) == 100:
                                            meta["submetas"][int(idx) - 1]["concluida"] = True
                                        salvar_tudo()
                                        print("Progresso atualizado!")
                                    else:
                                        print("Valor inválido.")

                                elif subopc == '4':
                                    if not meta["submetas"]:
                                        print("Nenhuma submeta cadastrada.")
                                        continue

                                    for i, s in enumerate(meta["submetas"], 1):
                                        print(f"{i}. {s['nome']}")

                                    idx = input("Escolha a submeta: ").strip()
                                    if not idx.isdigit() or not (1 <= int(idx) <= len(meta["submetas"])):
                                        print("Inválido.")
                                        continue

                                    novo_nome = input("Novo nome: ").strip()
                                    if novo_nome:
                                        meta["submetas"][int(idx) - 1]["nome"] = novo_nome
                                        salvar_tudo()
                                        print("Renomeada!")
                                    else:
                                        print("Nome vazio.")

                                elif subopc == '5':
                                    if not meta["submetas"]:
                                        print("Nenhuma submeta cadastrada.")
                                        continue

                                    for i, s in enumerate(meta["submetas"], 1):
                                        print(f"{i}. {s['nome']}")

                                    idx = input("Escolha a submeta: ").strip()
                                    if idx.isdigit() and 1 <= int(idx) <= len(meta["submetas"]):
                                        removida = meta["submetas"].pop(int(idx) - 1)
                                        salvar_tudo()
                                        print(f"Submeta '{removida['nome']}' excluída!")
                                    else:
                                        print("Inválido.")

                                elif subopc == '6':
                                    if not meta["submetas"]:
                                        print("Nenhuma submeta cadastrada.")
                                        continue

                                    for i, s in enumerate(meta["submetas"], 1):
                                        status = "✓" if s.get("concluida", False) else ""
                                        print(f"{i}. {s['nome']} - {s['progresso']}% {status}")

                                    idx = input("Escolha a submeta para marcar como concluída: ").strip()
                                    if idx.isdigit() and 1 <= int(idx) <= len(meta["submetas"]):
                                        sub = meta["submetas"][int(idx) - 1]
                                        sub["concluida"] = not sub.get("concluida", False)
                                        if sub["concluida"]:
                                            sub["progresso"] = 100
                                            print(f"Submeta '{sub['nome']}' marcada como concluída!")
                                        else:
                                            print(f"Submeta '{sub['nome']}' desmarcada.")
                                        salvar_tudo()
                                    else:
                                        print("Inválido.")

                                elif subopc == '0':
                                    break
                                else:
                                    print("Opção inválida.")

                        elif opc == '4':
                            if not metas:
                                print("Nenhuma meta cadastrada.")
                            else:
                                total_metas = 0
                                for meta in metas:
                                    if meta.get("concluida", False):
                                        total_metas += 100
                                    else:
                                        sbs = meta["submetas"]
                                        if sbs:
                                            prog = sum(s.get("progresso", 0) for s in sbs) / len(sbs)
                                            total_metas += prog
                                geral = total_metas / len(metas) if metas else 0
                                print("\nProgresso geral:")
                                mostrar_barra_progresso(geral)

                        elif opc == '5':
                            if not metas:
                                print("Nenhuma meta cadastrada.")
                                continue

                            print("\nEscolha a meta para marcar como concluída:")
                            for i, meta in enumerate(metas, 1):
                                status = "✓" if meta.get("concluida", False) else ""
                                print(f"{i}. {meta['nome']} {status}")

                            idx = input("Número da meta: ").strip()
                            if idx.isdigit() and 1 <= int(idx) <= len(metas):
                                meta = metas[int(idx) - 1]
                                meta["concluida"] = not meta.get("concluida", False)
                                if meta["concluida"]:
                                    print(f"Meta '{meta['nome']}' marcada como concluída!")
                                else:
                                    print(f"Meta '{meta['nome']}' desmarcada.")
                                salvar_tudo()
                            else:
                                print("Número inválido.")

                        elif opc == '6':
                            if not metas:
                                print("Nenhuma meta cadastrada.")
                                continue

                            print("\nEscolha a meta para editar/excluir:")
                            for i, meta in enumerate(metas, 1):
                                print(f"{i}. {meta['nome']}")

                            idx = input("Número da meta: ").strip()
                            if not idx.isdigit() or not (1 <= int(idx) <= len(metas)):
                                print("Número inválido.")
                                continue

                            print("\n1. Renomear meta")
                            print("2. Excluir meta")
                            print("3. Alterar prioridade")
                            print("0. Cancelar")

                            acao = input("Escolha: ").strip()
                            if acao == '1':
                                novo_nome = input("Novo nome: ").strip()
                                if novo_nome:
                                    metas[int(idx) - 1]["nome"] = novo_nome
                                    salvar_tudo()
                                    print("Meta renomeada!")
                                else:
                                    print("Nome vazio.")
                            elif acao == '2':
                                removida = metas.pop(int(idx) - 1)
                                salvar_tudo()
                                print(f"Meta '{removida['nome']}' excluída!")
                            elif acao == '3':
                                nova_prior = input("Nova prioridade (alta, média ou baixa): ").strip().lower()
                                if nova_prior in ["alta", "media", "baixa"]:
                                    metas[int(idx) - 1]["prioridade"] = nova_prior
                                    salvar_tudo()
                                    print("Prioridade atualizada!")
                                else:
                                    print("Valor inválido.")
                            elif acao == '0':
                                print("Operação cancelada.")
                            else:
                                print("Opção inválida.")

                        elif opc == '0':
                            print("Voltando ao menu…")
                            break

                        else:
                            print("Opção inválida.")


                # ---------- Cronograma ----------
                elif escolha == '2':
                    while True:
                        print('\n=== CRONOGRAMA ===')
                        print('1. Ver cronograma')
                        print('2. Gerenciar atividades e horários')
                        print('3. Ver relatório diário')
                        print('0. Voltar ao menu principal')

                        escolha_cron = input('Escolha: ').strip()

                        if escolha_cron == '0':
                            print('Voltando ao menu principal...')
                            break

                        elif escolha_cron == '1':
                            print('\n' + 'CRONOGRAMA'.center(130))
                            print('-' * 130)
                            print(f'{"HORÁRIO":<16}', end='')
                            for dia in dias:
                                print(f'{dia:^16}', end='')
                            print()
                            for i in range(len(horarios)):
                                print(f'{horarios[i]:<16}', end='')
                                for j in range(len(dias)):
                                    atividade = cronograma[i][j] if cronograma[i][j] else ' - '
                                    print(f'{atividade:^16}', end='')
                                print()
                            print('-' * 130)

                        elif escolha_cron == '2':
                            while True:
                                print('\n === GERENCIAR ATIVIDADES E HORÁRIOS ===')
                                print('1. Adicionar atividade')
                                print('2. Editar ou excluir atividade')
                                print('3. Adicionar ou editar horário')
                                print('0. Voltar')

                                subescolha = input('Escolha: ').strip()

                                if subescolha == '0':
                                    break

                                elif subescolha == '1':
                                    hora = input('Digite o horário (ex: 07:00 - 08:00): ').strip()
                                    if hora not in horarios:
                                        print('Horário não encontrado. Aqui estão os horários disponíveis:')
                                        for h in horarios:
                                            print(h)
                                        continue

                                    dia = input('Digite o dia da semana (ex: Segunda): ').strip().capitalize()
                                    if dia not in dias:
                                        print('Dia inválido.')
                                        continue

                                    i = horarios.index(hora)
                                    j = dias.index(dia)
                                    atividade = input('Digite a atividade: ').strip()

                                    if cronograma[i][j]:
                                        print(f'Já existe uma atividade: {cronograma[i][j]}')
                                        print('1. Substituir atividade')
                                        print('2. Acrescentar atividade')
                                        print('3. Cancelar')
                                        escolha_op = input('Escolha: ').strip()

                                        if escolha_op == '1':
                                            cronograma[i][j] = atividade
                                            salvar_tudo()
                                            print('Atividade atualizada!')

                                        elif escolha_op == '2':
                                            valor_atual = str(cronograma[i][j]).strip()
                                            if valor_atual == '':
                                                cronograma[i][j] = atividade.strip()
                                            else:
                                                cronograma[i][j] = valor_atual + ' + ' + atividade.strip()
                                            salvar_tudo()
                                            print('Atividade acrescentada!')

                                        elif escolha_op == '3':
                                            print('Operação cancelada!')
                                        else:
                                            print('Opção inválida!')
                                    else:
                                        cronograma[i][j] = atividade
                                        salvar_tudo()
                                        print('Atividade adicionada!')

                                elif subescolha == '2':
                                    hora = input('Digite o horário (ex: 07:00 - 08:00): ').strip()
                                    dia = input('Digite o dia da semana (ex: segunda): ').strip().capitalize()

                                    if hora in horarios and dia in dias:
                                        i = horarios.index(hora)
                                        j = dias.index(dia)

                                        if cronograma[i][j]:
                                            atividades = cronograma[i][j].split(' + ')
                                            if len(atividades) >= 1:
                                                print('\nAtividades encontradas nesse horário: ')
                                                for id, ativi in enumerate(atividades, start=1):
                                                    print(f'[{id}] {ativi}')

                                                escolha_atividade = input('Qual atividade deseja alterar/excluir? ').strip()
                                                try:
                                                    escolha_atividade = int(escolha_atividade)
                                                    if 1 <= escolha_atividade <= len(atividades):
                                                        print('\n[1] Editar atividade')
                                                        print('[2] Excluir atividade')

                                                        acao = input('Escolha: ').strip()

                                                        if acao == '1':
                                                            nova_atividade = input('Nova descrição: ').strip()
                                                            atividades[escolha_atividade - 1] = nova_atividade
                                                            cronograma[i][j] = ' + '.join(atividades)
                                                            salvar_tudo()
                                                            print('Atividade editada!')

                                                        elif acao == '2':
                                                            atividades.pop(escolha_atividade - 1)
                                                            if atividades:
                                                                cronograma[i][j] = ' + '.join(atividades)
                                                            else:
                                                                cronograma[i][j] = ''
                                                            salvar_tudo()
                                                            print('Atividade excluída!')
                                                        else:
                                                            print('Opção inválida.')
                                                            continue
                                                    else:
                                                        print('Escolha fora do intervalo.')
                                                except ValueError:
                                                    print('Você deve digitar um número.')
                                            else:
                                                print('Não há atividades.')
                                        else:
                                            print('Não há atividade cadastrada no dia/horário informado!')
                                    else:
                                        print('Dia ou horário inválido.')

                                elif subescolha == '3':
                                    print('\nHorários atuais:')
                                    for h in horarios:
                                        print(h)

                                    print('\n1. Adicionar novo horário')
                                    print('2. Editar horário existente')
                                    print('3. Excluir horário')

                                    escolha_h = input('Escolha: ').strip()

                                    if escolha_h == '1':
                                        novo_horario = input('Digite o novo horário (ex: 18:00 - 19:00): ').strip()

                                        if novo_horario not in horarios:
                                            horarios.append(novo_horario)
                                            cronograma.append(['' for _ in dias])
                                            salvar_tudo()
                                            print('Horário adicionado com sucesso!')
                                            
                                            for i in range(len(horarios)):
                                                for j in range(i + 1,len(horarios)):
                                                    if horarios[i] > horarios[j]:
                                                        horarios[i], horarios[j] = horarios[j], horarios[i]
                                                        cronograma[i], cronograma[j] = cronograma[j], cronograma[i]                                            
                                        else:
                                            print('Esse horário já existe.')

                                    elif escolha_h == '2':
                                        antigo_horario = input('Qual horário deseja alterar? ').strip()

                                        if antigo_horario in horarios:
                                            novo_horario = input('Digite o novo horário: ').strip()
                                            idx = horarios.index(antigo_horario)
                                            horarios[idx] = novo_horario
                                            salvar_tudo()
                                            print('Horário atualizado!')
                                        else:
                                            print('Horário não encontrado!')

                                    elif escolha_h == '3':
                                        excluir = input('Qual horário deseja excluir? ').strip()

                                        if excluir in horarios:
                                            idx = horarios.index(excluir)
                                            horarios.pop(idx)
                                            cronograma.pop(idx)
                                            salvar_tudo()
                                            print('Horário excluído com sucesso!')
                                        else:
                                            print('Esse horário não está incluído no cronograma.')

                                    else:
                                        print('Opção inválida.')

                                else:
                                    print('Opção inválida.')

                        elif escolha_cron == '3':
                            # Relatório diário
                            print("\n=== RELATÓRIO DIÁRIO ===")
                            dia_escolhido = input("Digite o dia da semana (ex: Segunda): ").strip().capitalize()

                            if dia_escolhido not in dias:
                                print("Dia inválido.")
                                continue

                            j = dias.index(dia_escolhido)

                            print(f"\n=== Atividades de {dia_escolhido} ===\n")
                            for i in range(len(horarios)):
                                atividade = cronograma[i][j] if cronograma[i][j] else "-"
                                print(f"{horarios[i]:<16} | {atividade}")

                        else:
                            print("Opção inválida.")

                # ----------- Anotações -----------
                elif escolha == '3':
                    while True:
                        print("\n=== ANOTAÇÕES ===")
                        print("1. Adicionar anotação")
                        print("2. Ver anotações")
                        print("3. Excluir anotação")
                        print("4. Pesquisar anotação")
                        print("0. Voltar ao menu principal")

                        op = input("Escolha uma opção: ").strip()

                        if op == '1':
                            texto = input("\nDigite sua anotação: ")
                            if texto.strip():
                                anotacoes.append(texto)
                                salvar_tudo()
                                print("Anotação adicionada com sucesso!")
                            else:
                                print("Anotacao vazia nao adicionada.")

                        elif op == '2':
                            print("\n=== Minhas Anotações ===")
                            if len(anotacoes) == 0:
                                print("Nenhuma anotação salva.")
                            else:
                                for i, nota in enumerate(anotacoes, 1):
                                    print(f"{i}. {nota}")

                        elif op == '3':
                            print("\n=== Excluir Anotação ===")
                            if len(anotacoes) == 0:
                                print("Nenhuma anotação para excluir.")
                            else:
                                for i, nota in enumerate(anotacoes, 1):
                                    print(f"{i}. {nota}")
                                apagar = input("Digite o número da anotação para excluir: ")

                                if apagar.isdigit() and 1 <= int(apagar) <= len(anotacoes):
                                    del anotacoes[int(apagar) - 1]
                                    salvar_tudo()
                                    print("Anotação excluída!")
                                else:
                                    print("Opção inválida.")

                        elif op == '4':
                            termo = input("Digite a palavra-chave para pesquisar: ").strip().lower()
                            resultados = [nota for nota in anotacoes if termo in nota.lower()]
                            print("\n=== Resultados da pesquisa ===")
                            if resultados:
                                for i, r in enumerate(resultados, 1):
                                    print(f"{i}. {r}")
                            else:
                                print("Nenhuma anotação encontrada com esse termo.")

                        elif op == '0':
                            break

                        else:
                            print("Opção inválida. Tente novamente.")

                # ---------- Lembretes ----------
                elif escolha == "4":
                    while True:
                        print("\n=== LEMBRETES ===")
                        print("1. Adicionar lembrete")
                        print("2. Ver lembretes")
                        print("3. Editar lembrete")
                        print("4. Excluir lembrete")
                        print("5. Pesquisar lembrete")
                        print("0. Voltar ao menu principal")

                        opcao = input("Escolha uma opção: ").strip()

                        if opcao == "1":
                            lembrete = input("Digite o lembrete: ").strip()
                            if lembrete:
                                lembretes.append(lembrete)
                                salvar_tudo()
                                print("Lembrete adicionado!")
                            else:
                                print("Lembrete vazio não adicionado.")

                        elif opcao == "2":
                            print("\nLISTA DE LEMBRETES")
                            print("==============================")
                            if len(lembretes) == 0:
                                print("Nenhum lembrete cadastrado.")
                            else:
                                for i in range(len(lembretes)):
                                    print(f"{i+1}. {lembretes[i]}")

                        elif opcao == "3":
                            if len(lembretes) == 0:
                                print("Nenhum lembrete para editar.")
                            else:
                                for i in range(len(lembretes)):
                                    print(f"{i+1}. {lembretes[i]}")

                                num = input("Número do lembrete para editar: ").strip()
                                if num.isdigit():
                                    num = int(num) - 1
                                    if 0 <= num < len(lembretes):
                                        novo = input("Novo texto: ")
                                        lembretes[num] = novo
                                        salvar_tudo()
                                        print("Lembrete editado!")
                                    else:
                                        print("Número inválido.")
                                else:
                                    print("Número inválido.")

                        elif opcao == "4":
                            if len(lembretes) == 0:
                                print("Nenhum lembrete para excluir.")
                            else:
                                for i in range(len(lembretes)):
                                    print(f"{i+1}. {lembretes[i]}")

                                num = input("Número do lembrete para excluir: ").strip()
                                if num.isdigit():
                                    num = int(num) - 1
                                    if 0 <= num < len(lembretes):
                                        removido = lembretes.pop(num)
                                        salvar_tudo()
                                        print(f"Lembrete '{removido}' excluído!")
                                    else:
                                        print("Número inválido.")
                                else:
                                    print("Número inválido.")

                        elif opcao == "5":
                            termo = input("Digite a palavra-chave para pesquisar: ").strip().lower()
                            resultados = [l for l in lembretes if termo in l.lower()]
                            print("\n=== Resultados da pesquisa ===")
                            if resultados:
                                for i, r in enumerate(resultados, 1):
                                    print(f"{i}. {r}")
                            else:
                                print("Nenhum lembrete encontrado com esse termo.")

                        elif opcao == "0":
                            print("Voltando ao menu principal...")
                            break

                        else:
                            print("Opção inválida!")

                # ---------- Cronômetro Pomodoro ----------
                elif escolha == '5':
                    print('\n--- Cronômetro Pomodoro ---')
                    try:
                        foco = int(input('Minutos de foco (padrão 25): ').strip() or '25')
                        pausa = int(input('Minutos de pausa (padrão 5): ').strip() or '5')
                        ciclos = int(input('Quantos ciclos você quer fazer?').strip() or '1')
                        print('\nPomodoro iniciado! Concentre-se, evite distrações e bons estudos. \n')
                        ciclo = 1
                        while ciclo <= ciclos:
                            print(f'== Ciclo {ciclo} de {ciclos} ==')

                            # tempo de foco
                            minutos_foco = foco*60
                            print('Foco:')
                            while minutos_foco > 0:
                                m= minutos_foco // 60
                                s= minutos_foco % 60
                                print(f'{m:02d}:{s:02d}')
                                time.sleep(1)
                                minutos_foco-=1
                            print('\n Foco concluído! Hora da pausa.')

                            if ciclo < ciclos:
                                minutos_pausa = pausa * 60
                                print('Pausa: ')
                                while minutos_pausa > 0:
                                    m= minutos_pausa // 60
                                    s = minutos_pausa % 60
                                    print(f'{m:02d}:{s:02d}')
                                    time.sleep(1)
                                    minutos_pausa-=1
                                print('\nPausa encerrada! Volte ao foco.')
                            ciclo+= 1
                    except ValueError:
                        print('Valor inválido. Digite apenas números.')

                # ---------- Suporte ----------
                elif escolha == "6":
                    while True:
                        print("\n===== SUPORTE =====")
                        print('1. Enviar nova solicitação')
                        print('2. Ver minhas solicitações')
                        print('0. Voltar ao menu principal')

                        opcao_sup = input('Escolha: ').strip()

                        if opcao_sup == '1':
                            duvida = input('Descreva sua dúvida ou problema: ').strip()

                            if duvida:
                                solicitacoes.append({
                                    "usuario": usuario_encontrado[0],
                                    "email": usuario_encontrado[1],
                                    "duvida": duvida,
                                    "respondida": False,
                                    "resposta": ""
                                })
                                salvar_tudo()
                                print("\nObrigado por relatar seu problema!")
                                print("Nosso suporte responderá em breve.\n")

                        elif opcao_sup == '2':
                            minhas_solicitacoes = [s for s in solicitacoes if s["email"] == usuario_encontrado[1]]
                            if len(minhas_solicitacoes) == 0:
                                print('Você não possui solicitações.\n')
                            else:
                                print('\n=== Minhas Solicitações ===')
                                for i, s in enumerate(minhas_solicitacoes, 1):
                                    print(f'\nSolicitação {i}')
                                    print(f'Dúvida: {s["duvida"]}')
                                    if s['respondida']:
                                        print(f'Resposta do admin: {s["resposta"]}')
                                    else:
                                        print('Ainda não respondida.')
                            print()

                        elif opcao_sup == '0':
                            print("Voltando ao menu principal...\n")
                            break

                        else:
                            print("Opção inválida!\n")

                # ------- Sair -----------
                elif escolha == "0":
                    print("\nSaindo do sistema...")
                    print("Obrigado por utilizar o programa! Até a próxima!\n")
                    # salvar antes de sair da conta
                    usuarios_dados[email_logado]["metas"] = metas
                    usuarios_dados[email_logado]["matriz_cronograma"] = cronograma
                    usuarios_dados[email_logado]["horarios"] = horarios
                    usuarios_dados[email_logado]["anotacoes"] = anotacoes
                    usuarios_dados[email_logado]["lembretes"] = lembretes
                    salvar_tudo()
                    break

                else:
                    print("Opção inválida. Tente novamente.\n")

    #----- recuperação de senha -----
    elif opcao == '3':
        print("\n=== Recuperação de Senha ===")
        email_recuperacao = input("Digite seu e-mail cadastrado: ")

        usuario_encontrado = None
        for usuario in usuarios:
            if usuario[1].lower() == email_recuperacao.lower():
                usuario_encontrado = usuario
                break

        if usuario_encontrado:
            print("E-mail encontrado. Vamos redefinir sua senha.")
            while True:
                novasenha = input("Digite sua nova senha (mínimo 6 caracteres e pelo menos 1 número): ")
                if novasenha == "":
                    print("A senha não pode ser vazia. Tente novamente.")
                    continue
                elif len(novasenha) < 6:
                    print("A senha deve ter pelo menos 6 caracteres. Tente novamente.")
                    continue
                elif novasenha == usuario_encontrado[2]:
                    print("A nova senha não pode ser igual à senha antiga. Tente novamente.")
                    continue

                senha_confirmacao = input("Confirme sua nova senha: ")
                if novasenha == senha_confirmacao:
                    usuario_encontrado[2] = novasenha
                    salvar_tudo()
                    print("Senha redefinida com sucesso!\n")
                    break
                else:
                    print("As senhas não coincidem. Tente novamente.\n")
        else:
            print("E-mail não encontrado. Verifique e tente novamente.")
    else:
        print("Opção inválida. Tente novamente.\n")
        
""hnhnjdv""