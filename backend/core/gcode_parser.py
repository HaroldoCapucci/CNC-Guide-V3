from dataclasses import dataclass
from typing import List, Tuple
import re

@dataclass
class GcodeCommand:
    command: str
    x: float = None
    y: float = None
    z: float = None
    feed_rate: float = None
    spindle_speed: float = None

class GcodeParser:
    def __init__(self):
        self.commands: List[GcodeCommand] = []
        self.current_position = (0.0, 0.0, 0.0)

    def parse(self, gcode_content: str) -> List[GcodeCommand]:
        lines = gcode_content.strip().split('\n')
        for line in lines:
            line = self.remove_comments(line).strip()
            if not line:
                continue
            cmd = self.parse_line(line)
            if cmd:
                self.commands.append(cmd)
        return self.commands

    def parse_line(self, line: str) -> GcodeCommand:
        cmd = GcodeCommand(command=None)
        cmd_match = re.search(r'([GM]\d{2})', line)
        if cmd_match:
            cmd.command = cmd_match.group(1)
        x_match = re.search(r'X([-\d.]+)', line)
        y_match = re.search(r'Y([-\d.]+)', line)
        z_match = re.search(r'Z([-\d.]+)', line)
        f_match = re.search(r'F(\d+)', line)
        s_match = re.search(r'S(\d+)', line)
        if x_match: cmd.x = float(x_match.group(1))
        if y_match: cmd.y = float(y_match.group(1))
        if z_match: cmd.z = float(z_match.group(1))
        if f_match: cmd.feed_rate = float(f_match.group(1))
        if s_match: cmd.spindle_speed = float(s_match.group(1))
        return cmd if cmd.command else None

    @staticmethod
    def remove_comments(line: str) -> str:
        if '(' in line:
            line = line[:line.index('(')]
        if ';' in line:
            line = line[:line.index(';')]
        return line.strip()

    def get_path_points(self) -> List[Tuple[float, float, float]]:
        points = []
        x, y, z = 0, 0, 0
        for cmd in self.commands:
            if cmd.x is not None: x = cmd.x
            if cmd.y is not None: y = cmd.y
            if cmd.z is not None: z = cmd.z
            if cmd.command in ['G00', 'G01']:
                points.append((x, y, z))
        return points
