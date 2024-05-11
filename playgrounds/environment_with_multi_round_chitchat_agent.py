from src.agent.agent_factory import AgentFactory
from src.environment.environment import Environment


def main():
    print('Creating an empty environment')
    env = Environment()
    print(str(env))

    print('Creating an agent: chitchat_agent')
    agent_factory = AgentFactory()
    agent = agent_factory.create_log_based_agent(
        'chitchat_agent', 'You are an agent for chitchatting with'
    )

    print('Registering chitchat_agent to env')
    agent.register_environment(env)
    print(str(env))

    print('Registering test_agent with an info name: INFO1')
    agent.register_information_queue('INFO1')
    print(str(env))

    print(env.get_all_agent_status())

    try:
        while True:
            user_input = input()
            agent.listen(user_input)
    except KeyboardInterrupt:
        exit()


if __name__ == '__main__':
    main()
