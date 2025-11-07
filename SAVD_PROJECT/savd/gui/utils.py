from tkinter import filedialog
from tkinter import messagebox
from analyzer import *
from pathlib import Path
import os


#  ----------------- CORES E ESTILOS -----------------
BG_COLOR = "#0d3b52"         
BTN_COLOR = "#ece5e5"      
BTN_ANALYZE_COLOR = "#0052cc"  
FONT_COLOR_WHITE = "#ffffff"
LABEL_COLOR = "#ffffff"
FONT_COLOR_BLACK = "#000000"
FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_TEXT = ("Calibri", 13)
PADY = 20


# ----------------- SELEÇÃO DE ARQUIVO .DOCX (sem mudanças) -----------------
def select_docx(label, btn):
    file_types = [("Documento Word","*.docx"), ("Todos os arquivos", "*.*")]

    docx_path = filedialog.askopenfilename(
        filetypes=file_types,
        defaultextension="*.docx"
    )

    ext = Path(docx_path).suffix
    
    try:
        if docx_path and ext == ".docx":
            file_name = os.path.basename(docx_path)
            label.config(text=f"📄 {file_name}", font=("Calibri", 13, "bold") )
            btn.pack(pady=PADY)
            return docx_path
        
        elif docx_path and ext != ".docx":
            messagebox.showwarning("Tipo Inválido", "Por favor, selecione um arquivo .docx")
            label.config(text="Nenhum arquivo selecionado", font=FONT_TEXT)
            btn.pack_forget()
            return None
    except Exception as e:
        print(f"ERRO: {e}")

# ----------------- SALVAMENTO DO ARQUIVO -----------------
def save_txt_docx(txt_file_to_convert):
    """Pede ao usuário um local e NOME de arquivo para salvar o .docx final."""
    try:
        docx_output_path = filedialog.asksaveasfilename(
            filetypes=[("Documento Word", "*.docx")],
            defaultextension="*.docx",
            title="Salvar como..."
        )

        # Se o usuário não cancelar a janela de salvar
        if docx_output_path:
            # Agora chamamos a função do backend com os dois caminhos
            txt_to_docx(txt_file_to_convert, docx_output_path)
            messagebox.showinfo("Salvamento concluído!", "Arquivo salvo com sucesso em formato .docx")
        else:
            # Usuário clicou em "cancelar"
            return None
        # -----------------------------------------------
    except Exception as e:
        print(f'ERRO: {e}')
        messagebox.showerror("Erro ao Salvar", f"Não foi possível salvar o arquivo.\nErro: {e}")


def save_txt_html(txt_file_to_convert):
    """
    Pede ao usuário onde salvar o relatório final em formato .html
    """
    try:
        html_output_path = filedialog.asksaveasfilename(
            filetypes=[("Página Web", "*.html")],
            defaultextension="*.html",
            title="Salvar como..."
        )

        if html_output_path:
            txt_to_html(txt_file_to_convert, html_output_path)
            messagebox.showinfo("Salvamento concluído!", "Arquivo salvo com sucesso em formato .html")
        else:
            return None

    except Exception as e:
        print(f'ERRO: {e}')
        messagebox.showerror("Erro ao Salvar", f"Não foi possível salvar o arquivo.\nErro: {e}")


# ----------------- ANÁLISE E VERIFICAÇÃO DO ARQUIVO .DOCX -----------------
def analyzer_docx(docx_file, txt_output_path):
    """ Função para chamar o backend."""
    
    try:
        docx_to_txt(docx_file, txt_output_path)
        print(f"Arquivo temporário gerado em: {txt_output_path}")
    except Exception as e:
        print(f"Erro em analyzer_docx: {e}")
        messagebox.showerror("Erro na Análise", f"Não foi possível processar o arquivo.\nErro: {e}")
