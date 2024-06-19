# Controlador - Aplicación {Gestor de Inventarios}
# Autor: Sebastian Sanchez Bentolila

# Librerias
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from vista import MenuScreen, HomeScreen, AltaScreen, CreadorScreen, EstadisticasScreen
from modelo import BaseDatos
from kivy.lang import Builder
import webbrowser

# Cargar los archivos KV
Builder.load_file('menu.kv')
Builder.load_file('mi.kv')

class InventarioApp(App):
    # Clase principal -main- de la aplicación
    def build(self):
        sm = ScreenManager()
        db = BaseDatos()  # Crear una instancia de la base de datos
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(AltaScreen(name='alta'))
        sm.add_widget(EstadisticasScreen(name='estadisticas'))
        sm.add_widget(CreadorScreen(name='creador'))

        # Pasar la instancia de la base de datos a cada pantalla
        for screen in sm.screens:
            screen.db = db

        return sm

    def agregar_producto(self, producto, cantidad, costo, precio_venta, proveedor):
        db = self.root.get_screen('menu').db
        db.insertar(producto, int(cantidad), float(costo), float(precio_venta), proveedor)
        self.root.current = 'home'
        
    def open_link(self, url):
        webbrowser.open(url)

if __name__ == '__main__':
    InventarioApp().run()