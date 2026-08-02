import asyncio
from src.core.agent_factory import AgentFactory
from src.core.environment import Environment


async def main():
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

    # Start the async monitoring tasks
    env.start()
    agent.start()

    print("\n[Sending Request]")
    await agent.listen('Hello World!')

    # Wait for the agent to finish thinking before shutting down
    await asyncio.sleep(0.5)
    if hasattr(agent, '_pause_event') and agent._pause_event is not None:
        while not agent._pause_event.is_set():
            await asyncio.sleep(0.5)

    await asyncio.sleep(0.5)

    print("\n[Shutting Down Services...]")
    await agent.stop()
    await env.stop()


if __name__ == '__main__':
    asyncio.run(main())
