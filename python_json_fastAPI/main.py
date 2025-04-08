from fastapi import FastAPI
import json

app = FastAPI()

# Carreguem dades
llista_alumnes = []

def carregar_dades():
    try:
        fitxer = open("alumnes.json", "rt")
        dades = json.load(fitxer)
        fitxer.close()
        return dades
    except:
        return []

def guardar_dades(dades):
    fitxer = open("alumnes.json", "wt")
    json.dump(dades, fitxer)
    fitxer.close()

def obtenir_seguent_id(dades):
    id_mes_alt = 0
    for alumne in dades:
        if alumne["id"] > id_mes_alt:
            id_mes_alt = alumne["id"]
    return id_mes_alt + 1

# Inicialitzem
llista_alumnes = carregar_dades()

@app.get("/")
def inici():
    return {"missatge": "Institut TIC de Barcelona"}

@app.get("/alumnes/")
def comptar_alumnes():
    return {"total_alumnes": len(llista_alumnes)}

@app.get("/alumne/{id_alumne}")
def llegir_alumne(id_alumne: int):
    for alumne in llista_alumnes:
        if alumne["id"] == id_alumne:
            return alumne
    return {"error": "Alumne no trobat"}

@app.post("/alumne/")
def afegir_alumne(nom: str, cognom: str, curs: str):
    nou_id = obtenir_seguent_id(llista_alumnes)
    alumne_nou = {
        "id": nou_id,
        "nom": nom,
        "cognom": cognom,
        "curs": curs
    }
    llista_alumnes.append(alumne_nou)
    guardar_dades(llista_alumnes)
    return {"missatge": "Alumne afegit", "id": nou_id}

@app.delete("/alumne/{id_alumne}")
def eliminar_alumne(id_alumne: int):
    trobat = False
    nova_llista = []
    for alumne in llista_alumnes:
        if alumne["id"] == id_alumne:
            trobat = True
        else:
            nova_llista.append(alumne)
    if trobat:
        llista_alumnes.clear()
        for a in nova_llista:
            llista_alumnes.append(a)
        guardar_dades(llista_alumnes)
        return {"missatge": "Alumne esborrat"}
    else:
        return {"error": "Alumne no trobat"}
