**Prompt Engineering (AI Engineering)** - Sztuka współpracy z modelem AI tak, aby ten zrozumiał, co siedzi nam w głowie. I żebyśmy my sami ustalili, o co nam chodzi.

### **Charakterystyka modelu AI:**
- **Obcy**, więc oczekuje _kontekstu_ - on wie dużo o świecie, ale nie wie nic o użytkowniku, jego środowisku i jego problemach.
- **Dosłowny**, więc wymaga _jednoznaczności_ - jeśli nie sprecyzujemy dokładnie wszystkich parametrów oczekiwanego rozwiązania, to model sam sobie je wywnioskuje/wylosuje.
- **Posłuszny**, więc słucha _feedbacku_ - jako jedyne narzędzie "słucha się" użytkownika, dzięki czemu można kierować jego sposobem myślenia.

### **Definicje pojęć**
- **Token:** Podstawowa jednostka tekstu (słowo, część słowa, znak interpunkcyjny) używana przez modele językowe.

### **Kluczowe Rodzaje Informacji Potrzebne w Prompcie:**
- **Kontekst:** Dostarczenie niezbędnych informacji tła lub danych, które pozwolą AI na poprawne zrozumienie sytuacji.
- **Zadanie:** Jasno i konkretnie sformułowane polecenie dla modelu.
- **Format wyjściowy:** Jawne zdefiniowanie oczekiwanej struktury odpowiedzi modelu (np. lista, tabela, JSON).
- **Ton i styl:** Świadome sterowanie formalnością, emocjonalnym zabarwieniem i charakterem języka odpowiedzi.

### **Podstawowe Techniki Promptowania:**
- **Few-shot:** Technika dostarczania modelowi przykładów poprawnego wykonania zadania (najlepiej kilku).
    - Użytkownik wtedy musi wyklarować przed samym sobą to, czego chce.
    - Modele bardzo dobrze wnioskują z przykładów nieopisane parametry oczekiwanej odpowiedzi.
- **Chain-of-Thought:** Zaproponowanie modelowi toku rozumowania w formie listy kroków.
    - Użytkownik sam musi zastanowić się nad atomowymi krokami, potencjalnymi problemami i sposobami ich obejścia. Przedstawienie tego modelowi wymusi pożądane zachowanie.
    - Można też poprosić czat o to, by sam ```krok po kroku``` lub z ```dokładnymi instrukcjami``` przedstawił nam sposób otrzymania odpowiedzi. Wymusza to na nim skupienie, co samo w sobie zwiększa skuteczność. Dodatkowo, mając wgląd w to, jak model myśli, użytkownik będzie mógł łatwiej go zrozumieć i nim kierować. Może zresztą sam się czegoś nauczy.
- **AI-Assisted Questioning:** Zachęcanie modelu, aby on sam zadawał pytania potrzebne do lepszego zrozumienia problemu lub kontekstu użytkownika.
    - Pomocne, jeśli sami nie jesteśmy w stanie nadać odpowiedniego kontekstu.
    - Uczymy się, co jest istotne dla modelu.
- **Role Prompting:** Nadawanie modelowi roli, np. "Ekspert od marketingu".
    - Przekazujemy modelowi, na czym nam zależy.
    - (Role Playing) Tworzenie złożonych scenariuszy interakcji z AI, definiując role, cele i kontekst sytuacyjny.
- **Guided Iteration:** Wspólna praca z AI nad iteracyjnym udoskonalaniem odpowiedzi.
    - Wykorzystywanie tego, jak skutecznie AI słucha feedbacku.

### **Zaawansowane (Dodatkowe) Techniki Promptowania:**
- **Profil użytkownika:** Zapisany kawałek tekstu, w którym opisujemy samych siebie. Nasz zawód, zainteresowania, poziom edukacji, osobowość, co umiemy. Możemy też od razu zawrzeć nasze preferencje odnośnie typowego oczekiwanego stylu odpowiedzi, np. ```nigdy nie lej wody``` albo ```nie dodawaj komentarzy w kodzie```.
    - Pokazujemy modelowi, z kim w ogóle rozmawia, aby dostosował swój styl.
    - Do zastanowienia: kwestie prywatności.
- **Skróty dla konfiguracji promptów:** Tworzenie własnych aliasów dla często używanych instrukcji lub fragmentów promptu, np. ```--table```, jeśli chcemy, żeby odpowiedź była w formie tabeli.
- **Chaos Prompting:** Technika stymulowania kreatywności AI poprzez dostarczanie losowych lub nieoczekiwanych danych wejściowych.
    - Dobre dla artystów do szukania inspiracji.

