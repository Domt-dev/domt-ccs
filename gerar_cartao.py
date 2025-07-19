import random
import time
import os

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def ascii_caveira():
    return r"""
       ▄██████████████▄▐█▄▄▄▄█▌
      ██████▌▄▌▄▐▐▌███▌▀▀██▀▀
      ████▄█▌▄▌▄▐▐▌▀███▄▄█▌
      ▄▄▄▄▄██████████████▀
    """

def iniciar_programa():
    print("🛠️ Iniciando programa Império das GGs Domt...")
    for i in range(10, 0, -1):
        print(f"⌛ {i}s restante(s)...")
        time.sleep(1)
    print("✅ Sistema carregado!\n")

def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10

def generate_luhn_number(prefix, length=16):
    number = prefix
    while len(number) < (length - 1):
        number += str(random.randint(0, 9))
    checksum = luhn_checksum(number + '0')
    check_digit = (10 - checksum) % 10
    return number + str(check_digit)

def generate_expiry_date():
    month = random.randint(1, 12)
    year = random.randint(25, 29)
    return f"{month:02d}/{year}"

def generate_cvv(tipo="credito"):
    if tipo == "amex":
        return str(random.randint(1000, 9999))
    return str(random.randint(100, 999))

def gerar_cartao(tipo):
    clear()
    print(ascii_caveira())
    print("   ☠️ Domt CC'S ☠️\n")
    iniciar_programa()

    if tipo == 1:
        nome = "Crédito"
        prefixos = ['4111', '5500', '4000']
    elif tipo == 2:
        nome = "Débito"
        prefixos = ['5067', '5041', '5090']
    else:
        validar_manual()
        return

    prefixo = random.choice(prefixos)
    numero = generate_luhn_number(prefixo)
    validade = generate_expiry_date()
    cvv = generate_cvv()

    print(f"\n🎴 Cartão {nome} Gerado:")
    print(f" Número  : {numero}")
    print(f" Validade: {validade}")
    print(f" CVV     : {cvv}")
    print(f" Bandeira: {'Visa' if prefixo.startswith('4') else 'Mastercard'}")
    print("\n👻 Use apenas para fins de teste/estudo.\n")

def validar_manual():
    num = input("Digite o número do cartão para validar: ").strip()
    if luhn_checksum(num) == 0:
        print("✅ Cartão válido pelo algoritmo de Luhn.")
    else:
        print("❌ Cartão inválido.")

def menu():
    while True:
        print("""
☠️==== MENU DOMT CC'S ====☠️

1 - Gerar Cartão de Crédito
2 - Gerar Cartão de Débito
3 - Validar Número de Cartão
0 - Sair
""")
        try:
            opcao = int(input("Escolha uma opção: "))
            if opcao == 0:
                break
            elif opcao in [1, 2, 3]:
                gerar_cartao(opcao)
            else:
                print("❌ Opção inválida.")
        except ValueError:
            print("❌ Digite um número válido.")

if __name__ == "__main__":
    menu()
  
