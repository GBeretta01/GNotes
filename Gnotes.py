import datetime
import csv
import sqlite3
import re

conn = sqlite3.connect('GNotesBD.db')
cursor = conn.cursor()

# Funciones

def log_in(email_is, pass_is, cursor):

    cursor.execute('SELECT * FROM users WHERE Email = ? AND Password = ?', (email_is, pass_is))
    user_v = cursor.fetchone()


    if user_v is not None and user_v[3] == pass_is:
        print("Iniciando sesión...")
        return True
    else:
        print("Usuario o contraseñas erróneas")
        return False

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

        table_name = format_table_name(email)
        cursor.execute(f'CREATE TABLE {table_name} (Id INTEGER PRIMARY KEY, Title TEXT, Content TEXT, "Date" DATE)')
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

    
    table_name = format_table_name_log_in(email_is)
    cursor.execute(f"INSERT INTO {table_name} (title, content, date) VALUES (?, ?, ?)", (title_note, content_note, str(date_now)))
    
    conn.commit()

    print("Guardando nota...")

def read_notes(cursor):

    table_name = format_table_name_log_in(email_is)
    cursor.execute(f"SELECT title FROM {table_name}")
    rows = cursor.fetchall()

    for i, row in enumerate(rows, start=1):
        title = row[0]
        print(f"{i}- {title}")

def show_note(cursor):

    print("x- Volver")
    opc = input("Elija el nº de la nota a mostrar: ")

    table_name = format_table_name_log_in(email_is)
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    for i, row in enumerate(rows, start=1):
        title = row[1]
        print(f"{i}- {title}")

    if opc.lower() == "x":
        return
    
    try:
        chosen_index = int(opc) - 1

        if chosen_index < 0 or chosen_index >= len(rows):
            print("Seleccione una opción válida.")
            return

        chosen_note = rows[chosen_index]
        title = chosen_note[1]
        content = chosen_note[2]
        date = chosen_note[3]

        print(f"Título: {title}")
        print(f"Nota: {content}")
        print(f"Fecha de creación: {date}")
        
    except ValueError:
        print("Ingrese una opción válida (número) o 'x' para volver.")

def delete_note(cursor, conn):

    print("X- Volver")
    opc = input("Elije una nota a borrar: ")

    table_name = format_table_name_log_in(email_is)
    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchall()

    if opc.lower() == "x":
        return
    
    try:
        chosen_index = int(opc) - 1

        if chosen_index < 0 or chosen_index >= len(rows):
            print("Seleccione una opción válida.")
            return

        cursor.execute(f'DELETE FROM {table_name} WHERE id = {chosen_index}')
        conn.commit()
        
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
    
    formatted_email = email.replace('.', '_')

    formatted_email = formatted_email.replace('@', '_')

    match = re.match(r'([^@]+)@[^@]+\.[^@]+', formatted_email)
    if match:
        username = match.group(1)
    else:
        username = formatted_email

    table_name = f'Notes_{username}'

    return table_name

def format_table_name_log_in(email_is):

    formatted_email = email_is.replace('.', '_')

    formatted_email = formatted_email.replace('@', '_')

    match = re.match(r'([^@]+)@[^@]+\.[^@]+', formatted_email)
    if match:
        username = match.group(1)
    else:
        username = formatted_email

    table_name_log_in = f'Notes_{username}'

    return table_name_log_in


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

        verification = log_in(email_is, pass_is, cursor)

        if verification:
            while True:
                table_name_log_in = format_table_name_log_in(email_is)
                menu()
                answ = input("\nElija una opción: ")

                if answ == "1":
                    title_note, content_note, date_now = new_note()
                    save_note(title_note, content_note, date_now, conn, cursor)
                    input("Presione [ENTER] para continuar...")
                elif answ == "2":
                    read_notes(cursor)
                    show_note(cursor)
                    input("Presione [ENTER] para continuar...")
                elif answ == "3":
                    read_notes(cursor)
                    edit_notes()
                    input("Presione [ENTER] para continuar...")
                elif answ == "4":
                    read_notes(cursor)
                    delete_note(cursor, conn)
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
