
# Wstęp do programowania

## Piotr Andrzejewski

### Nr indeksu: 300873

## Projekt gry wyścigowej - *Formula Champions Racing*

### Główne założenia

- *Formula Champions Racing* to jednoosobowa gra wyścigowa przypominająca wyścigi Formuły 1.
 Gracz wpisuje swoje imię, a następnie wybiera bolid spośród kilku dostępnych wariantów (różnią się one osiągami),
 tor, na którym chce się ścigać oraz ustawienia sesji:
    - liczba okrążeń,
    - liczba i poziom przeciwników,
    - pozycja startowa (do wyboru jest konkretne miejsce, bądź pozycja losowa)
    - zasady wyścigowe:
      - przyznawanie kar za ścinanie zakrętów
      - przyznawanie kar za zderzenia z innymi bolidami
- Po przejechaniu linii mety graczowi przyznawane są punkty w zależności od zajętego miejsca zgodnie z następującym schematem:
  - I miejsce: 10 pkt.
  - II miejsce: 6 pkt.
  - III miejsce: 5 pkt.
  - IV miejsce: 4 pkt.
  - V miejsce: 2 pkt.
  - VI miejsce: 1 pkt.
  - pozostałe miejsca: 0 pkt.
- Podczas wyścigu mierzony jest czas zarówno każdego rozpoczętego okrążenia, jak i czas sumaryczny całego wyścigu.
- Po wyścigu, na podstawie czasu sumarycznego, zajętego miejsca, poziomu przeciwników, wybranych zasad wyścigowych oraz bolidu, graczowi przyznawany jest wynik,
 który trafia na tablicę wyników.
- Na tablicy wyników wyświetlanych jest 10 najlepszych wyników.
