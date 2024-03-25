{
    "name": "generate_sql",
    "description": "The agent should understand user's request and generate SQL query to fetch the required data.",
    "system_prompt_template": "",
    "task_prompt_template": "PROMPT_TEMPLATE_FOR_GENERATE_SQL_PATH",
    "input_information_names": [],
    "output_information_spec": {
        "task_name": {
          "information_type": "string"
        },
        "sql_query": {
          "information_type": "string"
        },
        "reasoning": {
          "information_type": "string"
        }
    },
    "action_names": [],
    "temperature": 0.0
}