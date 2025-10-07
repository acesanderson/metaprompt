from conduit.sync import Prompt, Model, Conduit, Response, Verbosity
from conduit.cache.cache import ConduitCache
from pathlib import Path
import argparse
import sys
from rich.console import Console

dir_path = Path(__file__).resolve().parent
prompts_path = dir_path / "prompts"
cache_file = dir_path / ".conduit_cache.db"
Model._conduit_cache = ConduitCache(db_path=cache_file)
console = Console(width=100)
Model._console = console
verbose = Verbosity.COMPLETE


def extract_instructions(text: str) -> str:
    """
    Extract instructions from text.
    """
    # We're very meta here, so we have to turn single curly braces into
    # double curly braces so we have proper jinja formatting.
    text = text.replace("{", "{{").replace("}", "}}")
    # Now we extract the instructions
    start = text.find("<Instructions>")
    end = text.find("</Instructions>")
    if start != -1 and end != -1:
        return text[start + len("<instructions>") : end].strip()
    else:
        raise ValueError("No instructions found in the text.")


def main():
    # Our parser
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
        with open(prompts_path / "example_task.jinja", "r") as f:
            task = f.read()
    with open(prompts_path / "metaprompt.jinja", "r") as f:
        metaprompt_string = f.read()
    with open(prompts_path / "metaprompt_examples.jinja", "r") as f:
        metamodel_examples_string = f.read()
    metaprompt = Prompt(metaprompt_string + metamodel_examples_string)
    model = Model("claude")
    conduit = Conduit(prompt=metaprompt, model=model)
    response = conduit.run(input_variables={"TASK": task}, verbose=verbose)
    assert isinstance(response, Response), "Response is not of type Response"
    output = str(response.content)
    instructions = extract_instructions(output)
    console.print(instructions)


if __name__ == "__main__":
    main()
