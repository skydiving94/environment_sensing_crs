import asyncio
from src.agent.agent_factory import AgentFactory
from src.environment.environment import Environment


async def main():
    print('Creating an empty environment')
    env = Environment()
    print(str(env))

    print('Creating an agent: chitchat_agent')
    agent_factory = AgentFactory()
    agent = agent_factory.create_log_based_agent(
        'chitchat_agent',
        'You are an agent for chitchatting with',
        is_verbose=False
    )

    print('Registering chitchat_agent to env')
    agent.register_environment(env)
    print(str(env))

    print('Registering test_agent with an info name: INFO1')
    agent.register_information_queue('INFO1')
    print(str(env))

    print(env.get_all_agent_status())

    # Start the async monitoring tasks
    env.start()
    agent.start()

    print("\n--- Chitchat Agent is ready. Type 'exit' to quit. ---")
    try:
        while True:
            # Prevent input() from freezing the async event loop
            user_input = await asyncio.to_thread(input, "\nYou: ")

            if user_input.strip().lower() in ['exit', 'quit']:
                break

            if user_input.strip():
                await agent.listen(user_input)

                await asyncio.sleep(0.5)
                # Smart Wait: Check the agent's pause event to know when it finishes thinking
                if hasattr(agent, '_pause_event') and agent._pause_event is not None:
                    while not agent._pause_event.is_set():
                        await asyncio.sleep(0.5)

                await asyncio.sleep(0.2)

    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    finally:
        print("\n[Shutting Down Services...]")
        await agent.stop()
        await env.stop()


if __name__ == '__main__':
    asyncio.run(main())
