# Fast Jumps - Mechanika gry (aktualizacja)

Ten plik opisuje aktualne zachowanie gry i algorytm generowania poziomów — treść dopasowana do rzeczywistej implementacji w plikach źródłowych.

## 1. Inicjalne platformy

* Na start gra tworzy kilka stałych platform zdefiniowanych w `PLATFORM_LIST` (w `settings.py`). Każda z nich jest tworzona z domyślną szerokością 100 px i wysokością 20 px.
* Dodatkowo tworzony jest duży "ground" (ziemia) o współrzędnych `x=0`, `y=HEIGHT-40` i szerokości `WIDTH * 2`.

## 2. Proceduralne dodawanie platform

* Kiedy liczba istniejących platform spada poniżej 6, gra generuje nowe platformy po prawej stronie świata.
* Algorytm generowania nowych platform:
  1. Wybierany jest "rightmost" — najbardziej prawy punkt odniesienia spośród platform (zwykle z pominięciem "ziemi", czyli platform z y >= HEIGHT-60).
  2. Obliczana jest pozycja nowej platformy:
     - szerokość: losowo z zakresu 50–99 px (random.randrange(50, 100))
     - x: rightmost.rect.right + losowy gap z zakresu 10–49 px
     - y: rightmost.rect.y - losowy offset z zakresu -20..99 (czyli new_y = old_y - rand)
     - y jest następnie przycinane do granic ekranu: new_y = max(10, min(HEIGHT - 40, new_y)).
  3. Nowa platforma dostaje losowy lifetime (wiek) — domyślnie od 4000 do 7000 ms, ale jest on skracany wraz ze wzrostem punktów (patrz sekcja "Trudność").

## 3. Kruszące się platformy (Crumbling)

* Nowe platformy otrzymują pole `lifetime`.
* Domyślny zakres stworzonych platform to 4000–7000 ms (4–7 s).
* W czasie życia platforma zmienia kolor z zielonego na czerwony i po przekroczeniu czasu jest usuwana (`kill()`).
* Jeśli jest aktywny powerup "Time Freeze", czas starzenia platform jest pauzowany (kod przesuwa `spawn_time` tak, by wiek platformy nie rósł).

## 4. Przedmioty losowe na platformach

Dla każdej nowo wygenerowanej platformy następuje pojedyncze sprawdzenie (kolejne if/elif) — tylko jeden typ przedmiotu może pojawić się w danej losowaniu:

* Obstacle (czerwony 20x20): 10% szans, ale tylko na platformach o szerokości > 60 px.
* Trampoline (niebieska 20x10): ~8% szans.
* Coin (żółty 15x15): ~8% szans; zebranie monety daje +100 punktów i ma efekt tekstu pływającego.
* Powerup (cyjan 15x15): ~4% szans; daje efekt Time Freeze (pauza starzenia platform) przez 5 sekund.

(Uwaga: kod sprawdza warunki w kolejnych elif, więc tylko pierwsza spełniona gałąź zadziała — np. jeśli los wskazał obstacle, żadne inne nie pojawią się na tej platformie.)

## 5. Powerup: Time Freeze

* Po zebraniu powerupa ustawiany jest `powerup_active = True`, `powerup_start = pygame.time.get_ticks()` i `powerup_duration = 5000` (5 sekund).
* W czasie działania powerupa mechanika starzenia platform jest pauzowana (w kodzie platformy kompensują `spawn_time`).
* Interfejs: pasek czasu (cyan) jest rysowany u góry ekranu podczas aktywnego powerupa.

## 6. Progressive difficulty (skalowanie trudności)

* Nowo tworzone platformy mają lifetime zmniejszane wraz ze wzrostem wyniku:
  - Dla każdego pełnego 1000 punktów `score` zmniejszana jest maksymalna/minimalna wartość lifetime o 500 ms.
  - Lifetime jest przycinane: minimalne do 1500 ms, maksymalne do 2500 ms — nigdy nie spadnie poniżej tych wartości.

## 7. Przewijanie i skoring

* Jeśli gracz przejdzie na prawą połowę ekranu (`player.rect.right > WIDTH/2`), cała scena przesuwa się w lewo o `scroll = max(abs(player.vel.x), 2)` pikseli na klatkę. Taki przesuw:
  - przesuwa wszystkie platformy i przedmioty (obstacles, trampolines, coins, powerups),
  - dodaje `scroll` do wyniku (`score += int(scroll)`),
  - usuwa obiekty, które przeszły poza lewą krawędź ekranu (`rect.right < 0`).

* Jeśli gracz wspina się ponad 1/4 wysokości ekranu, scena przesuwa się pionowo (platformy i obiekty schodzą w dół).

## 8. Fizyka i kolizje

* Grawitacja i ruch gracza są zdefiniowane w `sprites.py`.
* Skok (`jump`) działa tylko wtedy, gdy gracz stoi na platformie (detektor kolizji z `platforms`).
* Kolizje z trampoliną sprawdzane są przed kolizjami z platformami, więc odbicie następuje natychmiast.

## 9. Uwagi implementacyjne

* Początkowe platformy mają stałą szerokość 100 px; można to zmienić w kodzie, modyfikując miejsce tworzenia platform w `Game.new()` lub rozszerzając `PLATFORM_LIST` o szerokości.
* "Ziemia" jest wykrywana przy generowaniu kandydatów przez filtr `p.rect.y < HEIGHT - 60`.
* Granice losowania (szerokości platform, gap, zakres zmian wysokości, procenty spawnów, czasy lifeitme) znajdują się bezpośrednio w `game.py` i można je tam zmieniać, aby dostosować trudność i styl rozgrywki.


Jeśli chcesz, mogę: zaktualizować wartości spawnów (np. zwiększyć liczbę monet), uczynić losowanie przedmiotów niezależnym (więcej niż jeden przedmiot na platformie), albo wprowadzić zmienne konfiguracyjne w `settings.py` żeby łatwiej edytować szanse i zakresy — napisz, którą zmianę preferujesz.
