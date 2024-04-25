from tabulate import tabulate

NUMEROS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
LETRAS = ['A', 'B', 'C', 'D', 'E', 'F']
MAIUSCULAS = "[ABCDEFGHIJKLMNOPQRSTUVWXYZ]"
MINUSCULAS = "[abcdefghijklmnopqrstuvwxyz]"
RESERVADAS = [
    'rotina', 'fim_rotina', 'se', 'senao', 'imprima', 'leia', 'para',
    'enquanto'
]


def analisador_lexico(arquivo):

  estado = 0
  lexema = ""
  resultados = []
  id_coluna = 0
  for caractere in arquivo.strip() + "\n":

      if caractere == "+" and estado == 0:
        lexema += caractere
        estado = 70
      elif estado == 70:
        resultados.append(("TK_SOMA", lexema, id_coluna))
        if caractere in NUMEROS:
            lexema += caractere
            estado = 1
        else:
            estado = 0
  
      elif caractere == "-" and estado == 0:
        lexema += caractere
        estado = 71
      elif estado == 71:
        resultados.append(("TK_SUBTRAÇÃO", lexema, id_coluna))
        if caractere in NUMEROS:
            lexema += caractere
            estado = 1
        else:
            estado = 0
  
      elif caractere == "*" and estado == 0:
        lexema += caractere
        estado = 84
      elif estado == 84:
        resultados.append(("TK_MULTIPLICAÇÃO", lexema, id_coluna))
  
      elif caractere == "%" and estado == 0:
        lexema += caractere
        estado = 72
      elif estado == 72:
        resultados.append(("TK_RESTO", lexema, id_coluna))
  
      elif caractere == "&" and estado == 0:
        lexema += caractere
        estado = 73
      elif estado == 73:
        resultados.append(("TK_AND", lexema, id_coluna))
  
      elif caractere == "~" and estado == 0:
        lexema += caractere
        estado = 74
      elif estado == 74:
        resultados.append(("TK_NEGAÇÃO", lexema, id_coluna))
  
      elif caractere == "|" and estado == 0:
        lexema += caractere
        estado = 75
      elif estado == 75:
        resultados.append(("TK_OR", lexema, id_coluna))
  
      elif caractere == ":" and estado == 0:
        lexema += caractere
        estado = 77
      elif estado == 77:
        resultados.append(("TK_OP", lexema, id_coluna))
  
      elif caractere == ")" and estado == 0:
        lexema += caractere
        estado = 78
      elif estado == 78:
        resultados.append(("TK_FECHA_PARENTESES", lexema, id_coluna))
  
      elif caractere == "(" and estado == 0:
        lexema += caractere
        estado = 79
      elif estado == 79:
        resultados.append(("TK_ABRE_PARENTESES", lexema, id_coluna))
  
      elif caractere == ">" and estado == 0:
        lexema += caractere
        estado = 85
      elif caractere == "=" and estado == 85:
        lexema += caractere
        estado = 87
      elif estado == 87:
        resultados.append(("TK_MENOR_IGUAL", lexema, id_coluna))
  
      elif caractere not in [">", "=", "NUMEROS"] and estado == 85:
        lexema += caractere
        estado = 86
  
      elif caractere == "=" and estado == 0:
        lexema += caractere
        estado = 41
      elif caractere == "=" and estado == 41:
        lexema += caractere
        estado = 69
      elif estado == 69:
        resultados.append(("TK_COMPARA", lexema, id_coluna))
  
      elif caractere == "<" and estado == 0:
        lexema += caractere
        estado = 27
      elif caractere == ">" and estado == 27:
        lexema += caractere
        estado = 66
      elif estado == 66:
        resultados.append(("TK_DIFERENTE", lexema, id_coluna))
  
      elif caractere == "=" and estado == 46:
        lexema += caractere
        estado = 41
      elif caractere == "=" and estado == 41:
        lexema += caractere
        estado = 68
      
      elif estado == 68:
        resultados.append(("TK_ATRIBUIÇÃO", lexema, id_coluna))
    
      # Reconhecer comentários de bloco
      elif caractere == "<" and estado == 0:
          lexema += caractere
          estado = 27
      elif estado == 27 and caractere == "<":
          lexema += caractere
      elif estado == 27:
          lexema += caractere
          estado = 28
      elif estado == 28 and caractere == "<":
          lexema += caractere
      elif estado == 28:
          lexema += caractere
          estado = 29
      elif estado == 29 and caractere == "<":
          lexema += caractere
      elif estado == 29:
          lexema += caractere
          estado = 30
      elif estado == 30 and caractere == ">":
          lexema += caractere
          estado = 67
      elif estado == 30:
          lexema += caractere
      elif estado == 67:
          resultados.append(("TK_COMENT_BLOCO", lexema, id_coluna))
          estado = 0
          lexema = ""
      elif estado == 0 and caractere == ">":
          estado = 0
          lexema = ""
    
      elif estado in [27, 28, 29, 30]:
        
          resultados.append(("ERRO_COMENT_NAO_FECHADO", lexema, id_coluna))
          estado = 0
          lexema = ""

    # Reconhecer float
      elif estado == 0 and caractere in NUMEROS:
            lexema += caractere
            estado = 1
      elif estado == 1 and caractere in NUMEROS:
            lexema += caractere
            estado = 2
      elif estado == 2 and caractere == ".":
            lexema += caractere
            estado = 8
      elif estado == 8 and caractere in NUMEROS:
            lexema += caractere
            estado = 9
      elif estado == 9 and caractere in NUMEROS:
            lexema += caractere
      elif estado == 9 and caractere == "e":
            lexema += caractere
            estado = 6
      elif estado == 6 and caractere in NUMEROS:
            lexema += caractere
            estado = 7
      elif estado == 6 and caractere == "-":
            lexema += caractere
            estado = 21
      elif estado == 21 and caractere in NUMEROS:
            lexema += caractere
            estado = 7
      elif estado == 7 and caractere in NUMEROS:
            lexema += caractere
            estado = 7

        # Reconhecer INT
      elif estado == 0 and caractere in NUMEROS:
            lexema += caractere
            estado = 1
      elif estado in [1, 2, 3] and caractere in NUMEROS:
            lexema += caractere
            estado += 1
      elif estado in [1, 3] and caractere == [".", "/", "_", "x"]:
            resultados.append(("Número Inválido", lexema))
            lexema = ""
            estado = 0
      elif estado == 4 and caractere in [".", "/", "_"]:
            resultados.append(("Número Inválido", lexema))
            lexema = ""
            estado = 0
      elif estado == 2 and caractere == "x":
            lexema += caractere
            estado = 4
      elif estado == 61 and caractere in NUMEROS + LETRAS:
            lexema += caractere
            estado = 61
      elif estado == 61:
            resultados.append(("TK_INT", lexema))
            lexema = ""
            estado = 0

    # Checar se o último lexema é um número float
      if estado in [9, 7]:
        resultados.append(("TK_FLOAT", lexema, id_coluna))
        
        #reconhecer data
      elif estado == 0 and caractere in NUMEROS:
        lexema += caractere
        estado = 1
      elif estado == 1 and caractere in NUMEROS:
        lexema += caractere
        estado = 2
      elif estado == 2:
        if caractere == "/":
          lexema += caractere
          estado = 5
      elif caractere == "_":
          lexema += caractere
          estado = 17
      elif estado == 5 and caractere in NUMEROS:
        lexema += caractere
        estado = 11
      elif estado == 11 and caractere in NUMEROS:
        lexema += caractere
        estado = 12
      elif estado == 12:
        if caractere == "/":
          lexema += caractere
          estado = 13
      elif caractere == "_":
        lexema += caractere
        estado = 19
      elif estado == 13 and caractere in NUMEROS:
        lexema += caractere
        estado = 14
      elif estado == 14 and caractere in NUMEROS:
        lexema += caractere
        estado = 15
      elif estado == 15 and caractere in NUMEROS:
        lexema += caractere
        resultados.append(("TK_DATA", lexema))
        lexema = ""
        estado = 0
      elif estado == 5 and caractere == "_":
        resultados.append(("ERRO: Formato de DATA inválido", lexema))
        lexema = ""
        estado = 0
      elif estado == 13 and caractere == "_":
        resultados.append(("ERRO: Formato de DATA inválido", lexema))
        lexema = ""
        estado = 0
      elif estado == 15 and caractere == "_":
        resultados.append(("ERRO: Formato de DATA inválido", lexema))
        lexema = ""
        estado = 0

      # Reconhecer ENDEREÇO
      elif caractere.isalnum() and estado == 0:
        lexema += caractere
        estado = 52
      elif caractere == "x" and estado == 52:
        lexema += caractere
        estado = 53
      elif caractere.isalnum() and estado == 53:
        lexema += caractere
        estado = 54
      elif caractere.isalnum() and estado == 54:
        lexema += caractere
        estado = 54
      elif caractere == "x" and estado == 1:
        lexema += caractere
        estado = 53
      elif caractere.isalnum() and estado == 53:
        lexema += caractere
        estado = 54
      elif caractere.isalnum() and estado == 54:
        lexema += caractere
        estado = 54
 
      elif estado in [53, 54] and not caractere.isalnum():
        if all(c.isdigit() or c.lower() in 'abcdef' for c in lexema[2:]):
          resultados.append(("TK_END", lexema))
        else:
          resultados.append(("ERRO: Endereço Inválido", lexema))
        lexema = ""
        estado = 0
  
      # Reconhecer id
      elif estado == 0 and caractere.islower():
        lexema += caractere
        estado = 48
      elif caractere.isupper() and estado == 48:
        lexema += caractere
        estado = 33
      elif caractere.islower() and estado == 33:
        lexema += caractere
        estado = 51
      elif caractere.isupper() and estado == 51:
        lexema += caractere
        estado = 76
  
      # Verificação de ID
      elif estado == 0 and caractere.islower():
        lexema += caractere
        estado = 51
      elif estado == 0 and caractere.isupper():
        lexema += caractere  # Adiciona o caractere ao lexema
        estado = 51  # Transita para o estado 51
      elif estado == 51 and caractere.isupper():
        resultados.append(("ERRO: ID Inválido", lexema + caractere))
        lexema = ""
        estado = 0
      elif estado == 76 and caractere.islower():
        lexema += caractere
        estado = 51
      elif estado == 51 and caractere.islower():
        lexema += caractere
        estado = 51
      elif estado == 76 and caractere.isupper():
        resultados.append(("ERRO: ID Inválido", lexema + caractere))
        lexema = ""
        estado = 0
      elif estado == 51 and not caractere.isalpha():
        if len(lexema) >= 2:
          resultados.append(("TK_ID", lexema))
        else:
          resultados.append(("ERRO: ID Inválido", lexema))
        lexema = ""
        estado = 0
      elif estado == 76 and not caractere.isalpha():
        if len(lexema) >= 2 and lexema[0].islower() and all(c.isalpha()
                                                            for c in lexema[1:]):
          resultados.append(("TK_ID", lexema))
        else:
          resultados.append(("ERRO: ID Inválido", lexema))
        lexema = ""
        estado = 0
  
      # Reconhecer palavras reservadas
      elif estado == 48:
          if caractere in MINUSCULAS:
              estado = 81
          else:
              estado = 33
      elif estado == 81:
          if caractere in MINUSCULAS:
              estado = 81
          elif caractere == "_":
              estado = 82
          elif caractere in MAIUSCULAS:
              estado = 83
      elif estado == 82:
          if caractere in MINUSCULAS:
              estado = 82
          elif caractere in MAIUSCULAS:
              estado = 83
  
      elif estado == 83 and lexema in RESERVADAS:
          print("Lexema", lexema, caractere)
          resultados.append(("TK_PALAVRAS_RESERVADAS", lexema, id_coluna))
          estado, lexema = (23, "") if caractere == '"' else (0, "")
  
      # Reconhecer comentários de linha
      elif caractere == '#' and estado == 0:
        lexema += caractere
        estado = 25
      elif estado == 25 and caractere != '\n':
        lexema += caractere
      elif estado == 25 and caractere == '\n':
        resultados.append(("TK_COMENTARIO_LINHA", lexema))
        lexema = ""
        estado = 0
      elif estado == 65 and caractere == '\n':
        estado = 0
  
  # Reconhecer Cadeias
      elif caractere == '"' and estado == 0:
        if '"' in lexema:
          resultados.append(("ERRO: Cadeia Inválida", lexema))
          lexema = ""
        else:
          lexema += caractere
          estado = 23
      elif estado == 23:
        if caractere == '"' and '\n' not in lexema:
          lexema += caractere
          estado = 64
          resultados.append(("TK_CADEIA", lexema))
          lexema = ""
        else:
          lexema += caractere
  
  if estado == 23:
      resultados.append(("ERRO: Cadeia não fechada", arquivo.strip()))
  elif estado == 0 and '"' in arquivo.strip():
      resultados.append(
        ("TK_ERRO: Cadeia não aberta corretamente", arquivo.strip()))
      resultados = [r for r in resultados if r[0] != "TK_ERRO: Cadeia Inválida"]
  
  if resultados == [] and arquivo.strip():
      if lexema.isdigit():
        resultados.append(("TK_INT", lexema))
      elif '/' in lexema or '_' in lexema:
        resultados.append(("TK_DATA", lexema))


  lexema = "" if caractere == " " else caractere
  if caractere == '"':
    estado = 23
  elif caractere == "*":
    estado = 84
  elif caractere == "+":
    estado = 70
  elif caractere == "-":
    estado = 71
  elif caractere == "%":
    estado = 72
  elif caractere == "&":
    estado = 73
  elif caractere == "~":
    estado = 74
  elif caractere == ":":
    estado = 77
  elif caractere == "/":
    estado = 75
  elif caractere == "=":
    estado = 41
  elif caractere == "<":
    estado = 27
  elif caractere == ">":
    estado = 84
  elif caractere == "(":
    estado = 78
  elif caractere == ")":
    estado = 79
  elif caractere in MINUSCULAS:
    estado = 48
  elif caractere == "#":
    estado = 25
  elif caractere == ".":
    estado = 8
  elif caractere in NUMEROS:
    estado = 1
  elif caractere in LETRAS:
    estado = 52
  elif caractere == " ":
    estado = 0
  
  return resultados


