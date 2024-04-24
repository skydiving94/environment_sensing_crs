from src.agent.agent_factory import AgentFactory
from src.environment.environment import Environment


def main():
    print('Creating an empty environment')
    env = Environment()
    print(str(env))

    print('Creating an agent: test_agent')

    # Create a SQL Agent handling users request
    agent_factory = AgentFactory()
    sql_agent = agent_factory.create_knowledge_based_agent(
        agent_id='sql_agent',
        role_description='You are a SQL agent writing and executing SQL queries.',
        current_objective='Write and execute SQL queries, '
                          'and then, return the response in natural language back to user.')


    print('Registering test_agent to env')
    # agent.register_environment(env)
    sql_agent.register_environment(env)
    print(str(env))

    print('Registering test_agent with an info name: INFO2')
    # agent.register_information_queue('INFO1')
    sql_agent.register_information_queue('INFO2')
    print(str(env))

    print(env.get_all_agent_status())

    sql_agent.listen('Find the best average rating movie.')


if __name__ == '__main__':
    main()
