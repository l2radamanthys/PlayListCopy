
import Tkinter as tk 
import ttk
from tkFileDialog import askopenfilename, askdirectory
import tkMessageBox
from copy import CopyProcess

ftypes = (('M3U Play List','*.m3u'), ('Todos los Formatos', '*'))


class MainFrame(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, master=root, width=400)
        self.pack()

        #gui definition
        lbl1 = tk.Label(self, text="Ruta Lista Musica")
        lbl1.grid(row=0, padx=5, pady=5, sticky=tk.W)

        self.pl_path = tk.StringVar()
        txt_plpath = tk.Entry(self, textvariable=self.pl_path, width=60)
        txt_plpath.grid(row=1, column=0)     

        btn_plsearch = tk.Button(self, text="Seleccionar", command=self.select_playlist, pady=3)
        btn_plsearch.grid(row=1, column=1, padx=5)
        
        lbl2 = tk.Label(self, text="Carpeta Destino")
        lbl2.grid(row=2, padx=5, pady=5, sticky=tk.W)

        self.folder_path = tk.StringVar()
        txt_folder_path = tk.Entry(self, textvariable=self.folder_path, width=60)
        txt_folder_path.grid(row=3, column=0)

        btn_folder_search = tk.Button(self, text="Seleccionar", command=self.select_dest_folder, pady=3)
        btn_folder_search.grid(row=3, column=1, padx=5)

        btn_copy = tk.Button(self, text="Copiar Archivos", command=self.copy_files, padx=5, pady=5)
        btn_copy.grid(row=4, pady=10, padx=10)


    def select_playlist(self):
        fpath = askopenfilename(filetypes=ftypes)
        if fpath != None:
            self.pl_path.set(fpath)
        

    def select_dest_folder(self):
        fpath = askdirectory()
        if fpath != None:
            self.folder_path.set(fpath)
       

    def copy_files(self):
        run = True
        #asegurando que la lista de reproducion exista
        try:
            data = open(self.pl_path.get(), 'r').readlines()
            #for line in data:
                #print line[:-1]
        except:
            run = False
            print "Error Archivo inecistente"
        
        if self.folder_path.get() != None:
            _folder = self.folder_path.get()

        else:
            run = False

        if run:
            self.new_window = tk.Toplevel(self.master)
            self.copy_app = CopyFrame(root=self.new_window, files=data, folder=_folder) 



class CopyFrame(tk.Frame):
    def __init__(self, root, files, folder=""):
        tk.Frame.__init__(self, master=root)
        self.pack()
        #self.title('Copiando Archivos..')

        lbl = tk.Label(self, text="Progreso..")
        lbl.grid(row=0, pady=10, padx=10, sticky=tk.W)

        self.gauge = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=600, maximum=len(files))
        self.gauge.grid(row=1, padx=10)

        self.blist = tk.Listbox(self, width=100, height=10)
        self.blist.grid(row=2, padx=10, pady=20)
        
       # btn = tk.Button(self, text="Copiar", command=self.on_copy, padx=5, pady=5)
       # btn.grid(row=5)
        
        self.copylog = open('copylog.txt', 'a')

        
        self.copy = CopyProcess(files, folder, self.blist, self.gauge, self.copylog) 
        self.copy.start()
        self.run_copy()

    
    def run_copy(self):
            #moviendo archivo
        if self.copy.is_run:
            self.master.after(100, self.run_copy)

        else:
            tkMessageBox.showinfo('Informacion', 'Finalizo el Copiado')
            self.copylog.close()
            self.master.destroy()



 
if __name__ == '__main__':
    main = tk.Tk()
    main.title("PlayList Copy")
    app = MainFrame(main)
    main.mainloop()

