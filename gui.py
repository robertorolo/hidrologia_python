import chuvas
import vazoes

from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilenames

import matplotlib.pyplot as plt

pluvi_d = {}
fluvi_d = {}

def quit_me():
    print('quit')
    root.quit()
    root.destroy()
    
def select_pluvi_files():
    filenames = askopenfilenames(title = "Selecione as estações pluviométricas (.csv ou .txt)")
    for filename in filenames:
    ler_chuvas.
    
    
root = Tk()
root.protocol("WM_DELETE_WINDOW", quit_me)
root.title("Caracterização pluvi-fluvial")
root.geometry("500x200")
root.resizable(True, True)

tabcontrol = ttk.Notebook(root)

#pluvi tab
pluvi_frame = Frame(tabcontrol)
tabcontrol.add(pluvi_frame, text="Pluvi")

#fluvi tab
fluvi_frame = Frame(tabcontrol)
tabcontrol.add(fluvi_frame, text="Fluvi")

#pack tabs
tabcontrol.pack(expan=1, fill="both")

#adding itens to pluvi tab
#select stations button
pluvi_est_btn = Button(pluvi_frame, text="Selecionar estações", command=select_files)
pluvi_est_btn.grid(row=0, column=0, sticky=W, padx=(5, 5), pady=(5, 5))

root.mainloop()