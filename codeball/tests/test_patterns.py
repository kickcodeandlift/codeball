import pickle
from codeball.models import GameDataset, Pattern
import codeball.patterns as patt


class TestPatterns:
    def setup_class(self):
        with open(r"./codeball/tests/files/game_dataset.obj", "rb") as f:
            self.game_dataset = pickle.load(f)

    def test_team_stretched(self):
        parameters = {"team_code": "FIFATMA", "threshold": 40}
        team_stretched = patt.TeamStretched(
            game_dataset=self.game_dataset,
            name="Test Team Stretched",
            code="TEST_001",
            parameters=parameters,
        )
        events = team_stretched.run()

        assert len(events) > 0

    def test_set_pieces(self):
        set_pieces = patt.SetPieces(
            game_dataset=self.game_dataset, name="Set Pieces", code="TEST_002"
        )
        events = set_pieces.run()

        assert len(events) > 0

    def test_passes_into_the_box(self):
        passes_into_the_box = patt.PassesIntoTheBox(
            game_dataset=self.game_dataset,
            name="Passes into the box",
            code="TEST_003",
        )
        events = passes_into_the_box.run()

        assert len(events) > 0
