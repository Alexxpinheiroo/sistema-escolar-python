import json
import os

# Define os arquivos para cada módulo
arquivos = {
    "estudantes": "estudantes.json",
    "professores": "professores.json",
    "disciplinas": "disciplinas.json",
    "turmas": "turmas.json",
    "matriculas": "matriculas.json"
}

# Campos para cada módulo
campos = {
    "estudantes": ["codigo", "nome", "cpf"],
    "professores": ["codigo", "nome", "cpf"],
    "disciplinas": ["codigo", "nome"],
    "turmas": ["codigo", "codigo_professor", "codigo_disciplina"],
    "matriculas": ["codigo_turma", "codigo_estudante"]
}

def carregar(nome):
    if not os.path.exists(arquivos[nome]):
        return []
    with open(arquivos[nome], "r") as f:
        return json.load(f)

def salvar(nome, dados):
    with open(arquivos[nome], "w") as f:
        json.dump(dados, f)

def existe_codigo(lista, codigo, campo="codigo"):
    for item in lista:
        if item.get(campo) == codigo:
            return True
    return False

def incluir(nome):
    dados = carregar(nome)
    novo = {}
    for c in campos[nome]:
        valor = input(f"Digite {c}: ")
        if c == "codigo" or c.startswith("codigo"):
            # tenta converter para inteiro
            try:
                valor = int(valor)
            except:
                print("Valor inválido, deve ser número.")
                return
            if existe_codigo(dados, valor, c):
                print(f"Já existe um registro com {c} {valor}")
                return
        novo[c] = valor
    dados.append(novo)
    salvar(nome, dados)
    print(f"{nome.capitalize()} incluído com sucesso!")

def listar(nome):
    dados = carregar(nome)
    if not dados:
        print(f"Nenhum {nome} cadastrado.")
        return
    for i, d in enumerate(dados):
        info = " | ".join(f"{k}: {v}" for k, v in d.items())
        print(f"{i+1} - {info}")

def editar(nome):
    dados = carregar(nome)
    if not dados:
        print(f"Nenhum {nome} cadastrado.")
        return
    try:
        cod = int(input("Digite o código para editar: "))
    except:
        print("Código inválido.")
        return
    for d in dados:
        if d.get("codigo") == cod:
            for c in campos[nome]:
                if c == "codigo" or c.startswith("codigo"):
                    continue
                novo = input(f"Novo valor para {c} (atual: {d.get(c)}): ")
                if novo.strip() != "":
                    d[c] = novo
            salvar(nome, dados)
            print("Registro atualizado!")
            return
    print("Registro não encontrado.")

def excluir(nome):
    dados = carregar(nome)
    if not dados:
        print(f"Nenhum {nome} cadastrado.")
        return
    try:
        cod = int(input("Digite o código para excluir: "))
    except:
        print("Código inválido.")
        return
    for i, d in enumerate(dados):
        if d.get("codigo") == cod:
            dados.pop(i)
            salvar(nome, dados)
            print("Registro excluído!")
            return
    print("Registro não encontrado.")

def menu_modulo(nome):
    while True:
        print(f"\n--- {nome.capitalize()} ---")
        print("1 - Incluir")
        print("2 - Listar")
        print("3 - Editar")
        print("4 - Excluir")
        print("5 - Voltar")
        op = input("Opção: ")
        if op == "1":
            incluir(nome)
        elif op == "2":
            listar(nome)
        elif op == "3":
            editar(nome)
        elif op == "4":
            excluir(nome)
        elif op == "5":
            break
        else:
            print("Opção inválida")

def menu_principal():
    while True:
        print("\n=== Sistema Escolar ===")
        print("1 - Estudantes")
        print("2 - Professores")
        print("3 - Disciplinas")
        print("4 - Turmas")
        print("5 - Matrículas")
        print("6 - Sair")
        escolha = input("Escolha uma opção: ")
        if escolha == "1":
            menu_modulo("estudantes")
        elif escolha == "2":
            menu_modulo("professores")
        elif escolha == "3":
            menu_modulo("disciplinas")
        elif escolha == "4":
            menu_modulo("turmas")
        elif escolha == "5":
            menu_modulo("matriculas")
        elif escolha == "6":
            print("Saindo...")
            break
        else:
            print("Opção inválida")

if __name__ == "__main__":
    menu_principal()
