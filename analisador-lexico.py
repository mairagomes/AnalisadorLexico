import tabulate  # Importa o módulo tabulate para formatar dados em tabelas

NUMEROS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']  # Lista de dígitos numéricos de 0 a 9
LETRAS = ['A', 'B', 'C', 'D', 'E', 'F']  # Lista de letras hexadecimais de A a F
MAIUSCULAS = "[ABCDEFGHIJKLMNOPQRSTUVWXYZ]"  # Expressão regular representando letras maiúsculas
MINUSCULAS = "[abcdefghijklmnopqrstuvwxyz]"  # Expressão regular representando letras minúsculas
HEXADECIMAIS = "0123456789ABCDEF"  # String contendo todos os dígitos hexadecimais
RESERVADAS = [  # Lista de palavras reservadas em uma linguagem de programação
    'rotina', 'fim_rotina', 'se', 'senao', 'imprima', 'leia', 'para', 'enquanto'
]


tokens = []
resultados = []

#Responsável por realizar a análise léxica de um arquivo de entrada.
def analisador_lexico(arquivo):
  lexema = ''
  coluna = 1
  linha = 1
  estado = 0
  posicao = 0

#Inicializa as variáveis necessárias para rastrear o lexema atual, a posição na linha e no arquivo, e o estado atual do analisador léxico.
  while posicao < len(arquivo):
    c = arquivo[posicao]

    if estado == 0:
      if digitos(c):
        estado = 1
      elif hexadecimal(c):
        estado = 52
      if c == '"':
        estado = 23
      elif c == "*":
        estado = 84
      elif c == "+":
        estado = 70
      elif c == "-":
        estado = 71
      elif c == "%":
        estado = 72
      elif c == "&":
        estado = 73
      elif c == "~":
        estado = 74
      elif c == ":":
        estado = 77
      elif c == "/":
        estado = 75
      elif c == "=":
        estado = 41
      elif c == "<":
        estado = 27
      elif c == ">":
        estado = 84
      elif c == "(":
        estado = 79
      elif c == ")":
        estado = 78
      elif c in MINUSCULAS:
        estado = 48
      elif c == "#":
        estado = 25
      elif c == ".":
        estado = 8
      elif c in NUMEROS:
        estado = 1
      elif c in LETRAS:
        estado = 52
      elif c == " ":
        estado = 0
    elif estado == 1:
      if digitos(c):
        estado = 2
      elif c == 'x':
        estado = 53
      elif c == '.':
        estado = 8
      if not digitos(c) and c != 'x' and c != '.':
        estado = 61
        
#RECONHCER DATA
    elif estado == 2:
      if (digitos(c) is False
        and c != '/'
        and c != '_'
        and c != '.'):
        estado = 61
      elif c == '/':
        estado = 5
      elif c == '_':
        estado = 17
      elif digitos(c):
        estado = 3
      elif c == '.':
        estado = 8
    elif estado == 5:
      if digitos(c):
        estado = 11
      else:
        salvar_resultados(linha, coluna, "TK_ERRO: DATA INVALIDA")
        estado = 0
        lexema = ''
    elif estado == 11:
      if digitos(c):
        estado = 12
      else:
        salvar_resultados(linha, coluna, "TK_ERRO: DATA INVALIDA")
        estado = 0
        lexema = ''
    elif estado == 12:
      if c == '/':
        estado = 13
      else:
        salvar_resultados(linha, coluna, "TK_ERRO: DATA INVALIDA")
        estado = 0
        lexema = ''
    elif estado == 13:
      if digitos(c):
        estado = 14
      else:
        salvar_resultados(linha, coluna, "TK_ERRO: DATA INVALIDA")
        estado = 0
        lexema = ''
    elif estado == 14:
      if digitos(c):
        estado = 15
      else:
        salvar_resultados(linha, coluna, "TK_ERRO: DATA INVALIDA")
        estado = 0
        lexema = ''
    elif estado == 15:
      if digitos(c):
        estado = 60
      else:
        salvar_resultados(linha, coluna, "TK_ERRO: DATA INVALIDA")
        estado = 0
        lexema = ''
    elif estado == 60:
      if digitos(c):
        estado = 62
      else:
        salvar_resultados(linha, coluna, "TK_ERRO: DATA INVALIDA")
        estado = 0
        lexema = ''
    elif estado == 17:
      if digitos(c):
        estado = 18
      else:
        salvar_resultados(linha, coluna, "TK_ERRO: DATA INVALIDA")
        estado = 0
        lexema = ''
    elif estado == 18:
      if digitos(c):
        estado = 19
      else:
        salvar_resultados(linha, coluna, "TK_ERRO: DATA INVALIDA")
        estado = 0
        lexema = ''
    elif estado == 19:
      if c == '_':
        estado = 13
      else:
        salvar_resultados(linha, coluna, "TK_ERRO: DATA INVALIDA")
        estado = 0
        lexema = ''

