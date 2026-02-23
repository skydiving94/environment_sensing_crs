# Environment Sensing CRS (Legacy POC)

Initial proof-of-concept for an environment-aware, task-driven autonomous agent system. The architecture isolates environment interaction, temporal state tracking, and sequential task execution.

## Architectural Components

### 1. Environment System (`src/environment`)
Manages external state and interaction boundaries. Acts as the interface between the agent and external stimuli, including simulated user chat and database connections.

### 2. Memory Architecture (`src/memory`)
Segregates information storage into distinct temporal and semantic classifications.
* **Activity Log:** Tracks episodic, short-term interaction history.
* **Information Cache:** Manages extracted entities and stateful data.
* **Long Term Memory:** Persists semantic facts and extracted knowledge across sessions.

### 3. Task Management (`src/task` & `resources`)
Defines agent operations through deterministic JSON specifications.
* **Task Spec:** Structured definitions of inputs, outputs, and execution constraints.
* **Agent Configurations:** Resource definitions located in `resources/knowledge_based_agent/` and `resources/log_based_agent/`. Contains prompts and task constraints for operations such as `pick_a_task`, `formulate_response`, and `generate_sql`.

### 4. Agent & Action Execution (`src/agent`)
Executes bounded tasks and interfaces with the environment.
* **Agent Initialization:** `agent_factory.py` constructs agents with specific memory bounds and task configurations.
* **Action Modules:** Discrete execution units including `query_sql_database`, `collect_information_by_names`, and `put_information_into_queue`.

## Execution Environments

Testing and execution entry points are contained within the `playgrounds/` directory.

* Multi-round conversational testing: `python -m old_poc.playgrounds.environment_with_multi_round_chitchat_agent`
* SQL agent interaction: `python -m old_poc.playgrounds.environment_with_sql_agent`
* Interactive SQL evaluation: `python -m old_poc.playgrounds.environment_with_sql_agent_interactive`

## Configuration and Setup

Database initialization scripts are located in `src/commandline_scripts/db_setup_scripts/setup_ml_25_db.py`. System parameters and LLM connections are defined within `src/config.py`. Standard execution requires a configured OpenAI API connection via `src/llm/openai.py`.

## Setup
1. Create a `.env` in project root and copy the environment variables and values to this file.
2. 

# Dataset
## GoRecDial
* Dataset Download: https://drive.google.com/drive/folders/1nilk6FUktW2VjNlATdM0VMehzSOPIvJ0

## TG-ReDial
* Download dataset here: https://github.com/RUCAIBox/TG-ReDial

## MovieLens
This [Notion Link](https://www.notion.so/zhejian/Examine-the-movie-dataset-and-related-paper-if-needed-bde345da59cb4abe962c8a390dbfe055?pvs=4) contain detailed dataset information.
