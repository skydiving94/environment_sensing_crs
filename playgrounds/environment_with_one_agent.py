from src.agent.agent_factory import AgentFactory
from src.environment.environment import Environment


def main():
    print('Creating an empty environment')
    env = Environment()
    print(str(env))

    print('Creating an agent: test_agent')
    agent_factory = AgentFactory()
    agent = agent_factory.create_log_based_agent(
        'test_agent', 'You are a test agent'
    )

    print('Registering test_agent to env')
    agent.register_environment(env)
    print(str(env))

    print('Registering test_agent with an info name: INFO1')
    agent.register_information_queue('INFO1')
    print(str(env))

    print(env.get_all_agent_status())

    agent.listen('Hello World!')


if __name__ == '__main__':
    main()
