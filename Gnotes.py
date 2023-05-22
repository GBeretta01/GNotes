import datetime
import csv
import sqlite3
import re

conn = sqlite3.connect('GNotesBD.db')
cursor = conn.cursor()
verification = False

# Funciones

def log_in(email_is, pass_is, cursor, conn, verification):

    cursor.execute('SELECT * FROM users WHERE Email = ? AND Password = ?', (email_is, pass_is))
    user_v = cursor.fetchone()


    if user_v is not None:
        print("Iniciando sesión...")
        verification = True
    else:
        print("Usuario o contraseñas erróneas")
        verification = False

    return verification

def register(cursor, conn):
    print("---REGISTRO---")
    email = input("Ingrese su email: ")
    cursor.execute('SELECT * FROM users WHERE Email = ?', (email,))
    user = cursor.fetchone()

    if user is not None:
        print("Ya existe ese correo. Verifique los datos...")
    else:
        password = input("Ingrese su contraseña: ")
        username = input("Ingrese su nombre de usuario: ")
        phone = input("Ingrese su número de teléfono empezando por el código: ")

        cursor.execute('INSERT INTO users (Email, Username, Password, Phone) VALUES (?, ?, ?, ?)', (email, username, password, phone))

        # Crear la tabla correspondiente al usuario registrado
        table_name = format_table_name(email)
        cursor.execute(f'CREATE TABLE {table_name} (Id INTEGER PRIMARY KEY, title TEXT, content TEXT, "Date" DATE)')
        conn.commit()

        print("Usuario registrado exitosamente.")

def menu():
    print("/// MENU ///")
    print("1- Crear nota")
    print("2- Ver Notas")
    print("3- Editar nota")
    print("4- Borrar Nota")
    print("5- Cerrar sesión")

def new_note():
    title_note = input("Título de la nota: ")
    content_note = input("Nota: ")
    date_now = datetime.datetime.now().date()
    return title_note, content_note, date_now

def save_note(title_note, content_note, date_now, conn, cursor):
    
    cursor.execute("INSERT INTO notes (title, content, date) VALUES (?, ?, ?)", (title_note, content_note, str(date_now)))
    
    conn.commit()

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

def edit_notes():
    print("x- volver")
    opc = input("Elija una opción a editar: ")

    with open("notas.csv", "r") as doc:
        reader_notes = csv.reader(doc)
        lines = list(reader_notes)

    if opc.lower() == "x":
        return

    try:
        if int(opc) < 1 or int(opc) > len(lines):
            print("Escoja una opción válida...")
            return

        note_to_edit = lines[int(opc) - 1]
        actual_title = note_to_edit[0]
        actual_content = note_to_edit[1]

        print("---EDITANDO NOTA---")
        print(f"Título actual: {actual_title}")
        print(f"Contenido actual: {actual_content}")

        new_title = input(f"Nuevo título [{actual_title}]: ")
        new_content = input(f"Nuevo contenido [{actual_content}]: ")

        if not new_title:
            new_title = actual_title
        if not new_content:
            new_content = actual_content

        note_to_edit[0] = new_title
        note_to_edit[1] = new_content

        with open("notas.csv", "w", newline="") as doc:
            writer = csv.writer(doc)
            writer.writerows(lines)

        print("Se guardó con éxito la nota...")

    except ValueError:
        print("Ingrese una opción válida (número) o 'x' para volver.")

def format_table_name(email):
    # Reemplazar los puntos en el dominio por guiones bajos
    formatted_email = email.replace('.', '_')

    # Reemplazar el carácter '@' por un guion bajo
    formatted_email = formatted_email.replace('@', '_')

    # Extraer el nombre de usuario del correo electrónico
    match = re.match(r'([^@]+)@[^@]+\.[^@]+', formatted_email)
    if match:
        username = match.group(1)
    else:
        # Si no se encuentra una coincidencia, usar el correo electrónico completo como nombre de usuario
        username = formatted_email

    # Formar el nombre de la tabla con el prefijo "Notes_" y el nombre de usuario
    table_name = f'Notes_{username}'

    return table_name

# Programa principal


while True:
    print("///GNOTES///")
    print("1- Iniciar sesión")
    print("2- Registrarse")
    print("3- Salir")
    opc_m = input("Ingrese una opción: ")

    if opc_m == '1':
        print("---INCIAR SESIÓN---")
        email_is = input("Ingrese su email: ")
        pass_is = input("Ingrese su contraseña: ")

        verification = log_in(email_is, pass_is, cursor, conn, verification)

        if verification:
            while True:
                menu()
                answ = input("\nElija una opción: ")

                if answ == "1":
                    title_note, content_note, date_now = new_note()
                    save_note(title_note, content_note, date_now, conn, cursor)
                    input("Presione [ENTER] para continuar...")
                elif answ == "2":
                    read_notes()
                    show_note()
                    input("Presione [ENTER] para continuar...")
                elif answ == "3":
                    read_notes()
                    edit_notes()
                    input("Presione [ENTER] para continuar...")
                elif answ == "4":
                    read_notes()
                    delete_note()
                    input("Presione [ENTER] para continuar...")
                elif answ == "5":
                    print("Cerrando sesión...")
                    break
                else:
                    print("Agregue una opción válida...")
                    input("Presione [ENTER] para continuar...")

    elif opc_m == '2':
        register(cursor, conn)
    elif opc_m == '3':
        break
    else:
        print("Ingrese una opción válida")
        input("Presione ENTER para continuar...")
