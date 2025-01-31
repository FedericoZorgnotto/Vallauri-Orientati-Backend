from __future__ import annotations

import random
import string
from typing import List, Optional

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

association_table_orientati = Table(
    "Association_orientati_gruppi",
    Base.metadata,
    Column("idOrientato", ForeignKey("Orientati.id")),
    Column("idGruppo", ForeignKey("Gruppi.id")),
)


class Gruppo(Base):
    __tablename__ = "Gruppi"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column()
    data: Mapped[str] = mapped_column()
    orario_partenza: Mapped[str] = mapped_column()
    codice: Mapped[Optional[str]] = mapped_column()

    orario_partenza_effettivo: Mapped[Optional[str]] = mapped_column()
    orario_fine_effettivo: Mapped[Optional[str]] = mapped_column()
    orientati: Mapped[List["Orientato"]] = relationship(secondary=association_table_orientati,  # noqa: F821
                                                        back_populates="gruppi")

    utenti: Mapped[List["Utente"]] = relationship("Utente", back_populates="gruppo")  # noqa: F821

    percorso_id: Mapped[int] = mapped_column(ForeignKey("Percorsi.id"))
    percorso: Mapped["Percorso"] = relationship("Percorso", back_populates="gruppi")  # noqa: F821

    numero_tappa: Mapped[Optional[int]] = mapped_column()
    arrivato: Mapped[Optional[bool]] = mapped_column()
    presenti: Mapped[List["Presente"]] = relationship("Presente", back_populates="gruppo")  # noqa: F821
    assenti: Mapped[List["Assente"]] = relationship("Assente", back_populates="gruppo")  # noqa: F821

    @classmethod
    def genera_codice(cls):
        return ''.join(random.choices(string.ascii_uppercase, k=3))
        pass

    def __repr__(self):
        return (f"Gruppo(id={self.id!r}, nome={self.nome!r}, data={self.data!r},"
                f" orario_partenza={self.orario_partenza!r}, percorso_id={self.percorso_id!r},"
                f" numero_tappa={self.numero_tappa!r}, arrivato={self.arrivato!r})")
