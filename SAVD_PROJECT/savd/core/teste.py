import re
from savd.gui.conversion import *

pattern_itens = re.compile(r'^\s*(\d+(?:\.\d+)*\.)\s*(.*)$', re.MULTILINE)
# NOVO: Padrão para encontrar REFERÊNCIAS (versão robusta)
# Encontra padrões como '1.2' ou '10.5.3'
# Não captura mais o ponto final, se houver.
pattern_references = re.compile(r'(\d+(?:\.\d+)+)')

# ----------------  FUNÇÕES DE EXTRAÇÃO DE ÍNDICES ---------------- 
def extract_itens(txt_file_path):
    """Lê o arquivo .txt e retorna um dicionário de {indice: texto}."""
    itens = {}
    line_number = 0

    try:
        with open(txt_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line_number+=1
                
                # Aplica o regex em cada linha
                match = pattern_itens.match(line)
                
                if match:
                    key_iten = match.group(1)
                    text = match.group(2).strip()
                
                    itens[key_iten] = {'text': text,
                                       'line': line_number}
        return itens
        
    except FileNotFoundError:
        print(f"ERRO: O arquivo '{txt_file_path}' não foi encontrado.")
        return {}
    except Exception as e:
        print(f"ERRO inesperado ao processar o arquivo: {e}")
        return {}


def conversion_index(index_str):
    """ Converte um índice string '10.1.' em uma tupla de inteiros (10, 1)
    para permitir a ordenação numérica correta."""
    
    # Remove o ponto final e divide pelos outros pontos
    parses = index_str.strip('.').split('.')
    
    # Converte cada parte em um inteiro
    try:
        return [int(p) for p in parses]
    except ValueError:
        return [float('inf')]

# ----------------  FUNÇÃO DE ORDENAÇÃO ---------------- 
def key_ordering(itens):
    """Recebe o dicionário de itens e retorna uma LISTA de suas chaves
    ordenadas numericamente usando a função 'conversion_index'.
    Se 'conversion_index' falhar, esta função irá propagar a exceção."""
    ordered_keys = sorted(itens.keys(), key=conversion_index)
    
    return ordered_keys

# ----------------  FUNÇÕES DE VERIFICAÇÃO DA NUMERAÇÃO ---------------- 
def verified_sequence_number_order(dict_itens, index_list):
    """Verifica se a ordem dos itens no documento corresponde à ordem
    numérica correta. Encontra erros de "Transposição"."""

    key_document = list(dict_itens.keys())
    errors = []
    
    for position, index in enumerate(index_list):
        
        index_real = key_document[position]
        
        if index != index_real:
            
            error_line = dict_itens[index_real]['line']
            
            erro = (f"Linha {error_line}: Item {index_real} fora de ordem. "
                    f"A sequência correta esperava o item {index} nesta posição.")
    
            errors.append(erro)

    return errors


# ----------------  FUNÇÕES DE VERIFICAÇÃO DE REFERÊNCIAS ---------------- 
def verified_references(txt_file_path: str, definicoes_itens: dict) -> list[str]:
    """Verifica se todas as referências a itens no texto são válidas. (V2)
    Agora lida com referências sem ponto final (ex: "item 1.2 e...")"""

    errors_found = []
    set_itens = set(definicoes_itens.keys())
    line_number = 0

    try:
        with open(txt_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line_number += 1
                
                found_text = ""
                
                match_itens = pattern_itens.match(line)
                
                if match_itens:
                    found_text = match_itens.group(2) # Texto após a definição
                else:
                    found_text = line # Linha inteira

                # 3. Encontrar todas as referências (com o NOVO regex)
                #    'item 1.2 e...' -> encontra '1.2'
                #    'item 1.2. e...' -> encontra '1.2.'
                references_line = pattern_references.findall(found_text)
                
                if not references_line :
                    continue

                for ref in set(references_line):
                    
                    ref_norman = ref.strip('.') + '.'
                    
                    # 5. Validar a referência NORMALIZADA
                    if ref_norman not in set_itens:
                        
                        # Reporta o erro usando a referência original (como apareceu)
                        error = f"Linha {line_number}: Referência ao item '{ref}' que não existe."
                        errors_found.append(error)
                        
    except FileNotFoundError:
        errors_found.append(f"ERRO CRÍTICO: Arquivo {txt_file_path} não encontrado.")
    except Exception as e:
        errors_found.append(f"ERRO INESPERADO: {e} na linha {line_number}.")
        
    return errors_found


# ------------------ TESTANDO FUNÇÕES -------------------
txt = r"C:\Users\rutea\Desktop\SAVD_PROJECT\savd\docs\teste2.txt"
docx = r"C:\Users\rutea\Desktop\SAVD_PROJECT\savd\docs\teste4.docx"
html_f = r"C:\Users\rutea\Desktop\SAVD_PROJECT\savd\docs\teste4.html"


p = extract_itens(txt)
print(p)
f = key_ordering(p)
print(f)
print(verified_sequence_number_order(p, f))
print(verified_references(txt, p))
print("verificação")