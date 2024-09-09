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


command = 0
while not command in (1, 2):
    command = int(input("Vítejte v knihovně. [1 - přihlásit se, 2 - založit účet] "))
    if command == 1:
        try:
            id_user, now_user = login()
        except ValueError as error_message:
            command = 0
            print(error_message)
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
while not command in (1,2,3,4):
    command = int(input("Možné akce? [1 - Zapůjčit knihu, 2 - Vrátit knihu, 3 - Prohlédnout si výběr knih, 4 - Ukončit program, 5 - Zrušit účet] "))
    if command == 1:
        print("Dostupné knihy:")
        available_books = []
        for isbn, book in books.items():
            if isbn in now_user["borrowed"] or not book["in_library"]:
                continue
            print(f"\t{book['title']} - ({isbn})")
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
        command = 0