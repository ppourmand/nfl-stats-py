# Parses pro-football-reference to gather player stats for comparison
using beautifulsoup4

# Usage
```
from nfl_stats.player import QB

tb = QB("Tom Brady")
tb.set_stats("2017)
tb.print_stats()
```
