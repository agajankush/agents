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

### 3. Input Guardrails

**Guardrails** are safety checks that are applied to an agent's input to prevent it from performing unwanted or unsafe actions. In this project, we implement a guardrail to stop the agent if a personal name is included in the initial request, enhancing the safety and compliance of the system.

**Key Implementations:**

- **Pydantic Model for Structured Output**: We first define a `Pydantic` model to ensure that our guardrail's check produces a reliable, structured output. This model dictates that the check must return a boolean (`is_name_in_message`) and the name that was found.

  ```python
  # From guardrails.ipynb
  class NameCheckOutput(BaseModel):
      is_name_in_message: bool
      name: str
  ```

- **The Guardrail Agent**: A specialized agent (`Name check`) is created with the sole purpose of checking the input message. Its `output_type` is set to our `NameCheckOutput` Pydantic model to enforce the structure.

- **The Guardrail Function**: We create a function decorated with `@input_guardrail`. This function runs our "Name check" agent on the user's message. Based on the structured output, it returns a `GuardrailFunctionOutput`. This special object tells the SDK whether to trigger the tripwire. If triggered, it immediately stops the main agent's execution and raises an exception.

  ```python
  # From guardrails.ipynb
  @input_guardrail
  async def guardrail_against_name(ctx, agent, message):
      result = await Runner.run(guardrail_agent, message, context=ctx.context)
      is_name_in_message = result.final_output.is_name_in_message
      return GuardrailFunctionOutput(
          output_info={"found_name": result.final_output},
          tripwire_triggered=is_name_in_message
      )
  ```

- **Attaching the Guardrail**: Finally, the guardrail function is attached to our main "Sales Manager" agent via the `input_guardrails` list. Now, before the manager agent even begins its primary task, this guardrail will run, ensuring no personal names are processed.

  ```python
  # From guardrails.ipynb
  careful_sales_manager = Agent(
      name = "Sales Manager",
      instructions = sales_manager_instructions,
      tools=[tool1, tool2, tool3],
      model="gpt-4o-mini",
      handoffs=[handoff_push_agent],
      input_guardrails=[guardrail_against_name]
  )
  ```

---

---

## Getting Started

Follow these steps to run the project on your local machine.

### 1. Installation

Install the necessary Python libraries.

```bash
pip install python-dotenv requests openai agents pydantic
```

### 2. Configuration

Create a .env file in the root directory of the project. You will need to add your API token and user key for the Pushover notification service.

```bash
PUSHOVER_TOKEN=your_pushover_api_token
PUSHOVER_USER=your_pushover_user_key
OPENAI_API_KEY=your_openai_api_key
```

### 3. Running the Notebooks

Open and execute the cells in the Jupyter notebooks to see the concepts in action:

1. **openai_sdk/agent.ipynb:** Demonstrates the fundamentals of creating and using tools.
2. **openai_sdk/handoffs.ipynb:** Builds on the first notebook to show how to implement a multi-step workflow with handoffs.
3. **guardrails.ipynb:** The final version combining all concepts to create a robust, multi-agent system with safety checks.
