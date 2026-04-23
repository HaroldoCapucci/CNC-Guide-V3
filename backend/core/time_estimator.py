import math
from dataclasses import dataclass
from typing import List

@dataclass
class EstimationResult:
    total_time_seconds: float
    total_distance_mm: float
    estimated_cost: float
    rapid_moves: int
    cutting_moves: int

class TimeEstimator:
    def __init__(self, hourly_rate: float = 100.0):
        self.hourly_rate = hourly_rate
    def estimate(self, gcode_commands: List) -> EstimationResult:
        total_time = 0.0
        total_distance = 0.0
        rapid_moves = 0
        cutting_moves = 0
        current_pos = (0.0, 0.0, 0.0)
        current_feed = 500
        for cmd in gcode_commands:
            new_pos = self._get_position(current_pos, cmd)
            dist = self._distance_3d(current_pos, new_pos)
            if cmd.command == "G00":
                speed = 5000
                rapid_moves += 1
            else:
                speed = current_feed
                cutting_moves += 1
            if cmd.feed_rate:
                current_feed = cmd.feed_rate
            if speed > 0:
                total_time += dist / speed
            total_distance += dist
            current_pos = new_pos
        total_time_seconds = total_time * 60
        cost = (total_time_seconds / 3600) * self.hourly_rate
        return EstimationResult(
            total_time_seconds=total_time_seconds,
            total_distance_mm=total_distance,
            estimated_cost=cost,
            rapid_moves=rapid_moves,
            cutting_moves=cutting_moves
        )
    @staticmethod
    def _get_position(current, cmd):
        x, y, z = current
        if cmd.x is not None: x = cmd.x
        if cmd.y is not None: y = cmd.y
        if cmd.z is not None: z = cmd.z
        return (x, y, z)
    @staticmethod
    def _distance_3d(p1, p2):
        return math.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 + (p2[2]-p1[2])**2)
