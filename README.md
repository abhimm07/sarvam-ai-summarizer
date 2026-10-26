# Sarvam AI Text Summarizer & Chat Starter

A Python project demonstrating integration with [Sarvam AI](https://sarvam.ai/) foundational models, including chat completions and multilingual text summarization across Indian languages and English.

## Features

- **Model Setup**: Built with the official `sarvamai` SDK.
- **Chat Completion**: Basic starter call using `sarvam-105b-conversations`.
- **Multilingual Summarization**:
  - Multiple styles: `bullet_points`, `concise`, `detailed`, `key_takeaways`.
  - Supports English and Indian languages (Hindi, Tamil, Telugu, Bengali, Marathi, etc.).
  - Command-line interface with `--text` and `--file` support.

## Project Structure

```text
├── .env                # API key configuration (kept private / gitignored)
├── .gitignore          # Ignores .env and virtual environment files
├── requirements.txt    # Project dependencies
├── main.py             # Simple starter chat completion script
└── summarizer.py       # Multilingual text summarization module & CLI
```

## Setup & Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure your API key**:
   Create a `.env` file in the root directory:
   ```env
   SARVAM_API_KEY=your_actual_sarvam_api_key_here
   ```

## Usage

### 1. Test Chat API
```bash
python main.py
```

### 2. Run Text Summarizer

**Default demo summary:**
```bash
python summarizer.py
```

**Summarize custom text into Hindi:**
```bash
python summarizer.py --text "Your text here..." --lang Hindi --style bullet_points
```

**Summarize a file:**
```bash
python summarizer.py --file path/to/document.txt --style concise
```

## License
MIT
