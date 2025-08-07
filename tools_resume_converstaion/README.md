---
title: career_conversation
app_file: app.py
sdk: gradio
sdk_version: 5.41.0
---
# 🤖 Resume AI Chatbot: Your Personal Digital Twin

---

Ever wished your resume could talk? This Python script brings your professional profile to life as an interactive AI chatbot! Built with **Gradio**, this application allows anyone to converse with your resume and a personalized summary, providing a dynamic and engaging way to showcase your skills, experience, and background.

Perfect for job seekers, freelancers, or anyone looking to create an innovative online presence, this chatbot acts as your digital twin, ready to answer questions about your career in a professional and engaging manner.

## ✨ Features

- **Interactive Chat Interface:** Engage in natural language conversations with your resume and professional summary.

- **Context-Aware Responses:** The AI is grounded in your provided resume (PDF) and a custom summary, ensuring relevant and accurate answers.

- **Self-Correction Mechanism:** An integrated evaluation system (powered by the Gemini API) assesses the quality of responses and can trigger a "rerun" with feedback, improving the chatbot's performance over time.

- **Intelligent Tool Use:** The chatbot can proactively use defined tools to:

  - **Record User Interest:** Capture email addresses and names from interested users.

  - **Log Unanswered Questions:** Keep track of questions it couldn't answer, helping to identify knowledge gaps.

  - **Capture Recruiter Inquiries:** Automatically log job descriptions or inquiries from recruiters.

- **Real-time Notifications:** Utilizes Pushover to send instant notifications when tools are triggered (e.g., a user provides their email, a recruiter sends an inquiry).

- **Professional Persona:** The chatbot is designed to maintain a professional and engaging tone, as if speaking to a potential client or employer.

- **Easy Customization:** Easily swap out your resume and summary files, and define new tools to personalize the chatbot's capabilities.

---

## 🚀 Getting Started

Follow these steps to set up and run your own Resume AI Chatbot.

### Prerequisites

- **Python 3.8+**

- **pip** (Python package installer) or **uv** (recommended for speed)

### Installation

1.  **Clone this repository (or copy the script):**
    If you have a repository, you'd typically clone it here. For a single script, just save the provided Python code.

2.  **Install the required libraries:**
    It's recommended to create a virtual environment to manage dependencies.

    **Using `uv` (recommended with `pyproject.toml` and `uv.lock`):**
    If you have `uv` installed (e.g., `pip install uv`), and since this project includes `pyproject.toml` and `uv.lock` for precise dependency management, you can set up your environment and install dependencies reliably by running:

    ```bash
    uv venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    uv sync
    ```

    This will create a virtual environment and synchronize it with the exact dependencies specified in `uv.lock`.

    **Manual `uv` installation (if not using `pyproject.toml` or `uv.lock`):**
    If for some reason you are not using the `pyproject.toml` and `uv.lock` files, you can manually install the dependencies:

    ```bash
    uv venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    uv pip install python-dotenv openai pypdf gradio pydantic requests
    ```

    **Using `pip`:**
    Alternatively, you can use `pip`:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install python-dotenv openai pypdf gradio pydantic requests
    ```

### Configuration

1.  **Create a `.env` file:**
    In the same directory as your Python script, create a file named `.env`. This file will store your API keys and Pushover credentials securely.

    Add your OpenAI API key, Google API key (for Gemini evaluation), and Pushover credentials to this file:

    ```
    OPENAI_API_KEY="your_openai_api_key_here"
    GOOGLE_API_KEY="your_google_api_key_here"
    PUSHOVER_USER="your_pushover_user_key_here"
    PUSHOVER_TOKEN="your_pushover_api_token_here"
    ```

    **Important:** Replace the placeholder values with your actual API keys and Pushover credentials. If you don't have Pushover, you can leave these blank, but the notification feature will not work.

2.  **Prepare your Resume and Summary:**

    - Place your resume PDF file (e.g., `Ashutosh_Gajankush.pdf`) in a directory accessible by the script (e.g., `ashutosh/Ashutosh_Gajankush.pdf`).

    - Create a text file with a summary of your background/LinkedIn profile (e.g., `summary.txt`) and place it in a directory accessible by the script (e.g., `ashutosh/summary.txt`).

    **Adjust the file paths in the script** if your files are located elsewhere:

    ```python
    reader = PdfReader("../data/resume/Ashutosh_Gajankush.pdf") # Update this path
    # ...
    with open("../data/resume/summary.txt", "r", encoding="utf-8") as f: # Update this path
    ```

3.  **Set your Name:**
    Update the `name` variable in the script to your actual name:

    ```python
    name = "Your Name" # Change this to your name
    ```

---

## 🏃‍♀️ Usage

Once configured, running the chatbot is straightforward:

1.  **Run the Python script:**
    Open your terminal or command prompt, navigate to the directory where you saved the script, and run:

    ```bash
    python your_script_name.py
    ```

    (Replace `your_script_name.py` with the actual name of your Python file).

2.  **Access the Gradio Interface:**
    The script will output a local URL (e.g., `http://127.0.0.1:7860`). Open this URL in your web browser to interact with your AI resume chatbot!

