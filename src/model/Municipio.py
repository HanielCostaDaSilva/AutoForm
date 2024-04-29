class MunicipioException(Exception):
    def __init__(self,message):
        super().__init__(message)
        


class Municipio:
    codigo:str
    nome:str
    UF:str
    
    def __init__(self,codigo:str,nome:str,UF:str):
        self.nome = str.upper(nome)
        self.codigo = codigo
        self.UF = UF
        
    def __str__(self) -> str:
        return f"nome: {self.nome}, código: {self.codigo}, UF: {self.UF}"
        
