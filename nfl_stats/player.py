import os
import yaml
from pathlib import Path

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
        """
        Gets the statistics from the scraped site and sets appriopiate variables.

        TODO: 
            - have better exception handling for requests/bs4

        Parameters:
            year - the year to get statistics for
        Returns:
            None
        """
        first_letter_lastname = list(self.name.split()[1])[0].upper() # lol so convoluted
        first_four_lastname = self.name.split()[1][0:4]
        first_two_firstname = self.name.split()[0][0:2]
        self.year = year
        
        if self.is_player_stats_cached():
            print(">> Player stats cached for year, setting from cache")
            self.set_player_stats_from_cache()
            return
        
        print(">> Retrieving data from pro-football-reference.com")

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

            # save it to its own file for later retrieval
            self.save_stats_to_yaml()
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
        """
        Saves statistical data to a yaml file

        Returns:
            - None
        """
        # if the directory for proper organization doesn't exist, make it
        directory = "./players/QB/{}_{}/".format(self.name.split()[0], self.name.split()[1]) 
        if not os.path.exists(directory):
            os.makedirs(directory)        

        data = {
            "name": self.name,
            "number": self.number,
            "position": self.position,
            "team": self.team,
            "games_played": self.games_played,
            "games_started": self.games_started,
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
    
    def is_player_stats_cached(self) -> bool:
        """
        Checks if the player + year yaml file exists

        Returns:
            - bool: True if player file exists, False otherwise
        """
        player_file = Path("./players/QB/{}_{}/{}.yaml".format(self.name.split()[0], self.name.split()[1], self.year))
        return player_file.is_file()
    
    def set_player_stats_from_cache(self) -> None:
        """
        Reads the corresponding yaml file and set player stats.

        Returns:
            - None
        """
        player_file = "./players/QB/{}_{}/{}.yaml".format(self.name.split()[0], self.name.split()[1], self.year)

        with open(player_file, "r") as file:
            try:
                yaml_data = yaml.safe_load(file)
                self.name = yaml_data["name"]
                self.number = yaml_data["number"]
                self.team = yaml_data["team"] 
                self.games_played = yaml_data["games_played"]
                self.games_started = yaml_data["games_started"]
                self.passes_completed = yaml_data["passes_completed"]
                self.passes_attempted = yaml_data["passes_attempted"]
                self.pass_completion_percentage = yaml_data["pass_completion_perc"]
                self.yards_gained_by_passing = yaml_data["yards_gained_by_passing"]
                self.passing_touchdowns = yaml_data["passing_touchdowns"]
                self.passing_touchdown_percentage = yaml_data["passing_touchdown_perc"]
                self.interceptions = yaml_data["interceptions"]
                self.interception_percentage = yaml_data["interception_perc"]
                self.longest_completed_pass = yaml_data["longest_completed_pass"]
                self.yards_gained_per_pass_attempt = yaml_data["yards_gained_per_pass_attempt"]
                self.yards_gained_per_pass_completion = yaml_data["yards_gained_per_pass_completion"]
                self.qb_rating = yaml_data["qb_rating"]
                self.times_sacked = yaml_data["times_sacked"]
                self.yards_lost_due_to_sacks = yaml_data["yards_lost_due_to_sacks"]
                self.approximate_value = yaml_data["approximate_value"]
            except yaml.YAMLError as e:
                print(e)


class WR:
    def __init__(self, name: str):
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
        self.rush_attempts: int = 0
        self.rushing_yards: int = 0
        self.rushing_touchdowns: int = 0
        self.longest_rushing_attempt: int = 0
        self.rushing_yards_per_attempt: float = 0.0
        self.rushing_yards_per_game: float = 0.0
        self.rushing_attempts_per_game: float = 0.0
        self.touches: int = 0
        self.approximate_value: int = 0
        self.fumbles: int = 0

    def set_stats(self, year: str) -> None:
        """
        Given the year, scrape pro-football-reference to get stats

        Parameters:
            year - the year to get statistics for
        Returns:
            - None
        """
        first_letter_lastname = list(self.name.split()[1])[0].upper() # lol so convoluted
        first_four_lastname = self.name.split()[1][0:4]
        first_two_firstname = self.name.split()[0][0:2]
        self.year = year

        if self.is_player_stats_cached():
            print(">> Player stats cached for year, setting from cache")
            self.set_stats_from_cache()
            return

        print(">> Retrieving data from pro-football-reference.com")

        request_url = "https://www.pro-football-reference.com/players/{}/{}{}00.htm".format(first_letter_lastname,
                                                                                            first_four_lastname,
                                                                                            first_two_firstname)
        
        try:
            response = requests.get(request_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            stats_for_year = soup.find("tr", {"id": "receiving_and_rushing.{}".format(year)})
            self.number = int(stats_for_year.find("td", {"data-stat": "uniform_number"}).text)
            self.team = stats_for_year.find("td", {"data-stat": "team"}).find('a').text 
            self.position = stats_for_year.find("td", {"data-stat":"pos"}).text
            self.games_played = int(stats_for_year.find("td", {"data-stat":"g"}).text)
            self.games_started = int(stats_for_year.find("td", {"data-stat":"gs"}).text)
            self.pass_targets = int(stats_for_year.find("td", {"data-stat":"targets"}).text)
            self.receptions = int(stats_for_year.find("td", {"data-stat":"rec"}).text)
            self.receiving_yards = int(stats_for_year.find("td", {"data-stat":"rec_yds"}).text)
            self.yards_per_reception = float(stats_for_year.find("td", {"data-stat":"rec_yds_per_rec"}).text)
            self.receiving_touchdowns = int(stats_for_year.find("td", {"data-stat":"rec_td"}).text)
            self.longest_reception = int(stats_for_year.find("td", {"data-stat":"rec_long"}).text)
            self.receptions_per_game = float(stats_for_year.find("td", {"data-stat":"rec_per_g"}).text)
            self.receiving_yards_per_game = float(stats_for_year.find("td", {"data-stat":"rec_yds_per_g"}).text)
            self.rush_attempts = int(stats_for_year.find("td", {"data-stat":"rush_att"}).text)
            self.rushing_yards = int(stats_for_year.find("td", {"data-stat":"rush_yds"}).text)
            self.rushing_touchdowns = int(stats_for_year.find("td", {"data-stat":"rush_td"}).text)
            self.longest_rushing_attempt = int(stats_for_year.find("td", {"data-stat":"rush_long"}).text)
            self.rushing_yards_per_attempt = float(stats_for_year.find("td", {"data-stat":"rush_yds_per_att"}).text)
            self.rushing_yards_per_game = float(stats_for_year.find("td", {"data-stat":"rush_yds_per_g"}).text)
            self.rushing_attempts_per_game = float(stats_for_year.find("td", {"data-stat":"rush_att_per_g"}).text)
            self.touches = int(stats_for_year.find("td", {"data-stat":"touches"}).text)
            self.fumbles = int(stats_for_year.find("td", {"data-stat":"fumbles"}).text)
            self.approximate_value = int(stats_for_year.find("td", {"data-stat":"av"}).text)
            self.save_stats_to_yaml()
        except Exception as e:
            print(e)
    
    def save_stats_to_yaml(self) -> None:
        """
        Saves data scraped to a yaml file for caching.

        Returns:
            - None
        """
        # if the directory for proper organization doesn't exist, make it
        directory = "./players/WR/{}_{}/".format(self.name.split()[0], self.name.split()[1]) 
        if not os.path.exists(directory):
            os.makedirs(directory)     

        data = {
            "name": self.name,
            "number": self.number,
            "team": self.team,
            "position": self.position,
            "games_played": self.games_played,
            "games_started": self.games_started,
            "pass_targets": self.pass_targets,
            "receptions": self.receptions,
            "receiving_yards": self.receiving_yards,
            "yards_per_reception": self.yards_per_reception,
            "receiving_touchdowns": self.receiving_touchdowns,
            "longest_reception": self.longest_reception,
            "receptions_per_game": self.receptions_per_game,
            "receiving_yards_per_game": self.receiving_yards_per_game,
            "rush_attempts": self.rush_attempts,
            "rushing_yards": self.rushing_yards,
            "rushing_touchdowns": self.rushing_touchdowns,
            "longest_rushing_attempt": self.longest_rushing_attempt,
            "rushing_yards_per_attempt": self.rushing_yards_per_attempt,
            "rushing_yards_per_game": self.rushing_yards_per_game,
            "rushing_attempts_per_game": self.rushing_attempts_per_game,
            "touches": self.touches,
            "approximate_value": self.approximate_value,
            "fumbles": self.fumbles
        } 

        with open("{}/{}.yaml".format(directory, self.year), "w") as file:
            yaml.dump(data, file, default_flow_style=False)
        
    def set_stats_from_cache(self) -> None:
        player_file = "./players/WR/{}_{}/{}.yaml".format(self.name.split()[0], self.name.split()[1], self.year)

        with open(player_file, "r") as file:
            try:
                yaml_data = yaml.safe_load(file)
                self.name = yaml_data["name"]
                self.number = yaml_data["number"]
                self.team = yaml_data["team"]
                self.position = yaml_data["position"]
                self.games_played = yaml_data["games_played"]
                self.games_started = yaml_data["games_started"]
                self.pass_targets = yaml_data["pass_targets"]
                self.receptions = yaml_data["receptions"]
                self.receiving_yards = yaml_data["receiving_yards"]
                self.yards_per_reception = yaml_data["yards_per_reception"]
                self.receiving_touchdowns = yaml_data["receiving_touchdowns"]
                self.longest_reception = yaml_data["longest_reception"]
                self.receptions_per_game = yaml_data["receptions_per_game"]
                self.receiving_yards_per_game = yaml_data["receiving_yards_per_game"]
                self.rush_attempts = yaml_data["rush_attempts"]
                self.rushing_yards = yaml_data["rushing_yards"]
                self.rushing_touchdowns = yaml_data["rushing_touchdowns"]
                self.longest_rushing_attempt = yaml_data["longest_rushing_attempt"]
                self.rushing_yards_per_attempt = yaml_data["rushing_yards_per_attempt"]
                self.rushing_yards_per_game = yaml_data["rushing_yards_per_game"]
                self.rushing_attempts_per_game = yaml_data["rushing_attempts_per_game"]
                self.touches = yaml_data["touches"]
                self.approximate_value = yaml_data["approximate_value"]
                self.fumbles = yaml_data["fumbles"]
            except yaml.YAMLError as e:
                print(e)

    def print_stats(self) -> None:
        print(self.name)
        print(self.number)
        print(self.team)
        print(self.position)
        print(self.games_played)
        print(self.games_started)
        print(self.pass_targets)
        print(self.receptions)
        print(self.receiving_yards)
        print(self.yards_per_reception)
        print(self.receiving_touchdowns)
        print(self.longest_reception)
        print(self.receptions_per_game)
        print(self.receiving_yards_per_game)
        print(self.rush_attempts)
        print(self.rushing_yards)
        print(self.rushing_touchdowns)
        print(self.longest_rushing_attempt)
        print(self.rushing_yards_per_attempt)
        print(self.rushing_yards_per_game)
        print(self.rushing_attempts_per_game)
        print(self.touches)
        print(self.approximate_value)
        print(self.fumbles)

    def is_player_stats_cached(self) -> bool:
        player_file = Path("./players/WR/{}_{}/{}.yaml".format(self.name.split()[0], self.name.split()[1], self.year))
        return player_file.is_file()


class RB:
    def __init__(self, name: str):
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
        self.rushing_yards_per_attempt: float = 0.0
        self.rushing_yards_per_game: float = 0.0
        self.rushing_attempts_per_game: float = 0.0
        self.pass_targets: int = 0
        self.receptions: int = 0
        self.receiving_yards: int = 0
        self.receiving_yards_per_reception: float = 0.0
        self.receiving_touchdowns: int = 0
        self.longest_reception: int = 0
        self.receptions_per_game: float = 0.0
        self.receiving_yards_per_game: float = 0.0
        self.approximate_value: int = 0
        self.fumbles: int = 0

    def set_stats(self, year: str) -> None:
        """
        Given the year, scrape pro-football-reference to get stats

        Parameters:
            year - the year to get statistics for
        Returns:
            - None
        """
        first_letter_lastname = list(self.name.split()[1])[0].upper() # lol so convoluted
        first_four_lastname = self.name.split()[1][0:4]
        first_two_firstname = self.name.split()[0][0:2]
        self.year = year

        if self.is_player_stats_cached():
            print(">> Player stats cached for year, setting from cache")
            self.set_stats_from_cache()
            return

        print(">> Retrieving data from pro-football-reference.com")

        request_url = "https://www.pro-football-reference.com/players/{}/{}{}00.htm".format(first_letter_lastname,
                                                                                            first_four_lastname,
                                                                                            first_two_firstname)
        
        try:
            response = requests.get(request_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            stats_for_year = soup.find("tr", {"id": "rushing_and_receiving.{}".format(year)})
            self.number = int(stats_for_year.find("td", {"data-stat": "uniform_number"}).text)
            self.team = stats_for_year.find("td", {"data-stat": "team"}).find('a').text 
            self.games_played = int(stats_for_year.find("td", {"data-stat": "g"}).text)
            self.games_started = int(stats_for_year.find("td", {"data-stat": "gs"}).text)
            self.rushing_attempts = int(stats_for_year.find("td", {"data-stat": "rush_att"}).text)
            self.rushing_yards = int(stats_for_year.find("td", {"data-stat": "rush_yds"}).text)
            self.rushing_touchdowns = int(stats_for_year.find("td", {"data-stat": "rush_td"}).text)
            self.longest_rushing_attempt = int(stats_for_year.find("td", {"data-stat": "rush_long"}).text)
            self.rushing_yards_per_attempt = float(stats_for_year.find("td", {"data-stat": "rush_yds_per_att"}).text)
            self.rushing_yards_per_game = float(stats_for_year.find("td", {"data-stat": "rush_yds_per_g"}).text)
            self.rushing_attempts_per_game = float(stats_for_year.find("td", {"data-stat": "rush_att_per_g"}).text)
            self.pass_targets = int(stats_for_year.find("td", {"data-stat": "targets"}).text)
            self.receptions = int(stats_for_year.find("td", {"data-stat": "rec"}).text)
            self.receiving_yards = int(stats_for_year.find("td", {"data-stat": "rec_yds"}).text)
            self.receiving_yards_per_reception = float(stats_for_year.find("td", {"data-stat": "rec_yds_per_rec"}).text)
            self.receiving_touchdowns = int(stats_for_year.find("td", {"data-stat": "rec_td"}).text)
            self.longest_reception = int(stats_for_year.find("td", {"data-stat": "rec_long"}).text)
            self.receptions_per_game = float(stats_for_year.find("td", {"data-stat": "rec_per_g"}).text)
            self.receiving_yards_per_game = float(stats_for_year.find("td", {"data-stat": "rec_yds_per_g"}).text)
            self.approximate_value = int(stats_for_year.find("td", {"data-stat": "av"}).text)
            self.fumbles = int(stats_for_year.find("td", {"data-stat": "fumbles"}).text)
            self.save_stats()
        except Exception as e:
            print(e)
    
    def save_stats(self) -> None:
        directory = "./players/RB/{}_{}/".format(self.name.split()[0], self.name.split()[1]) 
        if not os.path.exists(directory):
            os.makedirs(directory)    

        data = {
            "name": self.name,
            "number": self.number,
            "team": self.team,
            "games_played": self.games_played,
            "games_started": self.games_started,
            "rushing_attempts": self.rushing_attempts,
            "rushing_yards": self.rushing_yards,
            "rushing_touchdowns": self.rushing_touchdowns,
            "longest_rushing_attempt": self.longest_rushing_attempt,
            "rushing_yards_per_attempt": self.rushing_yards_per_attempt,
            "rushing_yards_per_game": self.rushing_yards_per_game,
            "rushing_attempts_per_game": self.rushing_attempts_per_game,
            "pass_targets": self.pass_targets,
            "receptions": self.receptions,
            "receiving_yards": self.receiving_yards,
            "receiving_yards_per_reception": self.receiving_yards_per_reception,
            "receiving_touchdowns": self.receiving_touchdowns,
            "longest_reception": self.longest_reception,
            "receptions_per_game": self.receptions_per_game,
            "receiving_yards_per_game": self.receiving_yards_per_game,
            "approximate_value": self.approximate_value,
            "fumbles": self.fumbles
        }
        
        with open("{}/{}.yaml".format(directory, self.year), "w") as file:
            yaml.dump(data, file, default_flow_style=False)
    
    def set_stats_from_cache(self) -> None:
        player_file = "./players/RB/{}_{}/{}.yaml".format(self.name.split()[0], self.name.split()[1], self.year)
        
        with open(player_file, "r") as file:
            try:
                yaml_data = yaml.safe_load(file)
                self.number = yaml_data["number"]
                self.team = yaml_data["team"]
                self.games_played = yaml_data["games_played"] 
                self.games_started = yaml_data["games_started"] 
                self.rushing_attempts = yaml_data["rushing_attempts"] 
                self.rushing_yards = yaml_data["rushing_yards"] 
                self.rushing_touchdowns = yaml_data["rushing_touchdowns"] 
                self.longest_rushing_attempt = yaml_data["longest_rushing_attempt"] 
                self.rushing_yards_per_attempt = yaml_data["rushing_yards_per_attempt"] 
                self.rushing_yards_per_game = yaml_data["rushing_yards_per_game"] 
                self.rushing_attempts_per_game = yaml_data["rushing_attempts_per_game"] 
                self.pass_targets = yaml_data["pass_targets"] 
                self.receptions = yaml_data["receptions"] 
                self.receiving_yards = yaml_data["receiving_yards"] 
                self.receiving_yards_per_reception = yaml_data["receiving_yards_per_reception"] 
                self.receiving_touchdowns = yaml_data["receiving_touchdowns"] 
                self.longest_reception = yaml_data["longest_reception"] 
                self.receptions_per_game = yaml_data["receptions_per_game"] 
                self.receiving_yards_per_game = yaml_data["receiving_yards_per_game"] 
                self.approximate_value = yaml_data["approximate_value"] 
                self.fumbles = yaml_data["fumbles"] 
            except yaml.YAMLError as e:
                print(e)
    
    def is_player_stats_cached(self) -> bool:
        player_file = Path("./players/RB/{}_{}/{}.yaml".format(self.name.split()[0], self.name.split()[1], self.year))
        return player_file.is_file()
    
    def print_stats(self) -> None:
        print("Year: {}".format(self.year))
        print("Name: {}".format(self.name))
        print("Number: {}".format(self.number))
        print("Position : {}".format(self.position))
        print("Team: {}".format(self.team))
        print("Games played: {}".format(self.games_played))
        print("Games started: {}".format(self.games_started))
        print("Rushing attempts: {}".format(self.rushing_attempts))
        print("Rushing yards: {}".format(self.rushing_yards))
        print("Rushing touchdowns: {}".format(self.rushing_touchdowns))
        print("Longest rushing attempt: {}".format(self.longest_rushing_attempt))
        print("Rushing yards per attempt: {}".format(self.rushing_yards_per_attempt))
        print("Rushing yards per game: {}".format(self.rushing_yards_per_game))
        print("Pass targets: {}".format(self.pass_targets))
        print("Receptions: {}".format(self.receptions))
        print("Receiving yards: {}".format(self.receiving_yards))
        print("Receiving yards per reception: {}".format(self.receiving_yards_per_reception))
        print("Receiving touchdowns: {}".format(self.receiving_touchdowns))
        print("Longest reception: {}".format(self.longest_reception))
        print("Receptions per game: {}".format(self.receptions_per_game))
        print("Receiving yards per game: {}".format(self.receiving_yards_per_game))
        print("Approximate value: {}".format(self.approximate_value))
        print("Fumbles: {}".format(self.fumbles))
         

class K:
    def __init__(self, name: str):
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
        self.total_field_goals_attempted: int = 0
        self.total_field_goals_made: int = 0
        self.extra_points_attempted: int = 0
        self.extra_points_made: int = 0
        self.approximate_value: int = 0
    
    def set_stats(self, year: str) -> None:
        first_letter_lastname = list(self.name.split()[1])[0].upper() # lol so convoluted
        first_four_lastname = self.name.split()[1][0:4]
        first_two_firstname = self.name.split()[0][0:2]
        self.year = year

        if self.is_player_stats_cached():
            print(">> Player stats cached for year, setting from cache")
            self.set_stats_from_cache()
            return

        print(">> Retrieving data from pro-football-reference.com")

        request_url = "https://www.pro-football-reference.com/players/{}/{}{}00.htm".format(first_letter_lastname,
                                                                                            first_four_lastname,
                                                                                            first_two_firstname)
        try:
            response = requests.get(request_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            stats_for_year = soup.find("tr", {"id": "kicking.{}".format(year)})
            self.number = int(stats_for_year.find("td", {"data-stat": "uniform_number"}).text)
            self.team = stats_for_year.find("td", {"data-stat": "team"}).find('a').text 
            self.games_played = int(stats_for_year.find("td", {"data-stat": "g"}).text)
            self.games_started = int(stats_for_year.find("td", {"data-stat": "gs"}).text)
            self.field_goal_attempts_20_to_29 = int(stats_for_year.find("td", {"data-stat": "fga2"}).text)
            self.field_goals_made_20_to_29 = int(stats_for_year.find("td", {"data-stat": "fgm2"}).text)
            self.field_goal_attempts_30_to_39 = int(stats_for_year.find("td", {"data-stat": "fga3"}).text)
            self.fields_goals_made_30_to_39 = int(stats_for_year.find("td", {"data-stat": "fgm3"}).text)
            self.field_goal_attempts_40_to_49 = int(stats_for_year.find("td", {"data-stat": "fga4"}).text)
            self.field_goals_made_40_to_49 = int(stats_for_year.find("td", {"data-stat": "fgm4"}).text)
            self.field_goal_attempts_50_plus = int(stats_for_year.find("td", {"data-stat": "fga5"}).text)
            self.field_goals_made_50_plus = int(stats_for_year.find("td", {"data-stat": "fgm5"}).text)
            self.longest_field_goal_made = int(stats_for_year.find("td", {"data-stat": "fg_long"}).text)
            self.total_field_goals_attempted = int(stats_for_year.find("td", {"data-stat": "fga"}).text)
            self.total_field_goals_made = int(stats_for_year.find("td", {"data-stat": "fgm"}).text)
            self.extra_points_attempted = int(stats_for_year.find("td", {"data-stat": "xpa"}).text)
            self.extra_points_made = int(stats_for_year.find("td", {"data-stat": "xpm"}).text)
            self.approximate_value = int(stats_for_year.find("td", {"data-stat": "av"}).text)
            self.save_stats()
        except Exception as e:
            print(e)
    
    def save_stats(self) -> None:
        directory = "./players/K/{}_{}/".format(self.name.split()[0], self.name.split()[1]) 
        if not os.path.exists(directory):
            os.makedirs(directory)    

        data = {
            "name": self.name,
            "number": self.number,
            "team": self.team,
            "games_played": self.games_played,
            "games_started": self.games_started,
            "field_goal_attempts_20_to_29": self.field_goal_attempts_20_to_29,
            "field_goals_made_20_to_29": self.field_goals_made_20_to_29,
            "field_goal_attempts_30_to_39": self.field_goal_attempts_30_to_39,
            "field_goals_made_30_to_39": self.fields_goals_made_30_to_39,
            "field_goal_attempts_40_to_49": self.field_goal_attempts_40_to_49,
            "field_goals_made_40_to_49": self.field_goals_made_40_to_49,
            "field_goal_attempts_50_plus": self.field_goal_attempts_50_plus,
            "field_goals_made_50_plus": self.field_goals_made_50_plus,
            "longest_field_goal_made": self.longest_field_goal_made,
            "total_field_goals_attempted": self.total_field_goals_attempted,
            "total_field_goals_made": self.total_field_goals_made,
            "extra_points_attempted": self.extra_points_attempted,
            "extra_points_made": self.extra_points_made,
            "approximate_value": self.approximate_value
        }
        
        with open("{}/{}.yaml".format(directory, self.year), "w") as file:
            yaml.dump(data, file, default_flow_style=False)
    
    def set_stats_from_cache(self) -> None:
        player_file = "./players/K/{}_{}/{}.yaml".format(self.name.split()[0], self.name.split()[1], self.year)
        
        with open(player_file, "r") as file:
            try:
                yaml_data = yaml.safe_load(file)
                self.number = yaml_data["number"]
                self.team = yaml_data["team"]
                self.games_played = yaml_data["games_played"] 
                self.games_started = yaml_data["games_started"] 
                self.field_goal_attempts_20_to_29 = yaml_data["field_goal_attempts_20_to_29"]
                self.field_goals_made_20_to_29 =  yaml_data["field_goals_made_20_to_29"]
                self.field_goal_attempts_30_to_39 = yaml_data["field_goal_attempts_30_to_39"]
                self.field_goals_made_30_to_39 = yaml_data["field_goals_made_30_to_39"] 
                self.field_goal_attempts_40_to_49 = yaml_data["field_goal_attempts_40_to_49"] 
                self.field_goals_made_40_to_49 = yaml_data["field_goals_made_40_to_49"]
                self.field_goal_attempts_50_plus = yaml_data["field_goal_attempts_50_plus"] 
                self.field_goals_made_50_plus = yaml_data["field_goals_made_50_plus"] 
                self.longest_field_goal_made = yaml_data["longest_field_goal_made"] 
                self.total_field_goals_attempted = yaml_data["total_field_goals_attempted"] 
                self.total_field_goals_made = yaml_data["total_field_goals_made"] 
                self.extra_points_attempted = yaml_data["extra_points_attempted"] 
                self.extra_points_made = yaml_data["extra_points_made"] 
                self.approximate_value = yaml_data["approximate_value"] 
            except yaml.YAMLError as e:
                print(e)
    
    def is_player_stats_cached(self) -> bool:
        player_file = Path("./players/K/{}_{}/{}.yaml".format(self.name.split()[0], self.name.split()[1], self.year))
        return player_file.is_file()

    def print_stats(self) -> None:
        print("Year: {}".format(self.year))
        print("Name: {}".format(self.name))
        print("Number: {}".format(self.number))
        print("Team: {}".format(self.team))
        print("Position: {}".format(self.position))
        print("Games played: {}".format(self.games_played))
        print("Games started: {}".format(self.games_started))
        print("Field goal attempts (20-29): {}".format(self.field_goal_attempts_20_to_29))
        print("Field goals made (20-29): {}".format(self.field_goals_made_20_to_29))
        print("Field goal attempts (30-39): {}".format(self.field_goal_attempts_30_to_39))
        print("Field goals made (30-39): {}".format(self.fields_goals_made_30_to_39))
        print("Field goal attempts (40-49): {}".format(self.field_goal_attempts_40_to_49))
        print("Field goals made (40-49): {}".format(self.field_goals_made_40_to_49))
        print("Field goal attempts (50+): {}".format(self.field_goal_attempts_50_plus))
        print("Field goals made (50+): {}".format(self.field_goals_made_50_plus))
        print("Longest field goal: {} yd".format(self.longest_field_goal_made))
        print("Total field goals attempted: {}".format(self.total_field_goals_attempted))
        print("Total field goals mdae: {}".format(self.total_field_goals_made))
        print("Extra points attempted: {}".format(self.extra_points_attempted))
        print("Extra points made: {}".format(self.extra_points_made))
        print("Approximate value: {}".format(self.approximate_value))

class TE:
    def __init__(self, name: str):
        self.name: str = name
        self.number: int = 0
        self.team: str = ""
        self.position: str = "TE"
        self.games_played: int = 0
        self.games_started: int = 0
        self.targets: int = 0
        self.receptions: int = 0
        self.receiving_yards: int = 0
        self.receiving_touchdowns: int = 0
        self.longest_reception: int = 0
        self.rushing_attempts: int = 0
        self.rushing_yards: int = 0
        self.rushing_touchdowns: int = 0
        self.touches: int = 0
        self.all_purpose_yards: int = 0
        self.fumbles: int = 0
        self.approximate_value: int = 0

    def set_stats(self, year:str) -> None:
        first_letter_lastname = list(self.name.split()[1])[0].upper() # lol so convoluted
        first_four_lastname = self.name.split()[1][0:4]
        first_two_firstname = self.name.split()[0][0:2]
        self.year = year

        # if self.is_player_stats_cached():
        #     print(">> Player stats cached for year, setting from cache")
        #     self.set_stats_from_cache()
        #     return

        print(">> Retrieving data from pro-football-reference.com")

        request_url = "https://www.pro-football-reference.com/players/{}/{}{}00.htm".format(first_letter_lastname,
                                                                                            first_four_lastname,
                                                                                            first_two_firstname)
        try:
            response = requests.get(request_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            stats_for_year = soup.find("tr", {"id": "receiving_and_rushing.{}".format(year)})
            self.number = int(stats_for_year.find("td", {"data-stat": "uniform_number"}).text)
            self.team = stats_for_year.find("td", {"data-stat": "team"}).find('a').text 
            self.games_played = int(stats_for_year.find("td", {"data-stat": "g"}).text)
            self.games_started = int(stats_for_year.find("td", {"data-stat": "gs"}).text)
            self.targets = int(stats_for_year.find("td", {"data-stat": "targets"}).text)
            self.receptions = int(stats_for_year.find("td", {"data-stat": "rec"}).text)
            self.receiving_yards = int(stats_for_year.find("td", {"data-stat": "rec_yds"}).text)
            self.receiving_touchdowns = int(stats_for_year.find("td", {"data-stat": "rec_td"}).text)
            self.longest_reception = int(stats_for_year.find("td", {"data-stat": "rec_long"}).text)
            self.touches = int(stats_for_year.find("td", {"data-stat": "touches"}).text)
            self.all_purpose_yards = int(stats_for_year.find("td", {"data-stat": "all_purpose_yds"}).text)
            self.fumbles = int(stats_for_year.find("td", {"data-stat": "fumbles"}).text)
            self.approximate_value =  int(stats_for_year.find("td", {"data-stat": "av"}).text)
        except Exception as e:
            print(e)
    
    def save_stats(self) -> None:
        pass
    
    def set_stats_from_cache(self) -> None:
        pass

    def is_player_stats_cached(self) -> bool:
        pass
    
    def print_stats(self) -> None:
        print("Year: {}".format(self.year))
        print("Name: {}".format(self.name))
        print("Number: {}".format(self.number))
        print("Team: {}".format(self.team))
        print("Position: {}".format(self.position))
        print("Games played: {}".format(self.games_played))
        print("Games started: {}".format(self.games_started))
        print("Targets: {}".format(self.targets)) 
        print("Receptions: {}".format(self.receptions)) 
        print("Receiving yards: {}".format(self.receiving_yards)) 
        print("Receiving touchdowns: {}".format(self.receiving_touchdowns)) 
        print("Longest reception: {}".format(self.longest_reception)) 
        print("Touches: {}".format(self.touches)) 
        print("All purpose yards: {}".format(self.all_purpose_yards)) 
        print("Fumbles: {}".format(self.fumbles)) 
        print("Approximate Value: {}".format(self.approximate_value)) 