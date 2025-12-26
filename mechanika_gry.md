# Mechanika Gry "Szybkie skoki"

Ten dokument opisuje techniczne aspekty działania gry, w tym algorytmy generowania poziomów i interakcje obiektów.

## 1. Generowanie Platform (Klocków)

Gra wykorzystuje system proceduralnego generowania nieskończonego poziomu. 

*   **Inicjalizacja**: Na początku gry tworzona jest lista startowa platform.
*   **Proceduralne dodawanie**: Kiedy liczba platform spada poniżej 6 (np. gdy stare wypadną poza ekran), gra generuje nowe.
*   **Algorytm**:
    1.  Znajdowana jest platforma najbardziej wysunięta na prawo.
    2.  Nowa platforma tworzona jest w losowej odległości w prawo (`delta_x`) oraz losowej wysokości (`delta_y`) względem poprzedniej.
    3.  Zapewnia to, że klocki układają się w "ścieżkę" prowadzącą w prawo i (zazwyczaj) w górę, symulując wspinaczkę.
*   **Znikające Klocki**: Każda nowo wygenerowana platforma otrzymuje losowy czas życia (od 4 do 7 sekund). W miarę upływu czasu platforma zmienia kolor z zielonego na czerwony, a po upływie czasu jest usuwana z gry (`kill()`).

## 2. Trampoliny (Niebieskie)

*   **Generowanie**: Przy tworzeniu nowej platformy istnieje 10% szans, że pojawi się na niej trampolina.
*   **Działanie**: Trampolina wybija gracza w górę ze zwiększoną siłą (mnożnik 1.3x siły skoku).
*   **Logika kolizji**: Sprawdzanie kolizji z trampolinami odbywa się **przed** sprawdzaniem kolizji z platformami. Dzięki temu gracz nie "przykleja się" do platformy pod trampoliną, ale od razu się odbija.

## 3. Przeszkody (Czerwone)

*   **Generowanie**: Przy tworzeniu nowej platformy istnieje 15% szans, że pojawi się na niej przeszkoda.
*   **Działanie**: Dotknięcie przeszkody kończy grę (Game Over).
*   **Pozycjonowanie**: Przeszkody są zawsze centrowane na środku platformy, na której się pojawiły.

## 4. Przesuwanie Kamery (Scrolling)

Gra nie posiada tradycyjnej kamery, lecz przesuwa cały świat gry względem gracza:

*   **W prawo**: Gdy gracz przekroczy połowę szerokości ekranu, wszystkie obiekty (platformy, przeszkody, trampoliny) są przesuwane w lewo.
*   **W górę**: Gdy gracz znajdzie się w górnej ćwiartce ekranu (wysokość < HEIGHT / 4), świat przesuwa się w dół, dając iluzję wspinaczki.
*   **Punktacja**: Przesunięcie świata w poziomie jest doliczane do wyniku gracza.

## 5. Fizyka i Kolizje

*   **Grawitacja**: Na gracza stale działa siła grawitacji ciągnąca go w dół.
*   **Skoki**: Skok jest możliwy tylko, gdy gracz stoi na platformie, chyba że odbije się od trampoliny.
*   **Kolizje**: Wykrywane są tylko, gdy gracz spada (prędkość w dół > 0), co pozwala na wskakiwanie na platformy od dołu (tzw. one-way platforms).