### **Sposoby sterowania modelem**
- **Temperatura:** Ustawienie kontrolujące losowość/kreatywność odpowiedzi modelu w skali 0-2 (niska = precyzja, wysoka = kreatywność).
- **Długość odpowiedzi:** Jeśli zależy nam na krótkich odpowiedziach, możemy odgórnie ustawić maksymalną liczbę tokenów, z jakiej może składać się odpowiedź modelu.
- **Top-p:** Alternatywny sposób kontrolowania losowości, w którym AI wybiera kolejne słowa, ograniczając wybór tylko do tych, które razem mają prawdopodobieństwo większe niż _p_, zamiast brać pod uwagę wszystkie możliwe słowa.
- **System prompt / Metaprompt:** To taki prompt, tylko traktowany przez model jako jego motyw przewodni, który powinien być utrzymywany przez całą konwersację.

### **Podstawowe Ograniczenia Modeli**
- **Ograniczony kontekst modelu:** Limit ilości informacji (mierzony w tokenach), które model może jednocześnie przetwarzać i "pamiętać", nie jest nieskończony.
    - **Skutki**
        - Historia czatu nie może ciągnąć się w nieskończoność. W pewnym momencie początkowe wiadomości będą odcinane, przez co utracony zostanie pełen kontekst.
        - Nie możemy naraz przekazać modelowi za dużo informacji, np. dziesięciu 1000-stronicowych PDF-ów.
    - **Rozwiązania**
        - Streszczanie tekstu lub dotychczasowej historii albo kompresowanie ich do formatu czytelnego tylko dla modelu.
        - Czyszczenie plików z niepotrzebnych znaków, metadanych itp. (zaawansowane).
        - RAG (Retrieval-Augmented Generation) - system poszukiwania potrzebnych danych w plikach, aby potem zasilić prompt nie całymi plikami, a właśnie tylko istotnymi fragmentami. (b. zaawansowane).
- **Ograniczenie czasowe wiedzy modelu:** Modele są trenowane na danych do pewnego momentu w przeszłości.
    - **Skutki**
        - Model może pominąć świeże wydarzenia, dane albo teorie naukowe.
    - **Rozwiązania**
        - Większość modeli może już przeszukiwać internet w poszukiwaniu aktualnej wiedzy, ale tylko, jeżeli im tak polecimy albo będzie to dla niego wystarczająco oczywiste. Dlatego warto zawsze i tak mu to jasno zasugerować.
        - Jeżeli mamy pliki zawierające te zbyt nowe informacje, można je przekazać bezpośrednio modelowi.

### **Niebezpieczeństwa i Pułapki**
- **Halucynacje:** Zjawisko generowania przez model informacji brzmiących wiarygodnie, lecz nieprawdziwych lub zmyślonych.
    - **Żądanie informacji, które nie istnieją:** Jeżeli żądamy 10 dowodów na to, że Ziemia jest płaska, to w takim wypadku sami prosimy się o halucynacje. W przypadku prośby o 1000 książek wychwalających komunizm może i pewna liczba pierwszych przykładów będzie prawdziwa, ale oczywistym jest, że od pewnego momentu model musi zacząć zmyślać.
    - **Zwrócenie mieszanki informacji poprawnych i zmyślonych:** Może wynikać z analizy bardzo złożonych tematów, np. "Opisz mi teorię względności" albo "Zrób notatkę streszczającą CAŁĄ dokumentację SAS". Taka mieszanka drastycznie zmniejsza szansę na zorientowanie się, że model zwrócił halucynacje.
    - **Rozwiązania**
        - Zawsze warto dać modelowi furtkę wyjścia w stylu ```Jeśli nie wiesz, to napisz, że nie wiesz```. Bez tego będzie próbował nas na siłę "usatysfakcjonować".
        - Nie żądaj od razu dużej liczby przykładów. Możesz się zapytać najpierw o 5. A potem o kolejne 5. Też warto tu mu dać opcję typu: ```Znajdź 5 - jeśli znajdziesz mniej, nie szukaj na siłę ani nie wymyślaj```.
        - Weryfikuj odpowiedzi. Proś o źródła i też je weryfikuj. Możesz do tego użyć innego AI.
        - Wymagaj oceny wiarygodności jego wypowiedzi, np. w skali 1-10.
        - Zadaj to samo pytanie (w różnych sesjach) kilka razy i wybierz najczęściej pojawiającą się odpowiedź.
