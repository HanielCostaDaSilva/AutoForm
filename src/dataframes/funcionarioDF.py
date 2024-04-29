#################################################################
#Modulo responsável por tratar a respeito de pesquisar, atualizar e remover funcionários  
#Os dados analisados estarão em uma planilha excel, no seguinte caminho: "../data" 
#Será utilzado Pandas para tal
#################################################################
import os
import pandas as pd


func_excel_path= "../data/func.xlsx"
func_situacao_df_excel_path= "../data/func_log.xlsx"

#== == Coletando os dados 

# Carregando o DataFrame
func_data_df = pd.read_excel(func_excel_path,dtype=str)

# Formatando os dados
func_data_df = func_data_df.fillna("")

situacao_lista = ["NAO CADASTRADO","CADASTRANDO","CADASTRADO"]

if os.path.exists(func_situacao_df_excel_path):
    # Carregue os cabeçalhos da planilha existente
    func_situacao_df = pd.read_excel(func_situacao_df_excel_path,dtype=str)
    
    #Trocamos os valores vazios por "situacao_lista[0]"
    
    func_situacao_df = func_situacao_df.fillna(situacao_lista[0])

else: 
    #CASO Não exista, criamos um Dataframe novo, com os dados dos funcionário. No final adicionamos a coluna SITUACAO
    func_situacao_df = func_data_df.copy()
    #Adicionamos a coluna SITUACAO no final da tabela 
    func_situacao_df["SITUACAO"] = situacao_lista[0]
    #Criamos a planilha na pasta data
    func_situacao_df.to_excel(func_situacao_df_excel_path,index=False)
    
print(func_data_df)
print(func_situacao_df)