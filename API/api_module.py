from sodapy import Socrata
import pandas as pd

class API: 

    def __init__(self): 
        self.client = Socrata("www.datos.gov.co", None)

    def consultar_datos(self, departamento, municipio, cultivo, limit):
        query = f"departamento='{departamento}' AND municipio='{municipio}' AND cultivo='{cultivo}'"
        print(f"Consulta realizada: {query}")
        try:
            # Realiza la consulta a la API con solo las columnas necesarias
            columnas_necesarias = "departamento, municipio, cultivo, topografia, ph_agua_suelo_2_5_1_0, f_sforo_p_bray_ii_mg_kg, potasio_k_intercambiable_cmol_kg"
            results = self.client.get("ch4u-f3i5", where=query, limit=limit, select=columnas_necesarias) 
            if not results:  
                return pd.DataFrame()  # Devuelve un DataFrame vacío
            df = pd.DataFrame(results)
            return df
        except Exception as e:
            print(f"Error al consultar datos: {e}")
            return pd.DataFrame()  

    def calcular_mediana(self, resultados):
        Data_frame = pd.DataFrame.from_records(resultados)  # Convertir resultados en DataFrame
        if Data_frame.empty:
            return {}
        
        # Verificar que las columnas existen antes de continuar
        required_columns = ['ph_agua_suelo_2_5_1_0', 'f_sforo_p_bray_ii_mg_kg', 'potasio_k_intercambiable_cmol_kg']
        missing_columns = [col for col in required_columns if col not in Data_frame.columns]
        if missing_columns:
            return {}
        
        # Extraer valores especiales (contienen carácter especial)
        valor_especial_ph = Data_frame['ph_agua_suelo_2_5_1_0'].apply(lambda x: x if isinstance(x, str) and '<' in x else None).dropna().unique()
        valor_especial_fosforo = Data_frame['f_sforo_p_bray_ii_mg_kg'].apply(lambda x: x if isinstance(x, str) and '<' in x else None).dropna().unique()
        valor_especial_potasio = Data_frame['potasio_k_intercambiable_cmol_kg'].apply(lambda x: x if isinstance(x, str) and '<' in x else None).dropna().unique()
       
        # Convertir columnas a numérico, solo las que NO sean cadenas especiales para calcular la mediana
        Data_frame['ph_agua_suelo_2_5_1_0'] = pd.to_numeric(Data_frame['ph_agua_suelo_2_5_1_0'].where(Data_frame['ph_agua_suelo_2_5_1_0'].
                                                                                                    apply(lambda x: not isinstance(x, str) or '<' not in x)), errors='coerce')
        Data_frame['f_sforo_p_bray_ii_mg_kg'] = pd.to_numeric(Data_frame['f_sforo_p_bray_ii_mg_kg'].where(Data_frame['f_sforo_p_bray_ii_mg_kg'].
                                                                                                    apply(lambda x: not isinstance(x, str) or '<' not in x)), errors='coerce')
        Data_frame['potasio_k_intercambiable_cmol_kg'] = pd.to_numeric(Data_frame['potasio_k_intercambiable_cmol_kg'].where(Data_frame['potasio_k_intercambiable_cmol_kg'].
                                                                                                    apply(lambda x: not isinstance(x, str) or '<' not in x)), errors='coerce')
        
        # Calcular medianas ignorando NaN (que se descartan automáticamente)
        mediana_ph = valor_especial_ph[0] if len(valor_especial_ph) > 0 else Data_frame['ph_agua_suelo_2_5_1_0'].median()
        mediana_fosforo = valor_especial_fosforo[0] if len(valor_especial_fosforo) > 0 else Data_frame['f_sforo_p_bray_ii_mg_kg'].median()
        mediana_potasio = valor_especial_potasio[0] if len(valor_especial_potasio) > 0 else Data_frame['potasio_k_intercambiable_cmol_kg'].median()
        
        medianas = {
            'pH': mediana_ph,
            'Fósforo': mediana_fosforo,
            'Potasio': mediana_potasio
        }

        return medianas





