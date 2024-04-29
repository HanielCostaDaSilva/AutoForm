import requests
from model.Municipio import Municipio, MunicipioException

# URL base do serviço de dados do IBGE
base_url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios/"

################################################################
# Codigo municipio: ID
# Caso haja um único município com determinado nome, é retornado um dicionário
# Caso haja mais de um município com determinado nome, é retornado uma lista de dicionários
################################################################


def get_municipio_codigo(municipio_nome: str, municipio_uf: str) -> Municipio:
    '''
    Retorna um objeto Municipio contendo o codigo do municipio, o nome e a UF.
    Caso não encontre, lança uma Exception
    '''
    # URL completa para a requisição GET
    municipio_nome = municipio_nome.strip().replace(" ", "-")
    url = f"{base_url}{municipio_nome}"
    
    municipio_encontrado = None

    # Fazendo a requisição GET
    response = requests.get(url)
    
    # Verificando se a requisição foi bem sucedida (código 200)

    if response.status_code == 200:
        data = response.json()

        # Caso a resposta seja apenas um item, a API retorna um dicionário:
        if isinstance(data, dict):
            
            municipio_encontrado_uf = data['microrregiao']['mesorregiao']['UF']['sigla']
            
            if municipio_uf == municipio_encontrado_uf:
                municipio_encontrado = Municipio(data['id'], data['nome'], municipio_encontrado_uf)

        # Caso a resposta seja mais de um item, a API retornará uma lista:
        elif isinstance(data, list):
            municipio_encontrado= __get_municipio_codigo_list(data, municipio_uf)
        
        else:
            raise MunicipioException(f"Não foi encontrado o municipio:\n {municipio_nome} na UF {municipio_uf}")
            
    else:
        # Se não, imprima o código d status
        raise MunicipioException(
            f"Erro{response.status_code} \n Não foi possível obter dados a respeito do município: {municipio_nome}.")
    
    # Caso tenha achado o municipio:
    if municipio_encontrado is not None:
        return municipio_encontrado
    
    # Caso tenha feito a requisição, mas não encontrou o município pertecente a tal uf:
    else:
        raise MunicipioException(f"Não foi possivel encontrar o municipio: {municipio_nome} da UF: {municipio_uf}")
    

def __get_municipio_codigo_list(municipio_lista: list[dict],uf:str)->Municipio:
    for municipio_encontrado in municipio_lista:

        municipio_encontrado_uf = municipio_encontrado['microrregiao']['mesorregiao']['UF']['sigla']

        if (uf == municipio_encontrado_uf):
            return Municipio(municipio_encontrado['id'], municipio_encontrado['nome'], municipio_encontrado_uf)


if __name__ == '__main__':
    # Nome do município desejado
    nome_do_municipio = "bom jesus"
    uf_municipio = "RN"

    print(get_municipio_codigo(nome_do_municipio, uf_municipio))

    uf_municipio = "PB"
    print(get_municipio_codigo(nome_do_municipio, uf_municipio))
