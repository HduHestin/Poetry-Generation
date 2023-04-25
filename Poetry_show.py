import re


def poems_show(poems):
    for i in poems:
        print(i)
        print('\n')


def poetry_show(poetry):
    pattern = r"([，。；？])"
    poems = []
    text = re.sub(pattern, r'\1 ', poetry)
    for p in text.split():
        if p:
            poems.append(p)
    poems_show(poems)
    return poems
