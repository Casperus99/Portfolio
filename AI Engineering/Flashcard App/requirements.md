# Założenia Aplikacji Fiszki SRS

## 1. Wprowadzenie

### 1.1. Cel aplikacji

Aplikacja "Fiszki SRS" ma być stworzona w celu ułatwienia nauki i utrwalania wiedzy z dowolnej dziedziny. Wykorzystuje ona metodę powtórek interwałowych (Spaced Repetition System - SRS), która optymalizuje proces zapamiętywania poprzez dostosowywanie częstotliwości powtórek pytań w zależności od stopnia ich znajomości przez użytkownika.

### 1.2. Główne funkcjonalności

*   **Interaktywny quiz:** Prezentowanie pytań otwartych, które są sprawdzane poprzez model AI. Pytania otwarte są sprawdzane przez model AI, który ocenia odpowiedzi pod kątem dopasowania semantycznego oraz obecności kluczowych słów.
*   **System Powtórek Interwałowych (SRS):** Dynamiczne dostosowywanie, kiedy dane pytanie powinno pojawić się ponownie, w oparciu o historię odpowiedzi i aktualny poziom znajomości.
*   **Śledzenie postępów:**
    *   Indywidualny poziom znajomości dla każdego pytania (domyślnie od 0 do 6, konfigurowalny).
    *   Zapis daty ostatniej odpowiedzi na każde pytanie.
    *   Wyświetlanie sumarycznego stanu wiedzy (rozkład pytań wg poziomów).
    *   Informowanie o liczbie pytań dostępnych do powtórki w danym dniu.
*   **Zarządzanie bazą pytań:** Przechowywanie pytań, odpowiedzi, poprawnych odpowiedzi, poziomu znajomości i daty ostatniej odpowiedzi w pliku JSON.
*   **Trwałość danych:** Zapisywanie postępów użytkownika odbywa się po każdej udzielonej odpowiedzi, co minimalizuje ryzyko utraty danych. Sesja nauki trwa od uruchomienia do wyłączenia aplikacji.
*   **Prosty interfejs użytkownika:** Obsługa za pomocą klawiatury w terminalu.

### 1.3. Technologie

*   **Język programowania:** Python 3
*   **Integracja z AI:** Model Google Gemini (z możliwością łatwej zmiany dostawcy w przyszłości).

### 1.4. Struktura projektu

Wstępna struktura prezentuje się następująco:

*   main.py - tylko uruchomienie aplikacji
*   src/ - folder ze wszystkimi plikami źródłowymi
*   config/ - folder z konfiguracją
*   flashcards/ - folder zawierający fiszki. Powinien on składać się docelowo z kilku podfolderów np. "Zdrowie", które to dopiero zawierałyby różne pliki JSON takie jak "owoce.json" lub "warzyce.json".
    *   Aplikacja domyślnie wczytuje wszystkie pliki JSON ze wszystkich podfolderów rekurencyjnie. Mechanizm ładowania danych jest zaprojektowany tak, aby umożliwić łatwą modyfikację w przyszłości (np. wybór konkretnych kategorii).

## 2. Instalacja i Uruchomienie

### 2.1. Wymagania

*   Python w wersji 3.x.

### 2.2. Struktura pliku JSON z pytaniami

Plik JSON jest listą obiektów JSON, gdzie każdy obiekt reprezentuje jedno pytanie. Struktura pojedynczego obiektu pytania jest następująca:

```json
{
  "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "front": "Kiedy urodził się Elthon John?",
  "back": "25 marca 1947r",
  "mastery_level": 3,
  "last_answer_date": "2025-03-25"
}
```

*   **`id`**: Unikalny identyfikator pytania, generowany jako UUID, jeśli brakuje go w pliku.
*   **`front`**: String zawierający treść pytania.
*   **`back`**: String, który zawiera odpowiedź na pytanie.
*   **`mastery_level`**: Liczba całkowita reprezentująca aktualny poziom opanowania pytania przez użytkownika.
*   **`last_answer_date`**: String z datą ostatniej odpowiedzi w formacie "YYYY-MM-DD" lub `null`, jeśli na pytanie nigdy nie odpowiadano.

## 3. Podręcznik Użytkownika

### 3.1. Interfejs główny

Po uruchomieniu aplikacji, użytkownikowi prezentowany jest interfejs w terminalu, który zawiera:

*   **Statystyki sesji:**
    *   `Dostępnych pytań w tym dniu: X` - liczba pytań, które zgodnie z logiką SRS są przewidziane do powtórki dzisiaj.
    *   `Ogólny stan wiedzy (poziomy X-Y): A|B|C|D|E|F|G` - rozkład wszystkich pytań w bazie danych według poziomów znajomości (np. `12|43|0|15|1|0|5` oznacza 12 pytań na poziomie 0, 43 na poziomie 1 itd., aż do maksymalnego poziomu).
*   **Aktualne pytanie:**
    *   `Pytanie (ID: X, Poziom: Y): Treść pytania...` - wyświetla ID pytania, jego aktualny poziom znajomości oraz treść.
