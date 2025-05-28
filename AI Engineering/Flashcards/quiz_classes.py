from datetime import date, timedelta, datetime
import os
import random
import readchar
import json

class Question:
    """
    Reprezentuje pojedyncze pytanie w quizie SRS.
    """
    
    # Definicje stałych jako atrybuty klasy dla łatwiejszej konfiguracji
    # Można je nadpisać przed tworzeniem instancji, jeśli jest taka potrzeba
    MIN_KNOWLEDGE_LEVEL = 0
    MAX_KNOWLEDGE_LEVEL = 6 # Domyślna wartość, dostosuj do ODSTEPY_CZASOWE
    
    # Odstępy czasowe w dniach w zależności od stopnia znajomości
    # Klucze muszą pokrywać zakres od MIN_KNOWLEDGE_LEVEL do MAX_KNOWLEDGE_LEVEL
    SRS_INTERVALS = { 
        0: 0,
        1: 1,
        2: 2,
        3: 4,
        4: 7,
        5: 12,
        6: 20
    }

    def __init__(self, id_pytania, text, options, correct_answer_text,
                 knowledge_level=None, last_answered_date=None):
        """
        Konstruktor obiektu Pytanie.

        Args:
            id_pytania (any): Unikalny identyfikator pytania.
            text (str): Treść pytania.
            options (list[str]): Lista możliwych odpowiedzi.
            correct_answer_text (str): Tekst poprawnej odpowiedzi.
            knowledge_level (int, optional): Początkowy stopień znajomości. 
                                            Domyślnie MIN_KNOWLEDGE_LEVEL.
            last_answered_date (date | str | None, optional): Data ostatniej odpowiedzi.
                                                            Może być obiektem date, stringiem YYYY-MM-DD lub None.
        """
        self.id = id_pytania
        self.text = text
        self.options = options
        self.correct_answer_text = correct_answer_text
        
        if knowledge_level is None:
            self.knowledge_level = Question.MIN_KNOWLEDGE_LEVEL
        else:
            # Upewniamy się, że poziom jest w dozwolonym zakresie
            self.knowledge_level = max(Question.MIN_KNOWLEDGE_LEVEL, 
                                       min(Question.MAX_KNOWLEDGE_LEVEL, knowledge_level))

        if isinstance(last_answered_date, str):
            try:
                self.last_answered_date = datetime.strptime(last_answered_date, "%Y-%m-%d").date()
            except ValueError:
                self.last_answered_date = None # Jeśli string jest niepoprawny
        elif isinstance(last_answered_date, date):
            self.last_answered_date = last_answered_date
        else:
            self.last_answered_date = None

    def is_due(self, current_date=None):
        """
        Sprawdza, czy pytanie jest "due" (powinno zostać zadane) na podaną datę.

        Args:
            current_date (date, optional): Data, dla której sprawdzamy. Domyślnie dzisiejsza data.

        Returns:
            bool: True, jeśli pytanie jest "due", False w przeciwnym razie.
        """
        if current_date is None:
            current_date = date.today()
        
        if self.last_answered_date is None:
            return True # Nigdy nie odpowiadano, zawsze "due"

        # Upewnij się, że self.knowledge_level jest kluczem w SRS_INTERVALS
        # Jeśli nie, użyj domyślnego odstępu dla MIN_KNOWLEDGE_LEVEL
        interval_days = Question.SRS_INTERVALS.get(
            self.knowledge_level, 
            Question.SRS_INTERVALS.get(Question.MIN_KNOWLEDGE_LEVEL, 0) 
        )
        
        next_due_date = self.last_answered_date + timedelta(days=interval_days)
        return current_date >= next_due_date

    def update_knowledge_level(self, is_correct):
        """
        Aktualizuje stopień znajomości na podstawie poprawności odpowiedzi.

        Args:
            is_correct (bool): True, jeśli odpowiedź była poprawna, False w przeciwnym razie.
        """
        if is_correct:
            self.knowledge_level = min(Question.MAX_KNOWLEDGE_LEVEL, self.knowledge_level + 1)
        else:
            self.knowledge_level = max(Question.MIN_KNOWLEDGE_LEVEL, self.knowledge_level - 1)
        
        # Dodatkowa logika: jeśli odpowiedź jest błędna, można zresetować poziom do MIN_KNOWLEDGE_LEVEL
        # if not is_correct:
        #     self.knowledge_level = Question.MIN_KNOWLEDGE_LEVEL

    def update_last_answered_date(self, answered_date=None):
        """
        Ustawia datę ostatniej odpowiedzi.

        Args:
            answered_date (date, optional): Data odpowiedzi. Domyślnie dzisiejsza data.
        """
        if answered_date is None:
            self.last_answered_date = date.today()
        else:
            self.last_answered_date = answered_date

    def to_dict(self):
        """
        Konwertuje obiekt Question na słownik, np. do zapisu w JSON.

        Returns:
            dict: Słownik reprezentujący obiekt Pytanie.
        """
        return {
            "id": self.id,
            "pytanie": self.text,
            "odpowiedzi": self.options,
            "poprawna_odpowiedz": self.correct_answer_text,
            "stopien_znajomosci": self.knowledge_level,
            "data_ostatniej_odpowiedzi": self.last_answered_date.strftime("%Y-%m-%d") if self.last_answered_date else None
        }

    @classmethod
    def from_dict(cls, data, default_id=None):
        """
        Metoda klasowa do tworzenia obiektu Question ze słownika.

        Args:
            data (dict): Słownik z danymi pytania.
            default_id (any, optional): Domyślne ID, jeśli brakuje w danych.

        Returns:
            Question: Nowy obiekt Pytanie.
        """
        # Upewnij się, że stałe klasy są zdefiniowane przed użyciem w konstruktorze
        # (zwykle są, bo są definiowane na poziomie klasy)
        
        return cls(
            id_pytania=data.get("id", default_id), # Użyj 'id' jeśli jest, inaczej default_id
            text=data["pytanie"],
            options=data["odpowiedzi"],
            correct_answer_text=data["poprawna_odpowiedz"],
            knowledge_level=data.get("stopien_znajomosci", cls.MIN_KNOWLEDGE_LEVEL),
            last_answered_date=data.get("data_ostatniej_odpowiedzi") # Konstruktor obsłuży None lub string
        )

    def __str__(self):
        return f"Pytanie ID: {self.id}, Poziom: {self.knowledge_level}, Ostatnio: {self.last_answered_date or 'Nigdy'}"


