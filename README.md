# Metaprompt

A command-line tool that generates detailed, structured prompts from high-level task descriptions using a large language model.

## Quick Start

This example runs the tool with the default task. Ensure you have set your Anthropic API key.

```sh
# 1. Clone the repository
git clone https://github.com/your-username/metaprompt-project.git
cd metaprompt-project

# 2. Create a virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install conduit-sync rich

# 3. Set your API key
export ANTHROPIC_API_KEY="your-api-key-here"

# 4. Run the default example
python src/metaprompt/meta.py
```

## Core Value Demonstration

The primary purpose of Metaprompt is to expand a simple task into a set of comprehensive, machine-readable instructions. This is useful for creating detailed prompts for another AI or for standardizing a complex process.

Here is an example of generating instructions for a code-related task by piping a description into the script.

**Command:**

```sh
echo "Create a Python script that takes a directory path and finds the top 10 largest files, printing their path and size in megabytes." | python src/metaprompt/meta.py
```

**Output:**

```text
You are an expert Python developer. Your task is to write a script that performs the following actions:

1.  **Argument Parsing**:
    *   The script must accept one command-line argument: `directory_path`.
    *   Use the `argparse` module to handle this argument.
    *   Provide a helpful description for the argument, e.g., "The path to the directory to scan."

2.  **File Discovery**:
    *   Recursively walk through the `directory_path`.
    *   For each file found, get its absolute path and its size in bytes.
    *   Ignore directories and broken symbolic links.

3.  **Data Storage**:
    *   Store the file paths and their corresponding sizes. A list of tuples or a list of simple objects is appropriate.

4.  **Sorting**:
    *   Sort the collected file data in descending order based on file size.

5.  **Output Formatting**:
    *   Take the top 10 files from the sorted list.
    *   For each of these 10 files, convert its size from bytes to megabytes (MB).
    *   Print a formatted string to the console for each file: `[File Path] - [Size] MB`.
    *   Format the size to two decimal places.

6.  **Error Handling**:
    *   Implement a check to ensure the provided `directory_path` is a valid, existing directory. If not, print an error message and exit gracefully.
    *   Handle potential `PermissionError` exceptions when accessing files or directories, printing a warning to stderr but continuing the scan if possible.

The final output should be a clean list of the top 10 files, ready for user consumption.
```

## Installation and Setup

### Prerequisites

*   Python 3.8+
*   Git

### 1. Clone the Repository

```sh
git clone https://github.com/your-username/metaprompt-project.git
cd metaprompt-project
```

### 2. Install Dependencies

It is recommended to use a virtual environment to manage dependencies.

```sh
# Create and activate the virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install conduit-sync rich
```

### 3. Configure API Key

This tool uses the Anthropic Claude model via the `conduit` library. You must provide an API key as an environment variable.

```sh
export ANTHROPIC_API_KEY="your-api-key-here"
```

## Usage

Metaprompt accepts a task description from three different sources, processed in the following order of priority:

| Method         | Command                                                                            | Description                                                      |
| -------------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| **Argument**   | `python src/metaprompt/meta.py "Your task description"`                            | The task is provided as a single string argument.                |
| **Piped Input**| `echo "Your task" \| python src/metaprompt/meta.py`                                  | The task is piped to the script via standard input.              |
| **Default**    | `python src/metaprompt/meta.py`                                                    | If no argument or piped input is found, a default example task is used. |

