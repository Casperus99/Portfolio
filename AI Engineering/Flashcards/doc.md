# Dokumentacja Aplikacji Fiszki SRS

## 1. Wprowadzenie

### 1.1. Cel aplikacji
Aplikacja "Fiszki SRS" została stworzona w celu ułatwienia nauki i utrwalania wiedzy z dowolnej dziedziny. Wykorzystuje ona metodę powtórek interwałowych (Spaced Repetition System - SRS), która optymalizuje proces zapamiętywania poprzez dostosowywanie częstotliwości powtórek pytań w zależności od stopnia ich znajomości przez użytkownika.

### 1.2. Główne funkcjonalności
*   **Interaktywny quiz:** Prezentowanie pytań wielokrotnego wyboru z trzema opcjami odpowiedzi.
*   **System Powtórek Interwałowych (SRS):** Dynamiczne dostosowywanie, kiedy dane pytanie powinno pojawić się ponownie, w oparciu o historię odpowiedzi i aktualny poziom znajomości.
*   **Śledzenie postępów:**
    *   Indywidualny poziom znajomości dla każdego pytania (domyślnie od 0 do 6, konfigurowalny).
    *   Zapis daty ostatniej odpowiedzi na każde pytanie.
    *   Wyświetlanie sumarycznego stanu wiedzy (rozkład pytań wg poziomów).
    *   Informowanie o liczbie pytań dostępnych do powtórki w danym dniu.
*   **Zarządzanie bazą pytań:** Przechowywanie pytań, odpowiedzi, poprawnych odpowiedzi, poziomu znajomości i daty ostatniej odpowiedzi w pliku JSON.
*   **Trwałość danych:** Zapisywanie postępów użytkownika po każdej sesji.
*   **Prosty interfejs użytkownika:** Obsługa za pomocą klawiatury w terminalu.

### 1.3. Technologie
*   **Język programowania:** Python 3
*   **Moduły standardowe Pythona:**
    *   `json`: Do serializacji i deserializacji danych pytań.
    *   `random`: Do losowania kolejności pytań.
    *   `os`: Do operacji systemowych (np. czyszczenie ekranu).
    *   `sys`: Do interakcji z systemem (np. `sys.exit`).
    *   `datetime` (z modułów `date`, `timedelta`, `datetime`): Do zarządzania datami i obliczania interwałów powtórek.
*   **Biblioteki zewnętrzne:**
    *   `readchar`: Do odczytywania pojedynczych znaków z klawiatury bez potrzeby wciskania Enter.

### 1.4. Struktura projektu
Aplikacja składa się z następujących głównych plików:
*   **`main.py`**: Główny plik wykonywalny aplikacji. Odpowiedzialny za inicjalizację, konfigurację stałych, tworzenie instancji klas zarządzających i uruchomienie głównej pętli quizu.
*   **`quiz_classes.py`**: Moduł zawierający definicje klas używanych w aplikacji:
    *   `Question`: Reprezentuje pojedynczą fiszkę/pytanie.
    *   `QuizSession`: Zarządza logiką sesji nauki i stanem pytań.
    *   `QuizUI`: Odpowiada za interfejs użytkownika i interakcję.
    *   `StorageManager`: Zarządza wczytywaniem i zapisywaniem danych quizu do/z pliku.
*   **`pytania_patent.json`** (lub inna nazwa pliku JSON): Plik w formacie JSON przechowujący bazę pytań, odpowiedzi, poprawnych odpowiedzi oraz metadane dotyczące postępów użytkownika (poziom znajomości, data ostatniej odpowiedzi). Nazwa pliku jest konfigurowalna w `main.py`.

## 2. Instalacja i Uruchomienie

### 2.1. Wymagania
*   Python w wersji 3.x.
*   Biblioteka `readchar`.

### 2.2. Instalacja zależności
Aby zainstalować wymaganą bibliotekę `readchar`, otwórz terminal lub wiersz poleceń i wykonaj komendę:
```bash
pip install readchar
```

### 2.3. Uruchomienie aplikacji
Aby uruchomić aplikację, przejdź w terminalu do katalogu, w którym znajdują się pliki `main.py` i `quiz_classes.py` oraz plik JSON z pytaniami (domyślnie `pytania_patent.json`), a następnie wykonaj komendę:
```bash
python main.py
```

