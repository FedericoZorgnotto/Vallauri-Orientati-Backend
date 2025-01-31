from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.middlewares.auth_middleware import admin_access
from app.models import Gruppo
from app.schemas.gruppo import GruppoList, GruppoResponse, GruppoUpdate, GruppoCreate
from app.schemas.tappa import TappaList
from app.services.orientatori import crea_codice_gruppo

gruppi_router = APIRouter()


@gruppi_router.get("/", response_model=GruppoList)
async def get_all_gruppi(db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge tutti i gruppi dal database
    """
    gruppi = db.query(Gruppo).all()
    return GruppoList(gruppi=[GruppoResponse.model_validate(gruppo) for gruppo in gruppi])


@gruppi_router.get("/{gruppo_id}", response_model=GruppoResponse)
async def get_gruppo(gruppo_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge un gruppo dal database
    """
    if not (db.query(Gruppo).filter(Gruppo.id == gruppo_id).first()):
        raise HTTPException(status_code=404, detail="Gruppo not found")
    try:
        gruppo = db.query(Gruppo).filter(Gruppo.id == gruppo_id).first()
        return gruppo
    except Exception as e:  # noqa: F841
        raise HTTPException(status_code=500, detail="Internal server error")


@gruppi_router.get("/tappe/{gruppo_id}", response_model=TappaList)
async def get_tappe_gruppo(gruppo_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Legge le tappe di un gruppo dal database, ordinandole per minuti_arrivo crescente
    """
    gruppo = db.query(Gruppo).filter(Gruppo.id == gruppo_id).first()

    if not gruppo:
        raise HTTPException(status_code=404, detail="Gruppo not found")

    TappaList.tappe = sorted(gruppo.percorso.tappe, key=lambda tappa: tappa.minuti_arrivo)
    return TappaList


@gruppi_router.put("/{gruppo_id}", response_model=GruppoResponse)
async def update_gruppo(gruppo_id: int, gruppo_update: GruppoUpdate, db: Session = Depends(get_db),
                        _=Depends(admin_access)):
    """
    Aggiorna un gruppo nel database
    """

    db_gruppo = db.query(Gruppo).filter(Gruppo.id == gruppo_id).first()

    if not db_gruppo:
        raise HTTPException(status_code=404, detail="Gruppo not found")

    if gruppo_update.nome is not None:
        db_gruppo.nome = gruppo_update.nome
    if gruppo_update.orario_partenza is not None:
        db_gruppo.orario_partenza = gruppo_update.orario_partenza
    if gruppo_update.data is not None:
        db_gruppo.data = gruppo_update.data
    if gruppo_update.percorso_id is not None:
        db_gruppo.percorso_id = gruppo_update.percorso_id
    if gruppo_update.numero_tappa is not None:
        db_gruppo.numero_tappa = gruppo_update.numero_tappa
    if gruppo_update.arrivato is not None:
        db_gruppo.arrivato = gruppo_update.arrivato

    db.commit()
    db.refresh(db_gruppo)

    return db_gruppo


@gruppi_router.post("/", response_model=GruppoResponse)
async def create_gruppo(gruppo: GruppoCreate, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Crea un gruppo nel database
    """

    db_gruppo = Gruppo(
        nome=gruppo.nome,
        data=gruppo.data,
        percorso_id=gruppo.percorso_id,
        orario_partenza=gruppo.orario_partenza,
        numero_tappa=0,
        arrivato=False
    )

    db.add(db_gruppo)
    db.commit()
    db.refresh(db_gruppo)
    return db_gruppo


@gruppi_router.delete("/{gruppo_id}")
async def delete_gruppo(gruppo_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Cancella un gruppo dal database
    """
    if not db.query(Gruppo).filter(Gruppo.id == gruppo_id).first():
        raise HTTPException(status_code=404, detail="Gruppo not found")
    try:
        db.query(Gruppo).filter(Gruppo.id == gruppo_id).delete()
        db.commit()
        return {"message": "Gruppo deleted successfully"}
    except Exception as e:
        if e.args[0] == 1451:
            raise HTTPException(status_code=400, detail="Gruppo has dependencies")
        else:
            raise HTTPException(status_code=500, detail="Internal server error")


@gruppi_router.put("/rigeneraCodice/{gruppo_id}", response_model=GruppoResponse)
async def rigenera_codice_gruppo(gruppo_id: int, db: Session = Depends(get_db), _=Depends(admin_access)):
    """
    Rigenera il codice di un gruppo
    """
    if not db.query(Gruppo).filter(Gruppo.id == gruppo_id).first():
        raise HTTPException(status_code=404, detail="Gruppo not found")
    try:
        gruppo = db.query(Gruppo).filter(Gruppo.id == gruppo_id).first()
        gruppo.codice = crea_codice_gruppo()
        db.commit()
        db.refresh(gruppo)
        return gruppo
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
