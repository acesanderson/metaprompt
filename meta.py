from Chain import Prompt, Model, Chain
from pathlib import Path
import argparse
import sys
from rich.console import Console

# set dir_path
dir_path = Path(__file__).resolve().parent
# set up console
console = Console(width=100)

example_task = """
I will use an LLM to help me curate courses from a catalogue of 10,000 courses to best address a topic for a given audience.

I want to give an LLM a detailed curriculum of video courses, typically around 3-8 courses with a full TOC and video-level descriptions. I want it to provide a very nuanced and accurate review of whether it achieves the following:
- covers the right topics
- accurately scaffolds from pre-requisites to new topics
- ccurately scaffolds from beginner to more intermediate topics
 
The review should also mention if a course feels out of place, if the coverage is too redundant in some sections, and whether a topic needs to be added.

Also have the LLM do chain of thought from the perspective of a learner. IF I watch this course, I will learn this. If I watch the next course, I will learn that. and reflecting along the way.
"""

if __name__ == "__main__":
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
        task = example_task
    with open(dir_path / "metaprompt.jinja", "r") as f:
        metaprompt_string = f.read()
    with open(dir_path / "metaprompt_examples.txt", "r") as f:
        metamodel_examples_string = f.read()
    metaprompt = Prompt(metaprompt_string + metamodel_examples_string)
    model = Model("claude")
    chain = Chain(prompt=metaprompt, model=model)
    response = chain.run(input_variables={"TASK": task})
    console.print(response)
