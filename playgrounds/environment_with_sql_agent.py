from src.agent.agent import Agent
from src.environment.environment import Environment


def main():
    print('Creating an empty environment')
    env = Environment()
    print(str(env))

    print('Creating an agent: test_agent')
    # agent = Agent('test_agent', 'You are a test agent')
    # Create a SQL Agent handling users request
    sql_agent = Agent('sql_agent', 'You are a SQL agent writing and executing SQL queries.', 
                        current_objective='Write and execute SQL queries.')
    

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
    # agent.listen('Hello World!')


if __name__ == '__main__':
    main()
