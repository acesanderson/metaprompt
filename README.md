# Metaprompt: Using Claude Metaprompt

This uses the xml-based metaprompt provided by anthropic for Claude, along with the large corpus of examples. This is token-greedy.

## Usage

Describe what you want an LLM to achieve, adding as much detail and context as you can. The script will generate a thorough metaprompt. Note: Claude will assume there are input variables in there, so you will need to leverage them when using the generated prompt.