def escrever_resultados_em_arquivo(resultados, nome_arquivo):
  with open(nome_arquivo, "w") as arquivo:
    for resultado in resultados:
      linha = " | ".join(map(str, resultado))
      arquivo.write(f"{linha.rstrip()}\n"
                    ) 

def contar_uso_tokens(resultados):
  tokens_table = [["TOKEN", "USOS"]]
  for token, uso in resultados.items():
    tokens_table.append([token, uso])
  tokens_table.append(["Total", sum(resultados.values())])

  return tokens_table


def main(nome_arquivo):
  linhas_tabela = []
  tokens = {}
  with open(nome_arquivo, "r") as arquivo:
    for num_linha, linha in enumerate(arquivo, start=1):
      resultados = analisador_lexico(linha)
      for resultado in resultados:
        token = resultado[0]  # Acessa o token da tupla
        lexema = resultado[1]  # Acessa o lexema da tupla
        if token in tokens:
          tokens[token] += 1
        else:
          tokens[token] = 1
        linhas_tabela.append([num_linha, token, lexema])

  print(
      tabulate(linhas_tabela,
               headers=["LINHA", "TOKEN", "LEXEMA"],
               tablefmt="grid"))

  tokens_table = contar_uso_tokens(tokens)
  print(tabulate(tokens_table, headers="firstrow", tablefmt="grid"))

  escrever_resultados_em_arquivo(linhas_tabela, "saida.txt")


if __name__ == "__main__":
  nome_arquivo = "arquivo.txt"
  main(nome_arquivo)
