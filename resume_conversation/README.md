# 🤖 Resume AI Chatbot: Your Personal Digital Twin

---

Ever wished your resume could talk? This Python script brings your professional profile to life as an interactive AI chatbot! Built with **Gradio**, this application allows anyone to converse with your resume and a personalized summary, providing a dynamic and engaging way to showcase your skills, experience, and background.

Perfect for job seekers, freelancers, or anyone looking to create an innovative online presence, this chatbot acts as your digital twin, ready to answer questions about your career in a professional and engaging manner.

## ✨ Features

- **Interactive Chat Interface:** Engage in natural language conversations with your resume and professional summary.

- **Context-Aware Responses:** The AI is grounded in your provided resume (PDF) and a custom summary, ensuring relevant and accurate answers.

- **Self-Correction Mechanism:** An integrated evaluation system (powered by the Gemini API) assesses the quality of responses and can trigger a "rerun" with feedback, improving the chatbot's performance over time.

- **Professional Persona:** The chatbot is designed to maintain a professional and engaging tone, as if speaking to a potential client or employer.

- **Easy Customization:** Easily swap out your resume and summary files to personalize the chatbot.

---

## 🚀 Getting Started

Follow these steps to set up and run your own Resume AI Chatbot.

### Prerequisites

- **Python 3.8+**

- **pip** (Python package installer)

### Installation

1. **Clone this repository (or copy the script):**
   If you have a repository, you'd typically clone it here. For a single script, just save the provided Python code.

2. **Install the required libraries:**
   Open your terminal or command prompt and run:

```

pip install python-dotenv openai pypdf gradio pydantic

```

### Configuration

1. **Create a `.env` file:**
   In the same directory as your Python script, create a file named `.env`. This file will store your API keys securely.

Add your OpenAI API key and Google API key (for Gemini evaluation) to this file:

```

OPENAI_API_KEY="your_openai_api_key_here"
GOOGLE_API_KEY="your_google_api_key_here"

```

**Important:** Replace `"your_openai_api_key_here"` and `"your_google_api_key_here"` with your actual API keys.

2. **Prepare your Resume and Summary:**

- Place your resume PDF file (e.g., `Ashutosh_Gajankush.pdf`) in a directory accessible by the script (e.g., `ashutosh/Ashutosh_Gajankush.pdf`).

- Create a text file with a summary of your background/LinkedIn profile (e.g., `summary.txt`) and place it in a directory accessible by the script (e.g., `me/summary.txt`).

**Adjust the file paths in the script** if your files are located elsewhere:

```

reader = PdfReader("../data/resume/Ashutosh_Gajankush.pdf") \# Update this path

# ...

with open("../data/resume/summary.txt", "r", encoding="utf-8") as f: \# Update this path

```

3. **Set your Name:**
   Update the `name` variable in the script to your actual name:

```

name = "Your Name" \# Change this to your name

```

## 🏃‍♀️ Usage

Once configured, running the chatbot is straightforward:

1. **Run the Python script:**
   Open your terminal or command prompt, navigate to the directory where you saved the script, and run:

```

python your_script_name.py

```

(Replace `your_script_name.py` with the actual name of your Python file).

2. **Access the Gradio Interface:**
   The script will output a local URL (e.g., `http://127.0.0.1:7860`). Open this URL in your web browser to interact with your AI resume chatbot!

## 🧠 How It Works

This chatbot leverages the power of Large Language Models (LLMs) and a self-correction loop to provide high-quality responses:

1. **Data Ingestion:** Your resume (PDF) is parsed, and both its content and your custom summary are loaded into memory.

2. **System Prompt Construction:** A detailed system prompt is dynamically created, instructing the AI to act as you, using your resume and summary as context. This ensures the AI stays "in character."

3. **Gradio Chat Interface:** The `gr.ChatInterface` from Gradio provides a user-friendly web interface for real-time conversation.

4. **AI Response Generation:** When a user asks a question, the conversation history, along with the system prompt, is sent to the **`gpt-4o-mini`** model via the OpenAI API to generate a reply.

5. **Self-Evaluation (The "Killer" Feature!):**

- An `Evaluation` Pydantic model defines the structure for feedback (`is_acceptable` and `feedback`).

- A separate `evaluator_system_prompt` is crafted, instructing another LLM (via the **Gemini API**) to act as an evaluator.

- The generated reply, user message, and conversation history are sent to the evaluator, which determines if the response is acceptable and provides feedback.

6. **Rerun with Feedback:** If the evaluator deems a response unacceptable, the original system prompt is augmented with the rejection reason and the "bad" reply. The `gpt-4o-mini` model is then prompted again with this additional context, guiding it to generate a better, corrected response. This creates a powerful self-improving loop!

## 🛠️ Customization

- **Resume & Summary Content:** Update `ashutosh/Ashutosh_Gajankush.pdf` and `me/summary.txt` with your own documents.

- **AI Model:** You can experiment with different `openai` models by changing `model="gpt-4o-mini"` to another available model.

- **Evaluation Logic:** Modify the `evaluator_system_prompt` or the `evaluate` function's logic to change how responses are judged. The `rerun` function can also be tweaked to alter how feedback is incorporated.

- **"Faking a condition" for Rerun:** The current script includes a line `if "patent" in message.lower():` to demonstrate the rerun functionality. You can remove or modify this condition to test the evaluation more broadly or based on different criteria.

## 🤝 Contributing

Feel free to fork this repository, open issues, and submit pull requests to improve this project.

## 📄 License

This project is open-source and available under the MIT License.
