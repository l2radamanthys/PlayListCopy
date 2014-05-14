import Tkinter as tk
from shutil import copy as file_copy
from threading import Thread, Condition
import time
import os
import datetime


class CopyProcess(Thread):
    def __init__(self, data, folder, blist, gauge, log):
        Thread.__init__(self)

        self.data = data #lista con las rutas archivos
        self.folder = folder #ruta destino
        self.gauge = gauge #Progressbar Widget
        self.blist = blist #ListWidget
        self.log = log #error output file
        self.is_run = True

        #self.size = len(data)
        #self.step = 0
        

    def run(self):
        step = 0
        size = len(self.data)
        while step < size:
            print '.',
            #quito los salto de linea
            path = self.data[step].replace('\n', '')
            filename = path.split('\\')[-1]

            try:
                npath = os.path.join(self.folder, filename)
                file_copy(path, npath)
                self.gauge.step()
                self.blist.insert(tk.END, "[%s] %s" %(str(step+1).zfill(3), filename))
            
            except:
                time = datetime.datetime.now().strftime("[%d-%m-%Y %H:%M:%S]") 
                text = "%s - ERROR AL COPIAR: %s \n" %(time, path)
                self.log.write(text)
                self.blist.insert(tk.END, "[%s] ERROR %s" %(str(step+1).zfill(3), filename))
            #time.sleep(10) #duermo el hilo          
            step += 1
        
        self.is_run = False






