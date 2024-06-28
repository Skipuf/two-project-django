from django import template

register = template.Library()

forbidden_words = [
    "нейросет",
    "знаменит",
]


def contains_forbidden_words(text) -> str:
    for word in forbidden_words:
        if word in text.lower():
            return f"{text[0]}{'*' * (len(text) - 1)}"
    return text


@register.filter()
def censor(value):
    ms = ""
    for item in value.split():
        ms += f"{contains_forbidden_words(item)} "
    return ms
