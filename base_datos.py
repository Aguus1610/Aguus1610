import sqlite3

class ConexionSql: 
    def __init__(self, nombre_base_datos):
        self.conexion = None
        self.cursor = None
        self.conectar(nombre_base_datos)
         
    def conectar(self, nombre_base_datos):
        try:
            self.conexion = sqlite3.connect(nombre_base_datos)
            self.cursor = self.conexion.cursor()
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            precio INTEGER,
            cantidad INTEGER,
            valor INTEGER,
            fecha TEXT)''')
            self.conexion.commit()
            print("Conexión establecida correctamente.")
        except sqlite3.Error as e:
            print("Error al conectar a la base de datos:", e)

    def desconectar(self):
        try:
            if self.conexion:
                self.conexion.close()
                print("Conexión cerrada correctamente.")
        except sqlite3.Error as e:
            print("Error al cerrar la conexión:", e)

class ConexionMongo:

    def __init__(self, nombre_base_datos):
        from pymongo import MongoClient         
        client = MongoClient()               # Instanciamos la clase MongoClient

        # Creamos la base 
        db = client["DBMongo1"]

        #Creamos la coleccion de datos
        collection = db["DBMongo1-collection"]
