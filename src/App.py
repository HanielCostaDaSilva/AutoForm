import os
import pandas as pd
import pyautogui as pag

# == == == Variaveis
#posicoes = [(100,300),(1970,343)] # x , y 
#caminho arquivos

func_excel_path= "../data/func.xlsx"
func_situacao_df_excel_path= "../data/func_log.xlsx"

#== Situação Vetor
situacao_lista = ["NAO CADASTRADO","CADASTRANDO","CADASTRADO"]

#== == parte da automação com os cursores 
x_cursor,y_cursor=0,0
x_posicao_inicial, y_posicao_inicial = 1970, 343

x_cursor, y_cursor = x_posicao_inicial, y_posicao_inicial

#tamanho das colunas
largura_coluna,altura_coluna = 65, 20

#limite da pagina
x_limite, y_limite= 3490, 906

def continuar_programa()->bool:
    """
    pergunta ao usuário se ele deseja continuar a excecução da automação
    Returns:
        caso o usuário deseja continuar, retorna ``True``, caso o contrário ``False``
    """
    
    print("Olá! Ainda por aí?") 
    print("Por questões de segurança, precisso que você confirme se deseja continuar")
    resposta = ""
    
    while resposta not in ["S","N"]:
        resposta = input("(s/n) -> ").upper()
        
    return resposta=="S"

#input("pressione 'Enter' para continuar ou ( CTRL + C ) para encerrar.")

# == == == Variaveis
#posicoes = [(100,300),(1970,343)] # x , y 

#caminho arquivos

#== Situação Vetor
situacao_lista = ["NAO CADASTRADO","CADASTRANDO","CADASTRADO"]

#== == parte da automação com os cursores 
x_cursor,y_cursor=0,0
x_posicao_inicial, y_posicao_inicial = 1970, 343

x_cursor, y_cursor = x_posicao_inicial, y_posicao_inicial

#tamanho das colunas
largura_coluna,altura_coluna = 65, 20

#limite da pagina
x_limite, y_limite= 3490, 906

#== == Coletando os dados 
# Carregando o arquivo Excel
func_data = pd.read_excel(func_excel_path,dtype=str)

# Formatando os dados
func_data = func_data.fillna("")

# Buscando uma tabela para analisar se funcionario já foi cadastrado 
func_situacao_df = None

if os.path.exists(func_situacao_df_excel_path):
    # Carregue os cabeçalhos da planilha existente
    func_situacao_df = pd.read_excel(func_situacao_df_excel_path,dtype=str)
    func_situacao_df = func_situacao_df.fillna("")

    # Use os cabeçalhos da planilha existente para criar uma nova planilha
else: 
    #CASO Não exista, criamos um Dataframe novo, com os dados dos funcionário. No final adicionamos a coluna SITUACAO
    func_situacao_df = func_data.copy()
    #Adicionamos a coluna SITUACAO no final da tabela 
    func_situacao_df["SITUACAO"] = situacao_lista[0]
    #Criamos a planilha na pasta data
    func_situacao_df.to_excel(func_situacao_df_excel_path,index=False)

#iteirando sobre o dataframe e com automação
for index, row in func_data.iterrows():
    #mova o cursor para o inicio da proxima linha,    
    y_cursor += altura_coluna 
    
    situacao_check= func_situacao_df.loc[func_situacao_df["MATRICULA"]==row["MATRICULA"],"SITUACAO"]
        
    if  situacao_check.iloc[0] != situacao_lista[0] and situacao_check.iloc[0] != "":
        print(f"{row['NOME']}, já havia sido cadastrado")
        continue

    if(y_cursor>=y_limite):
        y_cursor = y_posicao_inicial
        pag.scroll(100)
    #Checamos se o funcionário já não havia sido cadastrado
    print(row)
        
    if((index + 1)%2 ==0):
        print(f"você está cadastando a linha: {index + 1}")
        if not continuar_programa(): 
            break
    
    #dizemos ao func_situacao_df, que o funcionario com matricula tal vai ser cadastrado
    func_situacao_df.loc[func_situacao_df["MATRICULA"] == row["MATRICULA"], "SITUACAO"] = situacao_lista[1]
    func_situacao_df.to_excel(func_situacao_df_excel_path, index=False)

    
    # Movimenta o mouse para a posição da linha desejada
    #pag.moveTo(x_cursor, y_cursor)
    # Clique para selecionar a tela
    #pag.click()
    
    #acessando os valores da coluna
    """ for col in row.values:
        # clique para selecionar a coluna
        pag.click()
        
        #escreva a informação do funcionário
        pag.write(str(col))
        
        #pressione enter para finalizar o cadastro
        pag.press('enter')        
        
        #mude o x_cursor para a proxima coluna da linha
        x_cursor += largura_coluna 
        #mova o cursor para a proxima coluna
        pag.moveTo(x_cursor, y_cursor)        
        # repita o processo """
    
    #dizemos ao func_situacao_df, que o funcionario acabou de ser cadastrado
    func_situacao_df.loc[ func_situacao_df["MATRICULA"] == row["MATRICULA"], "SITUACAO"] = situacao_lista[-1]    
    #mandamos o dataframe para o excel
    
    func_situacao_df.to_excel(func_situacao_df_excel_path,index=False)
        
    x_cursor = x_posicao_inicial
    #input()
    
    
print("Programa encerrado")