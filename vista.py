# Vista - Aplicación {Gestor de Inventarios}
# Autor: Sebastian Sanchez Bentolila

# Librerías
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from modelo import BaseDatos

#Clases
class Row(BoxLayout):
    # Para borrar productos del inventario
    def __init__(self,):
        super(Row, self).__init__()

    def borrar(self,):
        id_item = str(self.ids.box.text).split()[1]
        print(id_item)
        db = BaseDatos()
        db.borrar(id_item)
        db.cerrar_db()
        

# Clases que dan origen a las ventanas       
class MenuScreen(Screen):
    # Clase de la pagina - Menu
    pass

class HomeScreen(Screen):  
    # Clase de la pagina - Home              
    def on_enter(self, **kw):
        super(HomeScreen, self).__init__(**kw)
        self.cargar_productos()

    def cargar_productos(self):
        try:
            db = BaseDatos()
            productos = db.seleccionar_todos()

            self.ids.row = [
                {
                    "id":f"{x[0]}",       
                    "producto":f"{x[1]}",
                    "cantidad":f"{x[2]}", 
                    "costo":f"{x[3]}",
                    "precio_venta":f"{x[4]}",
                    "proveedor":f"{x[5]}",
                    "categoria":f"{x[6]}",
                }
                for x in productos]
        except Exception as e:
            print(f"Error al cargar producto: {e}")
        

class AltaScreen(Screen):
    # Clase de la pagina - Alta
    def agregar_producto(self, producto, cantidad, costo, precio_venta, proveedor, categoria):
        try:
            if not producto or not cantidad or not costo or not precio_venta or not proveedor or not categoria:
                print("Por favor, complete todos los campos.")
                return
            try:
                cantidad = int(cantidad)
                costo = float(costo)
                precio_venta = float(precio_venta)
            except ValueError:
                print("Cantidad, Costo y Precio de Venta deben ser números.")
                return
            
            self.manager.get_screen('menu').db.insertar(producto, cantidad, costo, precio_venta, proveedor, categoria)
            self.manager.current = 'home'
        except Exception as e:
            print(f"Error al agregar producto: {e}")

class CreadorScreen(Screen):
    # Clase de la pagina - Creador
    pass

'''
class ProductoWidget(BoxLayout):
    def __init__(self,):
        db = BaseDatos()
        resultado = db.seleccionar_todos()
        self.ids.row = [
                {
                    "id":f"{x[0]}",       
                    "producto":f"{x[1]}",
                    "cantidad":f"{x[2]}", 
                    "costo":f"{x[3]}",
                    "precio_venta":f"{x[4]}",
                    "proveedor":f"{x[5]}",
                    "categoria":f"{x[6]}",
                }
                for x in resultado]

    def modificar_producto(self):
        # Implementar la lógica para modificar el producto
        pass

    def eliminar_producto(self):
        # Lógica para eliminar el producto
        db = self.parent.parent.parent.db
        db.borrar(self.producto)
        self.parent.remove_widget(self) '''
        
class EstadisticasScreen(Screen):
    # Clase de la pagina - Estadisticas
    def on_enter(self, *args):
        base_datos = BaseDatos()
        stats = base_datos.obtener_estadisticas()
        self.ids.total_productos.text = f"Cantidad Total de Productos: {stats['total_productos']}"
        self.ids.mayor_stock.text = f"Producto con Mayor Stock: {stats['mayor_stock'][0]} ({stats['mayor_stock'][1]})"
        self.ids.menor_stock.text = f"Producto con Menor Stock: {stats['menor_stock'][0]} ({stats['menor_stock'][1]})"
        self.ids.valor_total_inventario.text = f"Costos Totales: ${stats['valor_total_inventario']}"
        self.ids.ingresos_potenciales.text = f"Ingresos Potenciales (ventas): ${stats['ingresos_potenciales']}"
        