class QuizSession:
    """
    Zarządza logiką sesji quizu, stanem pytań i wyborem pytań do zadania.
    """

    def __init__(self, all_question_objects):
        """
        Konstruktor sesji quizu.

        Args:
            all_question_objects (list[Question]): Lista wszystkich obiektów Question.
        """
        self.all_questions = all_question_objects # Przechowuje listę obiektów Question
        self.due_questions_indices_in_all_questions = [] # Indeksy pytań 'due' w self.all_questions
        self.current_question_obj = None # Aktualnie zadane pytanie (obiekt Question)
        self.answered_in_session_count = 0
        self.total_due_at_session_start = 0
        
        # Inicjalizacja stałych, jeśli klasa Question ich nie ma jako atrybutów klasy
        # lub jeśli chcemy je tu nadpisać dla sesji.
        # Generalnie lepiej, aby Question zarządzało swoimi stałymi.
        # self.min_knowledge_level = Question.MIN_KNOWLEDGE_LEVEL 
        # self.max_knowledge_level = Question.MAX_KNOWLEDGE_LEVEL

    def _refresh_due_questions_indices(self):
        """
        Prywatna metoda do odświeżania listy indeksów pytań "due" na dzisiaj.
        Zwraca listę indeksów odnoszących się do self.all_questions.
        """
        today = date.today()
        due_indices = [
            idx for idx, q_obj in enumerate(self.all_questions) if q_obj.is_due(today)
        ]
        random.shuffle(due_indices) # Mieszamy za każdym razem, gdy odświeżamy
        return due_indices

    def start_new_session(self):
        """
        Rozpoczyna nową sesję quizu: resetuje liczniki i pobiera pytania "due".
        """
        self.answered_in_session_count = 0
        self.due_questions_indices_in_all_questions = self._refresh_due_questions_indices()
        self.total_due_at_session_start = len(self.due_questions_indices_in_all_questions)
        self.current_question_obj = None

    def get_next_question(self):
        """
        Wybiera i zwraca następne pytanie do zadania z puli "due".
        Jeśli pytanie ma poziom 0, może zostać wybrane ponownie w tej samej sesji.

        Returns:
            Question | None: Następny obiekt Question do zadania, lub None jeśli nie ma więcej.
        """
        # Odśwież listę pytań "due" za każdym razem, gdy pobieramy następne pytanie
        # To pozwoli na dynamiczne dodawanie pytań, które spadły do poziomu 0
        self.due_questions_indices_in_all_questions = self._refresh_due_questions_indices()
        
        if not self.due_questions_indices_in_all_questions:
            self.current_question_obj = None
            return None

        # Wybieramy pierwszy element z przetasowanej listy "due"
        # Nie usuwamy go, bo pytanie z poziomem 0 może wrócić
        next_question_index_in_db = self.due_questions_indices_in_all_questions[0]
        self.current_question_obj = self.all_questions[next_question_index_in_db]
        return self.current_question_obj

    def process_answer(self, was_correct):
        """
        Przetwarza odpowiedź użytkownika dla aktualnie zadanego pytania.
        Aktualizuje stan pytania (poziom znajomości, data ostatniej odpowiedzi).

        Args:
            was_correct (bool): True, jeśli odpowiedź użytkownika była poprawna.
        
        Returns:
            bool: True jeśli przetworzono odpowiedź, False jeśli nie było aktualnego pytania.
        """
        if self.current_question_obj:
            self.current_question_obj.update_knowledge_level(was_correct)
            self.current_question_obj.update_last_answered_date() # Używa dzisiejszej daty
            self.answered_in_session_count += 1
            return True
        return False

    def has_more_questions_today(self):
        """
        Sprawdza, czy są jeszcze pytania "due" na dzisiaj.
        Odświeża listę "due" przed sprawdzeniem.
        """
        return len(self._refresh_due_questions_indices()) > 0

    def get_knowledge_summary_string(self):
        """
        Zwraca string z podsumowaniem stanu wiedzy dla wszystkich pytań.
        Format: X|Y|Z... gdzie X,Y,Z to liczby pytań na kolejnych poziomach znajomości.
        """
        summary = {}
        min_level = Question.MIN_KNOWLEDGE_LEVEL # Używamy stałych z klasy Question
        max_level = Question.MAX_KNOWLEDGE_LEVEL

        for q_obj in self.all_questions:
            level = q_obj.knowledge_level
            summary[level] = summary.get(level, 0) + 1
        
        summary_parts = [str(summary.get(level, 0)) for level in range(min_level, max_level + 1)]
        return "|".join(summary_parts)

    def get_session_progress_info(self):
        """
        Zwraca informacje o postępie w sesji: liczbę dostępnych pytań "due" na dziś.
        """
        # Liczba pytań, które są aktualnie 'due'
        current_due_count = len(self._refresh_due_questions_indices())
        return {
            "current_due_count": current_due_count,
            "total_due_at_session_start": self.total_due_at_session_start, # Ile było na początku
            "answered_in_session_count": self.answered_in_session_count
        }
    

