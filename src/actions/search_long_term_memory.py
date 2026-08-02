from pydantic import BaseModel, Field
from src.actions import action_tool
from src.core.memory.long_term_memory import LongTermMemory


class SearchLTMArgs(BaseModel):
    query: str = Field(..., description="The search query or topic to look up in long-term semantic memory.")


@action_tool(name="search_long_term_memory")
def search_long_term_memory(args: SearchLTMArgs, long_term_memory: LongTermMemory, **kwargs) -> str:
    """Searches the agent's long-term semantic memory for historical facts or past context."""

    try:
        # Attempt to use the interface's intended context retrieval method
        results = long_term_memory.retrieve_unstructured_information_for_context(
            current_objective="Recall historical context",
            task_description=args.query
        )
        return f"SYSTEM RESULT:\n{results}"
    except NotImplementedError:
        # Fallback since SequentialLongTermMemory currently raises NotImplementedError
        all_memory = long_term_memory.retrieve_all_information_as_text()

        # Extremely basic text search for demonstration
        if args.query.lower() in all_memory.lower():
            return f"SYSTEM RESULT: Memory scan found relevant context:\n{all_memory}"
        else:
            return f"SYSTEM RESULT: No direct matches found for '{args.query}'. Dump of all memory:\n{all_memory}"