### 2.4. Struktura pliku JSON z pytaniami
Plik JSON (np. `pytania_patent.json`) jest listą obiektów JSON, gdzie każdy obiekt reprezentuje jedno pytanie. Struktura pojedynczego obiektu pytania jest następująca:

```json
{
  "id": 0, // Unikalny identyfikator pytania (liczba całkowita, opcjonalnie generowany)
  "pytanie": "Treść pytania...",
  "odpowiedzi": [
    "Opcja odpowiedzi 1",
    "Opcja odpowiedzi 2",
    "Opcja odpowiedzi 3"
  ],
  "poprawna_odpowiedz": "Tekst poprawnej odpowiedzi (musi być identyczny z jedną z opcji)",
  "stopien_znajomosci": 3, // Liczba całkowita od MIN_ZNAJOMOSC do MAX_ZNAJOMOSC
  "data_ostatniej_odpowiedzi": "YYYY-MM-DD" // Data w formacie ROK-MIESIĄC-DZIEŃ lub null
}
```
*   **`id`**: Unikalny identyfikator pytania. Jeśli brakuje go w pliku, zostanie nadany automatycznie podczas ładowania (na podstawie indeksu).
*   **`pytanie`**: String zawierający treść pytania.
*   **`odpowiedzi`**: Lista trzech stringów, reprezentujących możliwe opcje odpowiedzi.
*   **`poprawna_odpowiedz`**: String, który musi dokładnie odpowiadać jednej z treści w liście `odpowiedzi`.
*   **`stopien_znajomosci`**: Liczba całkowita reprezentująca aktualny poziom opanowania pytania przez użytkownika. Zakres jest dynamicznie określany przez stałe `MIN_ZNAJOMOSC` i `MAX_ZNAJOMOSC` (domyślnie 0-6, konfigurowalne poprzez słownik `ODSTEPY_CZASOWE` w `main.py`).
*   **`data_ostatniej_odpowiedzi`**: String z datą ostatniej odpowiedzi w formacie "YYYY-MM-DD" lub `null`, jeśli na pytanie nigdy nie odpowiadano.

## 3. Podręcznik Użytkownika

### 3.1. Interfejs główny
Po uruchomieniu aplikacji, użytkownikowi prezentowany jest interfejs w terminalu, który zawiera:
*   Informację o możliwości wyjścia z aplikacji (`Naciśnij 'q' aby wyjść.`).
*   **Statystyki sesji:**
    *   `Dostępnych pytań w tym dniu: X` - liczba pytań, które zgodnie z logiką SRS są przewidziane do powtórki dzisiaj.
    *   `Ogólny stan wiedzy (poziomy X-Y): A|B|C|D|E|F|G` - rozkład wszystkich pytań w bazie danych według poziomów znajomości (np. `12|43|0|15|1|0|5` oznacza 12 pytań na poziomie 0, 43 na poziomie 1 itd., aż do maksymalnego poziomu).
*   **Aktualne pytanie:**
    *   `Pytanie (ID: X, Poziom: Y): Treść pytania...` - wyświetla ID pytania, jego aktualny poziom znajomości oraz treść.
*   **Opcje odpowiedzi:**
    *   `A. Opcja odpowiedzi 1`
    *   `S. Opcja odpowiedzi 2`
    *   `D. Opcja odpowiedzi 3`
*   **Zachęta do działania:** `Wybierz odpowiedź (a, s, d) lub 'q' aby wyjść:`

### 3.2. Nawigacja i interakcja
*   **Odpowiadanie na pytania:** Użytkownik wybiera odpowiedź, naciskając jeden z klawiszy:
    *   `a` - dla pierwszej opcji (A)
    *   `s` - dla drugiej opcji (S)
    *   `d` - dla trzeciej opcji (D)
    Wielkość liter nie ma znaczenia.