#RECONHECER FLOAT
    elif estado == 3:
      if c != '.' and not digitos(c):
        estado = 61 #RECONHECE INT
      elif digitos(c):
        estado = 4
      elif c == '.':
        estado = 9
    elif estado == 4:
      if digitos(c):
        estado = 4
      elif not digitos(c):
        estado = 61 # RECONHECE INT
    elif estado == 4:
      if digitos(c):
        estado = 4
      elif c == 'e':
        estado = 6
      elif c != 'e':
        estado = 63
      else:
        salvar_resultados(linha, coluna - 1, "TK_ERRO: FLOAT NÃO RECONHECIDO")
        estado = 0
        lexema = ''
    elif estado == 6:
      if digitos(c):
        estado = 6
      elif c == '-':
        estado = 21
      elif c != '-' and not digitos(c):
        estado = 63
    elif estado == 21:
      if digitos(c):
        estado = 21
      elif not digitos(c):
        estado = 63
      else:
        salvar_resultados(linha, coluna - 1, "TK_ERRO: FLOAT NÃO RECONHECIDO")
        estado = 0
        lexema = ''
    elif estado == 8:
      if digitos(c):
        estado = 1
      else:
        salvar_resultados(linha, coluna - 1, "TK_ERRO: FLOAT NÃO RECONHECIDO")
        estado = 0
        lexema = ''

#RECONHECE ENDEREÇO, CADEIA, ID, PALAVRA RESERVADA
    elif estado == 52:
      if c == 'x':
        estado = 53
      else:
        salvar_resultados(linha, coluna - 1, "Formato de endereço inválido")
    elif estado == 53:
      if hexadecimal(c) or digitos(c):
        estado = 54
      else:
        salvar_resultados(linha, coluna - 1, "Formato de endereço inválido")
    elif estado == 54:
      if hexadecimal(c) or digitos(c):
        estado = 54
      elif not hexadecimal(c) and digitos(c):
        estado = 80
    elif estado == 23:
      if c == '"':
        estado = 64
      elif caracter(c):
        estado = 100
      else:
        salvar_resultados(linha, coluna - 1, "TK_ERRO: CADEIA INVALIDA")
        estado = 0
        lexema = ''
    elif estado == 100:
      if c == '"':
        estado = 64
      elif caracter(c):
        estado = 100
      else:
        salvar_resultados(linha, coluna - 1, "TK_ERRO: CADEIA ABERTA E NÃO FECHADA")
        estado = 0
        lexema = ''
    elif estado == 48:
      if letra_minuscula(c):
        estado = 81
      elif letra_maiuscula(c):
        estado = 49
      else:
        salvar_resultados(linha, coluna - 1, "ID || palavra reservada")
        estado = 0
        lexema = ''
    elif estado == 81:
      if letra_minuscula(c):
        estado = 81
      elif c == '_':
        estado = 82
      elif not letra_minuscula(c):
        estado = 83
      else:
        salvar_resultados(linha, coluna - 1, "Palavra reservada")
        estado = 0
        lexema = ''
    elif estado == 82:
      if letra_minuscula(c):
        estado = 82
      elif not letra_minuscula(c):
        estado = 83
      else:
        salvar_resultados(linha, coluna - 1, "Palavra reservada")
        estado = 0
        lexema = ''
    elif estado == 49:
      estado = 51 if letra_minuscula(c) else 76
    elif estado == 51:
      estado = 49 if letra_maiuscula(c) else 76
    elif estado == 50:
      if c != '=':
        estado = 88
      elif c == '=':
        estado = 45
    elif estado == 41:
      if c == '=':
        estado = 69
      else:
        salvar_resultados(linha, coluna, "Erro ==")
    elif estado == 27:
      if c != '>' and c != '<' and c != '=':
        estado = 68
      elif c == '>':
        estado = 66
      elif c == '=':
        estado = 27
      elif c == '<':
        estado = 28
      else:
        salvar_resultados(linha, coluna, "TK_ERRO: COMENTÁRIO INVÁLIDO")
    elif estado == 27:
      if c != '=':
        estado = 87
      elif c == '=':
        estado = 68
    elif estado == 28:
      if c == '<':
        estado = 30
      else:
        salvar_resultados(linha, coluna, "TK_ERRO: COMENTÁRIO ABERTO E NÃO FECHADO")
    elif estado == 30:
      if letra_minuscula(c) or digitos(
          c) or letra_maiuscula(c):
        estado = 30
      elif c == '>':
        estado = 31
      elif posicao == len(arquivo) - 1:
        salvar_resultados(linha, coluna, "TK_ERRO: COMENTÁRIO ABERTO E NÃO FECHADO")
        estado = 0
        lexema = ''
    elif estado == 31:
      if letra_minuscula(c) or digitos(
          c) or letra_maiuscula(c):
        estado = 31
      elif c == '>':
        estado = 32
      else:
        estado = 42
    elif estado == 32:
      if c == '>':
        estado = 67
    elif estado == 25 or estado == 101:
      if ((letra_minuscula(c) or digitos(c) or letra_maiuscula(c)) and
              c != '\n'):
          estado = 101
      elif c == '\n':
          estado = 65

    if estado == 83:
      if lexema.rstrip('\n') in palavras_reservadas:
        estado = palavras_reservadas.get(lexema.rstrip('\n'))
      else:
        salvar_resultados(linha, coluna - 1, "TK_ERRO: PALAVRA RESERVADA NÃO CONSTA")
        estado = 0
        lexema = ''
    if estado in estados_finais:
      salvar_token(estados_finais.get(estado), lexema, linha, coluna - 1)
      estado = 0
      lexema = ''
    elif estado in estados_finais_op:
      lexema += c
      salvar_token(estados_finais_op.get(estado), lexema, linha, coluna)
      estado = 0
      lexema = ''
      posicao += 1
      coluna += 1
    elif c == '\n':
      posicao += 1
      coluna = 1
      linha += 1
    elif c == ',' or c == ' ':
      posicao += 1
      coluna += 1
    elif estado == 0:
      if digitos(c) == False and c != '"':
        posicao += 1
    else:
      lexema += c
      posicao += 1
      coluna += 1


  return tokens, resultados

