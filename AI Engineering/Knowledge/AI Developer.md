### Pomoc w Kodowaniu
Proces efektywnego wykorzystania AI do pisania kodu obejmuje następujące kroki:

*   **Krok 1: Definiowanie wymagań.**
    *   Należy dokładnie **udokumentować cel aplikacji, grupę docelową, pożądane funkcje** oraz wszelkie ograniczenia.
    *   Nie można zapomnieć o **wymaganiach niefunkcjonalnych**: bezpieczeństwo, wydajność, zgodność (compliance), skalowalność. AI może pomóc **zidentyfikować niejednoznaczności, niespójności i brakujące informacje w wymaganiach.**
*   **Krok 2: Wybór stosu technologicznego.**
    *   Należy zdecydować o języku programowania, frameworkach, bibliotekach, narzędziach.
    *   Można **poprosić AI o sugestie lub listę zalet/wad dokonanego wyboru.**
*   **Krok 3: Podział projektu na mniejsze zadania.**
    *   **Lepsze rezultaty osiągnie się, dzieląc kod na mniejsze, bardziej zarządzalne fragmenty.**
    *   Należy brać pod uwagę **ograniczenia `max_token`** modelu AI.
*   **Krok 4: Rozpoczęcie rozmowy z AI.**
    *   Należy dostarczyć zebrane dane w **kompleksowym, ale zwięzłym prompcie.**
    *   Postępować stopniowo i iterować w małych przyrostach.
*   **Krok 5: Porady dotyczące architektury i wzorców projektowych.**
    *   W razie potrzeby można **zapytać AI o odpowiednie wzorce architektoniczne i projektowe.** Warto mieć ogólny zarys projektu przed pisaniem kodu.
*   **Krok 6: Prośba o fragmenty kodu i przykłady.**
    *   Można zacząć prosić o konkretne fragmenty kodu.
    *   Należy pamiętać, aby:
        *   **Zastąpić wszelkie wartości zastępcze (placeholdery)** prawidłowymi danymi.
        *   **Testować i walidować każdą linię kodu.**
        *   **Dostosować kod** do specyficznych wymagań.
    *   Jeśli AI obetnie skrypt (np. z powodu limitu tokenów), można po prostu poprosić "kontynuuj" lub "dokończ generowanie kodu".
*   **Krok 7: Rozwiązywanie problemów i debugowanie.**
    *   Należy testować kod. Jeśli napotka się błędy, których nie da się samodzielnie rozwiązać, **można przekazać AI komunikaty o błędach.**
    *   Można także prosić AI o **potencjalne rozwiązania, techniki debugowania czy najlepsze praktyki.** AI może pomóc **identyfikować bugi, luki bezpieczeństwa czy niespójności stylistyczne.**
*   **Krok 8: Optymalizacja i refaktoryzacja kodu.**
    *   AI może pomóc zoptymalizować kod pod kątem **wydajności, czytelności i łatwości utrzymania.**
*   **Krok 9: Przegląd i testowanie aplikacji.**
    *   Należy upewnić się, że aplikacja spełnia początkowe wymagania i działa zgodnie z przeznaczeniem (w tym wymagania niefunkcjonalne).
    *   Można poprosić o **rady dotyczące strategii testowania, narzędzi i najlepszych praktyk.** AI może pomóc **generować przypadki testowe i dane testowe.**
*   **Krok 10: Wdrożenie i utrzymanie.**
    *   Można poprosić o **sugestie dotyczące strategii wdrożenia, konfiguracji serwerów czy automatyzacji zadań konserwacyjnych.**
*   **Dodatkowe możliwości AI w kodowaniu:**
    *   Automatyczne generowanie **komentarzy i dokumentacji** do kodu.
    *   Pomoc w budowaniu bardziej **intuicyjnych i naturalnych interfejsów użytkownika.**
    *   **Tłumaczenie kodu** z jednego języka na inny.

Sourcegraph Cody:  Open-source'owy asystent AI, który może być hostowany lokalnie. Działa z VS Code, JetBrains IDEs i w przeglądarce. Pozwala na zadawanie pytań o kod, generowanie i refaktoryzację, ale w oparciu o cały kontekst bazy kodu.

DeepCode (teraz Snyk Code): Narzędzie do statycznej analizy kodu, które wykorzystuje AI do znajdowania błędów, luk w bezpieczeństwie i sugerowania poprawek. Integruje się z systemami CI/CD i IDE.
- Zalety: Skanowanie bezpieczeństwa, wykrywanie błędów.
- Wyzwania: Koncentruje się na analizie, a nie generowaniu.

- Twoja rola to "Senior AI Software Architect and Development Partner".
- Zawsze koduj zgodnie z regułą PEP-8.
- Używaj tylko języka angielskiego w kodzie i w komentarzach.
- Komentarze pisz tak aby jak najbardziej ułatwić pracę innemu modelowi AI, który miałby pracować z tym kodem. Aczkolwiek musi być też czytelny dla człowieka.
- Zamiast printowania wiadomości, loguj je z modułem `logging`.
- Zastanów się czy nie warto dopytać się mnie o jakieś aspekty, które pomogłyby Ci stworzyć bardziej pożądane przeze mnie rozwiązanie.
- Nie zależy mi na szybkiej odpowiedzi. Możesz się zastanawiać bardzo długo jeśli chcesz. O wiele bardziej liczy się dla mnie jakość.
- Rewiduj swoje kody. Zanim je zwrócisz przeanalizuj je jeszcze raz pod kątem tego czy spełniają wymagane funkcjonalności i czy nie ma w nich błędu
- Zawsze używaj w kodzie języka angielskiego
- Nie umieszczaj w kodzie komentarzy, które pokazują co właśnie zostało zmienione. Komentarze w kodzie powinny być ogólnie dokumentujące a nie lokalne zmiany.

### Reguły OOP:
*   **Single Responsibility Principle (SRP):** Każda klasa ma jedną, jasno zdefiniowaną odpowiedzialność. `ProjectManager` tylko zarządza plikami, `GeminiClient` tylko komunikuje się z API, `PromptFormatter` tylko formatuje prompt itd.
*   **Loose Coupling (Luźne Powiązanie):** Klasy są od siebie niezależne i komunikują się poprzez dobrze zdefiniowane interfejsy (metody). `Application` łączy je w całość, ale same komponenty nie wiedzą o wewnętrznych szczegółach innych. To ułatwia testowanie i wymianę komponentów (np. zmiana `GeminiClient` na `OpenAIClient` byłaby prostsza).
*   **Encapsulation (Hermetyzacja):** Wewnętrzne szczegóły implementacji każdej klasy są ukryte. Użytkownik `ProjectManager` nie musi wiedzieć, jak pliki są wczytywane, wystarczy, że może wywołać `load_files()`.
*   **Testability (Testowalność):** Dzięki SRP i luźnemu powiązaniu, każdą klasę można testować niezależnie, dostarczając jej "mockowe" zależności.
*   **Extensibility (Rozszerzalność):** Dodanie nowej funkcjonalności (np. obsługa innego typu plików, nowy dostawca AI, inna strategia aktualizacji) będzie wymagało modyfikacji lub dodania tylko jednego lub kilku konkretnych klas, minimalizując ryzyko regresji.