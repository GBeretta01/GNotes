import datetime
import csv

# Funciones

def menu():
    print("/// MENU ///")
    print("1- Crear nota")
    print("2- Ver Notas")
    print("3- Editar nota")
    print("4- Borrar Nota")

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

    print("x- Volver")
    opc = input("Elija el nº de la nota a mostrar: ")

    with open("notas.csv", "r") as doc:
        read_csv = csv.reader(doc)
        linea = list(read_csv)

        if opc.lower() == "x":
            return
        
        try:
            if int(opc)<1 or int(opc)>len(linea):
                print("Seleccione una opción válida.")
                return
            
            linea_chose = linea[int(opc)-1]
            title = linea_chose [0]
            content = linea_chose[1]
            date = linea_chose[2]

            print(f"Título: {title}")
            print(f"Nota: {content}")
            print(f"Fecha de creación: {date}")
        
        except ValueError:
            print("Ingrese una opción válida (número) o 'x' para volver.")

def delete_note():

    print("X- Volver")
    opc = input("Elije una opción a borrar: ")


    lines = []
    with open("notas.csv", "r") as doc:
        reader_notes = csv.reader(doc)
        lines = list(reader_notes)

    if opc.lower() == "x":
        return
    
    try:

        if int(opc)<1 or int(opc)>len(lines):
            print("Escoja una opción válida...")
            return
        
        lines.pop(int(opc) - 1)

        with open("notas.csv", "w", newline="") as doc_w:
            rewriter_csv = csv.writer(doc_w)
            rewriter_csv.writerows(lines)

    except ValueError:
        print("Ingrese una opción válida (número) o 'x' para volver.") 


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
        show_note()
        input("Presione [ENTER] para continuar...")
    elif answ == "3":
        print("In progress...")
        input("Presione [ENTER] para continuar...")
    elif answ == "4":
        read_notes()
        delete_note()
        input("Presione [ENTER] para continuar...")
    else:
        print("Agregue una opción válida...")
        input("Presione [ENTER] para continuar...")