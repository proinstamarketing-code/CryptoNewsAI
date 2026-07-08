MODELS = [

    # Основная модель
    "openai/gpt-oss-120b:free",

    # Резерв 1
    "meta-llama/llama-3.3-70b-instruct:free",

    # Резерв 2
    "qwen/qwen3-next-80b-a3b-instruct:free",

]


def get_models():
    return MODELS


def get_model():
    return MODELS[0]