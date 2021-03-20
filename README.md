# Flower-parser

Скрипт для парсинга сайта цветов floristan.ru

## Описание

Парсер сохраняет информацию о букетах в json файл. Структура файла:

```json
[
    {
        "title": "Букет  Вдохновение",
        "sizes": [
            {
                "size": "SMALL",
                "price": 2826,
                "flowers": [
                    {
                        "title": "Гвоздика",
                        "count": 3
                    },
                    {
                        "title": "Ирис синий",
                        "count": 5
                    },
                    {
                        "title": "Роза 60 см",
                        "count": 5
                    },
                    {
                        "title": "Статица",
                        "count": 1
                    },
                    {
                        "title": "Писташ",
                        "count": 3
                    },
                    {
                        "title": "Оформление",
                        "count": 1
                    }
                ]
            },
            {
                "size": "MIDDLE",
                "price": 4423,
                "flowers": [
                    ...
                ]
            },
            {
                "size": "BIG",
                "price": 7031,
                "flowers": [
                   ...
                ]
            }
        ]
    }
]
```

## Требования

- Python3.8+

## Установка

```bash
git clone https://github.com/Safintim/flower-parser.git
cd flower-parser
pip install -r requirements.txt
```

## Использование

В текущей директории создаст bouquets.json с результатом
```bash
python main.py
```

Создаст ~/home/bouquets_12_03_2021.json с результатом
```bash
python main.py -d ~/home -n bouquets_12_03_2021
```

