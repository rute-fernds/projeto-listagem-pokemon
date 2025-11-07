import tkinter as tk
import os
from utils import *

# ----------------- CONFIGURAÇÕES DA JANELA PRINCIPAL -----------------
main_window = tk.Tk()
main_window.title('SAVD - Sistema de Análise e Verificação de Documentos')
main_window.config(bg=BG_COLOR)
main_window.minsize(750, 450)

# Centralizando a janela na tela
main_window.update_idletasks()
width = main_window.winfo_width()
height = main_window.winfo_height()
x = (main_window.winfo_screenwidth() // 2) - (width // 2)
y = (main_window.winfo_screenheight() // 2) - (height // 2)
main_window.geometry(f"+{x}+{y}")

# ---------------- VARIÁVEL GLOBAL ----------------
selected_file_path = None
txt_file = None
report_txt_path = "relatorio_temp.txt"  # arquivo temporário de erros

# ---------------- FUNÇÕES DE SELEÇÃO ----------------
def handle_select_file():
    global selected_file_path
    selected_file_path = select_docx(label_file_name, btn_analyze)


def handle_analyzer_file():
    global selected_file_path, report_txt_path

    if not selected_file_path:
        messagebox.showwarning("Nenhum arquivo", "Selecione um arquivo .docx primeiro.")
        return

    # Caminho temporário do txt convertido
    txt_output_path = "documento_temp.txt"

    try:
        # Conversão do .docx em .txt
        analyzer_docx(selected_file_path, txt_output_path)

        # Análise do documento
        itens = extract_itens(txt_output_path)
        ordered = key_ordering(itens)
        errors_sequence = verified_sequence_number_order(itens, ordered)
        errors_references = verified_references(txt_output_path, itens)

        # Gera o relatório .txt de erros
        save_errors_to_txt(errors_sequence, errors_references, report_txt_path)

        # Abre a tela de salvamento
        show_save_frame()

    except Exception as e:
        messagebox.showerror("Erro na análise", f"Ocorreu um erro durante a análise:\n{e}")



# ---------------- FUNÇÕES DOS FRAMES (TELAS) ----------------
def show_main_frame():
    """Mostra a tela principal"""

    # Esconde o frame de salvamento do arquivo
    save_frame.pack_forget()

    # Mostra o frame principal
    main_frame.pack(fill="both", expand=True)

    # Resetar o estado visual
    global selected_file_path
    selected_file_path = None
    label_file_name.config(text="Nenhum arquivo selecionado", font=FONT_TEXT)
    btn_analyze.pack_forget()


def show_save_frame():
    """Mostra a tela de salvamento"""
    global selected_file_path

    # Esconde o main frame
    main_frame.pack_forget()

    # Mostra tela de salvamente
    save_frame.pack(fill="both", expand=True)

    # Nome do arquivo
    file_name = os.path.basename(selected_file_path)
    label_name.config(
        text=f"Escolha o formato de salvamento do arquivo:\n\n📄 {file_name}"
    )

    # Resetar label de seleção de arquivo
    selected_file_path = None
    label_file_name.config(text="Nenhum arquivo selecionado", font=FONT_TEXT)
    btn_analyze.pack_forget()


# ---------------- FUNÇÃO DE ESTILO (EFEITO HOVER) ---------------- 
def hover_effect(widget, color_hover, color_normal):
    def on_enter(e):
        widget.config(bg=color_hover)
    def on_leave(e):
        widget.config(bg=color_normal)
    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)


# ---------------- FRAME PRINCIPAL ----------------
main_frame = tk.Frame(main_window, bg=BG_COLOR)
save_frame = tk.Frame(main_window, bg=BG_COLOR)

# Label de informações
label_instruction = tk.Label(main_frame, text="Selecione um documento para analisar",bg=BG_COLOR, fg=FONT_COLOR_WHITE, font=FONT_TITLE)
label_instruction.pack(pady=30)

# Botão de seleção de arquivo
btn_select = tk.Button(main_frame, text="📂 Selecione um documento .docx",bg=BTN_COLOR,fg=FONT_COLOR_BLACK,font=FONT_TEXT, relief="flat", borderwidth=0, 
                       padx=20, pady=10, cursor="hand2", highlightthickness=0, command=handle_select_file)
btn_select.pack(pady=15)
hover_effect(btn_select, "#d9d3d3", BTN_COLOR)

# Label com o nome do arquivo
label_file_name = tk.Label(main_frame, text="Nenhum arquivo selecionado", bg=LABEL_COLOR, fg=FONT_COLOR_BLACK, font=FONT_TEXT, relief="flat", pady=10)
label_file_name.pack(pady=10)


# Botão de analisar documento
btn_analyze = tk.Button(main_frame, text="ANALISAR DOCUMENTO", bg=BTN_ANALYZE_COLOR,fg=FONT_COLOR_WHITE, font=("Segoe UI", 13, "bold"),relief="flat", 
                        borderwidth=0, padx=20, pady=10, cursor="hand2", highlightthickness=0, command=handle_analyzer_file)
hover_effect(btn_analyze, "#003d99", BTN_ANALYZE_COLOR)
btn_analyze.pack_forget()

# ---------------- FRAME DE SALVAMENTO ----------------
label_name = tk.Label(save_frame, bg=BG_COLOR, fg=FONT_COLOR_WHITE, font=FONT_TITLE)
label_name.pack(pady=30)

# Botão de salvar em.html
btn_save_html = tk.Button(save_frame, text="💾 Salvar como .html", bg=BTN_COLOR, fg=FONT_COLOR_BLACK, font=FONT_TEXT, relief="flat", 
                          borderwidth=0, padx=20, pady=10, cursor="hand2", highlightthickness=0)
btn_save_html.pack(pady=15)
hover_effect(btn_save_html, "#d9d3d3", BTN_COLOR)
btn_save_html.config(command=lambda: save_txt_html(report_txt_path))

#Botão de salvar em .docx
btn_save_docx = tk.Button(save_frame, text="💾 Salvar como .docx", bg=BTN_COLOR, fg=FONT_COLOR_BLACK, font=FONT_TEXT, relief="flat", 
                          borderwidth=0, padx=20, pady=10, cursor="hand2", highlightthickness=0)
btn_save_docx.pack(pady=10)
hover_effect(btn_save_docx, "#d9d3d3", BTN_COLOR)
btn_save_docx.config(command=lambda: save_txt_docx(report_txt_path))

# Botão de retornar ao menu
btn_menu = tk.Button(save_frame, text="⏪ Analisar outro documento", bg=BTN_ANALYZE_COLOR, fg=FONT_COLOR_WHITE, font=("Segoe UI", 13, "bold"), relief="flat", 
                     borderwidth=0, padx=20, pady=10, cursor="hand2", command=show_main_frame)
btn_menu.pack(pady=25)
hover_effect(btn_menu, "#003d99", BTN_ANALYZE_COLOR)

# ---------------- INICIALIZAÇÃO ----------------
show_main_frame()
main_window.mainloop()
