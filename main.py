users = [
    None,
    { # users get IDs automatically by index in the list
        "name": "Skvělý Uživatel",
        "password": "heslo1234",
        "borrowed": ["978-80-85988-32-3"] # isbn
    }
]

books = { # keys are ISBN
    "978-80-85988-32-3": {
        "title": "Válka s Mloky",
        "author": "Karel Čapek",
        "in_library": 5
    },
    "978-80-85988-32-4": {
        "title": "R.U.R.",
        "author": "Karel Čapek",
        "in_library": 4
    }
}

borrows = [
    {
        "user": "0",
        "book": "978-80-85988-32-3",
        "date": "2021-06-01"
    }
]

now_user = None # current user
id_user = None # id of current user

def login():
    name = input("Napiš své jméno: ")
    password = input("Zadej heslo: ")
    for user_id, user in enumerate(users):
        if user["name"] == name:
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
    user = {
        "name": name,
        "password": password,
        "borrowed": []
    }
    if None in users:
        users[users.index(None)] = user
    else:
        users.append(user)
    return user

command = 0
while not command in (1,2):
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

#############
print((id_user,now_user),"\n\n")
print(users)

