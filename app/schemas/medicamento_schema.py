from pydantic import BaseModel, ConfigDict

class Medicamento_Response(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    nome: str
    dosagem: str
    forma: str