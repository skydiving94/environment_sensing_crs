import asyncio
from src.agent.agent_factory import AgentFactory
from src.environment.environment import Environment


async def main():
    print('Creating an empty environment')
    env = Environment()
    print(str(env))

    print('Creating an agent: interactive_sql_agent')

    # Create a SQL Agent handling users request
    agent_factory = AgentFactory()
    sql_agent = agent_factory.create_log_based_agent(
        agent_id='sql_agent',
        role_description='You are a SQL agent writing and executing SQL queries.',
        current_objective='Write and execute SQL queries.')

    print('Registering interactive_sql_agent to env')
    sql_agent.register_environment(env)
    print(str(env))

    print('Registering interactive_sql_agent with an info name: INFO2')
    sql_agent.register_information_queue('INFO2')
    print(str(env))

    print(env.get_all_agent_status())

    # Start the async monitoring tasks
    env.start()
    sql_agent.start()

    print("\n[Sending Request]")
    await sql_agent.listen('Find the best average rating movie.')

    # Wait for the agent to finish thinking before shutting down
    await asyncio.sleep(0.5)
    if hasattr(sql_agent, '_pause_event') and sql_agent._pause_event is not None:
        while not sql_agent._pause_event.is_set():
            await asyncio.sleep(0.5)

    await asyncio.sleep(0.5)

    print("\n[Shutting Down Services...]")
    await sql_agent.stop()
    await env.stop()


if __name__ == '__main__':
    asyncio.run(main())
