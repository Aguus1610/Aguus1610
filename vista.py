from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from modelo import *
from base_datos import *


class Ventana:
    

    def __init__(self, master, nombre_base_datos):

        self.conex = ConexionSql(nombre_base_datos)
        self.conex.conectar(nombre_base_datos)
    
        # Interfaz de usuario
        master.title("Control de Stock")
        master.configure(bg="lightgray")
        master.geometry("800x400")

        
            
        titulo = Label(master, text="Ingrese sus datos", bg="gray", fg="black", height=1, width=80, font=("Arial", 12, "bold"))
        titulo.grid(row=0, column=0, columnspan=6)

        menubar=Menu(master)
        menuotros=Menu(menubar, tearoff=0)
        
        menuotros.add_command(label="Vaciar Base de Datos", command=lambda:FuncionesVentana.vaciar_base_datos(self))
        menuotros.add_command(label="Salir", command=lambda:FuncionesVentana.salir_aplicacion(master))
        menubar.add_cascade(label="Otros",menu=menuotros )

        menubase=Menu(menubar, tearoff=0)
        menubase.add_command(label="Borrar campos", command=lambda:FuncionesVentana.limpiar_campos(self))
        menubar.add_cascade(label="Campos de Datos",menu=menubase )

        menu_personalizar = Menu(master, tearoff=0)
        menu_personalizar.add_command(label="Cambiar de tema")
        menubar.add_cascade(label="Personalizar app", menu=menu_personalizar)

        master.config(menu=menubar)

        # Variables de control para los Entry widgets

        self.nombre_var = StringVar()
        self.precio_var = IntVar()
        self.cantidad_var = IntVar()

        # Etiquetas y Entry para ingresar datos
        Label(master, text="Nombre:", background="lightgray", font=("Arial", 10)).grid(row=1, column=1, pady=5, padx=5)
        self.nombre_entry = tk.Entry(master, textvariable=self.nombre_var)
        self.nombre_entry.grid(row=1, column=2, pady=5, padx=5)
        
        Label(master, text="Precio:", background="lightgray", font=("Arial", 10)).grid(row=2, column=1, pady=5, padx=5)
        self.precio_entry = tk.Entry(master, textvariable=self.precio_var)
        self.precio_entry.grid(row=2, column=2, pady=5, padx=5)
        
        Label(master, text="Cantidad:", background="lightgray", font=("Arial", 10)).grid(row=3, column=1, pady=5, padx=5)
        self.cantidad_entry = tk.Entry(master, textvariable=self.cantidad_var)
        self.cantidad_entry.grid(row=3, column=2, pady=5, padx=5)

        # self.Treeview para mostrar datos
        self.tree = ttk.Treeview(master, columns=("ID", "Nombre", "Precio", "Cantidad", "Valor", "Fecha"), show="headings")
        self.tree.column("ID", width=50, minwidth=100, anchor= W)
        self.tree.column("Nombre", width=100, minwidth=100)
        self.tree.column("Precio", width=100, minwidth=100)
        self.tree.column("Cantidad", width=100, minwidth=100)
        self.tree.column("Valor", width=100, minwidth=100)
        self.tree.column("#0", width=100, minwidth=100, anchor=E)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Valor", text="Valor")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.grid(row=9, column=0, columnspan=6, pady=5, padx=5)

        # Botones de acciones
        self.boton_crear=Button(master, text="Crear Registro", font=("Arial", 8, "bold"), fg="white", bg="gray",  command=lambda:FuncionesVentana.crear(self)).grid(row=5, column=1)
        self.boton_actual=Button(master, text="Actualizar Vista", font=("Arial", 8, "bold"), fg="white", bg="gray", command=lambda:Crud.actualizar(self, self.tree)).grid(row=5, column=2)
        self.boton_modif=Button(master, text="Modificar", font=("Arial", 8, "bold"), fg="white", bg="gray", command=lambda:Crud.modificar(self, self.tree, self.nombre_var.get(), self.precio_var.get(), self.cantidad_var.get())).grid(row=5, column=3)
        self.boton_baja=Button(master, text="Eliminar", font=("Arial", 8, "bold"), fg="white", bg="gray", command=lambda:Crud.eliminar(self, self.tree)).grid(row=5, column=4)
        self.boton_mostrar=Button(master, text="Mostrar", font=("Arial", 8, "bold"), fg="blue", bg="yellow", command=lambda:FuncionesVentana.leer_producto(self)).grid(row=2, column=3)
    # Función para elegir la base de datos
    def elegir_db(self):
        return messagebox.askquestion(
        "Elegir Base de Datos", "¿Usar MongoDB? (Presiona 'No' para SQLite)"
    )




class FuncionesVentana:

    def salir_aplicacion(self, master): 
        valor=messagebox.askquestion("Salir","¿Deseas salir de la aplicación?")
        if valor=="yes":
            self.conex.desconectar()
            master.destroy()

    def limpiar_campos(self):
        self.nombre_var.set("")
        self.precio_var.set("0")
        self.cantidad_var.set("0")

    def leer_producto(self):
        producto = self.tree.selection()
        if producto:
            self.item = self.tree.item(producto)
            producto_seleccionado = self.tree.item(producto, "values" )
            self.nombre_entry.delete(0,tk.END)
            self.precio_entry.delete(0,tk.END)
            self.cantidad_entry.delete(0,tk.END)
            self.nombre_entry.insert(0, producto_seleccionado[1])
            self.precio_entry.insert(0, producto_seleccionado[2])
            self.cantidad_entry.insert(0, producto_seleccionado[3])
            mensaje = {"ID": producto_seleccionado[0],
                "Nombre": producto_seleccionado[1],
                "Precio": producto_seleccionado[2],
                "Cantidad": producto_seleccionado[3],
                "Valor Total": producto_seleccionado[4]}
        contenido = "\n".join([f"{clave}: {valor}" for clave, valor in mensaje.items()])
        messagebox.showinfo("Producto Seleccionado", contenido)
        print("Campos completos")
    
    def vaciar_base_datos(self):
        confirm=messagebox.askquestion("Salir","¿Desea eliminar el contenido de la base de datos?")
        if confirm=="yes":
            self.conex.cursor.execute("DELETE FROM productos")
            self.conex.cursor.execute("DELETE FROM sqlite_sequence WHERE name='productos'")
            self.conex.cursor.execute("SELECT MAX(id) FROM productos")
            max_id = self.conex.cursor.fetchone()[0] or 0
            self.conex.cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('productos', ?)", (max_id,))
            self.conex.conexion.commit()
            messagebox.showinfo("Base de datos", "Base de datos vaciada")
            Crud.actualizar(self, self.tree)
        else:
            messagebox.showwarning("Base de Datos", "Error! Hubo un problema al vaciar la base de datos")

    

    
    # Operaciones CRUD con selección de base de datos
    def crear(self):
        decision = Ventana.elegir_db(self)

        if decision == "yes":
            CrudMongo.alta(self, self.tree, self.nombre_var.get(), self.precio_var.get(), self.cantidad_var.get())
        else:
            Crud.crear(self, self.tree, self.nombre_var.get(), self.precio_var.get(), self.cantidad_var.get())
            Crud.actualizar(self, self.tree)

    def leer(self):
        decision = Ventana.elegir_db(self)

        if decision == "yes":
            documentos =CrudMongo.select(self, self.tree)
            messagebox.showinfo("Resultados MongoDB", str(documentos))
        else:
            registros = FuncionesVentana.leer_producto(self)
            messagebox.showinfo("Resultados SQLite", str(registros))
        

            


 

    











