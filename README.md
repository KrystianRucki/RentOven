## Aplikacja webowa do obsługi zleceń wypału ceramiki

### Problem biznesowy i zakres:

Mała pracownia ceramiczna świadcząca usługę wypału przyjmuje zlecenia od wielu klientów. Przy obsłudze przez telefon, e-mail, wiadomości i arkusz trudno szybko ustalić, jakie zlecenia należą do konkretnego klienta, które są w realizacji, ile kosztują i czy są już gotowe do odbioru.

### Cel produktu:

Stworzyć aplikację webową, w której klient zakłada konto, loguje się, tworzy zlecenia wypału i śledzi ich status, a pracownik pracowni obsługuje te zlecenia w jednym panelu.

### MVP

- Klient rejestruje konto i loguje się do aplikacji.

- Zalogowany klient tworzy zlecenie wypału.

- Klient ma panel „Moje zlecenia” i widzi tylko własne zlecenia.

- Pracownik loguje się do panelu pracowni i widzi wszystkie zlecenia.

- Pracownik otwiera zlecenie, uzupełnia wagę i cenę oraz zmienia status.

- Klient widzi aktualny status, wagę i cenę w szczegółach swojego zlecenia.

### Nasze DoD:

Story jest Done dopiero wtedy, gdy spełnia kryteria akceptacji, działa w aplikacji, ma adekwatne testy, kod jest w repozytorium, Pull Request został przejrzany i scalony do main, zadanie jest zamknięte w Jirze i funkcję da się pokazać na Sprint Review.

### Zespół i role:

- Product Owner - Krystian Rucki

- Scrum Master - Seweryn Satro

- Developer - Szymon Ptasznik

### Running locally

Requirements: Python 3.12+ and Git.

```bash
git clone https://github.com/KrystianRucki/RentOven.git
cd RentOven
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The app is available at http://127.0.0.1:8000/. The database is a local SQLite file (`db.sqlite3`, not committed).

Run tests:

```bash
python manage.py test
```

Optional environment variables: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG` (`1`/`0`), `DJANGO_ALLOWED_HOSTS` (comma separated).
