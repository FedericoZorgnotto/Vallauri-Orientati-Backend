from app.database import get_db
from app.models import Gruppo
from app.schemas.admin.dashboard.gruppo import GruppoList, GruppoResponse


def get_all_gruppi():
    """
    Legge tutti i gruppi del giorno dal database
    """
    db = next(get_db())
    # gruppi = db.query(Gruppo).filter(Gruppo.data == datetime.now().strftime("%d/%m/%Y")).all()
    gruppi = db.query(Gruppo).all()
    listaGruppi = GruppoList(gruppi=[])

    listaGruppi.gruppi = [GruppoResponse.model_validate(gruppo) for gruppo in gruppi]
    for gruppo in listaGruppi.gruppi:
        db_gruppo = db.query(Gruppo).filter(Gruppo.id == gruppo.id).first()

        if db_gruppo.numero_tappa == 0 and db_gruppo.arrivato:
            gruppo.percorsoFinito = True

        if not gruppo.numero_tappa == 0:
            db_gruppo = db.query(Gruppo).filter(Gruppo.id == gruppo.id).first()

            tappe = sorted(db_gruppo.percorso.tappe, key=lambda tappa: tappa.minuti_partenza)

            gruppo.aula_nome = tappe[gruppo.numero_tappa - 1].aula.nome
            gruppo.aula_posizione = tappe[gruppo.numero_tappa - 1].aula.posizione
            gruppo.aula_materia = tappe[gruppo.numero_tappa - 1].aula.materia
            gruppo.minuti_arrivo = tappe[gruppo.numero_tappa - 1].minuti_arrivo
            gruppo.minuti_partenza = tappe[gruppo.numero_tappa - 1].minuti_partenza

        # orientati = db.query(Gruppo).filter(Gruppo.id == gruppo.id).first().orientati
        # gruppo.totale_orientati = len(orientati)
        # presenti = db.query(Presente).filter(Presente.gruppo_id == gruppo.id).all()
        # gruppo.orientati_presenti = len(presenti)
        # assenti = db.query(Assente).filter(Assente.gruppo_id == gruppo.id).all()
        # gruppo.orientati_assenti = len(assenti)

    listaGruppi.gruppi = sorted(listaGruppi.gruppi, key=lambda gruppo: gruppo.orario_partenza)
    listaGruppi.gruppi = sorted(listaGruppi.gruppi, key=lambda gruppo: gruppo.percorsoFinito is True)
    return listaGruppi
