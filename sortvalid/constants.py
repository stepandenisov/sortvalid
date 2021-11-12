PATTERN_DCT = {
    "telephone": r'[+]\d-[(]\d{3}[)]-\d{3}-\d{2}-\d{2}',
    "weight": r'[3-9]\d\Z',
    "inn": r'\d{12}\Z',
    "passport_series": r'\d{2} \d{2}\Z',
    "occupation": r'[А-Яа-яЁёA-z- ]+?',
    "age": r'\d{2}\Z',
    "political_views": r'[А-Яа-яЁё ]+?',
    "worldview": r'[А-Яа-яЁё ]+?',
    "address": r'[А-Яа-яЁё0-9- .]+? \d+?'
}