class QuizUI:
    """
    Obsługuje interfejs użytkownika dla quizu.
    """

    def __init__(self, quiz_session):
        """
        Konstruktor interfejsu użytkownika.

        Args:
            quiz_session (QuizSession): Obiekt sesji quizu.
        """
        self.quiz_session = quiz_session
        self.option_map = {'a': 0, 's': 1, 'd': 2} # Mapowanie klawiszy na indeksy
        self.option_labels = ['A', 'S', 'D']      # Etykiety dla opcji

    def _clear_screen(self):
        """Prywatna metoda do czyszczenia ekranu terminala."""
        if os.name == 'nt': # Dla Windows
            os.system('cls')
        else: # Dla Linux i macOS
            os.system('clear')

    def _display_session_stats(self):
        """Wyświetla statystyki bieżącej sesji."""
        progress_info = self.quiz_session.get_session_progress_info()
        knowledge_summary_str = self.quiz_session.get_knowledge_summary_string()
        
        # Używamy current_due_count, które odzwierciedla aktualnie dostępne pytania 'due'
        print(f"Dostępnych pytań w tym dniu: {progress_info['current_due_count']}")
        # Stałe MIN_ZNAJOMOSC i MAX_ZNAJOMOSC powinny być dostępne, np. z klasy Question
        # lub przekazane do UI, albo zdefiniowane globalnie. Dla uproszczenia, zakładam dostęp.
        min_lvl = Question.MIN_KNOWLEDGE_LEVEL 
        max_lvl = Question.MAX_KNOWLEDGE_LEVEL
        print(f"Ogólny stan wiedzy (poziomy {min_lvl}-{max_lvl}): {knowledge_summary_str}")
        print("------------------------------------")

    def display_question(self, question_obj):
        """
        Wyświetla pytanie i jego opcje.

        Args:
            question_obj (Question): Obiekt pytania do wyświetlenia.
        """
        self._clear_screen()
        print("Naciśnij 'q' aby wyjść.\n")
        self._display_session_stats()
        
        print(f"Pytanie (ID: {question_obj.id}, Poziom: {question_obj.knowledge_level}):")
        print(question_obj.text)
        print("\nOdpowiedzi:")
        for i, opt_text in enumerate(question_obj.options):
            print(f"{self.option_labels[i]}. {opt_text}")
        print("\nWybierz odpowiedź (a, s, d) lub 'q' aby wyjść:")

    def get_user_choice(self):
        """
        Pobiera i waliduje wybór odpowiedzi od użytkownika.

        Returns:
            str | None: Wybrany klawisz ('a', 's', 'd', 'q') lub None jeśli wystąpił błąd.
        """
        while True:
            key = readchar.readkey()
            if key.lower() in ['a', 's', 'd', 'q']:
                return key.lower()
            # Można dodać komunikat o nieprawidłowym klawiszu, jeśli potrzebne
            # print("Nieprawidłowy klawisz. Użyj 'a', 's', 'd' lub 'q'.")


    def display_error_feedback(self, question_obj, user_choice_key):
        """
        Wyświetla feedback dla błędnej odpowiedzi.

        Args:
            question_obj (Question): Obiekt pytania, na które odpowiedziano.
            user_choice_key (str): Klawisz ('a', 's', 'd') wybrany przez użytkownika.
        """
        self._clear_screen()
        print("Naciśnij 'q' aby wyjść.\n")
        self._display_session_stats() # Ponownie wyświetl statystyki

        print(f"Pytanie (ID: {question_obj.id}, Poziom: {question_obj.knowledge_level}):") # Poziom już zaktualizowany
        print(question_obj.text)
        print("\nOdpowiedzi:")
        
        user_answer_index = self.option_map[user_choice_key]
        user_choice_text = question_obj.options[user_answer_index]

        for i, opt_text in enumerate(question_obj.options):
            prefix = f"{self.option_labels[i]}. "
            if i == user_answer_index: # Zaznacz wybór użytkownika
                prefix = f"[{self.option_labels[i]}]. "
            print(f"{prefix}{opt_text}")
        
        print("\n------------------------------------")
        print(f"Twoja odpowiedź: {user_choice_key.upper()}. {user_choice_text} - ŹLE.")
        print("\nPoprawna odpowiedź:")
        
        correct_option_text = question_obj.correct_answer_text
        correct_option_label = ""
        try:
            correct_option_idx = question_obj.options.index(correct_option_text)
            correct_option_label = self.option_labels[correct_option_idx]
        except ValueError:
            # To nie powinno się zdarzyć, jeśli dane są spójne
            print("Błąd: Poprawna odpowiedź nie znaleziona w opcjach.")
        
        print(f"{correct_option_label}. {correct_option_text}")
        print("------------------------------------")
        print("\nNaciśnij DOWOLNY KLAWISZ, aby przejść do następnego pytania, lub 'q' aby wyjść...")


    def run_quiz_loop(self):
        """Główna pętla interakcji quizu z użytkownikiem."""
        self.quiz_session.start_new_session()

        if not self.quiz_session.has_more_questions_today():
            self._clear_screen()
            print("Gratulacje! Na dziś nie ma więcej pytań do powtórki.")
            self._display_session_stats() # Pokaż finalny stan wiedzy
            print("Spróbuj ponownie jutro.")
            return

        while self.quiz_session.has_more_questions_today():
            current_q_obj = self.quiz_session.get_next_question()
            if not current_q_obj: # Dodatkowe zabezpieczenie
                break 

            self.display_question(current_q_obj)
            user_key = self.get_user_choice()

            if user_key == 'q':
                self._clear_screen()
                print("Zakończono sesję. Postępy zostaną zapisane.")
                # Zapisanie powinno odbywać się w głównym skrypcie po zakończeniu pętli UI
                return # Zakończ pętlę UI

            user_answer_index = self.option_map[user_key]
            user_answer_text = current_q_obj.options[user_answer_index]
            
            is_correct = (user_answer_text == current_q_obj.correct_answer_text)
            
            self.quiz_session.process_answer(is_correct) # Aktualizuje pytanie w sesji

            if not is_correct:
                self.display_error_feedback(current_q_obj, user_key)
                next_action_key = readchar.readkey() # Czekaj na dowolny klawisz
                if next_action_key.lower() == 'q':
                    self._clear_screen()
                    print("Zakończono sesję. Postępy zostaną zapisane.")
                    return
            # Jeśli odpowiedź była poprawna, pętla automatycznie przejdzie dalej,
            # a display_question() na początku wyczyści ekran i wyświetli nowe pytanie.

        # Po zakończeniu pętli (wszystkie pytania "due" odpowiedziane)
        self._clear_screen()
        print("Koniec pytań w tym dniu! Postępy zostaną zapisane.")
        self._display_session_stats() # Pokaż finalny stan wiedzy


