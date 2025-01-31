from typing import Optional

from pydantic import BaseModel, ConfigDict


class OrientatoBase(BaseModel):
    nome: str
    cognome: str
    scuolaDiProvenienza_id: int

    model_config = ConfigDict(from_attributes=True)


class OrientatoResponse(OrientatoBase):
    nomeScuolaDiProvenienza: str
    id: int


class OrientatoBaseAdmin(OrientatoBase):
    id: int


class OrientatoCreate(BaseModel):
    nome: str
    cognome: str
    scuolaDiProvenienza_id: int


class OrientatoUpdate(BaseModel):
    nome: Optional[str] = None
    cognome: Optional[str] = None
    scuolaDiProvenienza_id: Optional[int] = None


class OrientatoDelete(BaseModel):
    id: int


class OrientatoList(BaseModel):
    orientati: list[OrientatoResponse]
