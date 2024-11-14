# Zania Question-Answering Bot

A Question-Answering bot that leverages large language models to answer questions based on document content. Built using FastAPI and LangChain framework.

## Setup & Installation

1. Clone and install dependencies
```bash
git clone <repository-url>
cd zania-qa
poetry install
```

2. Create .env file with your OpenAI API key
```bash
OPENAI_API_KEY=your-api-key-here
```

3. Start the server
```bash
poetry run start
```

## Quick Usage Example

1. Create a questions.json file:
```json
[
    "What are the four main categories of domain-independent challenges for interactive execution monitoring?",
    "How does the system determine the Value of Information (VOI) and Value of Alert (VOA)?",
    "What are the key differences between the SUO EA and UV-Robotics EA implementations?",
    "How does the system avoid overwhelming users with too many alerts?",
    "What are the different types of alerts generated by the SUO EA?"
]
```

2. Send request with your PDF and questions:
```bash
curl -X POST "http://localhost:8000/api/v1/qa" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "document=@/path/to/your/document.pdf" \
     -F "questions=@/path/to/your/questions.json"
```

The API will return responses in this format:
```json
{
  "results": [
    {
      "question": "What are the four main categories...",
      "answer": "The four main categories are..."
    },
    {
      "question": "How does the system determine...",
      "answer": "The system determines VOI and VOA by..."
    }
  ]
}
```

## Development Commands

```bash
# Start server
poetry run start

# Clean cache files
poetry run clean
```

## Tech Stack
- Python 3.9
- FastAPI
- LangChain
- OpenAI GPT Models
- FAISS for vector storage
- Poetry for dependency management

## Project Structure
```
zania-assignment/
├── app/
│   ├── api/
│   ├── core/
│   └── services/
├── tests/
├── .env
├── main.py
└── pyproject.toml
```

## Error Handling
- Invalid file formats
- Missing API keys
- Processing errors
- Invalid question formats

## Limitations
- Supports PDF and JSON files
- Rate limits based on OpenAI API
- Question complexity limited by context window

## Contact
Gourab Sinha - gourab19964u@gmail.com
