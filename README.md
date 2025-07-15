# ai_agent

AI Agent is a [Boot.dev](https://www.boot.dev) project

## Setup
1) [Clone repo locally](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
2) Ensure that [Python 3.x](https://www.python.org/downloads/) is installed
3) Ensure that [uv](https://docs.astral.sh/uv/getting-started/installation/) is installed
4) You will need to set up a [Google Gemini API Key](https://ai.google.dev/gemini-api/docs/api-key) in your local `.env` file

## Usage:
- To run, use the command: `uv run main.py <prompt> --verbose`

## Note:
- This agent has the capability to do the following:
  - List files
  - Get file content
  - Write files
  - Run Python scripts
- As of the writing of this README, these capabilities should be restricted to the `calculator` directory of this project. However, <b>use at your own risk.</b> 
