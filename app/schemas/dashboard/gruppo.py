from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class GruppoBase(BaseModel):
    nome: str
    orario_partenza: str
    numero_tappa: Optional[int] = None
    arrivato: Optional[bool] = None
    nomi_orientatori: Optional[List[str]] = None
    aula_nome: Optional[str] = None
    aula_posizione: Optional[str] = None
    aula_materia: Optional[str] = None
    minuti_arrivo: Optional[int] = None
    minuti_partenza: Optional[int] = None



class GruppoResponse(GruppoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class GruppoList(BaseModel):
    gruppi: List[GruppoResponse]
