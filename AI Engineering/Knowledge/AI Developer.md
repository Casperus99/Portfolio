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
