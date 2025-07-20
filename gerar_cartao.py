import os
import random
import time
def identificar_bandeira(numero_cartao: str) -> str:
    if numero_cartao.startswith('4'):
        return 'Visa'
    elif numero_cartao[:2] in [str(i) for i in range(51, 56)]:
        return 'MasterCard'
    elif numero_cartao[:2] in ['34', '37']:
        return 'Amex'
    elif numero_cartao.startswith('6011') or numero_cartao.startswith('65') or \
         numero_cartao[:3] in [str(i) for i in range(644, 650)] or \
         numero_cartao[:6] in [str(i) for i in range(622126, 622926)]:
        return 'Discover'
    elif numero_cartao[:2] == '35':
        return 'JCB'
    elif numero_cartao[:2] in ['36', '38']:
        return 'Diners Club'
    else:
        return 'Desconhecida'
ARQUIVO_BINS = "bins.txt"
ARQUIVO_GERADOS = "cartoes_gerados.txt"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def carregar_bins():
    if not os.path.exists(ARQUIVO_BINS):
        print(f"Arquivo {ARQUIVO_BINS} não encontrado! Crie um arquivo com BINs (6 dígitos) na raiz.")
        return []
    with open(ARQUIVO_BINS, "r") as f:
        bins = [linha.strip() for linha in f.readlines() if linha.strip() and linha.strip().isdigit()]
    return bins

def numero_ja_gerado(numero):
    if not os.path.exists(ARQUIVO_GERADOS):
        return False
    with open(ARQUIVO_GERADOS, "r") as f:
        return numero in f.read().splitlines()

def salvar_numero(numero):
    with open(ARQUIVO_GERADOS, "a") as f:
        f.write(numero + "\n")

def gerar_cvv(manual=None):
    if manual and manual.isdigit() and len(manual) == 3:
        return manual
    return str(random.randint(100, 999))

def gerar_validade():
    mes = str(random.randint(1, 12)).zfill(2)
    ano = str(random.randint(2025, 2035))
    return mes, ano

def calcular_luhn_check_digit(num_sem_ultimo):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(num_sem_ultimo)
    soma = 0
    for i in range(len(digits)):
        d = digits[-(i+1)]
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        soma += d
    check_digit = (10 - (soma % 10)) % 10
    return str(check_digit)

def gerar_cartao(bin6):
    if len(bin6) != 6 or not bin6.isdigit():
        raise ValueError("BIN deve ter exatamente 6 dígitos numéricos")
    # Gerar os 9 dígitos intermediários + 1 check digit
    while True:
        corpo = ''.join(str(random.randint(0,9)) for _ in range(9))
        num_sem_check = bin6 + corpo
        check_digit = calcular_luhn_check_digit(num_sem_check)
        numero_completo = num_sem_check + check_digit
        if not numero_ja_gerado(numero_completo):
            salvar_numero(numero_completo)
            return numero_completo

def print_banner():
    whale = r"""
             --------
                |  DOMT-DEV  |
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
    clear_screen()
    print(whale)
    print("Iniciando programa Império das GG's Domt...\n")
    time.sleep(2)

def menu():
    print_banner()
    print("1 - Gerar cartões de CRÉDITO")
    print("2 - Gerar cartões de DÉBITO")
    print("3 - Validar cartão manualmente (Luhn)")
    print("0 - Sair")
    return input("Escolha uma opção: ").strip()

def validar_luhn(numero):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(numero)
    soma = 0
    parity = len(digits) % 2
    for i, d in enumerate(digits):
        if i % 2 == parity:
            d *= 2
            if d > 9:
                d -= 9
        soma += d
    return soma % 10 == 0

def validar_manual():
    num = input("Digite o número do cartão para validar: ").strip()
    if len(num) < 13 or not num.isdigit():
        print("Número inválido. Deve conter pelo menos 13 dígitos numéricos.")
        return
    if validar_luhn(num):
        print("✅ Cartão VÁLIDO pelo algoritmo de Luhn.")
    else:
        print("❌ Cartão INVÁLIDO.")

def gerar_cartoes(tipo):
    bins = carregar_bins()
    if not bins:
        print("Nenhum BIN carregado. Verifique o arquivo bins.txt")
        return

    try:
        qtd = int(input("Quantos cartões deseja gerar? (1 a 100): "))
        if qtd < 1 or qtd > 100:
            print("Quantidade inválida.")
            return
    except:
        print("Quantidade inválida.")
        return

    custom_bin = input("Digite um BIN personalizado (6 dígitos) ou deixe vazio para usar aleatório: ").strip()
    if custom_bin and (not custom_bin.isdigit() or len(custom_bin) != 6):
        print("BIN inválido, usando aleatório.")
        custom_bin = ""

    cvv_custom = input("Digite CVV (3 dígitos) ou deixe vazio para gerar aleatório: ").strip()
    if cvv_custom and (not cvv_custom.isdigit() or len(cvv_custom) != 3):
        print("CVV inválido, gerando aleatório.")
        cvv_custom = ""

    print(f"\nGerando {qtd} cartões {tipo.upper()}...\n")
    for _ in range(qtd):
        bin_usado = custom_bin if custom_bin else random.choice(bins)
        numero = gerar_cartao(bin_usado)
        mes, ano = gerar_validade()
        cvv = gerar_cvv(cvv_custom)
        bandeira = identificar_bandeira(numero)
print(f"{numero}|{mes}|{ano}|{cvv} ➜ {bandeira}")
    print("\n✔️ Geração finalizada.\n")
    input("Pressione ENTER para voltar ao menu...")

def main():
    while True:
        escolha = menu()
        if escolha == "1":
            gerar_cartoes("crédito")
        elif escolha == "2":
            gerar_cartoes("débito")
        elif escolha == "3":
            validar_manual()
            input("Pressione ENTER para voltar ao menu...")
        elif escolha == "0":
            print("Encerrando o programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")
            time.sleep(1)

if __name__ == "__main__":
    main()
    
