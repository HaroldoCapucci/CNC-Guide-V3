import json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

@dataclass
class Tool:
    id: str
    name: str
    tool_type: str
    diameter: float
    flute_count: int
    max_rpm: float
    material: str
    coolant_type: str = "dry"

class ToolLibrary:
    def __init__(self, library_path: str = "tools_library.json"):
        self.library_path = Path(library_path)
        self.tools: Dict[str, Tool] = {}
        self.load()
    def load(self):
        if self.library_path.exists():
            with open(self.library_path, 'r') as f:
                data = json.load(f)
                for d in data:
                    tool = Tool(**d)
                    self.tools[tool.id] = tool
    def save(self):
        with open(self.library_path, 'w') as f:
            json.dump([asdict(t) for t in self.tools.values()], f, indent=2)
    def add_tool(self, tool: Tool) -> bool:
        if tool.id in self.tools: return False
        self.tools[tool.id] = tool
        self.save()
        return True
    def delete_tool(self, tool_id: str) -> bool:
        if tool_id in self.tools:
            del self.tools[tool_id]
            self.save()
            return True
        return False
    def list_tools(self, tool_type: str = None) -> List[Tool]:
        if tool_type is None:
            return list(self.tools.values())
        return [t for t in self.tools.values() if t.tool_type == tool_type]
    def get_tool(self, tool_id: str) -> Optional[Tool]:
        return self.tools.get(tool_id)
