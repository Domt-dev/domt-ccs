import random
import time
import os

def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10

def is_valid_luhn(card_number):
    return luhn_checksum(card_number) == 0

def generate_card_number(tipo="credito"):
    # BINs: crédito e débito fictícios
    if tipo == "debito":
        bin_prefixes = ['5067', '5041', '4093']
    else:
        bin_prefixes = ['4539', '4556', '4916', '5105', '5204', '5306']
    bin_prefix = random.choice(bin_prefixes)
    length = 16
    number = bin_prefix
    while len(number) < (length - 1):
        number += str(random.randint(0, 9))
    checksum = luhn_checksum(int(number) * 10)
    return number + str((10 - checksum) % 10)

def generate_valid_date():
    month = str(random.randint(1, 12)).zfill(2)
    year = str(random.randint(2025, 2030))
    return month, year

def generate_cvv():
    return str(random.randint(100, 999))

def print_banner():
    whale = r"""
                 --------
              |  DOMT-Dev  |
                 --------
         \                     ^    /^
          \                   / \  / |
           \                 /   \/  |
              |\___/|      /         |
              /0  0  \__  /          |
             /     /  \/_/           |
             @_^_@'/   \             |
             //_^_/     \           |
          ( //) |        \         |
        ( / /) _|_ /   )   |        )
      ( // /) '/,_ _ _/  ( ; -.    |
    (( / / )) ,-{        _      `-.|
   (( // / ))  '/\      /                 )
   (( /// ))      `.   {         \      / 
    (( / ))     .----~-.\        \   (
                ///.----..>        \   \
                  ///-._ _ _ _ _ _ _}  \__)

        🐋 Domt CC'S — Império das GG's 🐋
    """
    os.system('clear')
    print(whale)
    print("Iniciando programa Império das GG's Domt...\n")
    time.sleep(2)

def gerar_cartoes(tipo="credito"):
    while True:
        try:
            qtd = int(input("Quantos cartões você quer gerar? (1 a 100): "))
            if 1 <= qtd <= 100:
                break
            else:
                print("❌ Digite um valor entre 1 e 100.")
        except ValueError:
            print("❌ Entrada inválida. Tente novamente.")

    resultado = []
    print("\n💳 Cartões Gerados (formato: número|mês|ano|cvv):\n")
    for _ in range(qtd):
        card = generate_card_number(tipo)
        mes, ano = generate_valid_date()
        cvv = generate_cvv()
        linha = f"{card}|{mes}|{ano}|{cvv}"
        resultado.append(linha)
        print(linha)

    salvar = input("\n💾 Deseja salvar em um arquivo? (s/n): ").strip().lower()
    if salvar == "s":
        nome = input("📝 Nome do arquivo (sem .txt): ").strip()
        with open(f"{nome}.txt", "w") as f:
            f.write("\n".join(resultado))
        print(f"✅ Salvo como {nome}.txt")

def validar_manual():
    card = input("🔍 Digite o número do cartão para validar (somente números): ").strip()
    if card.isdigit() and len(card) >= 13:
        if is_valid_luhn(card):
            print("✅ Cartão VÁLIDO (passa no algoritmo de Luhn).")
        else:
            print("❌ Cartão INVÁLIDO (não passa no Luhn).")
    else:
        print("⚠️ Número inválido ou muito curto.")

def menu():
    print_banner()
    while True:
        print("\n📋 Menu Principal")
        print("1️⃣  Gerar cartões de CRÉDITO")
        print("2️⃣  Gerar cartões de DÉBITO")
        print("3️⃣  Validar cartão manualmente")
        print("0️⃣  Sair")
        escolha = input("Escolha uma opção: ").strip()
        if escolha == "1":
            gerar_cartoes("credito")
        elif escolha == "2":
            gerar_cartoes("debito")
        elif escolha == "3":
            validar_manual()
        elif escolha == "0":
            print("👋 Encerrando. Até mais, GG.")
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