#  mapeia estados finais para tokens léxicos
estados_finais = {
    61: "TK_INT",            # Estado final para números inteiros
    63: "TK_FLOAT",          # Estado final para números de ponto flutuante
    65: "TK_COMENT_LINHA",   # Estado final para comentários de linha
    87: "TK_MENOR_OU_IGUAL", # Estado final para o operador de menor ou igual
    86: "TK_MENOR",          # Estado final para o operador de menor que
    76: "TK_ID",             # Estado final para identificadores
    88: "TK_MAIOR",          # Estado final para o operador de maior que
    83: "TK_ROTINA",   # Estado final para palavras reservadas
    103: "TK_FIM_ROTINA",    # Estado final para o token de fim de rotina
    104: "TK_SE",            # Estado final para o token 'se'
    105: "TK_SENAO",         # Estado final para o token 'senão'
    106: "TK_IMPRIMA",       # Estado final para o token 'imprima'
    107: "TK_LEIA",          # Estado final para o token 'leia'
    108: "TK_PARA",          # Estado final para o token 'para'
    109: "TK_ENQUANTO",      # Estado final para o token 'enquanto'
    80: "TK_END"             # Estado final para o token 'end'
}

#  mapeia estados finais para tokens léxicos de operadores
estados_finais_op = {
    70: "TK_SOMA",           # Estado final para o operador de soma
    71: "TK_SUB",            # Estado final para o operador de subtração
    84: "TK_MULTI",          # Estado final para o operador de multiplicação
    72: "TK_RESTO",          # Estado final para o operador de resto
    73: "TK_AND",            # Estado final para o operador de AND lógico
    75: "TK_OR",             # Estado final para o operador de OR lógico
    74: "TK_NEGACAO",        # Estado final para o operador de negação
    79: "TK_DELIMITADOR_ABERTURA",  # Estado final para o delimitador de abertura
    78: "TK_DELIMITADOR_FECHAMENTO",# Estado final para o delimitador de fechamento
    77: "TK_OP",             # Estado final para operadores
    62: "TK_DATA",           # Estado final para datas
    67: "TK_COMENT_BLOCO",   # Estado final para comentários em bloco
    68: "TK_ATRIBUICAO",     # Estado final para o operador de atribuição
    66: "TK_DIFERENTES",     # Estado final para o operador de diferença
    69: "TK_COMPARACAO",     # Estado final para operadores de comparação
    45: "TK_MAIOR_OU_IGUAL", # Estado final para o operador de maior ou igual
    64: "TK_CADEIA"          # Estado final para cadeias de caracteres
}

