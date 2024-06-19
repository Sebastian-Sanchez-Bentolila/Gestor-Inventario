# Vista - Aplicación {Gestor de Inventarios}
# Autor: Sebastian Sanchez Bentolila

# Librerías
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from modelo import BaseDatos  

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
            product_grid = self.ids.product_grid
            product_grid.clear_widgets()  # Limpiar widgets existentes

            for producto in productos:
                producto_id, nombre, cantidad, costo, precio_venta, proveedor, categoria = producto
                
                box = BoxLayout(orientation='horizontal', padding=50, spacing=50)
                with box.canvas.before:
                    Color(0, 0, 0, 0.1)  # Color de fondo (negro translúcido)
                    Rectangle(pos=box.pos, size=box.size)
                
                box.bind(size=self._update_rect, pos=self._update_rect)

                box.add_widget(Label(text=f"ID: {producto_id}", color=(0, 0, 0, 1), font_size=18))
                box.add_widget(Label(text=f"{nombre}", color=(0, 0, 0, 1), font_size=18))
                box.add_widget(Label(text=f"{cantidad}", color=(0, 0, 0, 1), font_size=18))
                box.add_widget(Label(text=f"{costo}", color=(0, 0, 0, 1), font_size=18))
                box.add_widget(Label(text=f"{precio_venta}", color=(0, 0, 0, 1), font_size=18))
                box.add_widget(Label(text=f"{proveedor}", color=(0, 0, 0, 1), font_size=18))
                box.add_widget(Label(text=f"{categoria}", color=(0, 0, 0, 1), font_size=18))
                
                # Botón de eliminar
                eliminar_btn = Button(text="Eliminar", size_hint=(None, None), size=(100, 30))
                eliminar_btn.bind(on_press=lambda instance, pid=producto_id: self.eliminar_producto(pid))
                box.add_widget(eliminar_btn)

                product_grid.add_widget(box)

        except Exception as e:
            print(f"Error al cargar producto: {e}")
            
    def eliminar_producto(self, producto_id):
        try:
            db = BaseDatos()
            db.borrar(producto_id)
            self.cargar_productos()  # Recargar productos después de eliminar
        except Exception as e:
            print(f"Error al eliminar producto: {e}")

    def _update_rect(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0, 0, 0, 0.1)  # Color de fondo (negro translúcido)
            Rectangle(pos=instance.pos, size=instance.size)
        

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