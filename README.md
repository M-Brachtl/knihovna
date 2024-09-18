# Knihovní systém

Tento program implementuje jednoduchý knihovní systém v Pythonu. Umožňuje uživatelům přihlašovat se, půjčovat si knihy, vracet je a prohlížet dostupné tituly.

## Funkce

- Přihlášení uživatele
- Registrace nového uživatele
- Administrátorský přístup
- Půjčování knih
- Vracení knih
- Prohlížení dostupných knih
- Filtrování knih podle autora nebo názvu
- Rušení uživatelského účtu
- Správa knih (pouze pro administrátora)

## Použití

1. Spusťte program.
2. Vyberte jednu z možností:
   - Přihlášení
   - Založení nového účtu
   - Přístup administrátor
3. Po přihlášení můžete:
   - Půjčit si knihu
   - Vrátit knihu
   - Prohlížet dostupné knihy
   - Zrušit účet
   - Ukončit program
4. Administrátor má dodatečné možnosti:
   - Přidávat/odebírat knihy z knihovny

## Struktura JSON souborů

### users.json
```json
[
  {
    "name": "jméno_uživatele",
    "password": "heslo",
    "borrowed": ["ISBN1", "ISBN2"]
  }
]
```

### books.json
```json
{
  "ISBN": {
    "title": "název_knihy",
    "author": "autor",
    "in_library": počet_kusů
  }
}
```

### borrows.json
```json
[
  {
    "user": "id_uživatele",
    "book": "ISBN",
    "date": "YYYY-MM-DD"
  }
]
```
