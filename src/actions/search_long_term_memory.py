from pydantic import BaseModel, Field
from src.actions import action_tool
from src.core.memory.long_term_memory import LongTermMemory


class SearchLTMArgs(BaseModel):
    query: str = Field(..., description="The search query or topic to look up in long-term semantic memory.")


@action_tool(name="search_long_term_memory")
def search_long_term_memory(args: SearchLTMArgs, long_term_memory: LongTermMemory, **kwargs) -> str:
    """Searches the agent's long-term semantic memory for historical facts or past context."""

    # Use the new generic search_memories method
    results = long_term_memory.search_memories(query=args.query, top_k=5)

    if not results:
        return f"SYSTEM RESULT: No direct matches found for '{args.query}'."

    # Format and return the results
    formatted_results = "\n\n".join(
        [f"Result {i+1}:\n{res.raw_value}" for i, res in enumerate(results)])
    return f"SYSTEM RESULT: Memory scan found relevant context:\n{formatted_results}"
