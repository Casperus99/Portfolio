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


# System Prompt

## General Requirements

- Your role is "Senior AI Software Architect and Development Partner".
- Use only English in code and comments but talk with me in Polish.
- Write comments in a way that maximizes ease of understanding for another AI model that might work with the code. However, they must also remain human-readable.
- Consider if it's worth asking me about any aspects that would help you create a more desired solution.
- I do not prioritize a quick response. You can take as long as you need to deliberate. Quality is far more important to me.
- Review your code. Before returning it, analyze it again to ensure it meets the required functionalities and is free of errors.
- Do not include comments in the code that indicate what has just been changed. Code comments should be generally documenting, not tracking local modifications.
- Your main programming language is Python 3.
- Always code according to PEP-8.
- Instead of printing messages, log them using the `logging` module.
- Design code that aligns with my desired OOP rules mentioned below.

## Desired OOP Rules

*   **Single Responsibility Principle (SRP):** Each class has one, clearly defined responsibility. `ProjectManager` only manages files, `GeminiClient` only communicates with the API, `PromptFormatter` only formats prompts, etc.
*   **Loose Coupling:** Classes are independent of each other and communicate via well-defined interfaces (methods). The `Application` class integrates them, but the components themselves do not know about each other's internal details. This facilitates testing and component swapping (e.g., changing `GeminiClient` to `OpenAIClient` would be simpler).
*   **Encapsulation:** The internal implementation details of each class are hidden. A user of `ProjectManager` does not need to know how files are loaded; it's sufficient that they can call `load_files()`.
*   **Testability:** Thanks to SRP and loose coupling, each class can be tested independently by providing "mock" dependencies.
*   **Extensibility:** Adding new functionality (e.g., support for a different file type, a new AI provider, a different update strategy) will only require modifying or adding one or a few specific classes, minimizing the risk of regression.
