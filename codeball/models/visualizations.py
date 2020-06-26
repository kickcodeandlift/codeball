from dataclasses import dataclass, field
from typing import Optional, List, Dict


@dataclass  # Base Visualization Data Class
class Visualization:
    start_time: int
    end_time: int
    # tool_id: str
    # options: Optional[Dict] = field(default_factory=dict)


# Players
@dataclass
class Players(Visualization):
    players: List[str]
    tool_id: str = "players"
    options: Dict = field(
        default_factory=lambda: {
            "id": True,
            "speed": True,
            "spotlight": False,
            "ring": False,
            "spotlightColor": "#FFFFFF",
            "ringColor": "#000000",
            "size": 1.0,  # Multiplier, [0.6, 1.5]
        }
    )


# Trails
@dataclass
class Trails(Visualization):
    players: List[str]
    tool_id: str = "trails"
    options: Dict = field(
        default_factory=lambda: {
            "color": "#E66F7E",
            "width": 1.0,  # Multiplier, [0.5, 2.0]
        }
    )


# FutureTrails
@dataclass
class FutureTrails(Visualization):
    players: List[str]
    tool_id: str = "futureTrails"
    options: Dict = field(
        default_factory=lambda: {
            "color": "#E66F7E",
            "width": 1.0,  # Multiplier, [0.5, 2.0]
        }
    )


# Magnifiers
@dataclass
class Magnifiers(Visualization):
    players: List[str]
    tool_id: str = "magnifiers"
    options: Dict = field(
        default_factory=lambda: {
            "zoom": 1.0,  # Multiplier, [0.2, 1.5]
            "size": 1.0,  # Multiplier, [0.5, 1.5]
        }
    )


# Measurer
@dataclass
class Measurer(Visualization):
    players: List[str]
    tool_id: str = "measurer"
    options: Dict = field(
        default_factory=lambda: {
            "color": "#040602",
            "width": 1.0,  # Multiplier, [0.5, 2.0]
            "filled": False,
            "distances": True,
            "closed": False,
        }
    )


# TeamSize
@dataclass
class TeamSize(Visualization):
    team: str
    line: str = "width"  # Values: 'width' or 'length'
    tool_id: str = "teamSize"
    options: Dict = field(default_factory=lambda: {"color": "#E66F7E"})


# TacticalLines
@dataclass
class TacticalLines(Visualization):
    team: str
    line: str = "defenders"  # Values: 'defenders', 'midfielders' or 'strikers'
    tool_id: str = "tacticalLines"
    options: Dict = field(
        default_factory=lambda: {
            "color": "#E66F7E",
            "distances": False,
            "closed": False,  # Only used when line is 'midfielders'
        }
    )


# Pause TODO do Pause have start and end time? Or just start time?
@dataclass
class Pause:
    pause_time: float = 5000  # Milliseconds
    tool_id: str = "pause"


# ChromaKey
@dataclass
class ChromaKey:
    tool_id: str = "chromaKey"
    options: Dict = field(
        default_factory=lambda: {
            "threshold": 0.01,  # [0.0, 1.0]
            "smoothing": 0.1,  # [0.0, 1.0]
        }
    )
