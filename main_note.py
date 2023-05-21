import datetime
import csv

# Funciones

def menu():
    print("/// MENU ///")
    print("1- Crear nota")
    print("2- Ver Notas")
    print("3- Borrar Nota")
    print("4- Ver nota")

def new_note():
    title_note = input("Título de la nota: ")
    content_note = input("Nota: ")
    date_now = datetime.datetime.now().date()
    return title_note, content_note, date_now

def save_note(title_note, content_note, date_now):
    with open("notas.csv", "a", newline="") as doc:
        write_csv = csv.writer(doc)
        write_csv.writerow([title_note, content_note, str(date_now)])

    print("Guardando nota...")

def read_notes():

    with open("notas.csv", "r") as doc:
        read_csv = csv.reader(doc)
        i=0
        for notes in read_csv:
            i+=1
            title = notes[0]
            print(f"{i}- {title}")

def show_note():

    opc = input("Elija el nº de la nota a mostrar: ")

    with open("notas.csv", "r") as doc:
        read_csv = csv.reader(doc)

        for notes in read_csv:


# Programa principal

while True:
    menu()
    answ = input("\nElija una opción: ")

    if answ == "1":
        title_note, content_note, date_now = new_note()
        save_note(title_note, content_note, date_now)
        input("Presione [ENTER] para continuar...")
    elif answ == "2":
        read_notes()
        input("Presione [ENTER] para continuar...")
    elif answ == "3":
        print("In progress...")
        input("Presione [ENTER] para continuar...")
    elif answ == "4":
        print("In progress...")
        input("Presione [ENTER] para continuar...")
    else:
        print("Agregue una opción válida...")
        input("Presione [ENTER] para continuar...")