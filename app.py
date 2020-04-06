import tkinter as tk
from tkinter import filedialog, messagebox
import ghostscript
import locale
import os
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("")
    
    return os.path.join(base_path, relative_path)


# ghostscript modes
MODES = [
    ("Muito Baixa - visualização - 72 dpi", "screen"),
    ("Baixa - leitura - 150 dpi", "ebook"),
    ("Alta - impressão - 300 dpi", "printer"),
    ("Alta - impressão (preserva as cores) - 300 dpi", "prepress"),
    ("Padrão - arquivo para uso geral", "default")
]


# get path to pdf file
def get_path(file_type):
    path = tk.filedialog.askopenfilename(title="Selecione o arquivo de " + file_type,
                                         filetypes=(("Arquivos de PDF", "*.pdf"), ("Todos os tipos", "*.*")))
    if path:
        if '.pdf' in path:
            output_entry.delete("0", "end")

            if file_type is 'entrada':
                input_entry.delete("0", "end")
                input_entry.insert(0, path)
                output_entry.insert(0, path.split('.pdf')[0] + "_comprimido.pdf")

            else:
                output_entry.insert(0, path)
        else:
            messagebox.showerror("Erro ao selecionar arquivo", "Por favor escolha um arquivo válido")
    else:
        messagebox.showerror("Erro ao selecionar arquivo", "Por favor escolha um arquivo")


# compress pdf file
def compress():
    input_file = input_entry.get().strip()
    output_file = output_entry.get().strip()

    if input_file is not '' and output_entry is not '':
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

        ghostscript.Ghostscript(*args)
        input_entry.delete("0", "end")
        output_entry.delete("0", "end")
        messagebox.showinfo("Sucesso!", "Arquivo comprimido com sucesso!")
    else:
        messagebox.showerror("Erro ao converter arquivo",
                             "Por favor selecione corretamente os arquivos de entrada e saída")


# application window settings
root = tk.Tk()
root.title("Compressor de PDFs")
root.resizable(False, False)
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file=resource_path('icon.png')))

# definition of elements
files_frame = tk.LabelFrame(root, text="Selecione os arquivos: ", padx=10, pady=10)
compress_frame = tk.LabelFrame(root, text="Selecione a qualidade: ", padx=96, pady=10)

input_label = tk.Label(files_frame, text="Entrada:")
output_label = tk.Label(files_frame, text="Saída:")

input_entry = tk.Entry(files_frame, width=50)
output_entry = tk.Entry(files_frame, width=50)

folder_icon = tk.PhotoImage(file=resource_path('folder_open.png'))

input_button = tk.Button(files_frame, image=folder_icon, command=lambda: get_path('entrada'), width=20, height=20,
                         bg='white')
output_button = tk.Button(files_frame, image=folder_icon, command=lambda: get_path('saída'), width=20, height=20,
                          bg='white')

compress_type = tk.StringVar()
compress_type.set("screen")

for text, value in MODES:
    tk.Radiobutton(compress_frame, text=text, variable=compress_type, value=value).grid(sticky='w')

compress_button = tk.Button(root, text="Comprimir", command=compress, bg="green")

# packing elements - files
files_frame.pack(padx=50, pady=25)

input_label.grid(row=0, column=0)
output_label.grid(row=1, column=0)

input_entry.grid(row=0, column=1)
output_entry.grid(row=1, column=1)

input_button.grid(row=0, column=3, padx=5, pady=2.5)
output_button.grid(row=1, column=3, padx=5, pady=2.5)

# packing elements - compress
compress_frame.pack(padx=50, pady=25)

compress_button.pack(pady=25, anchor='center')

root.mainloop()