*   **Wyjście z aplikacji:** W dowolnym momencie (oczekiwania na wybór odpowiedzi lub na kontynuację po błędnej odpowiedzi) naciśnięcie klawisza `q` powoduje zapisanie aktualnego stanu postępów i zakończenie działania aplikacji.
*   **Po udzieleniu poprawnej odpowiedzi:** Aplikacja automatycznie przechodzi do następnego dostępnego pytania. Nie jest wyświetlany żaden dodatkowy komunikat.
*   **Po udzieleniu błędnej odpowiedzi:**
    *   Ekran jest odświeżany, wyświetlane są ponownie statystyki, pytanie i opcje (z zaznaczoną błędną odpowiedzią użytkownika).
    *   Pojawia się informacja `Twoja odpowiedź: X. ... - ŹLE.`
    *   Wyświetlana jest `Poprawna odpowiedź: Y. ...`
    *   Aplikacja oczekuje na naciśnięcie **dowolnego klawisza** przez użytkownika, aby przejść do następnego pytania (lub klawisza `q` aby wyjść).

### 3.3. System powtórek (SRS)
Aplikacja wykorzystuje system powtórek interwałowych, aby zoptymalizować naukę. Każde pytanie ma przypisany `stopien_znajomosci`. Na podstawie tego poziomu oraz daty ostatniej odpowiedzi, system decyduje, kiedy pytanie powinno pojawić się ponownie. Domyślne interwały (konfigurowalne w `main.py` poprzez słownik `ODSTEPY_CZASOWE`) są następujące:

| Poziom Znajomości | Minimalny Odstęp do Następnej Powtórki |
|--------------------|----------------------------------------|
| 0                  | Tego samego dnia                       |
| 1                  | 1 dzień                                |
| 2                  | 2 dni                                  |
| 3                  | 4 dni                                  |
| 4                  | 7 dni                                  |
| 5                  | 12 dni                                 |
| 6                  | 20 dni                                 |
*(Zakres poziomów i długości odstępów są definiowane przez słownik `ODSTEPY_CZASOWE` w pliku `main.py`)*

Po każdej odpowiedzi:
*   Jeśli odpowiedź jest poprawna, `stopien_znajomosci` pytania wzrasta o 1 (do maksymalnego zdefiniowanego poziomu).
*   Jeśli odpowiedź jest błędna, `stopien_znajomosci` pytania maleje o 1 (do minimalnego zdefiniowanego poziomu, tj. 0).
*   Zapisywana jest aktualna data jako `data_ostatniej_odpowiedzi`.
Pytania z poziomem znajomości 0 mogą pojawić się ponownie w tej samej sesji nauki.

### 3.4. Komunikaty i feedback
*   **`Gratulacje! Na dziś nie ma więcej pytań do powtórki.`**: Pojawia się, gdy wszystkie pytania przewidziane przez SRS na dany dzień zostały zadane lub gdy na starcie nie było dostępnych pytań.
*   **`Koniec pytań w tym dniu (...) Postępy zostały zapisane.`**: Pojawia się po zakończeniu sesji, w której odpowiedziano na wszystkie dostępne pytania.
*   **`Zapisano postępy. Do zobaczenia!`**: Pojawia się po wyjściu z aplikacji za pomocą klawisza 'q'.

## 4. Architektura Systemu (Opis Techniczny)

### 4.1. Moduły i klasy

#### 4.1.1. `main.py`
*   **Rola:** Główny punkt wejścia aplikacji.
*   **Odpowiedzialność:**
    *   Definiowanie i inicjalizacja globalnych stałych konfiguracyjnych (ścieżka do pliku JSON, definicja `ODSTEPY_CZASOWE`, automatyczne wyliczanie `MIN_ZNAJOMOSC`, `MAX_ZNAJOMOSC`).
    *   Przekazanie konfiguracji SRS (stałych) do klasy `Question` poprzez ustawienie jej atrybutów klasowych.
    *   Tworzenie instancji `StorageManager`.
    *   Wywołanie `storage_manager.load_all_question_objects()` w celu wczytania danych pytań i konwersji na listę obiektów `Question`.
    *   Tworzenie instancji `QuizSession` z listą obiektów `Question`.
    *   Tworzenie instancji `QuizUI` z obiektem `QuizSession`.
    *   Uruchomienie głównej pętli interakcji użytkownika poprzez `quiz_ui.run_quiz_loop()`.
    *   Po zakończeniu pętli quizu, wywołanie `storage_manager.save_all_question_objects(quiz_session.all_questions)` w celu zapisania zaktualizowanego stanu wszystkich pytań.

