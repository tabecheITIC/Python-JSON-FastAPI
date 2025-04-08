import json

# Variables globals
llista_alumnes = []
seguent_id = 1

def carregar_dades():
    dades = []
    try:
        fitxer = open("alumnes.json", "rt")
        dades = json.load(fitxer)
        fitxer.close()
        print("Dades carregades correctament!")
    except:
        print("No s'ha trobat alumnes.json. Comencem amb una llista buida.")

    return dades

def obtenir_seguent_id(llista):
    id_mes_alt = 0
    for alumne in llista:
        if alumne["id"] > id_mes_alt:
            id_mes_alt = alumne["id"]
    return id_mes_alt + 1

def guardar_dades(llista):
    fitxer = open("alumnes.json", "wt")
    json.dump(llista, fitxer)
    fitxer.close()
    print("Dades guardades correctament!")

def mostrar_llistat(llista):
    print("\n--- LLISTAT D'ALUMNES ---")
    for alumne in llista:
        print("ID:", alumne["id"], "|", alumne["nom"], alumne["cognom"])

def afegir_alumne(llista, seguent_id):
    print("\n--- AFEGIR ALUMNE ---")
    nom = input("Nom: ")
    cognom = input("Cognom: ")
    curs = input("Curs: ")

    alumne_nou = {
        "id": seguent_id,
        "nom": nom,
        "cognom": cognom,
        "curs": curs
    }

    llista.append(alumne_nou)
    print("Alumne afegit amb ID", seguent_id)

    return seguent_id + 1

# ---------------------
# Programa principal
# ---------------------
llista_alumnes = carregar_dades()
seguent_id = obtenir_seguent_id(llista_alumnes)

while True:
    print("\nMENÚ PRINCIPAL")
    print("1. Mostrar alumnes")
    print("2. Afegir alumne")
    print("3. Guardar dades")
    print("4. Carregar dades")
    print("0. Sortir")

    opcio = input("Opció: ")

    if opcio == "1":
        mostrar_llistat(llista_alumnes)
    elif opcio == "2":
        seguent_id = afegir_alumne(llista_alumnes, seguent_id)
    elif opcio == "3":
        guardar_dades(llista_alumnes)
    elif opcio == "4":
        llista_alumnes = carregar_dades()
        seguent_id = obtenir_seguent_id(llista_alumnes)
    elif opcio == "0":
        print("Fins aviat!")
        break
    else:
        print("Opció no vàlida.")
