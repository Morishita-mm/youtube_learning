# Folder Structure Proposal

This document outlines the proposed folder structure for the project to ensure maintainability and scalability.

```
.
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── FOLDER_STRUCTURE.md  # This file
├── docs/
│   ├── specification.md
│   └── functions.md
├── src/
│   ├── __init__.py
│   ├── app.py
│   └── modules/
│       ├── __init__.py
│       ├── youtube_handler.py
│       └── gemini_handler.py
└── tests/
    ├── __init__.py
    ├── mock_server.py
    ├── mock_data/
    │   ├── mock_gemini_summary.json
    │   └── mock_youtube_search.json
    └── scripts/
        └── api_test.py
```

## Directory and File Roles

*   **`docs/`**: Stores project documentation (e.g., `specification.md`, `functions.md`).
*   **`src/`**: Contains the main application source code.
    *   `app.py`: The entry point for the Streamlit application.
    *   `modules/`: Houses functionally separated modules (e.g., YouTube handling, Gemini handling).
*   **`tests/`**: Contains test-related files.
    *   `mock_server.py`: The mock server for development.
    *   `mock_data/`: Test data used by the mock server.
    *   `scripts/`: One-off test scripts and helper tools like `api_test.py`.
*   **Root Directory**: Contains project-wide configuration files such as `Dockerfile`, `docker-compose.yml`, etc.