#### 4.1.2. `quiz_classes.py`

##### Klasa `Question`
*   **Cel i odpowiedzialność:** Reprezentuje pojedynczą fiszkę (pytanie) wraz z jej stanem (poziom znajomości, data ostatniej odpowiedzi) i logiką SRS.
*   **Atrybuty:**
    *   `id` (any): Unikalny identyfikator.
    *   `text` (str): Treść pytania.
    *   `options` (list[str]): Lista trzech opcji odpowiedzi.
    *   `correct_answer_text` (str): Tekst poprawnej odpowiedzi.
    *   `knowledge_level` (int): Aktualny poziom znajomości.
    *   `last_answered_date` (datetime.date | None): Data ostatniej odpowiedzi.
    *   **Stałe klasowe (inicjalizowane z `main.py`):**
        *   `MIN_KNOWLEDGE_LEVEL` (int).
        *   `MAX_KNOWLEDGE_LEVEL` (int).
        *   `SRS_INTERVALS` (dict).
*   **Kluczowe metody:**
    *   `__init__(...)`: Inicjalizuje atrybuty pytania, konwertuje datę ze stringa (jeśli trzeba) i waliduje `knowledge_level`.
    *   `is_due(current_date)`: Oblicza, czy pytanie jest "due" na podstawie `last_answered_date`, `knowledge_level` i `SRS_INTERVALS`.
    *   `update_knowledge_level(is_correct)`: Modyfikuje `knowledge_level` (zwiększa przy poprawnej, zmniejsza przy błędnej odpowiedzi), utrzymując go w granicach `MIN_KNOWLEDGE_LEVEL` i `MAX_KNOWLEDGE_LEVEL`.
    *   `update_last_answered_date(answered_date)`: Ustawia `last_answered_date` na podaną datę (domyślnie dzisiejszą).
    *   `to_dict()`: Konwertuje obiekt `Question` na słownik (data konwertowana na string "YYYY-MM-DD" lub `None`).
    *   `from_dict(cls, data, default_id)`: Tworzy instancję `Question` ze słownika.

##### Klasa `QuizSession`
*   **Cel i odpowiedzialność:** Zarządza całą sesją nauki.
*   **Atrybuty:**
    *   `all_questions` (list[Question]): Przechowuje wszystkie obiekty `Question`.
    *   `due_questions_indices_in_all_questions` (list[int]): Indeksy pytań z `all_questions`, które są aktualnie "due".
    *   `current_question_obj` (Question | None): Aktualnie zadane pytanie.
    *   `answered_in_session_count` (int): Liczba odpowiedzi udzielonych w sesji.
    *   `total_due_at_session_start` (int): Liczba pytań "due" na początku sesji.
*   **Kluczowe metody:**
    *   `_refresh_due_questions_indices()`: Odświeża i miesza listę indeksów pytań "due" na podstawie metody `is_due()` każdego pytania.
    *   `start_new_session()`: Resetuje liczniki i inicjalizuje listę pytań "due" na start sesji.
    *   `get_next_question()`: Odświeża listę "due" i zwraca losowo wybrane pytanie (obiekt `Question`) z tej puli. Jeśli pula jest pusta, zwraca `None`.
    *   `process_answer(was_correct)`: Wywołuje metody `update_knowledge_level()` i `update_last_answered_date()` na `current_question_obj` oraz inkrementuje `answered_in_session_count`.
    *   `has_more_questions_today()`: Sprawdza, czy po odświeżeniu puli są jeszcze pytania "due".
    *   `get_knowledge_summary_string()`: Generuje string z rozkładem pytań wg poziomów znajomości.
    *   `get_session_progress_info()`: Zwraca słownik ze statystykami sesji (m.in. aktualna liczba pytań "due").

##### Klasa `QuizUI`
*   **Cel i odpowiedzialność:** Zarządza interakcją z użytkownikiem w terminalu.
*   **Atrybuty:**
    *   `quiz_session` (QuizSession): Instancja `QuizSession`.
    *   `option_map` (dict): Mapowanie klawiszy odpowiedzi na indeksy.
    *   `option_labels` (list[str]): Etykiety opcji.
