import tkinter as tk
from tkinter import filedialog, messagebox
import ghostscript
import locale
import os
import sys


MODES = [
    ("Muito Baixa - visualização - 72 dpi", "screen"),
    ("Baixa - leitura - 150 dpi", "ebook"),
    ("Alta - impressão - 300 dpi", "printer"),
    ("Alta - impressão (preserva as cores) - 300 dpi", "prepress"),
    ("Padrão - arquivo para uso geral", "default")
]


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("")

    return os.path.join(base_path, relative_path)


def get_input_path():
    """ Get path for input file """
    path = tk.filedialog.askopenfilename(
        title="Selecione o arquivo de entrada",
        filetypes=(("Arquivos de PDF", "*.pdf"), ("Todos os tipos", "*.*"))
    )
    
    err = verify_file(path, True)
    
    if err is None:
        output_entry.delete("0", "end")
        input_entry.delete("0", "end")
        input_entry.insert(0, path)
        output_entry.insert(0, path.split('.pdf')[0] + "_comprimido.pdf")

    else:
        messagebox.showerror("Erro ao selecionar o arquivo de entrada", err)


def get_output_path():
    """ Get path for output file """
    path = tk.filedialog.asksaveasfilename(
        title="Salvar como... ",
        filetypes=[("Arquivos de PDF", ".pdf")], 
        defaultextension='.pdf'
    )

    err = verify_file(path)

    if err is None:
        output_entry.delete("0", "end")
        output_entry.insert(0, path)
    else:
        messagebox.showerror("Erro ao selecionar o arquivo de saída", err)


def verify_file(path, input_file=False):
    """ Verify if file exists and is a pdf """
    if path:
        if input_file:
           if not os.path.exists(path):
                return "Arquivo de entrada inexistente"
        if '.pdf' in path:
            return None
        else:
            return "Escolha um arquivo no formato PDF"
    elif not path and input_file:
        return "Selecione o arquivo de entrada"
    else:
        return "Selecione o arquivo de saída"


def compress():
    """ Compress pdf file with ghostscript """
    input_file = input_entry.get().strip()
    output_file = output_entry.get().strip()

    err_in = verify_file(input_file, True)
    err_out = verify_file(output_file)
    
    if err_in is None and err_out is None:
        args = [
            "ps2pdf",
            "-dCompatibilityLevel=1.4",
            "-dNOPAUSE", "-dBATCH", "-dSAFER",
            "-sDEVICE=pdfwrite",
            "-dPDFSETTINGS=/" + compress_type.get(),
            "-sOutputFile=" + output_file,
            input_file
        ]

        encoding = locale.getpreferredencoding()
        args = [a.encode(encoding) for a in args]

        try:
            ghostscript.Ghostscript(*args)
        except ghostscript.GhostscriptError:
            messagebox.showerror("Erro ao converter arquivo",
                                 "Verifique os arquivos e tente novamente")
            return

        input_entry.delete("0", "end")
        output_entry.delete("0", "end")
        messagebox.showinfo("Sucesso!", "Arquivo comprimido com sucesso!")
    elif err_in:
        messagebox.showerror("Erro com arquivo de entrada", err_in)
    elif err_out:
        messagebox.showerror("Erro com arquivo de saída", err_out)


# application window settings
root = tk.Tk()
root.title("Compressor de PDFs")
root.resizable(False, False)
root.tk.call(
    'wm', 
    'iconphoto', 
    root._w, 
    tk.PhotoImage(file=resource_path('icon.png'))
)


# icon for buttons
folder_icon = tk.PhotoImage(file=resource_path('folder_open.png'))


# frames
files_frame = tk.LabelFrame(
    root, 
    text="Selecione os arquivos: ", 
    padx=10, pady=10
)
compress_frame = tk.LabelFrame(
    root, text="Selecione a qualidade: ", 
    padx=96, pady=10
)
# packing
files_frame.pack(padx=50, pady=25)
compress_frame.pack(padx=50, pady=25)


# labels
input_label = tk.Label(files_frame, text="Entrada:")
output_label = tk.Label(files_frame, text="Saída:")
# packing
input_label.grid(row=0, column=0)
output_label.grid(row=1, column=0)


# entries
input_entry = tk.Entry(files_frame, width=50)
output_entry = tk.Entry(files_frame, width=50)
# packing
input_entry.grid(row=0, column=1)
output_entry.grid(row=1, column=1)


# buttons
input_button = tk.Button(
    files_frame, 
    image=folder_icon, 
    command=get_input_path, 
    width=20, height=20, 
    bg='white'
)
output_button = tk.Button(
    files_frame, 
    image=folder_icon, 
    command=get_output_path, 
    width=20, height=20, 
    bg='white'
)
compress_button = tk.Button(
    root, 
    text="Comprimir", 
    command=compress, 
    bg='green'
)
# packing
input_button.grid(row=0, column=3, padx=5, pady=2.5)
output_button.grid(row=1, column=3, padx=5, pady=2.5)
compress_button.pack(pady=25, anchor='center')


# radio buttons
compress_type = tk.StringVar()
compress_type.set("screen")
for text, value in MODES:
    tk.Radiobutton(
        compress_frame, 
        text=text, 
        variable=compress_type, 
        value=value
    ).grid(sticky='w')


root.mainloop()
