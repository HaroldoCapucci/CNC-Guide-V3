from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass

@dataclass
class PostProcessorConfig:
    machine_type: str
    inch_mode: bool = False
    decimal_places: int = 4
    use_tool_change: bool = True

class PostProcessor(ABC):
    def __init__(self, config: PostProcessorConfig = None):
        self.config = config or PostProcessorConfig("generic")
    @abstractmethod
    def process(self, commands: List) -> str:
        pass
    @abstractmethod
    def get_header(self) -> str:
        pass
    @abstractmethod
    def get_footer(self) -> str:
        pass

class MitsubishiPostProcessor(PostProcessor):
    def __init__(self, config=None):
        super().__init__(config or PostProcessorConfig("Mitsubishi"))
    def process(self, commands):
        lines = [self.get_header()]
        for cmd in commands:
            line = self.format_command(cmd)
            lines.append(line)
        lines.append(self.get_footer())
        return '\n'.join(lines)
    def format_command(self, cmd):
        parts = [cmd.command]
        if cmd.x is not None: parts.append(f"X{cmd.x:.4f}")
        if cmd.y is not None: parts.append(f"Y{cmd.y:.4f}")
        if cmd.z is not None: parts.append(f"Z{cmd.z:.4f}")
        if cmd.feed_rate is not None: parts.append(f"F{int(cmd.feed_rate)}")
        if cmd.spindle_speed is not None: parts.append(f"S{int(cmd.spindle_speed)}")
        return ' '.join(parts)
    def get_header(self): return "O0001\n(MITSUBISHI CNC PROGRAM)\nG54 G90 G21"
    def get_footer(self): return "M30\n%"

class FanucPostProcessor(PostProcessor):
    def __init__(self, config=None):
        super().__init__(config or PostProcessorConfig("Fanuc"))
    def process(self, commands):
        lines = [self.get_header()]
        block = 10
        for cmd in commands:
            lines.append(self.format_command(cmd, block))
            block += 10
        lines.append(self.get_footer())
        return '\n'.join(lines)
    def format_command(self, cmd, block):
        parts = [f"N{block}", cmd.command]
        if cmd.x is not None: parts.append(f"X{cmd.x:.4f}")
        if cmd.y is not None: parts.append(f"Y{cmd.y:.4f}")
        if cmd.z is not None: parts.append(f"Z{cmd.z:.4f}")
        if cmd.feed_rate is not None: parts.append(f"F{int(cmd.feed_rate)}")
        if cmd.spindle_speed is not None: parts.append(f"S{int(cmd.spindle_speed)}")
        return ' '.join(parts)
    def get_header(self): return "O0001\n(FANUC CNC PROGRAM)\nG54 G90 G21"
    def get_footer(self): return "M30\n%"

class PostProcessorFactory:
    _processors = {
        'mitsubishi': MitsubishiPostProcessor,
        'fanuc': FanucPostProcessor,
    }
    @classmethod
    def create(cls, machine_type: str, config=None):
        processor_class = cls._processors.get(machine_type.lower())
        if processor_class is None:
            raise ValueError(f"Unknown machine type: {machine_type}")
        return processor_class(config)
