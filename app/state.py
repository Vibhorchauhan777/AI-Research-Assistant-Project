from typing import List, Dict, Any
from pydantic import BaseModel


class AgentState(BaseModel):
    query: str
    context: List[Dict[str, Any]] = []
    draft: str = ""
    final: str = ""
    iteration: int = 0
    output: Dict[str, Any]