from json import load as jload, dump as jdump
from datetime import datetime as dt

users = jload(open("users.json", encoding="utf-8"))
books = jload(open("books.json", encoding="utf-8"))

borrows = [{"user": "0", "book": "978-80-85988-32-3", "date": "2021-06-01"}]

now_user = None  # current user
id_user = None  # id of current user

def login():
    name = input("Napiš své jméno: ")
    password = input("Zadej heslo: ")
    for user_id, user in enumerate(users):
        if user == None:
            pass
        elif user["name"] == name:
            if user["password"] == password:
                return (user_id, user)
            else:
                raise ValueError("Špatné heslo")
    raise ValueError("Žádný takový uživatel neexistuje")


def new_user():
    name = input("Napište své jméno: ")
    for user in users:
        if user == None:
            pass
        elif user["name"] == name:
            raise ValueError("Uživatel s takovým jménem již existuje")
    password = input("Napište zvolené heslo: ")
    if password != input("Zopakujte heslo: "):
        raise ValueError("Hesla nesouhlasí")
    user = {"name": name, "password": password, "borrowed": []}
    if None in users:
        users[users.index(None)] = user
    else:
        users.append(user)
    jdump(users, open("users.json", "w", encoding='utf-8'))
    return user

admin = False
command = 0
while not command in (1,2,3):
    command = int(input("Vítejte v knihovně. [1 - přihlásit se, 2 - založit účet, 3 - admin] "))
    if command == 1:
        try:
            id_user, now_user = login()
        except ValueError as error_message:
            command = 0
            print(error_message)
    elif command == 3:
        if input("Zadej vstupní kód administrátora: ") == "VelkyBratr1984GO":
            print("Seznam uživatelů: ")
            for users_id, users_data in enumerate(users):
                print("\t"+str(users_id)+" "+users_data["name"])
            while id_user == None:
                try:
                    id_user = int(input("Zadej ID uživatele, kterého chceš ovládat: "))
                    now_user = users[id_user]
                except ValueError:
                    id_user = None
                    print("Neplatné ID")
                except IndexError:
                    id_user = None
                    print("Neplatné ID")
            admin = True
        else:
            command = 0
    else:
        try:
            now_user = new_user()
            id_user = users.index(now_user)
        except ValueError as error_message:
            command = 0
            print(error_message)
print("\nJste přihlášen jako:", now_user["name"], "\n")
print("Zapůjčené knihy:")
for book in now_user["borrowed"]:
    print(books[book]["title"],end="\n\n")
if len(now_user["borrowed"]) == 0:
    print("\n")

