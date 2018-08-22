import os
import yaml

from bs4 import BeautifulSoup
import requests

class QB:
    def __init__(self, name:str):
        self.name: str = name
        self.number: str = ""
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
        self.yards_gained_per_pass_attempt: float = 0.0
        self.yards_gained_per_pass_completion: float = 0.0
        self.qb_rating: float = 0.0
        self.times_sacked: int = 0
        self.yards_lost_due_to_sacks: int = 0
        self.approximate_value: int = 0
        self.year = ""

    def set_stats(self, year:str ) -> None:
        """Gets html of player site, sets values for the year

        TODO: have better exception handling for requests/bs4

        :param year: the year to get stats from
        :return: None
        """
        first_letter_lastname = list(self.name.split()[1])[0].upper() # lol so convoluted
        first_four_lastname = self.name.split()[1][0:4]
        first_two_firstname = self.name.split()[0][0:2]
        self.year = year

        request_url = "https://www.pro-football-reference.com/players/{}/{}{}00.htm".format(first_letter_lastname,
                                                                                         first_four_lastname,
                                                                                         first_two_firstname)
        try:
            response = requests.get(request_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            stats_for_year = soup.find("tr", {"id": "passing.{}".format(year)})

            self.team  = stats_for_year.find("td", {"data-stat": "team"}).find('a').text
            self.position = stats_for_year.find("td", {"data-stat": "pos"}).text
            self.number = stats_for_year.find("td", {"data-stat": "uniform_number"}).text 
            self.games_played = int(stats_for_year.find("td", {"data-stat": "g"}).text)
            self.games_started = int(stats_for_year.find("td", {"data-stat": "gs"}).text)
            self.passes_completed = int(stats_for_year.find("td", {"data-stat": "pass_cmp"}).text)
            self.passes_attempted = int(stats_for_year.find("td", {"data-stat": "pass_att"}).text)
            self.pass_completion_percentage = float(stats_for_year.find("td", {"data-stat": "pass_cmp_perc"}).text)
            self.yards_gained_by_passing = int(stats_for_year.find("td", {"data-stat": "pass_yds"}).text)
            self.passing_touchdowns = int(stats_for_year.find("td", {"data-stat": "pass_td"}).text)
            self.passing_touchdown_percentage = float(stats_for_year.find("td", {"data-stat": "pass_td_perc"}).text) 
            self.interceptions = int(stats_for_year.find("td", {"data-stat": "pass_int"}).text)
            self.interception_percentage = float(stats_for_year.find("td", {"data-stat": "pass_int_perc"}).text)
            self.longest_completed_pass = int(stats_for_year.find("td", {"data-stat": "pass_long"}).text)
            self.yards_gained_per_pass_attempt = float(stats_for_year.find("td", {"data-stat": "pass_yds_per_att"}).text)
            self.yards_gained_per_pass_completion = float(stats_for_year.find("td", {"data-stat": "pass_yds_per_cmp"}).text)
            self.qb_rating = float(stats_for_year.find("td", {"data-stat": "qbr"}).text)
            self.times_sacked = int(stats_for_year.find("td", {"data-stat": "pass_sacked"}).text)
            self.yards_lost_due_to_sacks = int(stats_for_year.find("td", {"data-stat": "pass_sacked_yds"}).text)
            self.approximate_value = int(stats_for_year.find("td", {"data-stat": "av"}).text)
        except Exception as e:
            print(e)

    def print_stats(self) -> None:
        print("Year: {}".format(self.year))
        print("Name: {}".format(self.name))
        print("Number: {}".format(self.number))
        print("Position : {}".format(self.position))
        print("Team: {}".format(self.team))
        print("Games played: {}".format(self.games_played))
        print("Games started: {}".format(self.games_started))
        print("Passes completed: {}".format(self.passes_completed))
        print("Passes attempted: {}".format(self.passes_attempted))
        print("Pass completion %: {}".format(self.pass_completion_percentage))
        print("Yards gained by passing: {}".format(self.yards_gained_by_passing))
        print("Passing touchdowns: {}".format(self.passing_touchdowns))
        print("Passing touchdown percentage: {}".format(self.passing_touchdown_percentage))
        print("Interceptions: {}".format(self.interceptions))
        print("Interception percentage: {}".format(self.interception_percentage))
        print("Longest completed pass: {}".format(self.longest_completed_pass))
        print("Yards gained per pass attempted: {}".format(self.yards_gained_per_pass_attempt))
        print("Yards gained per pass completion: {}".format(self.yards_gained_per_pass_completion))
        print("Rating: {}".format(self.qb_rating))
        print("Times sacked: {}".format(self.times_sacked))
        print("Yards lost due to sacks: {}".format(self.yards_lost_due_to_sacks))
        print("Approximate value: {}".format(self.approximate_value))

    def save_stats_to_yaml(self) -> None:
        """Once we have a queried for a years stats, lets save it so we dont spam the hell out of
        their website.

        :return: None
        """

        # if the directory for proper organizatio doesn't exist, make it
        directory = "./players/{}_{}/".format(self.name.split()[0], self.name.split()[1]) 
        if not os.path.exists(directory):
            os.makedirs(directory)        

        data = {
            "name": self.name,
            "number": self.number,
            "position": self.position,
            "team": self.team,
            "games_played": self.games_played,
            "games_sarted": self.games_started,
            "passes_completed": self.passes_completed,
            "passes_attempted": self.passes_attempted,
            "pass_completion_perc": self.pass_completion_percentage,
            "yards_gained_by_passing": self.yards_gained_by_passing,
            "passing_touchdowns": self.passing_touchdowns,
            "passing_touchdown_perc": self.passing_touchdown_percentage,
            "interceptions": self.interceptions,
            "interception_perc": self.interception_percentage,
            "longest_completed_pass": self.longest_completed_pass,
            "yards_gained_per_pass_attempt": self.yards_gained_per_pass_attempt,
            "yards_gained_per_pass_completion": self.yards_gained_per_pass_completion,
            "qb_rating": self.qb_rating,
            "times_sacked": self.times_sacked,
            "yards_lost_due_to_sacks":  self.yards_lost_due_to_sacks,
            "approximate_value": self.approximate_value
        }

        with open("{}/{}.yaml".format(directory, self.year), "w") as file:
            yaml.dump(data, file, default_flow_style=False)

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

    def get_stats(year: str) -> None:
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

    def get_stats(year: str) -> None:
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

    def get_stats(year: str) -> None:
        pass



tom = QB("Tom Brady")
tom.set_stats("2017")
tom.print_stats()
tom.save_stats_to_yaml()

