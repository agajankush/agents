# Agents

A Python project for experimenting with OpenAI Agents, FastAPI, and Gradio.

## Overview

This project provides a simple starting point for building applications that leverage OpenAI's agent capabilities, with a web interface powered by Gradio and an API layer using FastAPI. It is designed for Python 3.12+.

## Features

- **OpenAI Agents**: Integrate and experiment with OpenAI's agent framework.
- **FastAPI**: Build robust APIs quickly and efficiently.
- **Gradio**: Create interactive web UIs for your models and agents.
- **PDF Support**: Use `pypdf` to process PDF files.
- **Environment Management**: Use `.env` files for configuration.

## Requirements

- Python 3.12+
- See `pyproject.toml` for all dependencies.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/agajankush/agents.git
   cd agents
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   Or, if using a tool like [uv](https://github.com/astral-sh/uv):

   ```bash
   uv pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Create`.env` and fill in your OpenAI API key and other settings.
