import os

from dotenv import load_dotenv
from gpt4all import GPT4All  # type: ignore

load_dotenv()

GPT4ALL_MODEL = os.getenv('GPT4ALL_MODEL')


def main():
    model = GPT4All(GPT4ALL_MODEL)
    output = model.generate('The capital of France is ', max_tokens=10)
    print(output)
    pass


if __name__ == '__main__':
    main()
