from pydantic import BaseModel, ConfigDict

class Medico_Create(BaseModel):
    nome: str
    especializacao: str

class Medico_Response(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    nome: str
    especializacao: str
    atendendo: bool
