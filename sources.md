
# Odniesienia do zasobów, dokumentacji, samouczków oraz agentów AI

## Zasoby:

- czcionka: 
  - Space Bd BT https://blogfonts.com/space-4.font
- bolidy: 
  - https://www.freepik.com/free-vector/collection-formula-1-cars_2723962.htm#fromView=search&page=5&position=0&uuid=ff992e69-6859-419f-8549-ecff6bdf2cf2
- flagi, światła, puchar: 
  - https://www.freepik.com/free-vector/formula-1-element-collection_2638223.htm#fromView=search&page=6&position=24&uuid=ff992e69-6859-419f-8549-ecff6bdf2cf2
- tory:
  - https://freesvg.org/race-circuit-hungaroring-hungary
  - https://freesvg.org/race-circuit-interlagos
  - https://freesvg.org/race-circuit-monza
- linia mety:
  - https://www.vecteezy.com/vector-art/13867920-top-view-of-race-track-with-start-and-finish-line

Powyższe zasoby wykorzystałem jako bazę do stworzenia swoich obrazków. Po pobraniu pracowałem w programach
graficznych (inkscape, gimp), aby dostosować obrazki do moich potrzeb.

## Dokumentacja

- https://docs.python.org/3/
- https://pyga.me/docs/

Z dokumentacji korzystałem na różnych etapach, sprawdzając zastosowanie niektórych funkcji w celu zrozumienia ich działania.

*Data ostatniego dostępu do materiałów: 1.02.2025*

## Samouczki

- pygame car racing tutorial:
  - https://www.youtube.com/watch?v=L3ktUWfAMPg
  - https://www.youtube.com/watch?v=WfqXcyF0_b0
  - https://www.youtube.com/watch?v=V_B5ZCli-rA
  - https://www.youtube.com/watch?v=agnVylvZ038

W powyższego tutorialu zaczerpnąłem podstawowe pojęcia i zagadnienia związanie z wykorzystaniem modułu pygame,
jak również podstawową logikę ruchu pojazdu sterowanego przez gracza oraz komputer.

Na późniejszym etapie prac dość znacząco rozbudowałem istniejące klasy, dodając nowe funkcjonalności, pola i parametry.
Rozdzieliłem logikę gry od głównego pliku, dodałem obsługę ustawień, menu, zbieranie wyników, 
wyświetlanie najlepszych wyników.

Powyższy materiał stanowił jedynie bazę pod implementację moich pomysłów.

*Data ostatniego dostępu do materiałów: 13.01.2025*

- ### menu 
  - menu in game:
    - https://www.youtube.com/watch?v=GMBqjxcKogA
  - making buttons:
    - https://www.youtube.com/watch?v=al_V4OGSvFU
    - 
Z powyższych tutoriali wykorzystałem funkcje tworzenia, zmiany kolorów i warunki logiczne "klikania" dla przycisków,
a także sposób wyświetlania menu jako nadpisywanie obrazu.

Na późniejszym etapie prac zaktualizowałem niektóre funkcje, aby lepiej spełniały funkcjonalności, które chciałem osiągnąć.
Dodatkowo zmodyfikowałem kod tak, aby był możliwie reużywalny.

*Data ostatniego dostępu do materiałów: 19.01.2025*

    - user input text:
        - https://www.geeksforgeeks.org/how-to-create-a-text-input-box-with-pygame/

- AI 
  - Copilot in Edge (przeglądarka w wersji 132.0.2957.127 (64-bity))

Poniżej wklejam mój prompt i odpowiedź agenta - została ona przeze mnie wykorzystana w celu upłynnienia
ścieżki komputerowego gracza, aby jego ruch był bardziej płynny. Oczywiście dobrałem jeszcze parametry, aby osiągnąć
zamierzony przeze mnie efekt w stopniu zadowalającym.

Prompt:
> having such code:
 ```python
        self.path = self.TRACK_1_PATH
        self.current_point = 0
        self.vel = max_vel
        self.img = pygame.transform.rotate(img, -90)
        self.x, self.y = start_pos

    def move_towards(self, target_x: float, target_y: float) -> None:
        # calculate the direction vector
        direction = (target_x - self.x, target_y - self.y)
        distance = math.hypot(*direction)

        if distance != 0:
            direction = (direction[0] / distance, direction[1] / distance)
            self.angle = math.degrees(math.atan2(-direction[1], direction[0]))

        # Move towards the target
        self.x += direction[0] * self.vel
        self.y += direction[1] * self.vel

    def update_path_point(self, smooth_path: list[tuple[float, float]]) -> None:
        if self.current_point < len(smooth_path):
            target_x, target_y = smooth_path[self.current_point]
            self.move_towards(target_x, target_y)
            if math.hypot(target_x - self.x, target_y - self.y) < 5:
                self.current_point += 1

    def draw(self, window: pygame.display) -> None:
        self.update_path_point(self.smooth_path())
        super().draw(window)

        # # use of helper function to display path points
        # self.draw_points(window)

    # function to interpolate path with cubic splines to make more smooth path
    def smooth_path(self) -> list[tuple[float, float]]:
        # extract x and y coordinates from points in path
        pos_x, pos_y = zip(*self.path)

        # Interpolate with cubic splines
        t = numpy.linspace(0, 1, len(self.path))
        cs_x = CubicSpline(t, pos_x)
        cs_y = CubicSpline(t, pos_y)
        smooth_t = numpy.linspace(0, 1, 100)

        return list(zip(cs_x(smooth_t), cs_y(smooth_t)))
```
> make changing direction more smooth - right now there are instant changes which look not right
Copilot powiedział
To make direction changes smoother and avoid sudden movements, you can add a gradual adjustment to the direction vector before applying it. This technique is often called "smoothing" or "interpolation" of the direction changes. Here’s an updated version of your code to achieve smoother transitions:

