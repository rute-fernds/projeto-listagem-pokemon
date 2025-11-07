import re
import os
from conversion import *

pattern_itens = re.compile(r'^\s*(\d+(?:\.\d+)*\.|[a-zA-Z]\.)\s*(.*)$')
pattern_references = re.compile(r'(\d+(?:\.\d+)+)')

# ----------------  FUNÇÕES DE EXTRAÇÃO DE ÍNDICES ---------------- 
def extract_itens(txt_file_path):
    """Lê o arquivo .txt e retorna um dicionário de {indice: texto}."""
    itens = {}
    line_number = 0  # número real de linha (sem contar vazias)

    try:
        with open(txt_file_path, 'r', encoding='utf-8') as file:
            for i, line in enumerate(file):
                # Ignorar linhas vazias ou só com espaços
                if not line.strip():
                    continue
                
      
                line_number += 1

                # Aplica o regex em cada linha
                match = pattern_itens.match(line)
                
                if match:
                    key_iten = match.group(1)
                    text = match.group(2).strip()
                
                    itens[key_iten] = {'text': text,
                                       'line': line_number+1}

        return itens
        
    except FileNotFoundError:
        print(f"ERRO: O arquivo '{txt_file_path}' não foi encontrado.")
        return {}
    except Exception as e:
        print(f"ERRO inesperado ao processar o arquivo: {e}")
        return {}

def conversion_index(index_str):
    """ Converte um índice string em uma tupla de valores comparáveis.
    '10.1.' -> (10, 1)
    'a.'    -> (97,)
    'A.'    -> (65,)
    '1.a.'  -> (1, 97) """
    
    parses = index_str.strip('.').split('.')
    
    key_list = []
    try:
        for p in parses:
            try:
                key_list.append(int(p))
            except ValueError:
                if len(p) == 1 and p.isalpha():
                    key_list.append(ord(p))
                else:
                    key_list.append(float('inf'))
        
        return tuple(key_list)
        
    except Exception:
        return (float('inf'),)

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
            
            erro = (f"Linha {error_line-1}: {dict_itens[index_real]['text']} \nO índice '{index_real}' está fora de ordem. "
                    f"\nA sequência correta esperava o índice '{index}' nesta posição.")
    
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
                    found_text = line 

                references_line = pattern_references.findall(found_text)
                
                if not references_line :
                    continue

                for ref in set(references_line):
                    
                    ref_norman = ref.strip('.') + '.'
                    
                    if ref_norman not in set_itens:
                        
                        # Reporta o erro usando a referência original (como apareceu)
                        error = f"Linha {line_number}: referência o item '{ref}' que não existe."
                        errors_found.append(error)
                        
    except FileNotFoundError:
        errors_found.append(f"ERRO CRÍTICO: Arquivo {txt_file_path} não encontrado.")
    except Exception as e:
        errors_found.append(f"ERRO INESPERADO: {e} na linha {line_number}.")
        
    return errors_found


# ----------------  FUNÇÃO PARA GERAR RELATÓRIO DE ERROS ---------------- 
def save_errors_to_txt(errors_sequence, errors_references, output_path):
    """ Gera um relatório .txt consolidando as listas de erros de sequência e referência.
        Retorna o caminho do arquivo salvo. """
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("RELATÓRIO DE ANÁLISE DE DOCUMENTO\n")
            f.write("=" * 50 + "\n\n")

            # --- Erros de sequência ---
            f.write("🔢 ERROS DE SEQUÊNCIA NUMÉRICA\n")
            f.write("-" * 50 + "\n")
            if errors_sequence:
                for err in errors_sequence:
                    f.write(f"- {err}\n")
            else:
                f.write("Nenhum erro de sequência encontrado.\n")
            f.write("\n")

            # --- Erros de referência ---
            f.write("🔗 ERROS DE REFERÊNCIA\n")
            f.write("-" * 50 + "\n")
            if errors_references:
                for err in errors_references:
                    f.write(f"- {err}\n")
            else:
                f.write("Nenhum erro de referência encontrado.\n")
            f.write("\n")

        print(f"Relatório .txt salvo em: {output_path}")
        return output_path

    except Exception as e:
        print(f"Erro ao salvar relatório de erros: {e}")
        return None