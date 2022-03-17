import tkinter as tk
from tkinter.filedialog import askopenfilename
from analizadorLexico import analizadorLexico, clasificacion, Reportes


class ventana:

    def window(self):
        self.principal = tk.Tk()
        self.principal.title('Ventana Principal')
        self.principal.resizable(0,0)
        self.principal.geometry('1240x710')
        self.principal.config(bg='#0d83a3')
        self.editorTexto = tk.Text(self.principal, font=('Arial', 14), width=70, height=21, borderwidth=7, fg='#000000')
        self.editorTexto.place(x=50, y=100)
        tk.Label(self.principal, text='VENTANA PRINCIPAL', background='#000000', foreground='white')
        
        '''-------------------------BOTONES--------------------------'''
        tk.Button(self.principal, text='Cargar archivo', width=15, height=3, borderwidth=5, bg='#961823', fg='black', command=self.cargarArchivo).place(x=50, y=600)
        tk.Button(self.principal, text='Analizar', width=15, height=3, borderwidth=5, bg='#ba8013', fg='black', command=self.analizarArchivo).place(x=200, y=600)
        #tk.Button(self.principal, text='Guardar cambios', width=15, height=3, borderwidth=5, bg='#28eb4c', fg='black').place(x=350, y=600)

        tk.Button(self.principal, text='Reporte de tokens', width=15, height=3, borderwidth=5, bg='#143b73', fg='black', command=self.mostrarReporteTokens).place(x=880, y=100)
        tk.Button(self.principal, text='Reporte de errores', width=15, height=3, borderwidth=5, bg='#143b73', fg='black', command=self.mostrarReporteErrores).place(x=1080, y=100)
        tk.Button(self.principal, text='Manual de usuario', width=15, height=3, borderwidth=5, bg='#143b73', fg='black').place(x=880, y=200)
        tk.Button(self.principal, text='Manual Técnico', width=15, height=3, borderwidth=5, bg='#143b73', fg='black').place(x=1080, y=200)

        self.principal.mainloop()

    def cargarArchivo(self):
        try:
            file = askopenfilename()
            file = open(file).read()
            self.editorTexto.delete('1.0','end')
            self.editorTexto.insert(tk.INSERT, file)
        except:
            self.editorTexto.delete('1.0','end')
    
    def analizarArchivo(self):
        archivo = self.editorTexto.get('1.0', 'end').strip()
        if len(archivo) > 0:
            analizador = analizadorLexico()
            analizador.analizar(archivo)
            self.tokens = analizador.listaTokens
            self.errores = analizador.listaErrores
            if len(self.tokens) > 0:
                componente = clasificacion()
                componentes = componente.obtenerComponentes(self.tokens)
                #print('hola2')
                print(componentes)
                tk.messagebox.showinfo(message="Se analizó correctamente el archivo.", title="Éxito")
            else:
                tk.messagebox.showinfo(message="No se detectó ningún token.", title="Error")
        else:
            tk.messagebox.showinfo(message="No se ha cargado ningún archivo.", title="Error")
    
    def mostrarReporteTokens(self):
        contenido = self.editorTexto.get('1.0','end').strip()
        if len(contenido) > 0:
            if self.tokens:
                Reportes().reporteTokens(self.tokens)
            else:
                tk.messagebox.showinfo(message="No se encontraron tokens.", title="Reporte Tokens")
        else:
            tk.messagebox.showinfo(message="No se encontró ningun archivo.", title="Error")

    def mostrarReporteErrores(self):
        contenido = self.editorTexto.get('1.0','end').strip()
        if len(contenido) > 0:
            if self.errores:
                Reportes().reporteErrores(self.errores)
            else:
                tk.messagebox.showinfo(message="No se encontraron tokens.", title="Reporte Tokens")
        else:
            tk.messagebox.showinfo(message="No se encontró ningun archivo.", title="Error")


ventanaN = ventana()
ventanaN.window()
