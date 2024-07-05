# Vista - Aplicación {Gestor de Inventarios}
# Autor: Sebastian Sanchez Bentolila

# Librerías
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.image import Image
from modelo import BaseDatos  
import matplotlib.pyplot as plt
import seaborn as sns

# Clases que dan origen a las ventanas       
class MenuScreen(Screen):
    # Clase de la pagina - Menu
    pass

class HomeScreen(Screen):  
    # Clase de la pagina -Home-, donde figurarán cada item de la base de datos
    def on_enter(self, **kw):
        super(HomeScreen, self).on_enter(**kw)
        self.cargar_productos()

    def cargar_productos(self):
        try:
            db = BaseDatos()
            productos = db.seleccionar_todos()
            db.cerrar_db()
            product_grid = self.ids.product_grid
            product_grid.clear_widgets()  # Limpiar widgets existentes

            for producto in productos:
                producto_id, nombre, cantidad, costo, precio_venta, proveedor, categoria = producto
                
                box = BoxLayout(orientation='horizontal', padding=10, spacing=10, size_hint_y=None, height=50)
                with box.canvas.before:
                    Color(0, 0, 0, 0.1)  
                    Rectangle(pos=box.pos, size=box.size)
                
                box.bind(size=self._update_rect, pos=self._update_rect)

                # Caracteristicas de cada producto de la tabla stock
                box.add_widget(Label(text=f"ID: {producto_id}", color=(0, 0, 0, 1), font_size=18))
                box.add_widget(Label(text=f"{nombre}", color=(0, 0, 0, 1), font_size=18))
                box.add_widget(Label(text=f"{cantidad}", color=(0, 0, 0, 1), font_size=18))
                box.add_widget(Label(text=f"{costo}", color=(0, 0, 0, 1), font_size=18))
                box.add_widget(Label(text=f"{precio_venta}", color=(0, 0, 0, 1), font_size=18))
                box.add_widget(Label(text=f"{proveedor}", color=(0, 0, 0, 1), font_size=18))
                box.add_widget(Label(text=f"{categoria}", color=(0, 0, 0, 1), font_size=18))
                
                # Botón de modificar 
                editar_btn = Button(size_hint=(None, None), size=(32, 32))
                editar_btn.background_normal = 'archivos/img/editar.png'  
                editar_btn.producto_id = producto_id
                editar_btn.bind(on_press=self.editar_producto)
                box.add_widget(editar_btn)
                
                # Botón de eliminar
                eliminar_btn = Button(text="Eliminar", size_hint=(None, None), size=(100, 30))
                eliminar_btn.producto_id = producto_id  
                eliminar_btn.bind(on_press=self.eliminar_producto)
                box.add_widget(eliminar_btn)

                product_grid.add_widget(box)

        except Exception as e:
            print(f"Error al cargar productos: {e}")
            
    def eliminar_producto(self, instance):
        producto_id = instance.producto_id  # Obtener el producto_id del botón
        print(f"Intentando eliminar producto con ID: {producto_id}")  
        try:
            db = BaseDatos()
            db.borrar(producto_id)
            db.cerrar_db()
            print(f"Producto con ID {producto_id} eliminado exitosamente.")  
            self.cargar_productos()  # Recargar productos después de eliminar
        except Exception as e:
            print(f"Error al eliminar producto: {e}")

    def editar_producto(self, instance):
        producto_id = instance.producto_id
        edit_screen = self.manager.get_screen('edit')
        producto = self.db.seleccionar_producto(producto_id)
        if producto:
            edit_screen.cargar_datos(producto)
        self.manager.current = 'edit'
        
    def _update_rect(self, instance, value):
        instance.canvas.before.children[-1].pos = instance.pos
        instance.canvas.before.children[-1].size = instance.size
       

class AltaScreen(Screen):
    # Clase de la pagina - Alta de productos
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

class EditScreen(Screen):
    # Clase de la pagina - Editar/Modificar un productos en particular
    def cargar_datos(self, producto):
        producto_id, nombre, cantidad, costo, precio_venta, proveedor, categoria = producto
        self.ids.producto_id.text = str(producto_id)
        self.ids.producto.text = nombre
        self.ids.cantidad.text = str(cantidad)
        self.ids.costo.text = str(costo)
        self.ids.precio_venta.text = str(precio_venta)
        self.ids.proveedor.text = proveedor
        self.ids.categoria.text = categoria

    def guardar_cambios(self):
        producto_id = int(self.ids.producto_id.text)
        producto = self.ids.producto.text
        cantidad = int(self.ids.cantidad.text)
        costo = float(self.ids.costo.text)
        precio_venta = float(self.ids.precio_venta.text)
        proveedor = self.ids.proveedor.text
        categoria = self.ids.categoria.text

        self.db.actualizar(producto_id, producto, cantidad, costo, precio_venta, proveedor, categoria)
        self.manager.current = 'home'
        
        
class CreadorScreen(Screen):
    # Clase de la pagina - Creador
    pass

class EstadisticasScreen(Screen):
    # Clase de la pagina - Estadisticas
    def on_enter(self, *args):
        base_datos = BaseDatos()
        stats = base_datos.obtener_estadisticas()
        
        # Limpiar widgets
        self.ids.img_stats_container.clear_widgets()
        
        # Estadísticas
        self.ids.total_productos.text = f"Cantidad Total de Productos: {stats['total_productos']}"
        self.ids.mayor_stock.text = f"Producto con Mayor Stock: {stats['mayor_stock'][0]} ({stats['mayor_stock'][1]})"
        self.ids.menor_stock.text = f"Producto con Menor Stock: {stats['menor_stock'][0]} ({stats['menor_stock'][1]})"
        self.ids.valor_total_inventario.text = f"Costos Totales: ${stats['valor_total_inventario']}"
        self.ids.ingresos_potenciales.text = f"Ingresos Potenciales (ventas): ${stats['ingresos_potenciales']}" 
        
        # Gráficos
        base_datos.cursor.execute('SELECT categoria, cantidad FROM stock')
        productos = base_datos.cursor.fetchall()
        
        categorias = [producto[0] for producto in productos]
        cantidades = [producto[1] for producto in productos]
        
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
        base_datos.cerrar_db()

        # Agregar nuevos gráficos
        self.ids.img_stats_container.add_widget(Image(source='archivos/img/grafico_barras.png', size_hint_y=None, height=800))
        self.ids.img_stats_container.add_widget(Image(source='archivos/img/grafico_torta.png', size_hint_y=None, height=800))