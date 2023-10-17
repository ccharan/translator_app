from deep_translator import GoogleTranslator


def translate_text(source, target, text):
    translated = GoogleTranslator(source=source, target=target).translate_batch([text])
    return translated
