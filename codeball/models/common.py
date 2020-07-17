import json
from dataclasses import dataclass, field
from typing import Optional, List, Dict, TYPE_CHECKING
from enum import Enum
import pandas as pd
from kloppy.domain.models import Dataset, Team
from kloppy import load_epts_tracking_data, to_pandas
from codeball.models.visualizations import Visualization
import codeball
import codeball.utils as utils


if TYPE_CHECKING:
    from codeball.patterns.base import PatternAnalysis


@dataclass
class Coordinate:
    x: float
    y: float


@dataclass
class PatternEvent:
    pattern: str
    start_time: float
    event_time: float
    end_time: float
    coordinates: List[Coordinate] = field(default_factory=list)
    visualizations: List[Visualization] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


@dataclass
class Pattern:
    name: str
    code: str
    in_time: int = 0
    out_time: int = 0
    events: List[PatternEvent] = field(default_factory=list)


class DataType(Enum):
    TRACKING = "tracking"
    EVENT = "event"


@dataclass
class DataPackage:
    data_type: DataType
    data_file: str
    meta_data_file: str = None
    dataset: Dataset = None
    dataframe: pd.DataFrame = None

    def load_dataset(self):
        self.dataset = load_epts_tracking_data(
            self.meta_data_file, self.data_file
        )

    def build_dataframe(self):
        self.dataframe = to_pandas(self.dataset)

    def get_team_tracking_dataframe(
        self, team_code: str, with_goalkeeper: bool = True
    ) -> pd.DataFrame:

        team = self.get_team_by_code(team_code)

        players_ids = self.get_players_ids_for_team(
            team=team, with_goalkeeper=with_goalkeeper
        )

        column_names = []
        for player_id in players_ids:
            column_names.extend([player_id + "_x", player_id + "_y"])

        return self.dataframe[column_names]

    def get_team_by_code(self, team_code: str):
        for team in self.dataset.meta_data.teams:
            if team.team_id == team_code:
                return team

    def get_players_ids_for_team(self, team: Team, with_goalkeeper: bool):
        if with_goalkeeper:
            return [player.player_id for player in team.players]
        else:
            return [
                player.player_id
                for player in team.players
                if player.position.name != "Goalkeeper"
            ]


@dataclass
class GameDataset:
    tracking: DataPackage = None
    event: DataPackage = None
    patterns: List[Pattern] = field(default_factory=list)

    def load_patterns_config(self):
        self.patterns_config = codeball.get_patterns_config()

    def initialize_patterns(self):

        self.load_patterns_config()

        for pattern_config in self.patterns_config:
            if pattern_config["include"]:
                pattern = self._initialize_pattern(pattern_config)
                self.patterns.extend(pattern)

    def _initialize_pattern(self, pattern_config: Dict):
        pattern = Pattern(
            name=pattern_config["name"], code=pattern_config["code"]
        )

        pattern.pattern_analysis = []
        for pattern_analysis_config in pattern_config["pattern_analysis"]:
            pattern_analysis = self._initialize_pattern_analysis(
                pattern, pattern_analysis_config
            )
            pattern.pattern_analysis.append(pattern_analysis)

        return pattern

    def _initialize_pattern_analysis(
        self, pattern: Pattern, pattern_analysis_config: dict
    ):

        pattern_analysis_class = pattern_analysis_config["class"]
        return pattern_analysis_class(
            self, pattern, pattern_analysis_config["parameters"]
        )

    def run_patterns(self):
        for pattern in self.patterns:
            for analysis in pattern.pattern_analysis:
                pattern.events = pattern.events + analysis.run()

    def save_patterns_for_play(self, file_path: str):
        events_for_json = self._get_event_for_json()
        patterns_config = self._get_patterns_config()

        json_file_data = {
            "events": events_for_json,
            "insert": {"patterns": patterns_config},
        }

        with open(file_path, "w") as f:
            json.dump(json_file_data, f, cls=utils.DataClassEncoder, indent=4)

    def _get_event_for_json(self):
        events_for_json = []
        for pattern in self.patterns:
            events_for_json = events_for_json + pattern.events

        return events_for_json

    def _get_patterns_config(self):
        patterns_config = []
        for pattern in self.patterns_config:
            pattern_config = {"name": pattern["name"], "code": pattern["code"]}
            patterns_config.append(pattern_config)

        return patterns_config


def initialize_game_dataset(
    tracking_meta_data_file: str, tracking_data_file: str
) -> GameDataset:

    tracking_data_package = _initialize_data_package(
        data_type=DataType.TRACKING,
        data_file=tracking_data_file,
        meta_data_file=tracking_meta_data_file,
    )

    return GameDataset(tracking=tracking_data_package)


def _initialize_data_package(
    data_type: DataType, data_file: str, meta_data_file: str
) -> DataPackage:

    data_package = DataPackage(
        data_type=data_type,
        data_file=data_file,
        meta_data_file=meta_data_file,
    )

    data_package.load_dataset()

    data_package.build_dataframe()

    return data_package
