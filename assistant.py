from functools import wraps
from time import sleep
from openai import OpenAI
from dotenv import load_dotenv
from enum import Enum
from typing import Callable


client = OpenAI()


INSTRUCTIONS = "You are a software engineer. Help with coding in Python and TypeScript"
tools = [{"type": "code_interpreter"}]
model_performant = "gpt-4-1106-preview"
model_normal = "gpt-3.5-turbo-1106"


def createAssistant(name, instructions, tools="", model="gpt-3.5-turbo-1106"):
    try:
        assistant = client.beta.assistants.create(
            name=name,
            instructions=instructions,
            tools=tools,
            model=model,
        )
        return assistant
    except:
        raise ValueError


def createNewThread():
    print("Creating new thread...")
    return client.beta.threads.create()


def addMessageToThread(thread_id, content):
    if not thread_id:
        raise ValueError("addMessageToThread requires a thread_id")

    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content,
    )


def createRun(thread_id: str, assistant_id: str):
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        # instructions=""
    )
    return run


def getAssistant():
    print("Choose an assistant (integer)")
    print("=====Options=====")

    assistants_list = client.beta.assistants.list().data
    for index, assistant in enumerate(assistants_list):
        print(index, f"({assistant.name})")

    target_assistant = int(input("> "))

    if not (target_assistant >= 0 and target_assistant < len(assistants_list)):
        raise ValueError("Provide an integer that maps to an assistant")

    return assistants_list[target_assistant]


def main():
    assistant = getAssistant()
    print("Working with assistant:", assistant.name)
    print("Instructions: ", assistant.instructions)
    print("Model:", assistant.model)
    thread = None
    while True:
        if not thread:
            thread = createNewThread()
        else:
            try:
                print("0 for new thread, 1 to break, or simply enter prompt")
                option = int(input("> "))
            except ValueError:
                print("Enter a valid response")
                continue
            if option == 0:
                thread = createNewThread()
            if option == 1:
                break

        print("Prompt: ")
        message = input("> ")

        addMessageToThread(thread.id, message)
        run = createRun(thread.id, assistant.id)

        ping_counter = 0
        while run.status != "completed":
            if ping_counter % 2 == 0:
                print("Waiting for response...")
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            sleep(2)

        messages = client.beta.threads.messages.list(thread_id=thread.id)
        print(messages.data[0].content[0].text.value)
        print("")
