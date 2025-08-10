# OpenAI SDK: Agent Tooling and Handoffs Demo

This repository provides a hands-on demonstration of building advanced, multi-agent workflows using the OpenAI SDK. The primary focus is to showcase two powerful concepts: **Agent Tooling** and **Agent Handoffs**.

The project uses a practical example of a Financial AI company (FinAI) automating its cold email outreach process to illustrate how these features can be implemented.

---

## Core Concepts Highlighted

This project is structured around two key notebooks, each demonstrating a core concept.

### 1. Agent Tooling (`agent.ipynb`)

**Tooling** is the fundamental practice of converting agents and Python functions into modular, reusable components that can be used by other agents. This allows you to build complex systems from smaller, specialized parts.

**Key Implementations:**

- **Agents as Tools**: We define agents with specific "personalities" or skills (e.g., a "Professional Sales Agent" or a "Humorous Sales Agent"). Each agent is then packaged into a tool using the `.as_tool()` method, making its capabilities callable by another agent.

  ```python
  # From openai_sdk/agent.ipynb
  # Define an agent with specific instructions
  sales_agent_1 = Agent(instructions=intruction_1, name="Professional Sales Agent", model="gpt-4o-mini")

  # Convert the agent into a reusable tool
  tool1 = sales_agent_1.as_tool(tool_name="sales_agent_1", tool_description="Write a cold email")
  ```

- **Functions as Tools**: Standard Python functions can also be transformed into tools using the `@function_tool` decorator. This is ideal for integrating utilities like sending notifications or interacting with external APIs.

  ```python
  # From openai_sdk/agent.ipynb
  from agents import function_tool

  @function_tool
  def send_push_notification(message : str):
      # Function logic to send a push notification
      push(message)
      return {"status": "success"}
  ```

- **Orchestration Agent**: A "Sales Agent Manager" is created to orchestrate the workflow. Its instructions are to use the collection of agent and function tools to achieve a multi-step goal, generate three distinct email drafts, evaluate them, and then use the notification tool to send the best one.

### 2. Agent Handoffs (`handoffs.ipynb`)

**Handoffs** are used to create sophisticated, sequential workflows where a task is passed from a manager agent to a specialized agent for processing. This creates a clean and efficient division of labor.

**Key Implementations:**

- **Specialized Sub-Agents**: First, we create highly specialized agents for granular tasks, such as generating an email subject line or converting an email body to HTML. These are also converted into tools.

- **The Handoff Agent**: A dedicated agent (`Handoff Push Notification Agent`) is built to execute a specific sequence of sub-tasks. It is given the specialized tools (for subject writing, HTML conversion, and sending notifications) and a `handoff_description`. This description tells other agents what its purpose is.

  ```python
  # From openai_sdk/handoffs.ipynb
  handoff_push_agent = Agent(
      name="Handoff Push Notification Agent",
      instructions=push_notification_instruction,
      tools=[subject_writer_tool, html_converter_tool, send_push_notification],
      handoff_description="Conver the email to HTML and send it as a push notification"
  )
  ```

- **The Final Orchestrator**: The top-level "Sales Manager Agent" is configured to use both the basic drafting tools and the new handoff agent. The manager's role is simplified, it drafts emails, selects the best one, and then "hands it off" to the `handoff_push_agent` for all final formatting and sending. The manager doesn't need to know the details of HTML conversion or notification, it just delegates the task.

  ```python
  # From openai_sdk/handoffs.ipynb
  sales_manager_agent = Agent(
      name = "Sales Manager Agent",
      instructions = sales_manager_instructions,
      tools=[tool1, tool2, tool3], # Basic drafting tools
      handoffs=[handoff_push_agent] # The specialized handoff agent
  )
  ```

---

## Getting Started

Follow these steps to run the project on your local machine.

### 1. Installation

Install the necessary Python libraries.

```bash
pip install python-dotenv requests openai agents
```

### 2. Configuration

Create a .env file in the root directory of the project. You will need to add your API token and user key for the Pushover notification service.

```bash
PUSHOVER_TOKEN=your_pushover_api_token
PUSHOVER_USER=your_pushover_user_key
```

### 3. Running the Notebooks

Open and execute the cells in the Jupyter notebooks to see the concepts in action:

1. **openai_sdk/agent.ipynb:** Demonstrates the fundamentals of creating and using tools.
2. **openai_sdk/handoffs.ipynb:** Builds on the first notebook to show how to implement a multi-step workflow with handoffs.
