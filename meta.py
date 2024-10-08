from Chain import Prompt, Model, Chain
import argparse
import sys

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
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", type=str, help="TASK")
    args = parser.parse_args()
    if args.task:
        task = args.task
    else:
        task = example_task
    with open("metaprompt.jinja", "r") as f:
        metaprompt_string = f.read()
    with open("metaprompt_examples.txt", "r") as f:
        metamodel_examples_string = f.read()
    metaprompt = Prompt(metaprompt_string + metamodel_examples_string)
    model = Model("claude")
    chain = Chain(metaprompt, model)
    response = chain.run(input_variables = {'TASK':task})
    print(response)
