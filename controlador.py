# Controlador - Aplicación {Gestor de Inventarios}
# Autor: Sebastian Sanchez Bentolila

# Librerias
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from vista import MenuScreen, HomeScreen, AltaScreen, CreadorScreen, EstadisticasScreen, EditScreen
from modelo import BaseDatos
from kivy.lang import Builder
import webbrowser

# Cargar los archivos KV
Builder.load_file('menu.kv')
Builder.load_file('mi.kv')

class InventarioApp(App):
    # Clase principal -main- de la aplicación
    title = "Gestor de Inventario"
    icon = "archivos/img/inventario.png"
    
    def build(self):
        sm = ScreenManager()
        db = BaseDatos()  # Instancia de la base de datos
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(AltaScreen(name='alta'))
        sm.add_widget(EstadisticasScreen(name='estadisticas'))
        sm.add_widget(CreadorScreen(name='creador'))
        sm.add_widget(EditScreen(name='edit'))

        # Pasar la instancia de la base de datos a cada pantalla
        for screen in sm.screens:
            screen.db = db

        return sm

    def agregar_producto(self, producto, cantidad, costo, precio_venta, proveedor, categoria):
        db = self.root.get_screen('menu').db
        db.insertar(producto, int(cantidad), float(costo), float(precio_venta), proveedor, categoria)
        
    def open_link(self, url):
        # Abrir link externos que te lleven al navegador predeterminado
        webbrowser.open(url)

if __name__ == '__main__':
    InventarioApp().run()