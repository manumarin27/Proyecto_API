from API.api_module import API
from UI.ui_module import UI
import pandas as pd 
from sodapy import Socrata

class  Main:
    def __init__(self): 
        self.api = API()
        self.ui = UI()
        
    def iniciar_aplicacion(self): 
        while True: 
            self.ui.menu_bienvenida()
            opcion_escogida = input("\nEscriba la opción escogida: ")
            self.ui.limpiar_pantalla()

            if opcion_escogida == "1": 
                departamento, municipio, cultivo, limit = self.ui.obtener_datos_consulta()
                resultados = self.api.consultar_datos(departamento, municipio, cultivo, limit)
                if not resultados.empty:
                    medianas = self.api.calcular_mediana(resultados)
                    self.ui.mostrar_resultados(resultados, medianas)
                    self.ui.pausar_pantalla()
                    self.ui.limpiar_pantalla()  
                else:
                    print("\n\nERROR: NO SE ENCONTRARON DATOS PARA LOS CRITERIOS INGRESADOS")
                    print("Revíselos e intente nuevamente.\n")
                    self.ui.pausar_pantalla()
                    self.ui.limpiar_pantalla()               
            elif opcion_escogida == "2": 
                self.ui.mensaje_despedida()
                break
            else: 
                print("Opción no válida :(, intente nuevamente\n")
                self.ui.pausar_pantalla()
                self.ui.limpiar_pantalla() 

if __name__ == "__main__": 
    app = Main()
    app.iniciar_aplicacion()

    