# cs2-server-admin-callouts

[![CI](https://github.com/sink3x/cs2-server-admin-callouts/actions/workflows/ci.yml/badge.svg)](https://github.com/sink3x/cs2-server-admin-callouts/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/sink3x/cs2-server-admin-callouts)](https://github.com/sink3x/cs2-server-admin-callouts/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[English](README.md) · Русский

**Позиции callouts для 10 карт Counter-Strike 2** с названиями мест на **английском, русском, немецком и французском**. Это данные страницы «Callouts» проекта
**[cs2-server-admin-panel](https://github.com/sink3x/cs2-server-admin-panel)**, вынесенные в отдельный репозиторий, чтобы ими мог пользоваться любой.

| Карты | Dust II, Mirage, Inferno, Nuke, Overpass, Ancient, Anubis, Train, Vertigo, Cache |
|---|---|
| Языки | `en` (официальное название), `ru`, `de`, `fr` |
| Основной файл | `callouts.json` (около 18 КБ) |
| Лицензия | MIT для данных, кода и переводов (про радары см. [Картинки](#картинки)) |

## Два набора данных

| | Где | Позиции заданы в кадре | Картинки |
|---|---|---|---|
| **Основной** (его использует панель) | `callouts.json` | **радаров** CS2 проекта [Boltobserv](https://github.com/boltgolt/boltobserv) | **не лежат в этом репозитории** (см. ниже) |
| **Схемы** (набор с чистой лицензией) | `schematic/` | **нашей собственной схемы** проходимой геометрии (вид сверху на навигационную сетку, цвет это высота) | `schematic/maps/*.webp`, MIT |

Набор «схемы» полностью воспроизводится из файлов `schematic/data` (это проверяет тест) и не содержит материалов Valve. Берите его, если нужны картинки, которые можно свободно распространять.

## Формат `callouts.json`

Строка места: `[имя_en, x, y, сторона, рядом, этаж]`.

| Поле | Смысл |
|---|---|
| `имя_en` | Официальное английское название места из навигации карты; по нему в `names` лежат `ru` / `de` / `fr` |
| `x`, `y` | Позиция в кадре картинки карты, приведённом к `0..1000` |
| `сторона` | `t`, `ct` или `m` (середина): к чьей половине ближе |
| `рядом` | `a`, `b` или `m`: к какой точке закладки ближе |
| `этаж` | `-1` один уровень, иначе `0` низ, `1` середина, `2` верх (для карт с большим перепадом высот) |

У карты: `box` это `[x, y, размер]`, квадрат кадра `0..1000` с игровой зоной (панель обрезает радар по нему); `fit` (0..1) показывает, насколько области мест из CS:GO совпали с геометрией CS2 после автоматического сдвига и масштаба;
`conf` это `high` (>= 0.85), `mid` (>= 0.75) или `low`.

> **Точность.** Названия и области взяты из навигации CS:GO и автоматически подогнаны под CS2. На сильно переработанных картах (Train, Inferno, Cache) позиции **приблизительные**, об этом говорит `conf`. Это ориентир, а не линейка.

## Картинки

Основной набор рассчитан на рисование поверх радаров **Boltobserv** (`src/maps/<карта>/radar.png`, 1536x1536). Это радары Valve в том виде, как их распространяет Boltobserv под **GPL-3.0** (Ancient и Anubis: MIT, от Lexogrine);
мы их в этот репозиторий **не копируем**. [cs2-server-admin-panel](https://github.com/sink3x/cs2-server-admin-panel) везёт уменьшенные копии и описывает их происхождение в `app/admin/public/callouts/NOTICE.md`. Права на исходные изображения принадлежат Valve Corporation.

## Пересборка и тесты

```bash
python3 -m unittest discover -s tests -v      # только стандартная библиотека
python3 schematic/scripts/build.py            # schematic/data + names.py -> schematic/callouts.json
```

Для `render.py` и `places.py` (в `schematic/scripts`) нужны `awpy`, `numpy`, `Pillow` и данные карт awpy; как их запускать, написано в начале каждого файла. Переводы лежат в `schematic/scripts/names.py`.

## Участие

Исправления переводов и позиций приветствуются: [CONTRIBUTING.md](CONTRIBUTING.md).

## Лицензия и авторство

[MIT](LICENSE) для кода, данных и переводов. Названия мест и исходные навигационные данные получены через [awpy](https://github.com/pnxenopoulos/awpy) (MIT) из игр Valve; рамки радаров и метаданные карт из [Boltobserv](https://github.com/boltgolt/boltobserv).
Counter-Strike, названия карт и мест принадлежат Valve Corporation; проект с Valve не связан. Если вы правообладатель и хотите что-то изменить, откройте issue.
