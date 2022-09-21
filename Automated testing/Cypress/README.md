# Prezentacja Cypress za pomocą Salesforce
Powyższy projekt przedstawia podstawowe użycie frameworka Cypress na przykładzie przetestowania poprawności konwersji obiektu typu "Lead" w systemie Salesforce. Poniżej znajduje się GIF przejściem skryptu od początku do końca.

![Untitled_ Sep 22, 2022 12_28 AM (1)](https://user-images.githubusercontent.com/80170154/191622027-1374e48f-97a5-417e-abd8-522be143fff6.gif)

## Ogólny opis procesu 
1. Zalogowanie na konto Salesforce
2. Stworzenie nowego rekordu typu Lead
3. Otworzenie strony ze szczegółami nowego Leada
4. Przeklikanie domyślnej akcji konwertowania
5. Otworzenie list (odpowiednio kont, kontaktów oraz okazji) i sprawdzenie czy znajdują się w nich rekordy stworzone z pomocą konwersji
6. Usunięcie nowo utworzonego konta co skutkuje usunięcie powiązanego kontaktu i okazji

## Szczegółowy opis procesu 
### 1. Zalogowanie na konto Salesforce
Do wizualizacji wykorzystano Salesforce'owego Orga stworzonego na stronie Trailhead. Do zalogowania wykorzystano metodę ```cy.request()``` z metodą żądania typu **POST**. Najważniejsze pola to *pw* czyli hasło oraz *un* czyli username. Pozwala to na poprawne kontynuowanie działania skryptu w momencie wejścia na odpowiedni adres url. Klasyczne logowanie generuje niestety problemy, takie jak wyłączenie się skryptu zaraz po zalogowaniu.
### 2. Stworzenie nowego rekordu typu Lead
Czynność ta wykonuje się w tle za pomocą ręcznie napisanej funkcji. Jej implementacja wymaga rozszerzenia *JSforce* czyli izomorficznej biblioteki JavaScript wykorzystującej Salesforce API. W tym wypadku skorzystano z jej możliwości do wykonywania operacji CRUD. W wyniku tej czynności zapisywae jest *id* nowego rekordu.
### 3. Otworzenie strony ze szczegółami nowego Leada
Pierwszym widocznym efektem działania skryptu jest otworzenie strony szczegółowej nowo utworzonego Leada za pomocą wcześniej zapisanego *id*.
### 4. Przeklikanie domyślnej akcji konwertowania
Następnie następuje kliknięcie przycisku akcji "Convert" kontynuowane poprzez kliknięcie przycisku o tej samej etykiecie na nowym okienku. W dalszej kolejności spisywane jest *id* nowo utowrzonego konta po czym okienko jest zamykane. Pomiędzy niektórymi przejściami skryptu zastosowano metodę ```cy.wait()``` w celu upewnienia się, że wszystkie komponenty zostały całkowicie wczytane. Niekiedy skrypt próbuje kliknąć w przycisk, który jeszcze się całkowicie nie wygenerował generując błąd.
### 5. Otworzenie list (odpowiednio kont, kontaktów oraz okazji) i sprawdzenie czy znajdują się w nich rekordy stworzone z pomocą konwersji
W celu sprawdzenia czy w wyniku konwersji nowe rekordy rzeczywiście się utworzyły skrypt otwiera kolejne zakładki z listami rekordów. W każdej z nich dostaje się do pierwszego linku w pierwszym wierszu (rekordzie) i sprawdza czy te linki składają się z odpowiednich nazw użytych podczas tworzenia Leada.
### 6. Usunięcie nowo utworzonego konta co skutkuje usunięcie powiązanego kontaktu i okazji
Na końcu skryptu usuwany jest rekord nowego konta za pomocą funkcji analogicznej do tworzenia rekordów. Wykorzystywane jest do tego wcześniej zapisywane *id* tego konta. Reakcją systemu na usunięcie konta jest usunięcie wszystkich pochodnych rekordów czyli kontaktów oraz okazji biznesowych. W ten sposób skrypt nie pozostawia po sobie żadnych testowych rekordów. 

## Ważne pliki
