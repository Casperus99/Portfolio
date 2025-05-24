**Kluczowe Elementy Promptu:**
- **Kontekst:** Informacje dostarczane modelowi, aby zrozumiał zadanie; powinien być specyficzny i wystarczający, ale nie nadmierny.
- **Instrukcja/Zadanie:** Jasno sformułowane polecenie dla modelu, najlepiej zaczynające się od czasownika akcji.
- **Persona (Role Prompting):** Przypisanie AI konkretnej roli lub tożsamości w celu dostosowania stylu i perspektywy odpowiedzi.
- **Format Wyjściowy:** Jawne zdefiniowanie oczekiwanej struktury odpowiedzi modelu (np. lista, tabela, JSON).
- **Ton i Styl:** Świadome sterowanie formalnością, emocjonalnym zabarwieniem i charakterem języka odpowiedzi.

**Filozofia 3xC (CCC):**
- **Clarity (Klarowność):** Jednoznaczność i precyzja polecenia w prompcie.
- **Context (Kontekst):** Dostarczenie odpowiedniej ilości informacji potrzebnych modelowi.
- **Creativity (Kreatywność):** Zachęcanie AI do eksploracji i generowania nowatorskich pomysłów (jeśli pożądane).

**Słowa Kluczowe Naprowadzające:**
- "myśląc krok po kroku"
- "dokładne instrukcje"

**Zaawansowane Techniki Promptowania:**
- **Few-shot Prompting:** Technika dostarczania modelowi kilku (2-5) przykładów wykonania zadania w celu precyzyjnego pokazania oczekiwanego rezultatu.
- **Chain-of-Thought (CoT) Prompting:** Zaproponowanie modelowi swojego własnego toku rozumowania w krokach.
- **AI-Assisted Questioning:** Technika polegająca na zachęcaniu modelu, aby sam zadał pytania potrzebne do lepszego zrozumienia problemu lub kontekstu użytkownika.
- **Self-Consistency (w CoT):** Generowanie wielu ścieżek rozumowania (CoT) i wybieranie najczęściej pojawiającej się odpowiedzi dla zwiększenia wiarygodności.
- **Role Playing Zaawansowany:** Tworzenie złożonych scenariuszy interakcji z AI, definiując role, cele i kontekst sytuacyjny.
- **Prompt Chaining (Sekwencjonowanie Promptów):** Dzielenie złożonych zadań na serię mniejszych, prostszych promptów, gdzie wynik jednego jest wejściem dla następnego.
- **Chaos Prompting:** Technika stymulowania kreatywności AI poprzez dostarczanie losowych lub nieoczekiwanych danych wejściowych.
- **Guided Iteration (Prowadzona Iteracja):** Wspólna praca z AI nad iteracyjnym udoskonalaniem promptu lub wyniku.

**Iteracja, Testowanie i Debugowanie Promptów:**
- **Cykl Życia Promptu:** Iteracyjny proces obejmujący pomysł, implementację, testowanie, analizę, modyfikację i ponowne testowanie promptu.
- **Systematyczne Testowanie Promptów:** Wprowadzanie małych, kontrolowanych zmian i ocena wyników według zdefiniowanych kryteriów.
- **Kryteria Oceny Odpowiedzi:**
    - **Dokładność:** Weryfikacja prawdziwości informacji generowanych przez model.
    - **Trafność:** Sprawdzenie, czy odpowiedź modelu jest zgodna z tematem zapytania.
    - **Zaangażowanie:** Ocena, czy tekst jest interesujący i przyciągający uwagę (jeśli jest to celem).
- **Analiza Odpowiedzi Modelu - Halucynacje:** Zjawisko generowania przez model informacji brzmiących wiarygodnie, lecz nieprawdziwych lub zmyślonych.
- **Instrukcja "Nie wiem" dla AI:** Pouczanie modelu, aby sygnalizował brak wiedzy, zamiast generować niepewne odpowiedzi.

**Właściwości i Ograniczenia Modeli:**
- **Ograniczony Kontekst Modelu (Okno Kontekstowe):** Limit ilości informacji (mierzony w tokenach), które model może jednocześnie przetwarzać i "pamiętać".
- **Token:** Podstawowa jednostka tekstu (słowo, część słowa, znak interpunkcyjny) używana przez modele językowe.
- **Temperatura (Parametr Modelu):** Ustawienie kontrolujące losowość/kreatywność odpowiedzi modelu (niska = precyzja, wysoka = kreatywność).
- **Top-p (Nucleus Sampling):** Alternatywny parametr kontrolujący losowość odpowiedzi poprzez wybór najbardziej prawdopodobnych tokenów.
- **Ograniczenie Czasowe Wiedzy Modelu:** Świadomość, że modele są trenowane na danych do pewnego momentu w przeszłości i mogą nie znać najnowszych informacji.

**Ogólne Dobre Praktyki Promptowania:**
- **Zasada "Zaczynaj od prostych promptów":** Rekomendacja rozpoczynania pracy od nieskomplikowanych zapytań i stopniowego dodawania złożoności.
- **Zasada "Iteruj i ulepszaj":** Podkreślenie znaczenia ciągłego doskonalenia promptów poprzez powtarzalny proces testowania i modyfikacji.

**Techniki Specjalistyczne i Zastosowania:**
- **Prompt Compression Techniques:** Metody skracania tekstu (np. historii konwersacji) przy zachowaniu jego znaczenia, w celu oszczędności tokenów.
- **Użycie Metod Analitycznych z AI (np. SWOT, Ishikawa):** Kierowanie modelu do zastosowania znanych struktur rozwiązywania problemów.
- **Zrozumienie UML przez AI:** Zdolność niektórych modeli do interpretacji i generowania (w formie tekstowej) diagramów UML.

**Etyka i Odpowiedzialność w Prompt Engineeringu:**
- **Biasy (Uprzedzenia) w Modelach:** Tendencje modeli do powielania uprzedzeń obecnych w danych treningowych (np. płciowe, rasowe).
- **Minimalizowanie Biasów w Promptach:** Stosowanie języka inkluzywnego i zrównoważonych przykładów w celu ograniczenia wpływu uprzedzeń.
- **Odpowiedzialne Promptowanie**
    - **Szkodliwe Treści:** Unikanie generowania treści nielegalnych, nienawistnych, dyskryminujących lub dezinformujących.
    - **Prywatność i Dane Wrażliwe:** Kategoryczny zakaz umieszczania w promptach poufnych informacji.
    - **Transparentność:** Rozważenie informowania o użyciu AI do generowania treści, jeśli może to wprowadzać w błąd.

**Dodatkowe Triki i Ustawienia:**
- **Instrukcja "notalk; justgo":** Sposób na poinstruowanie modelu, aby udzielił zwięzłej odpowiedzi bez dodatkowych komentarzy.
- **Profil Użytkownika w Prompcie:** Predefiniowany fragment promptu określający stałe preferencje co do stylu odpowiedzi modelu.
- **Skróty dla Konfiguracji Promptów:** Tworzenie własnych aliasów dla często używanych instrukcji lub fragmentów promptu.
- **Wymaganie Oceny Pewności:** Prośba do modelu o oszacowanie wiarygodności własnej odpowiedzi, np. w skali liczbowej.