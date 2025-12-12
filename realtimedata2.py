from nba_api.stats.endpoints import leaguedashplayerstats # pyright: ignore[reportMissingImports]
import datetime
import schedule
import time
import subprocess

# Example call — adjust parameters as needed
df = leaguedashplayerstats.LeagueDashPlayerStats(
    per_mode_detailed='Totals',
    season_type_all_star='Regular Season',
).get_data_frames()[0]

df.drop(df.columns[1], axis=1)
df.to_excel(f"nba_player_totals_{datetime.datetime.now()}.xlsx", index=False)