# akce uživatele
command = 0
if admin: print("JSI V REŽIMU ADMINISTRÁTORA")
while not command in (1,2,3,4,5,6):
    try:
        if admin:
            command = int(input("Vyber akci [1 - Zapůjčit knihu, 2 - Vrátit knihu, 3 - Prohlédnout si výběr knih, 4 - Ukončit program, 5 - Zrušit účet, 6 - přidat/odebrat knihy v knihovně] "))
        else:
            command = int(input("Vyber akci [1 - Zapůjčit knihu, 2 - Vrátit knihu, 3 - Prohlédnout si výběr knih, 4 - Ukončit program, 5 - Zrušit účet] "))
    except ValueError:
        command = 0
    if command == 1:
        print("Dostupné knihy:")
        available_books = []
        if input("Chcete zobrazit všechny knihy? [ano/ne] ") == "ano": book_show = True
        for isbn, book in books.items():
            if isbn in now_user["borrowed"] or not book["in_library"]:
                continue
            if book_show: print(f"\t{book['title']} - ({isbn})")
            available_books.append(isbn)
        my_isbn = input("Zadej ISBN knihy, kterou chceš zapůjčit: ")
        if my_isbn in available_books:
            borrows.append({"user": str(id_user), "book": my_isbn, "date": dt.now().strftime("%Y-%m-%d")})
            now_user["borrowed"].append(my_isbn)
            books[my_isbn]["in_library"] -= 1
            jdump(books,open("books.json","w",encoding="utf-8"))
            jdump(borrows,open("borrows.json","w"))
            jdump(users,open("users.json","w",encoding="utf-8"))
            print(f"Kniha {books[my_isbn]['title']} byla zapůjčena")
        else:
            print("Toto není validní ISBN")
        print("")
        command = 0
    elif command == 2:
        print("Vámi zapůjčené knihy:")
        for book in now_user["borrowed"]:
            print(f"\t{books[book]['title']} - ({book})")
        my_isbn = input("Zadej ISBN knihy, kterou chceš vrátit: ")
        if my_isbn in now_user["borrowed"]:
            for item in borrows:
                if item["book"] == my_isbn and item["user"] == id_user:
                    borrows.remove(item)
                    break
            now_user["borrowed"].remove(my_isbn)
            books[my_isbn]["in_library"] += 1
            jdump(books,open("books.json","w",encoding="utf-8"))
            jdump(borrows,open("borrows.json","w"))
            jdump(users,open("users.json","w",encoding="utf-8"))
            print(f"Kniha {books[my_isbn]['title']} byla vrácena")
        else:
            print("Toto není validní ISBN")
        print("")
        command = 0
    elif command == 3:
        autor_q = input("Chcete filtrovat podle autora (1) nebo titulu (2)? ")
        if autor_q == "1":
            author = input("Zadej jméno autora nebo jeho část: ")
            for isbn, book in books.items():
                if author in book["author"]:
                    print(f"\t{book['title']}, {book['author']} - ({isbn})")
        else:
            title = input("Zadej titul knihy nebo jeho část: ")
            for isbn, book in books.items():
                if title in book["title"]:
                    print(f"\t{book['title']}, {book['author']} - ({isbn})")
        print("")
        command = 0
    elif command == 5:
        if now_user["borrowed"] != []:
            print("Nejdříve musíte vrátit všechny knihy")
        elif input("Opravdu chcete zrušit účet? [ano/ne] ") == "ano":
            if admin or (input("Zadejte své jméno: ") == now_user["name"] and input("Zadejte heslo: ") == now_user["password"]):
                users[id_user] = None
                jdump(users,open("users.json","w",encoding="utf-8"))
                print("Váš účet byl zrušen")
            else:
                print("Špatné jméno nebo heslo")
    elif command == 6:
        isbn = input("Zadej ISBN existující nebo nové knihy: ")
        try:
            change = int(input(f"Zadej počet kusů knihy {books[isbn]}, které chceš přidat (pro odebrání napiš záporné číslo): "))
            if books[isbn]["in_library"] + change < 0:
                print("Nelze odebrat více knih, než je v knihovně")
            else:
                books[isbn]["in_library"] += change
            if books[isbn]["in_library"] == 0 and input("Chceš knihu zcela odebrat ze seznamu? [ano/ne] ") == "ano":
                in_borrows = False
                for item in borrows:
                    if item["book"] == isbn:
                        in_borrows = True
                        break
                if in_borrows:
                    print("Tuto knihu má někdo zapůjčenou, nelze ji smazat")
                else:
                    del books[isbn]
                    jdump(books,open("books.json","w",encoding="utf-8"))
                    print("Kniha byla smazána")
            else:
                jdump(books,open("books.json","w",encoding="utf-8"))
                print(f"Počet kusů knihy {books[isbn]['title']} byl změněn")
        except KeyError:
            title = input("Zadej název knihy: ")
            author = input("Zadej autora knihy: ")
            in_library = int(input("Zadej počet kusů knihy: "))
            books[isbn] = {"title": title, "author": author, "in_library": in_library}
            jdump(books,open("books.json","w",encoding="utf-8"))
            print("Kniha byla přidána")
        print("")
        command = 0