from fastapi import FastAPI
import json

app = FastAPI()

# Carreguem dades
llista_alumnes = []  # Aquesta serà la llista on guardarem tots els alumnes

def carregar_dades():
    try:
        fitxer = open("alumnes.json", "rt")  # Obrim el fitxer per llegir-lo
        dades = json.load(fitxer)            # Carreguem el contingut del fitxer JSON
        fitxer.close()                       # Tanquem el fitxer un cop llegit
        return dades                         # Retornem la llista d’alumnes
    except:
        # Si el fitxer no existeix o hi ha algun error, retornem una llista buida
        return []

def guardar_dades(dades):
    fitxer = open("alumnes.json", "wt")  # Obrim el fitxer per escriure
    json.dump(dades, fitxer)             # Guardem la llista d’alumnes en format JSON
    fitxer.close()                       # Tanquem el fitxer després de guardar

def obtenir_seguent_id(dades):
    id_mes_alt = 0
    for alumne in dades:
        if alumne["id"] > id_mes_alt:
            id_mes_alt = alumne["id"]  # Busquem l'ID més alt a la llista
    return id_mes_alt + 1  # Retornem el següent ID disponible

# Inicialitzem
llista_alumnes = carregar_dades()  # Carreguem les dades des del fitxer a l'inici

@app.get("/")
def inici():
    # Endpoint bàsic per comprovar si l'API funciona
    return {"missatge": "Institut TIC de Barcelona"}

@app.get("/alumnes/")
def comptar_alumnes():
    # Retorna el nombre total d'alumnes a la llista
    return {"total_alumnes": len(llista_alumnes)}

@app.get("/alumne/{id_alumne}")
def llegir_alumne(id_alumne: int):
    # Busquem un alumne pel seu ID
    for alumne in llista_alumnes:
        if alumne["id"] == id_alumne:
            return alumne  # Si el trobem, el retornem
    return {"error": "Alumne no trobat"}  # Si no el trobem, retornem un error

@app.post("/alumne/")
def afegir_alumne(nom: str, cognom: str, curs: str):
    # Afegim un nou alumne a la llista
    nou_id = obtenir_seguent_id(llista_alumnes)  # Assignem un ID nou
    alumne_nou = {
        "id": nou_id,
        "nom": nom,
        "cognom": cognom,
        "curs": curs
    }
    llista_alumnes.append(alumne_nou)     # Afegim l'alumne nou a la llista
    guardar_dades(llista_alumnes)         # Guardem la nova llista al fitxer
    return {"missatge": "Alumne afegit", "id": nou_id}  # Retornem confirmació

@app.delete("/alumne/{id_alumne}")
def eliminar_alumne(id_alumne: int):
    # Esborrem un alumne pel seu ID
    trobat = False
    nova_llista = []  # Creem una nova llista sense l’alumne a esborrar
    for alumne in llista_alumnes:
        if alumne["id"] == id_alumne:
            trobat = True  # Marquem que l’hem trobat
        else:
            nova_llista.append(alumne)  # Afegim els altres alumnes a la nova llista
    if trobat:
        llista_alumnes.clear()  # Buidem la llista original
        for a in nova_llista:
            llista_alumnes.append(a)  # Tornem a afegir només els que volem mantenir
        guardar_dades(llista_alumnes)  # Guardem la nova llista al fitxer
        return {"missatge": "Alumne esborrat"}
    else:
        return {"error": "Alumne no trobat"}  # Si no hem trobat l’alumne, avisem
