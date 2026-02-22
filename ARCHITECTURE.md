# Architecture Documentation

## Layer-Based Architecture

This application follows a clean layer-based architecture pattern, ensuring separation of concerns and maintainability.

```
┌─────────────────────────────────────────────────────────────┐
│                         main.py                              │
│                    (Application Entry Point)                 │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   CONTROLLER LAYER                           │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │     EmailGeneratorController                          │  │
│  │  - Orchestrates the entire workflow                   │  │
│  │  - Coordinates between Data and Service layers       │  │
│  │  - Handles batch and streaming processing            │  │
│  └───────────────────────────────────────────────────────┘  │
└──────────────────┬──────────────────┬────────────────────────┘
                   │                  │
        ┌──────────▼──────────┐      │
        │                     │      │
        ▼                     ▼      ▼
┌──────────────┐    ┌──────────────────┐    ┌──────────────┐
│  DATA LAYER  │    │  SERVICES LAYER  │    │ CONFIG LAYER │
│              │    │                  │    │              │
│ ExcelReader  │    │ EmailGeneration  │    │  AppConfig   │
│              │    │    Service       │    │              │
│ - read_all   │    │                  │    │ - API keys   │
│   _rows()    │    │ - generate_email │    │ - Settings   │
│ - streaming  │    │   ()             │    │ - load_config│
│              │    │ - test_connection│    │   ()         │
└──────────────┘    └──────────────────┘    └──────────────┘
        │                     │
        │                     │
        └──────────┬──────────┘
                   │
                   ▼
        ┌──────────────────┐
        │   MODELS LAYER   │
        │                  │
        │  - RowData       │
        │  - GeneratedEmail│
        └──────────────────┘
```

## Data Flow

1. **Configuration Loading**
   ```
   .env file → load_config() → AppConfig object
   ```

2. **Excel Reading**
   ```
   Excel file → ExcelReader → RowData objects
   ```

3. **Email Generation**
   ```
   RowData → EmailGenerationService → OpenAI API → GeneratedEmail
   ```

4. **Full Workflow**
   ```
   main.py
     ↓
   Load Config
     ↓
   Initialize Controller
     ↓
   Read Excel (Data Layer)
     ↓
   For each row:
     ↓
   Generate Email (Service Layer)
     ↓
   Save to File
     ↓
   Display Summary
   ```

## Component Responsibilities

### Models Layer (`src/models/`)
- **Purpose**: Define data structures
- **Components**:
  - `RowData`: Represents a single Excel row
  - `GeneratedEmail`: Represents a generated email with metadata
- **Dependencies**: None (pure data models)

### Config Layer (`src/config/`)
- **Purpose**: Manage application configuration
- **Components**:
  - `AppConfig`: Configuration data model
  - `load_config()`: Load configuration from environment
- **Dependencies**: `python-dotenv`, `pydantic`

### Data Layer (`src/data/`)
- **Purpose**: Handle data access and Excel operations
- **Components**:
  - `ExcelReader`: Read Excel files
    - Batch reading: `read_all_rows()`
    - Streaming: `read_rows_generator()`
- **Dependencies**: `pandas`, `openpyxl`, Models layer

### Services Layer (`src/services/`)
- **Purpose**: Business logic and external API integration
- **Components**:
  - `EmailGenerationService`: OpenAI integration
    - Generate emails: `generate_email()`
    - Test connection: `test_connection()`
- **Dependencies**: `openai`, Config layer, Models layer

### Controllers Layer (`src/controllers/`)
- **Purpose**: Orchestrate workflows
- **Components**:
  - `EmailGeneratorController`: Main workflow orchestrator
    - Batch processing: `process_all_rows()`
    - Streaming: `process_rows_streaming()`
    - File output: `save_emails_to_file()`
- **Dependencies**: Data layer, Services layer, Config layer, Models layer

## Design Patterns

1. **Dependency Injection**: Controllers receive configuration, making them testable
2. **Repository Pattern**: Data layer abstracts Excel reading
3. **Service Pattern**: Business logic encapsulated in services
4. **Model-View-Controller (MVC)**: Adapted for CLI application
5. **Generator Pattern**: Memory-efficient streaming for large datasets

## Error Handling Strategy

- **Data Layer**: Raises exceptions for file not found, invalid format
- **Services Layer**: Returns GeneratedEmail with error field instead of raising
- **Controllers Layer**: Logs errors, continues processing other rows
- **Main Entry**: Catches all exceptions, logs, and exits gracefully

## Extensibility

The architecture makes it easy to:

1. **Add new data sources**: Implement a new reader in Data layer
2. **Switch AI providers**: Replace EmailGenerationService
3. **Add output formats**: Extend controller's save methods
4. **Add validation**: Add validators in Models layer
5. **Add monitoring**: Add middleware in Controller layer

## Testing Strategy

- **Unit Tests**: Test each layer independently
- **Integration Tests**: Test layer interactions
- **End-to-End Tests**: Test full workflow (mocked API)
- **Structure Tests**: Verify imports and basic functionality (see `test_structure.py`)

## Performance Considerations

1. **Memory**: Use streaming for large Excel files
2. **API Rate Limits**: Process one row at a time with delays if needed
3. **Logging**: Configurable log levels to reduce overhead
4. **Caching**: Can add caching layer for repeated data

## Security Considerations

1. **API Keys**: Stored in `.env`, never committed to git
2. **Input Validation**: Excel data validated through Pydantic models
3. **Error Messages**: Don't expose sensitive data in logs
4. **Dependencies**: Regular updates via `requirements.txt`
