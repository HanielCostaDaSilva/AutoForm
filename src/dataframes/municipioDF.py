import os
import pandas as pd
from unidecode import unidecode
from model.Municipio import Municipio, MunicipioException


def add_municipio(municipio: Municipio):
    municipio_registro = {
        "NOME": unidecode(municipio.nome),
        "UF": municipio.UF,
        "CODIGO": municipio.codigo
    }
    check_municipio = __municipios_df.loc[__municipios_df["NOME"]== municipio_registro["NOME"]].loc[__municipios_df["UF"]== municipio_registro["UF"]]
    
    if len(check_municipio) == 0:
        __municipios_df.loc[ len(__municipios_df) ] = municipio_registro
    else:
        raise MunicipioException(f"O municipio: {municipio}, já cadastrado")
    
    
def save_df():
    #Pegamos os valores antigos 
    municipios_antigos_df = pd.read_excel(__municipios_path, dtype=str)
    #Mesclamos com o dataframe atual
    municipios_combinados = pd.concat([__municipios_df, municipios_antigos_df],ignore_index=True)
    #Depois removemos os valores repitidos, a fim de garantir apenas os valores novos
    municipios_combinados = municipios_combinados.drop_duplicates()
    #Salvamos o Dataframe no caminho antigo
    municipios_combinados.to_excel(__municipios_path,index=False)
    print(municipios_combinados)


def get_municipio_codigo(municipio_nome:str,municipio_uf:str)->Municipio:
    
    municipio_nome = unidecode(municipio_nome).upper()
    
    municipio_row= __municipios_df.loc[__municipios_df["NOME"]== municipio_nome].loc[__municipios_df["UF"]== municipio_uf]
    
    if len(municipio_row) == 0:
        raise MunicipioException(f"Não foi possivel encontrar o municipio: {municipio_nome} da UF: {municipio_uf}")
    
    # Extrai os valores específicos da linha
    codigo = municipio_row.iloc[0]["CODIGO"]
    nome = municipio_row.iloc[0]["NOME"]
    uf = municipio_row.iloc[0]["UF"]

    # Cria um objeto Municipio com os valores extraídos
    municipio = Municipio(codigo, nome, uf)
    
    return municipio


#Procurando
diretorio_atual = os.path.dirname(os.path.realpath(__file__))

__municipios_path = os.path.join(diretorio_atual,"..","data","municipios.xlsx")
 
__municipios_df= None


if os.path.exists(__municipios_path):
    #apenas fazemos a leitura do arquivo
    __municipios_df = pd.read_excel(__municipios_path,dtype=str)
else:
    __municipios_df = pd.DataFrame(columns=["NOME", "UF", "CODIGO"])
    __municipios_df.to_excel(__municipios_path,index=False)
    
if __name__=="__main__":

    try:
        get_municipio_codigo("SAPE","PB")
        print("Achei Sape no dataframe")
    
    except MunicipioException as ME:
        print(ME)
        
        m1=Municipio("2515302","SAPE","PB")
        add_municipio(m1)
        save_df()
         
    while True:    
        municipio_nome= unidecode(str.upper(input("Nome do municipio=> ")))
        municipio_uf= str.upper(input("UF do municipio=> "))
        municipio_encontrado= None
        
        try:
            municipio_codigo = get_municipio_codigo(municipio_nome,municipio_uf)
    
        except MunicipioException as ME:
            print(ME)
            municipio_encontrado= input(f"\npor favor, pesquise pelo código do municipio {municipio_nome} e nos informe.\n  caso não queira, digite N =>").upper()
            
            if municipio_encontrado=="N": continue
            add_municipio(Municipio(municipio_codigo, municipio_nome, municipio_uf))
            save_df()
        
        except KeyboardInterrupt as KE:
            print("Programa finalizado. ")
   
        finally:
            print(f"Municipio: {municipio_encontrado}") 
            