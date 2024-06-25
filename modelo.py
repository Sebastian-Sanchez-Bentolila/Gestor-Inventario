# Modelo - Aplicación {Gestor de Inventarios}
# Autor: Sebastian Sanchez Bentolila

# Librerias
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# Clases
class BaseDatos():
    # Clase para el manejo de la base de datos 
    def __init__(self,):
        self.con = sqlite3.connect('base-datos/inventario.db')
        self.cursor = self.con.cursor()
        self.sql = ""
        self.observadores = []
        self.verificar_tabla()
        
    # Métodos
    def crear_tabla(self,):
        # Crear la tabla en la db
        self.sql = '''CREATE TABLE stock(
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      producto TEXT,
                      cantidad INT,
                      costo FLOAT,
                      precio_venta FLOAT, 
                      proveedor TEXT, 
                      categoria TEXT);'''
        self.cursor.execute(self.sql)
        self.guardar_cambios()
        
    def guardar_cambios(self,):
        # Guardar los cambios 
        try:
            self.con.commit()
        except sqlite3.Error as e:
            print(f"Error al guardar cambios: {e}")
            self.con.rollback()
    
    def cerrar_db(self,):
        # Cerrando la db
        self.con.close()
        
    def insertar(self, producto:str, cantidad:int, costo:float, precio_venta:float, proveedor:str, categoria:str):
        # Insertar un nuevo stock
        try:
            data = (producto, cantidad, costo, precio_venta, proveedor, categoria)
            self.sql = '''INSERT INTO stock(producto, cantidad, costo, precio_venta, proveedor, categoria) 
                        VALUES(?, ?, ?, ?, ?, ?)'''
            self.cursor.execute(self.sql, data)
            self.guardar_cambios()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error al insertar datos: {e}")
         
    def seleccionar_todos(self):
        # Seleccionando todo los elementos de la tabla
        self.sql = "SELECT * FROM stock ORDER BY id ASC"
        self.cursor.execute(self.sql)
        rows = self.cursor.fetchall()
        return rows

    
    def borrar(self, producto:int):
        # Borra algun stock que se haya vendido o consumido
        data = (producto,)
        self.sql = "DELETE from stock where id = ?;"
        self.cursor.execute(self.sql, data)
        self.guardar_cambios()
        
    def modificar(self, id:int, cantidad=0, costo=0.0, precio_venta=0.0, proveedor="", producto="", categoria=""):
        # Actualiza algun elemento de la db
        self.sql = "UPDATE stock SET "
        data = []
        
        # Verificamos que haya ingresado dato para modificarlo, caso contrario quedara igual
        if producto != "":
            self.sql = self.sql + "producto=?, "  
            data.append(producto) 
        if cantidad != 0:
            self.sql = self.sql + "cantidad=?, "
            data.append(cantidad)
        if costo != 0.0:
            self.sql = self.sql + "costo=?, "
            data.append(costo)
        if precio_venta != 0.0:
            self.sql = self.sql + "precio_venta=?, "
            data.append(precio_venta)
        if proveedor != "":
            self.sql = self.sql + "proveedor=?, "
            data.append(proveedor)
        if categoria != "":
            self.sql = self.sql + "categoria=?, "
            data.append(proveedor)
        
        # Elimina la coma y el espacion final del comando de SQL   
        self.sql = self.sql.rstrip(", ")
        
        data.append(id)   
        data_tupla = tuple(data)
        self.sql = self.sql + " WHERE id=?;"
        self.cursor.execute(self.sql, data_tupla)
        self.guardar_cambios()
    
    def verificar_tabla(self,):
        # Verifica si la tabla 'stock' existe
        self.cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='stock';''')
        
        if self.cursor.fetchone()[0] == 0: # Si no existe, la crea
            self.crear_tabla()
            
    def obtener_estadisticas(self, ):
        # Método para obtener un breve análisis Estadístico Descriptivo
        # 1. Cantidad total de productos
        self.cursor.execute("SELECT COUNT(*) FROM stock")
        total_productos = self.cursor.fetchone()[0]

        # 2. Cantidad de productos por categoría 
        self.cursor.execute("SELECT categoria, COUNT(*) FROM stock GROUP BY categoria")
        productos_por_categoria = self.cursor.fetchall()

        # 3. Producto con mayor y menor stock
        self.cursor.execute("SELECT producto, cantidad FROM stock ORDER BY cantidad DESC LIMIT 1")
        mayor_stock = self.cursor.fetchone()
        
        self.cursor.execute("SELECT producto, cantidad FROM stock ORDER BY cantidad ASC LIMIT 1")
        menor_stock = self.cursor.fetchone()

        # 4. Valor total del inventario en termino de costos
        self.cursor.execute("SELECT SUM(costo * cantidad) FROM stock")
        valor_total_inventario = self.cursor.fetchone()[0]

        # 5. Ingresos potenciales (si se llegase a vender)
        self.cursor.execute("SELECT SUM(precio_venta * cantidad) FROM stock")
        ingresos_potenciales = self.cursor.fetchone()[0]

        self.guardar_cambios()
        
        # Crear gráficos
        categorias = [categoria for categoria, _ in productos_por_categoria]
        cantidades = [cantidad for _, cantidad in productos_por_categoria]
        
        # Gráfico de Barras
        plt.figure(figsize=(8, 8))
        sns.barplot(x=categorias, y=cantidades)
        plt.title('Cantidad de Productos por Categoría')
        plt.xlabel('Categoría')
        plt.ylabel('Cantidad')
        plt.savefig('archivos/img/grafico_barras.png')
        plt.close()

        # Gráfico de Torta
        plt.figure(figsize=(8, 8))
        plt.pie(cantidades, labels=categorias, autopct='%1.1f%%', startangle=140)
        plt.title('Porcentaje de Productos por Categoría')
        plt.savefig('archivos/img/grafico_torta.png')
        plt.close()
        
        return {
            'total_productos': total_productos,
            'productos_por_categoria': productos_por_categoria,
            'mayor_stock': mayor_stock,
            'menor_stock': menor_stock,
            'valor_total_inventario': valor_total_inventario,
            'ingresos_potenciales': ingresos_potenciales
        }