from src.agent.agent import Agent
from src.environment.environment import Environment


def main():
    print('Creating an empty environment')
    env = Environment()

    print('Creating an agent: test_agent')
    agent = Agent('test_agent', 'You are a test agent')

    print('Registering test_agent to env')
    agent.register_environment(env)

    print('Registering test_agent with an info name: INFO1')
    agent.register_information_queue('INFO1')

    agent.listen('Hello World!')


if __name__ == '__main__':
    main()