*   **Kluczowe metody:**
    *   `_clear_screen()`: Czyści ekran.
    *   `_display_session_stats()`: Wyświetla statystyki sesji (liczbę dostępnych pytań, ogólny stan wiedzy).
    *   `display_question(question_obj)`: Prezentuje pytanie i opcje.
    *   `get_user_choice()`: Pobiera wybór użytkownika (klawisz 'a', 's', 'd' lub 'q').
    *   `display_error_feedback(question_obj, user_choice_key)`: Wyświetla feedback po błędnej odpowiedzi.
    *   `run_quiz_loop()`: Główna pętla quizu: inicjuje sesję, w pętli pobiera pytania, wyświetla je, pobiera odpowiedzi, przetwarza je i wyświetla feedback (jeśli błędna odpowiedź). Kontynuuje, dopóki są dostępne pytania "due" lub użytkownik nie wyjdzie.

##### Klasa `StorageManager`
*   **Cel i odpowiedzialność:** Odpowiada za odczyt danych pytań z pliku JSON i zapis zaktualizowanych danych z powrotem do pliku.
*   **Atrybuty:**
    *   `file_path` (str): Ścieżka do pliku JSON.
*   **Kluczowe metody:**
    *   `load_all_question_objects()`: Wczytuje listę słowników z pliku JSON. Dla każdego słownika wywołuje `Question.from_dict()` aby stworzyć obiekt `Question`, dbając o inicjalizację brakujących pól (`id`, `stopien_znajomosci`, `data_ostatniej_odpowiedzi`). Zwraca listę obiektów `Question`.
    *   `save_all_question_objects(question_objects_list)`: Dla każdego obiektu `Question` z listy wywołuje jego metodę `to_dict()`, a następnie zapisuje wynikową listę słowników do pliku JSON.

### 4.2. Przepływ danych (Szczegółowy)

1.  **Inicjalizacja Aplikacji (`main.py`):**
    *   Tworzony jest obiekt `StorageManager` z podaną ścieżką do pliku JSON.
    *   Wywoływana jest metoda `storage_manager.load_all_question_objects()`.
        *   `StorageManager`: Otwiera plik JSON, wczytuje listę słowników.
        *   `StorageManager`: Dla każdego słownika `q_data` z listy:
            *   Uzupełnia brakujące klucze (`id`, `stopien_znajomosci`, `data_ostatniej_odpowiedzi`) domyślnymi wartościami.
            *   Wywołuje `Question.from_dict(q_data, default_id=idx)`, co tworzy instancję `Question`.
                *   `Question.__init__(...)`: Inicjalizuje atrybuty obiektu, konwertuje string daty na obiekt `datetime.date`.
        *   `StorageManager`: Zwraca listę obiektów `Question` do `main.py`.
    *   W `main.py` tworzony jest obiekt `QuizSession`, przekazując mu listę obiektów `Question`.
        *   `QuizSession.__init__(...)`: Zapisuje listę pytań w `self.all_questions`.
    *   W `main.py` tworzony jest obiekt `QuizUI`, przekazując mu obiekt `QuizSession`.

2.  **Rozpoczęcie Sesji Nauki (`QuizUI.run_quiz_loop()`):**
    *   Wywoływana jest metoda `self.quiz_session.start_new_session()`.
        *   `QuizSession`: Resetuje `self.answered_in_session_count`.
        *   `QuizSession`: Wywołuje `self._refresh_due_questions_indices()`.
            *   `QuizSession`: Pobiera `date.today()`.
            *   `QuizSession`: Iteruje po `self.all_questions`. Dla każdego obiektu `q_obj` wywołuje `q_obj.is_due(today)`.
                *   `Question.is_due(...)`: Oblicza datę następnej powtórki na podstawie `self.last_answered_date`, `self.knowledge_level` i `Question.SRS_INTERVALS`. Zwraca `True`, jeśli `today` jest równe lub późniejsze niż obliczona data.
            *   `QuizSession`: Tworzy listę indeksów pytań "due" i ją miesza. Zapisuje w `self.due_questions_indices_in_all_questions` i `self.total_due_at_session_start`.
    *   `QuizUI`: Sprawdza, czy `self.quiz_session.has_more_questions_today()` (co ponownie wywołuje `_refresh_due_questions_indices`). Jeśli nie ma pytań, wyświetla komunikat i kończy.

