from functools import wraps
from openai import OpenAI
from dotenv import load_dotenv
from enum import Enum
from typing import Callable

load_dotenv()
client = OpenAI()


class Model(Enum):
    GPT3_5 = "gpt-3.5-turbo-1106"
    GPT4 = "gpt-4-1106-preview"


# Cost per 1k tokens
COSTS_FOR_1000 = {Model.GPT3_5.value: 0.003, Model.GPT4.value: 0.04}
COSTS = {
    Model.GPT3_5.value: COSTS_FOR_1000[Model.GPT3_5.value] / 1000,
    Model.GPT4.value: COSTS_FOR_1000[Model.GPT4.value] / 1000,
}


def token_usage(func: Callable) -> Callable:
    """
    Decorates any function that returns a completion object
    """

    def wrapper(*args, **kwargs):
        completion_object = func(*args, **kwargs)
        try:
            print(f"Token usage: {completion_object.usage.total_tokens}")
            print(
                f"Cost: {COSTS[completion_object.model] * completion_object.usage.total_tokens}"
            )
        except AttributeError:
            print("The decorated function must return a completion object")
        return completion_object

    return wrapper


def save_to_db(func: Callable) -> Callable:
    """
    Decorates any function that returns a completion object and saves the token usage to a database
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        completion_object = func(*args, **kwargs)
        if hasattr(completion_object, "usage") and hasattr(
            completion_object.usage, "total_tokens"
        ):
            # Replace with your actual database saving code
            print(
                f"Saving {completion_object.usage.total_tokens} tokens to database..."
            )
        return completion_object

    return wrapper


@token_usage
def get_response(prompt: str):
    GPT_MODEL = Model.GPT3_5

    completion = client.chat.completions.create(
        model=GPT_MODEL.value,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    response = completion.choices[0].message.content

    print(response)

    return completion


get_response("How can I wake up earlier without grogginess in the morning?")