*   **Miejsce na odpowiedź** - Nie ma w tym wypadku specjalnego tekstu.

### 3.2. Nawigacja i interakcja

*   **Odpowiadanie na pytania:** Użytkownik wpisuje swoją odpowiedź jako tekst.
*   **Wyjście z aplikacji:** Klawisz `*` (gwiazdka) w dowolnym momencie wprowadzania odpowiedzi.
*   **Po udzieleniu poprawnej odpowiedzi:** Ekran jest odświeżany i aplikacja automatycznie przechodzi do następnego pytania.
*   **Po udzieleniu błędnej odpowiedzi:**
    *   Ekran jest odświeżany, wyświetlane są ponownie statystyki, pytanie i opcje (z zaznaczoną błędną odpowiedzią użytkownika). Obecnie nie przewiduje się mechanizmu nadpisywania decyzji AI przez użytkownika.
    *   Pojawia się informacja `Twoja odpowiedź: ... - ŹLE.`
    *   Wyświetlana jest `Poprawna odpowiedź: ...`
    *   Aplikacja oczekuje na naciśnięcie **dowolnego klawisza** przez użytkownika, aby przejść do następnego pytania (lub klawisza `*` aby wyjść).
*   **Odświeżanie Ekranu:** Odświeżanie ekranu oznacza czyszczenie terminala przed wyświetleniem nowej treści.

### 3.3. System powtórek (SRS)
Aplikacja wykorzystuje system powtórek interwałowych, aby zoptymalizować naukę. Każde pytanie ma przypisany `mastery_level`. Na podstawie tego poziomu oraz daty ostatniej odpowiedzi, system decyduje, kiedy pytanie powinno pojawić się ponownie. Domyślne interwały (konfigurowane w plikach konfiguracyjnych) są następujące:

| Poziom Znajomości | Minimalny Odstęp do Następnej Powtórki |
|--------------------|----------------------------------------|
| 0                  | Tego samego dnia                       |
| 1                  | 1 dzień                                |
| 2                  | 2 dni                                  |
| 3                  | 4 dni                                  |
| 4                  | 7 dni                                  |
| 5                  | 12 dni                                 |
| 6                  | 20 dni                                 |

Po każdej odpowiedzi:

*   Jeśli odpowiedź jest poprawna, `mastery_level` pytania wzrasta o 1 (do maksymalnego zdefiniowanego poziomu).
*   Jeśli odpowiedź jest błędna, `mastery_level` pytania maleje o 1 (do minimalnego zdefiniowanego poziomu, tj. 0).
*   Zapisywana jest aktualna data jako `last_answer_date`.
Pytania z poziomem znajomości 0 mogą pojawić się ponownie w tej samej sesji nauki, losowo, niekoniecznie od razu po błędnej odpowiedzi (chyba że nie ma już innych pytań do powtórki). Nie ma limitu powtórek dla pytań na poziomie 0 w jednej sesji.

### 3.4. Komunikaty i feedback
*   **`Gratulacje! Na dziś nie ma więcej pytań do powtórki.`**: Pojawia się, gdy wszystkie pytania przewidziane przez SRS na dany dzień zostały zadane lub gdy na starcie nie było dostępnych pytań.
*   **`Koniec pytań w tym dniu (...) Postępy zostały zapisane.`**: Pojawia się po zakończeniu sesji, w której odpowiedziano na wszystkie dostępne pytania.
*   **`Zapisano postępy. Do zobaczenia!`**: Pojawia się po wyjściu z aplikacji za pomocą klawisza '*'.

## 4. Architektura Systemu (Opis Techniczny)

### 4.1. Format danych (JSON)

Szczegółowy opis formatu pliku JSON znajduje się w sekcji [2.2. Struktura pliku JSON z pytaniami](#22-struktura-pliku-json-z-pytaniami).

### 4.2. Zarządzanie Danymi i Błędy

*   **Obsługa Błędów w Plikach JSON:** W przypadku wykrycia niekompletnych lub błędnych danych w plikach JSON (np. brakujące pola `front`, `back`, niepoprawny format daty, `mastery_level` poza zakresem), aplikacja zgłosi błąd i zakończy działanie. Zachowanie to jest łatwe do zmiany w przyszłości.

### 4.3. Konfiguracja Aplikacji

*   Aplikacja będzie wykorzystywać pliki konfiguracyjne w formacie JSON. Kluczowe parametry konfiguracyjne obejmują: interwały powtórek SRS, zakres poziomów opanowania, klucz API dla Google Gemini oraz nazwę modelu AI (np. `gemini-1.5-flash`).

### 4.4. Logowanie

*   Aplikacja wykorzystuje moduł `logging` do rejestrowania zdarzeń. Logi są domyślnie wyświetlane na konsoli. Domyślny poziom logowania to `INFO`, jednak poziomy są dostosowywane do ważności wiadomości. Format logowania zawiera datę, czas, poziom logowania oraz treść wiadomości.

*Kod aplikacji przestrzega standardów PEP 8 dla języka Python.*