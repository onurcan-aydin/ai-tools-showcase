# Product Feedback Analyzer

This Python script analyzes customer feedback using the Claude API to identify key themes and suggest actionable improvements.

## Features

- Analyzes customer feedback to identify top themes
- Generates specific action items with priorities
- Supports both single feedback entries and multiple feedback entries
- Structured JSON output for easy integration

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your Claude API key as an environment variable:
```bash
export CLAUDE_API_KEY='your-api-key-here'
```

## Usage

1. Run the script with example feedback:
```bash
python feedback_analyzer.py
```

2. To analyze your own feedback, modify the `example_feedback` list in the `main()` function with your feedback entries.

## Example Output

The script will output:
- Top 3 themes identified from the feedback
- 3-5 specific action items with priorities and rationales

## Customization

You can modify the prompt in the `analyze_feedback` method to change how Claude analyzes the feedback or to request different types of insights.

## Error Handling

The script includes basic error handling for API calls and will display appropriate error messages if something goes wrong. 