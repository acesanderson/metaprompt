from Chain import Prompt, Model, Chain, Response, ChainCache, Verbosity
from Chain.prompt.prompt_loader import PromptLoader
from pathlib import Path
from rich.console import Console
import argparse
import sys

# constants
DIR_PATH = Path(__file__).resolve().parent
PROMPTS_PATH = DIR_PATH / "prompts"
CACHE_FILE = DIR_PATH / ".cache.db"
# prompt loader
loader = PromptLoader(PROMPTS_PATH)
# cache
Model._chain_cache = ChainCache(db_path=CACHE_FILE)


def generate_prompt(task: str) -> str:
    """
    Generate a prompt for a given task.

    This uses Anthropic's massive megaprompt to generate a prompt for a given task.

    Args:
        task (str): The task to generate a prompt for.

    Returns:
        str: The generated prompt.
    """
    metaprompt_string = loader["metaprompt"]
    metamodel_examples_string = loader["metaprompt_examples"]
    metaprompt = Prompt(
        metaprompt_string.prompt_string + metamodel_examples_string.prompt_string
    )
    model = Model("claude")
    chain = Chain(prompt=metaprompt, model=model)
    response = chain.run(input_variables={"TASK": task}, verbose=Verbosity.PROGRESS)
    if not isinstance(response, Response):
        raise ValueError("Response is not of type Response")
    else:
        return str(response.content)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("task", type=str, nargs="?", help="TASK")
    args = parser.parse_args()
    # Grab task from args if exists
    if args.task:
        task = args.task
    # Otherwise, check if a task is being piped into script through stdin
    elif not sys.stdin.isatty():
        context = sys.stdin.read()
        # We add this as context to the query
        task = f"\n<context>\n{context}</context>"
    # Otherwise, use the example task.
    else:
        task = loader["example_task"].prompt_string
    # Build our string
    metaprompt = generate_prompt(task)
    print(metaprompt)


if __name__ == "__main__":
    main()
