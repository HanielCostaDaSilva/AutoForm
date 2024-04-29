import pandas as pd
import pyautogui as pag

#from dataframes import funcionarioDF as fdf, municipioAPI as munapi, municipioDF as mundf

from dataframes.funcionarioDF import *
from dataframes import  municipioAPI as munapi, municipioDF as mundf
from model.Municipio import *
# == == == Variaveis
#posicoes = [(100,300),(1970,343)] # x , y 
#caminho arquivos

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

def get_municipio(municipio_nome:str, municipio_uf:str)->Municipio:
    r''':Função responsável por procurar pelo :class:`Municipio` do funcionario.
        :Primeiro irá procurar no `municipios_df`,
        :Caso não encontre, ele irá requisitar a API,
        :Se não for possível encontrar, lançará :class:`MunicipioException` 
    '''
    
    municipio= None
    try:
        municipio = mundf.get_municipio_codigo(municipio_nome,municipio_uf)
    
    except MunicipioException as ME:
        #Se não encontrou localmente, requiste a API
        municipio = munapi.get_municipio_codigo(municipio_nome,municipio_uf)
        #Caso tenha achado, salve no DataFrame Local
        mundf.add_municipio(municipio)   
        #Se não achou, não há o que fazer, lance um exceção
        mundf.save_df()
    return municipio

#input("pressione 'Enter' para continuar ou ( CTRL + C ) para encerrar.")

# == == == Variaveis
#posicoes = [(100,300),(1970,343)] # x , y 

#caminho arquivos

#== == parte da automação com os cursores 
x_cursor,y_cursor=0,0
x_posicao_inicial, y_posicao_inicial = 1970, 343

x_cursor, y_cursor = x_posicao_inicial, y_posicao_inicial

#tamanho das colunas
largura_coluna,altura_coluna = 65, 20

#limite da pagina
x_limite, y_limite= 3490, 906

#iteirando sobre o dataframe e com automação
for index, row in func_data_df.iterrows():
    #mova o cursor para o inicio da proxima linha,    
    y_cursor += altura_coluna 
    
    situacao_check= func_situacao_df.loc[func_situacao_df["MATRICULA"]==row["MATRICULA"],"SITUACAO"]
     
    #Checamos se o funcionário já não havia sido cadastrado   
    if  situacao_check.iloc[0] != situacao_lista[0] and situacao_check.iloc[0] != "":
        print(f"{row['NOME']}, já havia sido cadastrado")
        continue
    
    if(y_cursor>=y_limite):
        y_cursor = y_posicao_inicial
        pag.scroll(100)
    
        
    if((index + 1)%3 ==0):
        print(f"você está cadastando a linha: {index + 1}")
        if not continuar_programa(): 
            break
    
    #dizemos ao func_situacao_df, que o funcionario com matricula tal vai ser cadastrado
    func_situacao_df.loc[func_situacao_df["MATRICULA"] == row["MATRICULA"], "SITUACAO"] = situacao_lista[1]
    func_situacao_df.to_excel(func_situacao_df_excel_path, index=False)
    
    # == == Lógica antes de inserir o Funcionario no formulario
    
    # pesquisamos o codigo do municipio do Funcionario
    try:
        municipio_encontrado = get_municipio(row["MUNICIPIO"], row["UF"])
        func_situacao_df.loc[func_situacao_df["MATRICULA"] == row["MATRICULA"], "CODIGO_MUNICIPIO"] = municipio_encontrado.codigo

        print(municipio_encontrado)
    except MunicipioException as ME:
        #Informamos que não encontramos este municipio
        print(ME)
        input("Pressione Enter para pular este funcionário... ")
        #Atualizamos no DataFrame para informar que não encontramos o municipio
        func_situacao_df.loc[func_situacao_df["MATRICULA"] == row["MATRICULA"], "SITUACAO"] = situacao_lista[2]
        #Pulamos o funcionário
        continue

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