Odpowiedź:

```python
import pygame
import math
import numpy
from scipy.interpolate import CubicSpline

class Vehicle:
    def __init__(self, img, start_pos, max_vel, path):
        self.path = path
        self.current_point = 0
        self.vel = max_vel
        self.img = pygame.transform.rotate(img, -90)
        self.x, self.y = start_pos
        self.angle = 0
        self.smooth_direction = (0, 0)  # Initialize smooth direction

    def move_towards(self, target_x: float, target_y: float) -> None:
        # calculate the direction vector
        direction = (target_x - self.x, target_y - self.y)
        distance = math.hypot(*direction)

        if distance != 0:
            direction = (direction[0] / distance, direction[1] / distance)
            self.angle = math.degrees(math.atan2(-direction[1], direction[0]))

            # Smoothly adjust direction vector
            smooth_factor = 0.1  # Adjust this factor to control smoothness
            self.smooth_direction = (
                self.smooth_direction[0] + smooth_factor * (direction[0] - self.smooth_direction[0]),
                self.smooth_direction[1] + smooth_factor * (direction[1] - self.smooth_direction[1])
            )

        # Move towards the target using smooth direction
        self.x += self.smooth_direction[0] * self.vel
        self.y += self.smooth_direction[1] * self.vel

    def update_path_point(self, smooth_path: list[tuple[float, float]]) -> None:
        if self.current_point < len(smooth_path):
            target_x, target_y = smooth_path[self.current_point]
            self.move_towards(target_x, target_y)
            if math.hypot(target_x - self.x, target_y - self.y) < 5:
                self.current_point += 1

    def draw(self, window: pygame.display) -> None:
        self.update_path_point(self.smooth_path())
        # Draw your vehicle here, e.g., blit the image onto the window
        # window.blit(self.img, (self.x, self.y))
        super().draw(window)

        # Uncomment the following line to display path points if needed
        # self.draw_points(window)

    def smooth_path(self) -> list[tuple[float, float]]:
        # extract x and y coordinates from points in path
        pos_x, pos_y = zip(*self.path)

        # Interpolate with cubic splines
        t = numpy.linspace(0, 1, len(self.path))
        cs_x = CubicSpline(t, pos_x)
        cs_y = CubicSpline(t, pos_y)
        smooth_t = numpy.linspace(0, 1, 100)

        return list(zip(cs_x(smooth_t), cs_y(smooth_t)))
```

> Here, I introduced a smooth_direction vector that gradually adjusts to the current direction vector over time using a smooth_factor. 
> Adjusting the smooth_factor will allow you to control the smoothness of the direction changes. A smaller value will result in smoother transitions,
> while a larger value will make the changes more abrupt.
>
> This should help reduce the sudden changes and create smoother movements for your vehicle. 
> Let me know if you have any more questions!

*Data ostatniego dostępu do materiałów: 14.01.2025*

## Użyte moduły

Nazwy i wersje wykorzystywanych w projekcie modułów python zostały zawarte w pliku requirements.txt

## Własne implementacje

- utworzenie modułów zawierających:
  - logikę [gry](game.py),
  - klasy [graczy](cars.py),
  - widoki [menu](menu.py),
  - logikę danych wykorzystywanych przez grę, a które gracz może zmieniać jako [ustawienia](settings.py)
  - funkcje i klasy reaużywalne, wykorzystywane przez inne moduły, zebrane w jednym pliku [utils](utils.py)
  - [obrazy](images.py), wykorzystywane w grze
- uwzględnianie dodatkowych elementów w trakcie gry i wyświetlanie informacji na ekranie
- odliczanie do startu,
- "odradzanie się" w konkretnej pozycji przy próbie wyjechania poza granicę ekranu gry,
- zliczanie kolejnych pokonywanych okrążeń,
- zapisywanie czasu pokonanych okrążeń oraz liczenie czasu sumarycznego,
- wyświetlanie dodatkowych komunikatów na ekranie w związku z wystąpieniem różnych eventów, 
- zapisywanie wyniku do pliku csv,
- odczyt danych z pliku csv i wyświetlenie ich w menu z najlepszymi wynikami,
- wybór ustawień, 
- podgląd na wybrany bolid i tor
- obsługa kar za ścinanie zakrętów bądź długie pozostawanie poza torem,
- wprowadzenie współczynnika prędkości, różnicującego bolidy, ale również wpływającego na ostateczny wynik, 
- znajdowanie i wyświetlanie najlepszego okrążenia, 
- tworzenie ekranu z wynikami po zakończeniu wyścigu,
- wprowadzenie możliwości wyboru parametrów gry (ustawień), 
- możliwość wyboru między różnymi bolidami czy torami.
- opracowanie grafik na podstawie pobranych materiałów