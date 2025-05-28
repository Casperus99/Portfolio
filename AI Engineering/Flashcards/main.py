from quiz_classes import Question, QuizSession, QuizUI, StorageManager

# Stałe globalne (mogą być też wewnątrz klas, jeśli bardziej pasuje)
JSON_FILE_PATH = 'pytania_patent.json' # Ścieżka do Twojego pliku JSON
ODSTEPY_CZASOWE = {0: 0, 1: 1, 2: 2, 3: 4, 4: 7, 5: 12, 6: 20}
MIN_ZNAJOMOSC = min(ODSTEPY_CZASOWE.keys()) if ODSTEPY_CZASOWE else 0
MAX_ZNAJOMOSC = max(ODSTEPY_CZASOWE.keys()) if ODSTEPY_CZASOWE else 0


# Inicjalizacja stałych dla klasy Question (jeśli nie są przekazywane inaczej)
Question.MIN_KNOWLEDGE_LEVEL = MIN_ZNAJOMOSC
Question.MAX_KNOWLEDGE_LEVEL = MAX_ZNAJOMOSC
Question.SRS_INTERVALS = ODSTEPY_CZASOWE


if __name__ == "__main__":
    storage_manager = StorageManager(JSON_FILE_PATH)
    
    # Wczytaj wszystkie obiekty Question z pliku
    all_questions = storage_manager.load_all_question_objects()

    if not all_questions:
        # Możesz tu dodać logikę tworzenia nowego pliku JSON z szablonu,
        # jeśli plik nie istnieje i chcesz zacząć z predefiniowaną bazą pytań.
        # Na razie, jeśli plik jest pusty lub nie istnieje, program może po prostu zakończyć działanie
        # lub poinformować użytkownika.
        print("Nie udało się załadować pytań lub baza pytań jest pusta.")
        # sys.exit(1) # Można zakończyć, jeśli brak pytań jest krytyczny

    # Utwórz sesję quizu z wczytanymi obiektami
    quiz_session = QuizSession(all_questions)
    
    # Utwórz interfejs użytkownika
    quiz_ui = QuizUI(quiz_session)
    
    # Uruchom pętlę quizu
    quiz_ui.run_quiz_loop()
    
    # Po zakończeniu sesji (np. gdy użytkownik wyjdzie lub skończą się pytania)
    # zapisz zaktualizowany stan wszystkich pytań
    storage_manager.save_all_question_objects(quiz_session.all_questions)
    
    print("\nPostępy zostały zapisane. Do zobaczenia!")