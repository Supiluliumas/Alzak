# Kontrakt: ovládání a prezentační vrstva

**Vazba**: FR-003, FR-005…FR-010 · Princip VII · SC-019

Aplikace je ovladatelná **výhradně klávesnicí** (FR-005, A-008). Myš, dotyk ani
herní ovladače nejsou v rozsahu.

## Herní klávesy

| Klávesa | Akce | Kde platí | Vazba |
|---------|------|-----------|-------|
| `←` | pohyb doleva | PLAY | FR-006 |
| `→` | pohyb doprava | PLAY | FR-006 |
| obě šipky současně | žádné zrychlení | PLAY | Edge Case |
| `Mezerník` | skok (držením vyšší) | PLAY | FR-007, FR-014 |
| `X` | souvislý laser po dobu držení | PLAY | FR-008 |
| `Escape` | pauza | PLAY | FR-009 |
| `R` | restart aktuálního prostředí | PLAY | FR-010 |
| `F11` | okno ↔ fullscreen | **kterýkoli stav** | FR-003 |

## Klávesy v menu a překryvech

| Klávesa | Akce |
|---------|------|
| `↑` / `↓` | výběr položky |
| `Enter` / `Mezerník` | potvrzení položky |
| `Escape` | v PAUSE = Pokračovat; v TITLE/FINISH/GAMEOVER bez efektu (A-006) |

Escape **nikdy** neukončí aplikaci. Aplikaci ukončí pouze položka „Ukončit"
na úvodní nebo závěrečné obrazovce, případně systémové zavření okna (FR-083).

## `InputSnapshot` — hranice mezi pygame a simulací

`core/input.py` převede stav klávesnice na čistý datový objekt. Simulace
**nikdy** nevidí `pygame.key` ani kód klávesy (Princip V):

```python
@dataclass(frozen=True)
class InputSnapshot:
    left: bool
    right: bool
    jump_pressed: bool      # hrana v tomto snímku
    jump_held: bool         # stav držení
    fire_held: bool
```

Přemapování klávesy je pak změna na jednom místě a testy simulace se jí nedotknou.

## Prezentační kontrakt (Princip VII, FR-002, SC-019)

```python
def compute_viewport(window_w: int, window_h: int) -> tuple[float, tuple[int, int], tuple[int, int]]:
    """Vrací (scale, dst_size, offset). Čistá funkce — testovatelná bez okna."""
```

```text
scale  = min(window_w / 1920, window_h / 1080)      # bez horní i dolní meze
dst    = (round(1920 * scale), round(1080 * scale))
offset = ((window_w - dst[0]) // 2, (window_h - dst[1]) // 2)
```

Povinné testovací vstupy:

| Okno | Očekávané chování |
|------|-------------------|
| 1920×1080 | scale 1.0, offset (0, 0), žádné pruhy |
| 1280×720 | scale 0.666…, offset (0, 0) |
| 3840×2160 | scale 2.0 — **zvětšení** (OD-005) |
| 2560×1080 (ultrawide) | scale 1.0, **pillarbox** vlevo a vpravo |
| 1600×1200 (4:3) | scale 0.833…, **letterbox** nahoře a dole |

`compute_viewport` a blit s `letterbox_color` jsou **jediné** místo v celém kódu,
které zná velikost okna. Herní logika ji nikdy nečte.

## F11 (FR-003, US4 scénář 4)

Přepnutí mění pouze `pygame.display.set_mode(...)`. Logický `Surface` 1920×1080
zůstává týmž objektem, takže rozmístění objektů se z definice nezmění.