---

## 🧠 How It Works

This chatbot leverages the power of Large Language Models (LLMs), a self-correction loop, and powerful tool-calling capabilities to provide high-quality responses and proactive data collection:

1.  **Data Ingestion:** Your resume (PDF) is parsed, and both its content and your custom summary are loaded into memory.

2.  **System Prompt Construction:** A detailed system prompt is dynamically created, instructing the AI to act as you, using your resume and summary as context. This ensures the AI stays "in character" and also guides it on when to use specific tools.

3.  **Tool Definitions:** Three custom tools are defined with JSON schemas:

    - `record_user_details`: To capture user contact information (email, name, notes).

    - `record_unknown_question`: To log questions the AI couldn't answer.

    - `record_recruiter_question`: To record job descriptions or inquiries from recruiters.
      These tools are passed to the LLM, allowing it to decide when to invoke them.

4.  **Pushover Integration:** The `push` function uses the Pushover API to send real-time notifications to your device whenever one of the defined tools is triggered.

5.  **Gradio Chat Interface:** The `gr.ChatInterface` from Gradio provides a user-friendly web interface for real-time conversation.

6.  **AI Response Generation & Tool Execution Loop:**

    - When a user asks a question, the conversation history, along with the system prompt and available tools, is sent to the **`gpt-4o-mini`** model via the OpenAI API.

    - The LLM generates a response. If it decides to use a tool, it returns a `tool_calls` message.

    - The `handle_tool_calls` function intercepts these tool calls, executes the corresponding Python functions (`record_user_details`, `record_unknown_question`, `record_recruiter_question`), and sends Pushover notifications.

    - The results of the tool calls are then sent back to the LLM to inform its next conversational turn. This loop continues until the LLM generates a final text response.

7.  **Self-Evaluation (The "Killer" Feature!):**

    - An `Evaluation` Pydantic model defines the structure for feedback (`is_acceptable` and `feedback`).

    - A separate `evaluator_system_prompt` is crafted, instructing another LLM (via the **Gemini API**) to act as an evaluator.

    - The generated reply, user message, and conversation history are sent to the evaluator, which determines if the response is acceptable and provides feedback.

8.  **Rerun with Feedback:** If the evaluator deems a response unacceptable, the original system prompt is augmented with the rejection reason and the "bad" reply. The `gpt-4o-mini` model is then prompted again with this additional context, guiding it to generate a better, corrected response. This creates a powerful self-improving loop!

## 🛠️ Customization

- **Resume & Summary Content:** Update `ashutosh/Ashutosh_Gajankush.pdf` and `ashutosh/summary.txt` with your own documents.

- **AI Model:** You can experiment with different `openai` models by changing `model="gpt-4o-mini"` to another available model.

- **Evaluation Logic:** Modify the `evaluator_system_prompt` or the `evaluate` function's logic to change how responses are judged. The `rerun` function can also be tweaked to alter how feedback is incorporated.

- **Tool Definitions:** You can modify the existing tool definitions (`record_user_details_json`, `record_unknown_question_json`, `record_recruiter_question_json`) or add entirely new tools to extend the chatbot's capabilities. Remember to update the `tools` list and the `handle_tool_calls` function accordingly.

- **Pushover Notifications:** Customize the messages sent via Pushover in the `push` function and within the `record_*` functions.

- **"Faking a condition" for Rerun:** The current script includes a line `if "patent" in message.lower():` to demonstrate the rerun functionality. You can remove or modify this condition to test the evaluation more broadly or based on different criteria.

## 🤝 Contributing

Feel free to fork this repository, open issues, and submit pull requests to improve this project.

## 📄 License

This project is open-source and available under the MIT License.
