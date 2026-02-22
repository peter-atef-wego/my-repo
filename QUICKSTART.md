# Quick Start Guide

This guide will help you get started with the Excel to Email Generator in just a few minutes.

## Prerequisites

- Python 3.8 or higher
- An OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Configure the Application

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
EXCEL_FILE_PATH=data/input.xlsx
EMAIL_PROMPT_TEMPLATE=Generate a personalized and professional email based on the following data: {data}
```

## Step 3: Prepare Your Excel File

Use the sample file at `data/input.xlsx` or create your own with this structure:

| Name       | Email                  | Company        | Product          | Amount |
|------------|------------------------|----------------|------------------|--------|
| John Doe   | john.doe@example.com   | Tech Corp      | Software License | 1000   |
| Jane Smith | jane.smith@example.com | Innovation Inc | Cloud Service    | 2500   |

You can add any columns you want - the application will include all data when generating emails.

## Step 4: Run the Application

```bash
python main.py
```

The application will:
1. ✓ Read all rows from your Excel file
2. ✓ Generate a personalized email for each row using OpenAI
3. ✓ Save all emails to `output/generated_emails.txt`
4. ✓ Display a summary of the process

## Output

Generated emails will be saved in `output/generated_emails.txt`:

```
================================================================================
ROW NUMBER: 2
--------------------------------------------------------------------------------
Dear John Doe,

I hope this email finds you well. I wanted to reach out regarding the Software
License for Tech Corp...

[Rest of the generated email]
================================================================================
```

## Troubleshooting

### "OPENAI_API_KEY environment variable is required"
- Make sure you've created a `.env` file from `.env.example`
- Make sure your API key is correctly set in the `.env` file

### "Excel file not found"
- Check that your Excel file exists at the path specified in `EXCEL_FILE_PATH`
- Default location is `data/input.xlsx`

### API Rate Limits
- If you have a large Excel file, you might hit OpenAI rate limits
- Consider using `gpt-3.5-turbo` (faster and cheaper) instead of `gpt-4`
- Add delays between requests if needed

## Next Steps

- Check out `examples.py` for different usage patterns
- Read the full `README.md` for detailed documentation
- Customize the `EMAIL_PROMPT_TEMPLATE` in `.env` for your specific needs

## Support

For issues or questions, please check the README.md file or open an issue on GitHub.
