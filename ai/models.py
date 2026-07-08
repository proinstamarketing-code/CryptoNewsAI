"""
Список моделей OpenRouter.

Порядок имеет значение:
бот будет пробовать модели сверху вниз.
"""

MODELS = [

    # Самая качественная бесплатная модель
    "openai/gpt-oss-120b:free",

    # Очень хорошая резервная
    "meta-llama/llama-3.3-70b-instruct:free",

    # Хорошо пишет текст
    "google/gemma-4-31b:free",

    # Еще одна сильная модель
    "qwen/qwen3-next-80b-a3b-instruct:free",

    # Последний резерв
    "nousresearch/hermes-3-405b-instruct:free",

]


def get_models():
    """
    Возвращает список моделей
    в порядке приоритета.
    """
    return MODELS.copy()


def get_model():
    """
    Совместимость со старым кодом.
    """
    return MODELS[0]