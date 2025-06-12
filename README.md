# RAG Test Project

This project implements a Retrieval-Augmented Generation (RAG) system with integrations to various enterprise tools.

## Features

- Integration with Slack for communication
- Jira integration for project management
- Vector database using ChromaDB
- OpenAI integration for language model capabilities
- Haystack AI framework for document processing and retrieval

## Pending Integrations

- Confluence integration for documentation and knowledge base access

## Prerequisites

- Python 3.8+
- Docker and Docker Compose
- OpenAI API key
- Slack API credentials
- Jira API credentials

## Installation

1. Clone the repository:
```bash
git clone https://github.com/nicusbonannus/rag-integration.git
cd rag-test-2
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
OPENAI_API_KEY=your_openai_api_key
SLACK_API_TOKEN=your_slack_token
JIRA_API_TOKEN=your_jira_token
```

## Running with Docker

1. Build and start the containers:
```bash
docker-compose up --build
```

## Project Structure

- `app/`: Main application code
- `chroma/`: Vector database storage
- `requirements.txt`: Python dependencies
- `Dockerfile`: Container configuration
- `docker-compose.yml`: Multi-container setup

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 