#  mapeia palavras reservadas para tokens
palavras_reservadas = {
    'rotina': 83,       # Palavra reservada 'rotina' é mapeada para o token 83
    'fim_rotina': 103,  # Palavra reservada 'fim_rotina' é mapeada para o token 103
    'se': 104,          # Palavra reservada 'se' é mapeada para o token 104
    'senao': 105,       # Palavra reservada 'senao' é mapeada para o token 105
    'imprima': 106,     # Palavra reservada 'imprima' é mapeada para o token 106
    'leia': 107,        # Palavra reservada 'leia' é mapeada para o token 107
    'para': 108,        # Palavra reservada 'para' é mapeada para o token 108
    'enquanto': 109     # Palavra reservada 'enquanto' é mapeada para o token 109
}

# Funções lambda para verificar tipos de caracteres
digitos = lambda c: c.isdigit()  # Verifica se o caractere é um dígito
letra_maiuscula = lambda c: 'A' <= c <= 'Z'  # Verifica se o caractere é uma letra maiúscula
letra_minuscula = lambda c: 'a' <= c <= 'z'  # Verifica se o caractere é uma letra minúscula
hexadecimal = lambda c: 'A' <= c <= 'F'  # Verifica se o caractere é hexadecimal
caracter = lambda c: c != '\n'  # Verifica se o caractere não é uma quebra de linha

# Funções lambda para manipulação de resultados
verificar_erro = lambda lista_resultados, num_linha: [erro for erro in lista_resultados if erro['LINHA'] == num_linha]  # Verifica se há erros na linha especificada
salvar_token = lambda token, lexema, linha, coluna: tokens.append({"TOKEN": token, "LEXEMA": lexema.strip(), "LINHA": linha, "COLUNA": coluna})  # Salva um token na lista de tokens
salvar_resultados = lambda linha, coluna, error_msg: resultados.append({"LINHA": linha, "COLUNA": coluna, "ERRO": error_msg})  # Salva um erro na lista de resultados

# Funções lambda para geração de tabelas
gerar_tabela = lambda data, headers: tabulate.tabulate([[item[field] for field in headers] for item in data], headers=headers, tablefmt="grid")  # Gera uma tabela formatada a partir dos dados fornecidos
gerar_tabela_token = lambda tokens: gerar_tabela(tokens, ["LIN", "COL", "TOKEN", "LEXEMA"])  # Gera uma tabela de tokens
gerar_tabela_erro = lambda resultados: gerar_tabela(resultados, ["LINHA", "COLUNA", "ERRO"])  # Gera uma tabela de erros

# Função principal
def main():
    global tokens, resultados
    archive_name = 'Ex-02-incorreto.cic'  # Nome do arquivo a ser analisado

    # Abre o arquivo para leitura
    with open(archive_name, 'r') as arquivo:
        arquivo_content = arquivo.read()  # Lê o conteúdo do arquivo
        arquivo_content = arquivo_content.replace("<<<", "").replace(">>>", "")  # Remove certos padrões do conteúdo
        analisador_lexico(arquivo_content)  # Chama a função de análise léxica passando o conteúdo do arquivo

        # Imprime tokens e tabela de uso
        token_table = gerar_tabela(tokens, ['LINHA', 'COLUNA', 'TOKEN', 'LEXEMA'])  # Gera uma tabela de tokens
        usage_table = {}
        for token in tokens:
            if token["TOKEN"] not in usage_table:
                usage_table[token["TOKEN"]] = 1
            else:
                usage_table[token["TOKEN"]] += 1
        total_usage = sum(usage_table.values())  # Calcula o total de uso de cada token
        usage_table["TOTAL"] = total_usage
        usage_table_formatted = tabulate.tabulate(usage_table.items(),
                                                  headers=['TOKEN', 'USOS'],
                                                  tablefmt='grid')  # Formata a tabela de uso de tokens
        print("\n", token_table)  # Imprime a tabela de tokens
        print(usage_table_formatted)  # Imprime a tabela de uso de tokens

        # Imprime resultados se houver
        if resultados:
            print("\n\n")
            with open(archive_name, 'r') as arquivo:
                linhas = arquivo.readlines()  # Lê as linhas do arquivo

                for num_linha, linha in enumerate(linhas, start=1):  # Itera sobre as linhas do arquivo
                    print(f"[{num_linha}] {linha.rstrip()}")  # Imprime a linha atual sem espaços à direita

                    lista_resultados = verificar_erro(resultados, num_linha)  # Verifica se há erros na linha atual
                    if lista_resultados:
                        for erro in lista_resultados:
                            coluna = erro["COLUNA"]
                            print('-' * (coluna + 3) + '^')  # Imprime indicadores de erro abaixo da linha
                        for erro in lista_resultados:
                            coluna = erro["COLUNA"]
                            linha = erro["LINHA"]
                            mensagem = erro["ERRO"]
                            print(f'Erro linha {linha} coluna {coluna}: {mensagem}')  # Imprime mensagens de erro


main()  # Chama a função principal