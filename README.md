# Excel to Email Generator

A Python application that reads data from an Excel spreadsheet row by row and generates personalized emails using OpenAI's GPT models. The application follows a clean layer-based architecture with separation of concerns.

## Architecture

The application is built using a layer-based architecture:

```
src/
├── models/          # Data models and entities
├── config/          # Configuration management
├── data/            # Data access layer (Excel reading)
├── services/        # Business logic layer (OpenAI integration)
└── controllers/     # Orchestration layer (workflow management)
```

### Layers

- **Models Layer**: Defines data structures (`RowData`, `GeneratedEmail`)
- **Config Layer**: Manages application configuration and environment variables
- **Data Layer**: Handles Excel file reading with both batch and streaming options
- **Services Layer**: Integrates with OpenAI API for email generation
- **Controllers Layer**: Orchestrates the entire workflow from reading to generating emails

## Features

- ✅ Read Excel files (.xlsx, .xls) with multiple columns
- ✅ Process data row by row
- ✅ Generate personalized emails using OpenAI GPT models
- ✅ Memory-efficient streaming processing for large files
- ✅ Comprehensive error handling and logging
- ✅ Configurable via environment variables
- ✅ Save generated emails to output file

## Prerequisites

- Python 3.8 or higher
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/peter-atef-wego/my-repo.git
cd my-repo
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
```

4. Edit `.env` file and add your OpenAI API key:
```
OPENAI_API_KEY=your_actual_api_key_here
EXCEL_FILE_PATH=data/input.xlsx
EMAIL_PROMPT_TEMPLATE=Generate a personalized and professional email based on the following data: {data}
```

## Usage

### Prepare Your Excel File

Create an Excel file with your data. Example structure:

| Name       | Email                    | Company        | Product            | Amount |
|------------|--------------------------|----------------|-------------------|--------|
| John Doe   | john.doe@example.com     | Tech Corp      | Software License  | 1000   |
| Jane Smith | jane.smith@example.com   | Innovation Inc | Cloud Service     | 2500   |

A sample file is provided at `data/input.xlsx`.

### Run the Application

```bash
python main.py
```

The application will:
1. Read the Excel file
2. Process each row
3. Generate a personalized email for each row using OpenAI
4. Save all generated emails to `output/generated_emails.txt`
5. Display a summary of the process

### Output

Generated emails are saved in `output/generated_emails.txt` with the following format:

```
================================================================================
ROW NUMBER: 2
--------------------------------------------------------------------------------
[Generated email content]
================================================================================
```

## Configuration

You can customize the application behavior using environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key (required) | - |
| `EXCEL_FILE_PATH` | Path to the input Excel file | `data/input.xlsx` |
| `EMAIL_PROMPT_TEMPLATE` | Template for the email generation prompt | See `.env.example` |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-3.5-turbo` |

## Project Structure

```
my-repo/
├── src/
│   ├── config/              # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── controllers/         # Orchestration layer
│   │   ├── __init__.py
│   │   └── email_controller.py
│   ├── data/               # Data access layer
│   │   ├── __init__.py
│   │   └── excel_reader.py
│   ├── models/             # Data models
│   │   ├── __init__.py
│   │   └── email_models.py
│   ├── services/           # Business logic layer
│   │   ├── __init__.py
│   │   └── email_service.py
│   └── __init__.py
├── data/                   # Input data directory
│   └── input.xlsx          # Sample Excel file
├── output/                 # Output directory (created automatically)
│   └── generated_emails.txt
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore file
└── README.md              # This file
```

## Logging

The application logs to both:
- Console output (stdout)
- Log file: `email_generator.log`

Log levels and formatting can be customized in `main.py`.

## Error Handling

The application includes comprehensive error handling:
- Missing or invalid Excel files
- OpenAI API errors
- Configuration errors
- Individual row processing errors (continues processing remaining rows)

## Development

### Running Tests

(Tests can be added using pytest)

```bash
pytest tests/
```

### Code Style

The code follows PEP 8 style guidelines and uses type hints for better code clarity.

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
### B3 edit