- **Uprzedzenia:** Najczęściej nieświadome zmotywowanie AI do myślenia w konkretny, subiektywny sposób.
    - Są znane przypadki, kiedy ludzie byli w stanie przekonać AI, że 2+2 to nie jest 4. Oznacza to, że do specyficznego zdania w bardziej niejednoznacznych sytuacjach także można go przekonać.
    - Jeśli z rozmów wynika, że jesteśmy wielbicielami liberalnego podejścia do gospodarki, to nawet gdy się spytamy neutralnie "jak byś rozwiązał problem X? Liberalnie czy konserwatywnie?", to model przez historię czatu może być wystarczająco uprzedzony, aby na siłę faworyzować opcję - z jego punktu widzenia - bardziej satysfakcjonującą użytkownika. A użytkownik wtedy sam bardziej się uprzedza, skoro "nawet AI przyznało mu rację".
    - Jeśli zapytasz się czy przedstawiony pomysł jest dobry to model będzie bardziej skłonny rozpatrywania go pozytywnie. Czasem się tak zachowuje nawet jeśli zapytasz się neutralnie: "co myślisz o tym pomyśle?".
    - Każdy model trenuje na jakimś zbiorze danych. Jeśli ten zbiór jest generalnie uprzedzony, odbije się to też na zachowaniu modelu.
    - **Rozwiązania**
        - Zachowanie jak największej obiektywności wobec modelu. Bezpośrednie przypominanie mu: ```Zachowaj obiektywność. Nie sugeruj się moimi przekonaniami```.
        - Dodatkowe poinstruowanie go: ```Rozpatrz wady i zalety mojego punktu widzenia/pomysłu nawet jeśli bardzo bym chciał by on był nieskazitelny```. Może warto wtedy spróbować tak się zachowywać jakby to miał być najgorszy pomysł i zaznaczać, że ma pewnie same złe cechy. Jest spora szansa, że model będzie dopiero wtedy wystarczająco krytyczny.
        - W przypadku używania nieoficjalnych modeli, weryfikować zbiór treningowy.

### **Podstawowe Zastosowania**
- **Szablony e-maili** – warto zdefiniować:
    - Relacja z odbiorcą
    - Cel e-maila
    - Pożądany ton
- **Posty na media społecznościowe** – warto zdefiniować:
    - Platforma
    - Docelowa publiczność
    - Cel postów
- **Rozwiązywanie Problemów** – Użycie metod analitycznych (np. S.W.O.T., Ishikawa).
- **Podsumowywanie informacji.**
- **Transformacja i reformatowanie tekstu.**
- **Pomoc w kodowaniu.**
- i wiele innych...

### **Wytwarzanie Szablonów Promptów / Promptów Uniwersalnych**
Bardziej zaawansowany temat. Chodzi tu o sytuacje, kiedy staramy wytworzyć prompt (lub często też prompt systemowy), który ma być wykorzystywany do wielu podobnych sytuacji. Wtedy skupienie przenosi się z dopieszczania odpowiedzi modelu, czasem uzyskiwanej za pomocą wielu promptów, na dopieszczanie pojedynczego promptu.
- **Cykl życia promptu:** Tworzenie doskonałych promptów to rzadko kwestia jednego strzału. To proces iteracyjny.
    1. Pomysł,
    2. Implementacja,
    3. Testowanie,
    4. Analiza,
    5. Modyfikacja,
    6. Powtarzanie od 3 do 5.
- **Zaczynanie od prostych promptów:** Warto rozpocząć pracę od najprostszego promptu i stopniowo go komplikować.
    - Łatwiejsze debugowanie i analiza.
    - Zrozumienie działania i sposobu rozumowania modelu.
- **Przykładowe kryteria oceny odpowiedzi:**
    - **Dokładność:** Weryfikacja prawdziwości informacji generowanych przez model.
    - **Trafność:** Sprawdzenie, czy odpowiedź modelu jest zgodna z tematem zapytania.
    - **Zaangażowanie:** Ocena, czy tekst jest interesujący i przyciągający uwagę (jeśli jest to celem).

### **Dodatki**
- **Zaczynanie definicji zadania od czasownika.**
- **Instrukcja "notalk; justgo":** (To dla ChatGPT, sprawdzić, jak brzmi wersja dla innych modeli) Sposób na poinstruowanie modelu, aby udzielił zwięzłej odpowiedzi bez dodatkowych komentarzy.
- **Zrozumienie UML:** Niektóre modele dobrze interpretują i generują (w formie tekstowej) diagramy UML.