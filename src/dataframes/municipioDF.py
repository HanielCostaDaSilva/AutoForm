import os
import pandas as pd
from unidecode import unidecode
from model.Municipio import Municipio, MunicipioException


__municipios_path="../data/municipios.xlsx"
__municipios_df= None

if os.path.exists(__municipios_path):
    #apenas fazemos a leitura do arquivo
    __municipios_df = pd.read_excel(__municipios_path,dtype=str)
else:
    __municipios_df = pd.DataFrame(columns=["NOME", "UF", "CODIGO"])
    __municipios_df.to_excel(__municipios_path,index=False)

""" 
def __get_municipios_df():
    return __municipios_df.copy()
"""
""" 
def add_municipio(municipio_nome:str,codigo_municipio:str):
    
    # Verificando se o nome do município ou o código existem no DataFrame
    if not __municipios_df.loc[__municipios_df['NOME'] == municipio_nome].empty:
        raise MunicipioException(f"O município '{municipio_nome}' já está cadastrado.")
    
    elif not __municipios_df.loc[__municipios_df['CODIGO'] == codigo_municipio].empty:
        raise MunicipioException(f"O código '{codigo_municipio}' já foi cadastrado.")
    
    else:
        municipio={
            "MUNICIPIO":municipio_nome,
            "CODIGO":codigo_municipio
        }
        municipios_df.loc[ len(municipios_df)] =municipio          
        __save_df(municipios_df)
 """    

def add_municipio(municipio: Municipio):
    municipio_registro = {
        "NOME": municipio.nome,
        "UF": municipio.UF,
        "CODIGO": municipio.codigo
    }
    
    __municipios_df.loc[ len(__municipios_df) ] = municipio_registro
    print(__municipios_df)  # Adiciona esta linha para verificar o tipo do objeto

    
def save_df(municipios_novos:'pd.DataFrame',path="../data/municipios.xlsx"):
    #Pegamos os valores antigos 
    municipios_antigos_df = pd.read_excel(path, dtype=str)
    #Mesclamos com o dataframe atual
    municipios_combinados = pd.merge(municipios_novos, municipios_antigos_df, how="outer")
    #Depois removemos os valores repitidos, a fim de garantir apenas os valores novos
    municipios_combinados.drop_duplicates()
    #Salvamos o Dataframe no caminho antigo
    municipios_combinados.to_excel(path,index=False)


def get_municipio_codigo(municipio_nome:str,municipio_uf:str)->str:
    
    municipio= __municipios_df.loc[__municipios_df["NOME"]== municipio_nome].loc[__municipios_df["UF"]== municipio_uf, "CODIGO"]
    
    if len(municipio)==0:
        raise MunicipioException(f"Não foi possivel encontrar o municipio: {municipio_nome} da UF: {municipio_uf}")
    
    return municipio.iloc[0]

    
if __name__=="__main__":
    """ 
    try:
        get_municipio_codigo("SAPE","PB")
        print("Achei Sape no dataframe")
    
    except MunicipioException as ME:
        print(ME)

        m1=Municipio("2515302","SAPE","PB")
        add_municipio(m1)
        save_df(__municipios_df,__municipios_path)
         """
    while True:    
        municipio_nome= unidecode(str.upper(input("Nome do municipio=> ")))
        municipio_uf= str.upper(input("UF do municipio=> "))
        municipio_codigo= ''
        
        try:
            municipio_codigo = get_municipio_codigo(municipio_nome,municipio_uf)
    
        except MunicipioException as ME:
            print(ME)
            municipio_codigo= input(f"\npor favor, pesquise pelo código do municipio {municipio_nome} e nos informe.\n  caso não queira, digite N =>").upper()
            
            if municipio_codigo=="N": continue
            add_municipio( Municipio(municipio_codigo, municipio_nome, municipio_uf))
        
        except KeyboardInterrupt as KE:
            print("Programa finalizado. ")
   
        finally:
            print(f"Municipio: {municipio_nome}  Código: {municipio_codigo}")
            