class StorageManager:
    """
    Zarządza wczytywaniem i zapisywaniem danych quizu do/z pliku.
    """

    def __init__(self, file_path):
        """
        Konstruktor menedżera przechowywania danych.

        Args:
            file_path (str): Ścieżka do pliku JSON, gdzie przechowywane są dane quizu.
        """
        self.file_path = file_path

    def load_all_question_objects(self):
        """
        Wczytuje dane pytań z pliku JSON i konwertuje je na listę obiektów Question.
        Inicjalizuje brakujące pola 'stopien_znajomosci' i 'data_ostatniej_odpowiedzi'
        oraz 'id'.

        Returns:
            list[Question]: Lista obiektów Question. Zwraca pustą listę, jeśli plik nie istnieje
                            lub wystąpi błąd dekodowania.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                questions_data = json.load(f)
            
            question_objects = []
            # Używamy stałych zdefiniowanych w klasie Question
            min_level = Question.MIN_KNOWLEDGE_LEVEL 

            for idx, q_data in enumerate(questions_data):
                # Upewnij się, że każde pytanie ma domyślne wartości, jeśli brakuje pól
                q_data.setdefault('stopien_znajomosci', min_level)
                q_data.setdefault('data_ostatniej_odpowiedzi', None)
                # Używamy indeksu jako domyślnego ID, jeśli 'id' nie ma w danych
                # lub jeśli chcemy mieć pewność, że ID jest unikalne w ramach sesji ładowania
                q_data.setdefault('id', idx) 
                
                question_objects.append(Question.from_dict(q_data, default_id=idx))
            return question_objects
        except FileNotFoundError:
            print(f"Plik {self.file_path} nie został znaleziony. Zwracam pustą listę pytań.")
            return []
        except json.JSONDecodeError:
            print(f"Błąd dekodowania pliku JSON: {self.file_path}. Sprawdź jego poprawność. Zwracam pustą listę.")
            return []
        except Exception as e:
            print(f"Wystąpił nieoczekiwany błąd podczas ładowania pytań: {e}. Zwracam pustą listę.")
            return []

    def save_all_question_objects(self, question_objects_list):
        """
        Zapisuje listę obiektów Question do pliku JSON.
        Każdy obiekt Question jest konwertowany na słownik za pomocą jego metody to_dict().

        Args:
            question_objects_list (list[Question]): Lista obiektów Question do zapisania.
        """
        questions_data_to_save = [q_obj.to_dict() for q_obj in question_objects_list]
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(questions_data_to_save, f, ensure_ascii=False, indent=2)
            # print(f"Dane quizu zostały zapisane w pliku: {self.file_path}") # Opcjonalny komunikat
        except IOError:
            print(f"Błąd zapisu do pliku: {self.file_path}.")
        except Exception as e:
            print(f"Wystąpił nieoczekiwany błąd podczas zapisywania pytań: {e}.")