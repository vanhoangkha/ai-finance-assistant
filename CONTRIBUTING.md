# Contributing to AI Finance Assistant

We love your input! We want to make contributing to AI Finance Assistant as easy and transparent as possible.

## Development Process

We use GitHub to sync code, track issues and feature requests, as well as accept pull requests.

## Pull Requests

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project.

## Report bugs using GitHub's [issue tracker](https://github.com/your-username/ai-finance-assistant/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/your-username/ai-finance-assistant/issues/new).

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Development Setup

1. Clone the repository
```bash
git clone https://github.com/your-username/ai-finance-assistant.git
cd ai-finance-assistant
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp config/.env.example config/.env
# Edit config/.env with your API keys
```

5. Run the application
```bash
streamlit run app.py
```

## Code Style

- Use Python 3.10+
- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Test with different stock symbols and market conditions

## Documentation

- Update README.md if you change functionality
- Add docstrings to new functions
- Update API documentation if needed

## License

By contributing, you agree that your contributions will be licensed under its MIT License.
