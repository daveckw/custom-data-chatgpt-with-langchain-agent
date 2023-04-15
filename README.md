# GPT-3.5-turbo Chatbot with Document Search Index

A chatbot powered by OpenAI's GPT-3.5-turbo model that uses a document search index to answer user queries based on provided documents. This chatbot is implemented using the `langchain` library for managing chat models and the `llama_index` library for handling the search index.

## Prerequisites

Ensure you have the following installed:

- Python 3.6 or newer
- `openai`, `langchain`, and `llama_index` libraries
- A valid OpenAI API key
- A search index JSON file (index.json) in the working directory

## Installation

1. Clone the repository:

`clone https://github.com/your-username/your-repo.git
`

2. Install the required libraries:

`
pip install openai langchain llama_index
`

3. Add your OpenAI API key to a `.env` file in the working directory:

`
OPENAI_API_KEY=your_api_key_here
`

## Usage

1. Run the script:

`
python your_script_name.py
`

2. Enter your questions at the prompt. The chatbot will respond accordingly. Type "quit" to exit the loop.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

