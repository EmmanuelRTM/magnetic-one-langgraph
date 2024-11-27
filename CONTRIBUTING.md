# Contributing to magnetic-one-langgraph

Thank you for your interest in contributing to **magnetic-one-langgraph**! We're excited to collaborate with you. This guide will help you get started with contributing to our project, whether it’s fixing a bug, suggesting a feature, or improving documentation.

---

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [How Can You Contribute?](#how-can-you-contribute)
3. [Getting Started](#getting-started)
4. [Development Workflow](#development-workflow)
5. [Issue Reporting Guidelines](#issue-reporting-guidelines)
6. [Pull Request Guidelines](#pull-request-guidelines)
7. [Code Style and Standards](#code-style-and-standards)
8. [Community Support](#community-support)

---

## Code of Conduct
To maintain a welcoming and inclusive environment, all contributors are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please take a moment to review it.

---

## How Can You Contribute?

There are many ways to contribute:
- **Reporting bugs**: Help us improve by identifying and reporting issues.
- **Suggesting features**: Share your ideas to enhance the project.
- **Fixing bugs**: Submit pull requests with fixes for reported issues.
- **Adding features**: Help implement new features or improve existing ones.
- **Improving documentation**: Make our documentation clearer and more user-friendly.
- **Testing**: Test the project and help ensure it works as intended.

---

## Getting Started

### 1. Fork and Clone the Repository
1. Fork the repository by clicking the "Fork" button on the top-right of this page.
2. Clone your fork to your local machine:
   ```bash
   git clone https://github.com/EmmanuelRTM/magnetic-one-langgraph.git
   ```
3. Navigate to the project directory:
   ```bash
   cd magnetic-one-langgraph
   ```

### 2. Install Dependencies and Run the Project Locally
1. Go to [Magnetic One LangGraph Notebook](magnetic-one-langgraph.ipynb) and play the code where you'll need to install last dependencies with the next command that is already pasted in the notebook:

```bash
pip install -U langgraph langchain langchain_openai langchain_experimental
```

2. Copy [.env.example](.env.example) as .env, and add your own API Keys for OPEN AI and TAVILY.

3. Have fun playing with the Notebook.

---

## Development Workflow

### 1. Create a Branch
Create a new branch for your feature or bugfix:
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes
- Follow the [Code Style and Standards](#code-style-and-standards).
- Write clear, self-explanatory code.
- Add or update tests, if applicable.

### 3. Commit Your Changes
Write a meaningful commit message describing your changes:
```bash
git add .
git commit -m "Fix: [Short description of fix or feature]"
```

### 4. Push Your Branch
Push your branch to your fork:
```bash
git push origin feature/your-feature-name
```

### 5. Open a Pull Request
Go to the original repository and open a Pull Request (PR) from your branch to the `main` branch. Ensure your PR includes:
- A clear title and description.
- References to relevant issues (e.g., `Fixes #123`).
- Screenshots or logs (if applicable).

---

## Issue Reporting Guidelines

When reporting a bug:
1. **Search for duplicates**: Check the [issues](https://github.com/EmmanuelRTM/magnetic-one-langgraph/issues) to see if your bug is already reported.
2. **Provide details**: Include:
   - Steps to reproduce.
   - Expected and actual behavior.
   - Screenshots, logs, or error messages.
3. **Environment details**: Include information about your environment:
   - Operating system.
   - Version of the project.

For feature requests, clearly explain:
- The problem you're solving.
- Why the feature is valuable.
- Any ideas for implementation.

---

## Pull Request Guidelines

- Ensure your PR passes all tests (in case we set some).
- Keep PRs focused and concise. Avoid bundling unrelated changes.
- Update documentation, if your changes affect usage or features.
- Be responsive to feedback during the review process.

---

## Code Style and Standards

To maintain consistency, follow these standards:
- Use Python.
- Add comments to explain complex logic.
- Use meaningful variable and function names.
- Test your code.

---

## Community Support

If you have questions or need help:
- Check the [discussions board](https://github.com/EmmanuelRTM/magnetic-one-langgraph/discussions).
- Still we don't have Discord/Slack channel but we'll soon open it!
- Reach out by opening a general inquiry issue.

---

Thank you for contributing to **magnetic-one-langgraph**! Together, we can make this project better for everyone. 💻✨