MODELS = [

    # Автоматический выбор любой доступной бесплатной модели
    "openrouter/free",

    # Очень быстрая бесплатная Gemma
    "google/gemma-4-26b-a4b-it:free",

    # GPT OSS
    "openai/gpt-oss-120b:free",

    # Llama
    "meta-llama/llama-3.3-70b-instruct:free",

    # Qwen
    "qwen/qwen3-next-80b-a3b-instruct:free",

]


def get_models():
    return MODELS


def get_model():
    return MODELS[0]