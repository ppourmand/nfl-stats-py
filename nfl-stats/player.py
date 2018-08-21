class QB:
    def __init__(name:str):
        self.name: str = name
        self.number: int = 0
        self.position: str = "QB"
        self.team: str = ""
        self.games_played: int = 0
        self.games_started: int = 0
        self.passes_completed: int = 0
        self.passes_attempted: int = 0
        self.pass_completion_percentage: float = 0.0
        self.yards_gained_by_passing: int = 0
        self.passing_touchdowns: int = 0
        self.passing_touchdown_percentage: float = 0.0
        self.interceptions: int = 0
        self.interception_percentage: float = 0.0
        self.longest_completed_pass: int = 0
        self.yards_gained_per_pass_attempt: int = 0
        self.yards_gained_per_pass_completion: int = 0
        self.rating: int = 0
        self.times_sacked: int = 0
        self.yards_lost_due_to_sacks: int = 0
        self.approximate_value: int = 0

    def get_stats(year:str ) -> None:
        pass

class WR:
    def __init__(name: str):
        self.name: str = name
        self.number: int = 0
        self.team: str = ""
        self.position: str = "WR"
        self.games_played: int = 0
        self.games_started: int = 0
        self.pass_targets: int = 0
        self.receptions: int = 0
        self.receiving_yards: int = 0
        self.yards_per_reception: float = 0.0
        self.receiving_touchdowns: int = 0
        self.longest_reception: int = 0
        self.receptions_per_game: float = 0.0
        self.receiving_yards_per_game: float = 0.0
        self.catch_percentage: float = 0.0
        self.rush_attempts: int = 0
        self.rushing_yards: int = 0
        self.rushing_touchdowns: int = 0
        self.longest_rushing_attempt: int = 0
        self.rushing_yards_per_attempt: int = 0
        self.rushing_yards_per_game: int = 0
        self.rushing_attempts_per_game: int = 0
        self.touches: int = 0
        self.approximate_value: int = 0

    def get_stats(year: str) -> None:
        pass

class RB:
    def __init__(name: str):
        self.name: str = name
        self.number: int = 0
        self.team: str = ""
        self.position: str = "RB"
        self.games_played: int = 0
        self.games_started: int = 0
        self.rushing_attempts: int = 0
        self.rushing_yards: int = 0
        self.rushing_touchdowns: int = 0
        self.longest_rushing_attempt: int = 0
        self.rushing_yards_per_attempt: int = 0
        self.rushing_yards_per_game: int = 0
        self.rushing_attempts_per_game: int = 0
        self.pass_targets: int = 0
        self.receptions: int = 0
        self.receiving_yards: int = 0
        self.receiving_yards_per_reception: int = 0
        self.receiving_touchdowns: int = 0
        self.longest_reception: int = 0
        self.receptions_per_game: int = 0
        self.receiving_yards_per_game: int = 0
        self.catch_percentage: float = 0.0
        self.approximate_value: int = 0

    def get_stats(year: std) -> None:
        pass

class K:
    def __init__(name: str):
        self.name: str = name
        self.number: int = 0
        self.team: str = ""
        self.position: str = "K"
        self.games_played: int = 0
        self.games_started: int = 0
        self.field_goal_attempts_20_to_29: int = 0
        self.field_goals_made_20_to_29: int = 0
        self.field_goal_attempts_30_to_39: int = 0
        self.fields_goals_made_30_to_39: int = 0
        self.field_goal_attempts_40_to_49: int = 0
        self.field_goals_made_40_to_49: int = 0
        self.field_goal_attempts_50_plus: int = 0
        self.field_goals_made_50_plus: int = 0
        self.longest_field_goal_made: int = 0
        self.total_field_goals_attmpted: int = 0
        self.total_field_goals_made: int = 0
        self.total_field_goal_percentage: float = 0.0
        self.extra_points_attempted: int = 0
        self.extra_points_made: int = 0
        self.extra_points_percentage: float = 0.0
        self.approximate_value: int = 0

    def get_stats(year: std) -> None:
        pass

class TE:
    def __init__(name: str):
        self.name: str = name
        self.number: int = 0
        self.team: str = ""
        self.position: str = "TE"
        self.games_played: int = 0
        self.games_started: int = 0
        self.targets: int = 0
        self.receptions: int = 0
        self.receiving_yards: int = 0
        self.receiving_yards_per_reception: float = 0.0
        self.receiving_touchdowns: int = 0
        self.longest_reception: int = 0
        self.receptions_per_game: float = 0.0
        self.receiving_yards_per_game: float = 0.0
        self.catch_percentage: float = 0.0
        self.rushing_attempts: int = 0
        self.rushing_yards: int = 0
        self.rushing_touchdowns: int = 0
        self.longest_rushing_attempt: int = 0
        self.touches: int = 0
        self.all_purpose_yards: int = 0
        self.fumbles: int = 0
        self.approximate_value: int = 0

    def get_stats(year: std) -> None:
        pass


