import pandas as pd
import os
from rich.console import Console
from rich.table import Table

class UI:

    def __init__(self):
        self.console = Console()

    def menu_bienvenida(self):
        print("\n" + "="*80)
        print("\tCONSULTOR DE LAS PROPIEDADES EDÁFICAS DE LOS CULTIVOS")
        print("="*80 + "\n")
        print("¿Qué desea realizar?")
        print("Elija una opción:\n")
        print("1. Consultar propiedades")
        print("2. Salir")
        print("\n" + "="*80)
    
    def pausar_pantalla(self): 
        os.system("PAUSE")

    def limpiar_pantalla(self): 
        os.system("cls")

    def mensaje_despedida(self): 
        print("\n" + "="*80)
        print("\n¡Gracias por usar la aplicación!, hasta pronto :)\n SALIENDO...\n")
        print("="*80 + "\n")
        self.pausar_pantalla()
        
    def obtener_datos_consulta(self):
        print("\n" + "="*80)
        departamento = input("Ingrese el nombre del departamento: ").strip().upper()
        municipio = input("Ingrese el nombre del municipio: ").strip().upper()
        cultivo = input("Ingrese el nombre del cultivo: ").strip().title()
    
        while True:
            try:
                limit = int(input("Ingrese el número de registros a consultar: "))
                if limit > 1000:
                    print("Ha superado el límite de registros. Se consultará con el límite (1000 registros)")
                    limit = 1000
                print("="*80 + "\n")
                return departamento, municipio, cultivo, limit
            except ValueError:
                print("Por favor, ingrese un número válido para el límite.")

    def mostrar_resultados(self, resultados, medianas):
        medianas_df = pd.DataFrame([medianas], columns=['pH', 'Fósforo', 'Potasio'])
        tabla_final = pd.concat([resultados[['departamento', 'municipio', 'cultivo', 'topografia']].head(1), medianas_df], axis=1)
        # Crear la tabla con Rich
        table = Table(
            title="\nTABLA CON LA MEDIANA DE LAS VARIABLES EDÁFICAS\n",
            title_style="bold white",  # Color del título
            show_header=True,
            header_style="bold orange3",  # Estilo de los encabezados
            style="purple"  # Estilo de las celdas
        )
        for column in tabla_final.columns:
            table.add_column(column.title(), style="white")  # Cambiar el color de la celda
        for _, row in tabla_final.iterrows():
            table.add_row(*[str(item) for item in row])
        # Mostrar la tabla en la consola con color
        console = Console()
        console.print(table)