3.  **Pętla Zadawania Pytań (w `QuizUI.run_quiz_loop()`):**
    *   Dopóki `self.quiz_session.has_more_questions_today()` jest `True`:
        *   `QuizUI`: Wywołuje `self.quiz_session.get_next_question()`.
            *   `QuizSession`: Ponownie wywołuje `self._refresh_due_questions_indices()` (kluczowe dla dynamicznego powtarzania pytań z poziomem 0).
            *   `QuizSession`: Jeśli lista "due" nie jest pusta, wybiera losowo (przez wcześniejsze przetasowanie) indeks pytania, pobiera obiekt `Question` z `self.all_questions` i zapisuje go w `self.current_question_obj`. Zwraca ten obiekt.
        *   `QuizUI`: Jeśli `current_q_obj` nie jest `None`, wywołuje `self.display_question(current_q_obj)`.
            *   `QuizUI._display_session_stats()`: Wywołuje `self.quiz_session.get_session_progress_info()` (które znów może odświeżyć "due") i `self.quiz_session.get_knowledge_summary_string()` do wyświetlenia aktualnych statystyk.
            *   `QuizUI`: Wyświetla treść pytania i opcje z `current_q_obj`.
        *   `QuizUI`: Wywołuje `self.get_user_choice()` i czeka na klawisz ('a', 's', 'd' lub 'q').
        *   `QuizUI`: Jeśli użytkownik wybrał 'q', pętla jest przerywana, następuje przejście do zapisu.
        *   `QuizUI`: Na podstawie wybranego klawisza, określa tekst odpowiedzi użytkownika. Sprawdza, czy jest on równy `current_q_obj.correct_answer_text`, ustawiając `is_correct`.
        *   `QuizUI`: Wywołuje `self.quiz_session.process_answer(is_correct)`.
            *   `QuizSession`: Wywołuje `self.current_question_obj.update_knowledge_level(is_correct)`.
                *   `Question`: Zmienia `self.knowledge_level`.
            *   `QuizSession`: Wywołuje `self.current_question_obj.update_last_answered_date()`.
                *   `Question`: Ustawia `self.last_answered_date` na `date.today()`.
            *   `QuizSession`: Inkrementuje `self.answered_in_session_count`.
        *   `QuizUI`: Jeśli `is_correct` jest `False`:
            *   Wywołuje `self.display_error_feedback(current_q_obj, user_key)`.
                *   `QuizUI._display_session_stats()`: Ponownie wyświetla statystyki.
                *   `QuizUI`: Wyświetla pytanie, zaznaczony wybór użytkownika, informację o błędzie i poprawną odpowiedź.
            *   `QuizUI`: Czeka na naciśnięcie dowolnego klawisza (lub 'q'). Jeśli 'q', pętla jest przerywana.
        *   Jeśli `is_correct` jest `True`, pętla kontynuuje do następnej iteracji (następnego pytania).

4.  **Zakończenie Sesji i Zapis Danych:**
    *   Po zakończeniu pętli `run_quiz_loop` (naturalnie lub przez 'q'), sterowanie wraca do `main.py`.
    *   `main.py`: Wywołuje `storage_manager.save_all_question_objects(quiz_session.all_questions)`.
        *   `StorageManager`: Dla każdego obiektu `Question` w liście `quiz_session.all_questions` wywołuje jego metodę `q_obj.to_dict()`.
            *   `Question.to_dict()`: Konwertuje obiekt na słownik, formatując `last_answered_date` na string "YYYY-MM-DD" lub `None`.
        *   `StorageManager`: Zapisuje wynikową listę słowników do pliku JSON.
    *   `main.py`: Wyświetla komunikat o zapisaniu postępów.

### 4.3. Format danych (JSON)
Szczegółowy opis formatu pliku JSON znajduje się w sekcji [2.4. Struktura pliku JSON z pytaniami](#24-struktura-pliku-json-z-pytaniami).

*Kod aplikacji przestrzega standardów PEP 8 dla języka Python.*