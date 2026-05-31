# [IOP]

Aplikacja na pozór OLX, wystawianie, sprzedawanie oraz kupowanie przedmiotów wystawionych przez innych użytkowników.

## 🛠 Wymagania wstępne

Aby uruchomić ten projekt lokalnie, upewnij się, że masz zainstalowane:
* **Python** (wersja między 3.12 a 3.13)
* **Git**

## 🚀 Szybki start (Instalacja i uruchomienie)

Postępuj zgodnie z poniższymi instrukcjami, aby uruchomić aplikację na swoim komputerze.

### 1. Pobierz repozytorium
Stwórz pusty folder i  otwórz na nim bash gita a następnie po koleji:
- git clone https://github.com/KacperZa/IOP
- cd IOP

### 2. Utwórz środowisko wirtualne (venv)
Teraz tworzymy venva, wewnątrz folderu z projektem (IOP):
- python -m venv venv
I aktywujemy:
- .\venv\Scripts\Activate.ps1

### 3. Instajacja wymaganych bibliotek w środowisku venv
W folderze IOP:
- pip install -r requirements.txt

### 4. Dodanie pliku z kluczem do bazy danych
Przechodzimy do folderu projektowego (IOP -> iop)
- cd iop
Następnie wrzucamy tam plik .env (klucze baz danych, plik powinien być w posiadaniu osoby załączającej program)

### 5. Uruchomienie projektu
W folderze iop aktywujemy projekt: 
- Python manage.py runserver
