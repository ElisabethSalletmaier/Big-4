import pandas as pd
import numpy as np
import scipy.stats as stats
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

# data
nhl_df = pd.read_csv("data/nhl.csv")
nba_df = pd.read_csv("data/nba.csv")
mlb_df = pd.read_csv("data/mlb.csv")
nfl_df = pd.read_csv("data/nfl.csv")
cities = pd.read_html("data/wikipedia_data.html")[1]
cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]
cities_city = cities[["Metropolitan area"]]


def calculate_ratio(df, sport_col):
    """
    calculates the win/loss ratio
    """
    df.loc[:, "W"] = pd.to_numeric(df.loc[:, "W"], errors="coerce")
    df.loc[:, "L"] = pd.to_numeric(df.loc[:, "L"], errors="coerce")
    df = df.dropna().copy()
    df.loc[:, f"ratio_{sport_col}"] = df.loc[:, "W"] / (df.loc[:, "W"] + df.loc[:, "L"])
    return df


def corr_with_population(city_df, final_df, sports_col):
    merged_df = pd.merge(city_df, final_df, how="left", on="team")
    merged_df["Population"] = pd.to_numeric(merged_df["Population"])
    merged_df.dropna(inplace=True)
    population_by_region = merged_df["Population"].to_list()
    win_loss_by_region = merged_df[f"ratio_{sports_col}"].to_list()

    pearson_result = stats.pearsonr(population_by_region, win_loss_by_region)
    print(f"{sports_col.upper()} Pearson correlation coefficient: {pearson_result[0]}")
    print(f"{sports_col.upper()} p-value: {pearson_result[1]}")
    return pearson_result


def nhl_correlation():
    """
     calculates the win/loss ratio's correlation with the population of the city it is in for the NHL using 2018 data
    :return:
    """
    nhl_2018 = nhl_df[nhl_df["year"] == 2018]
    nhl_2018.loc[:, "team"] = [x.replace("*", "") for x in nhl_2018.loc[:, "team"]]
    nhl_18_winn = nhl_2018[["team", "W", "L", "year"]]
    nhl_wl = calculate_ratio(nhl_18_winn, "nhl")

    city_df = cities.rename(columns={"Population (2016 est.)[8]": "Population", 'Metropolitan area': "City"})
    city_nhl = city_df.loc[:, ['City', 'Population', 'NHL']]
    city_nhl.loc[:, "NHL"] = city_nhl.loc[:, "NHL"].str.split("[").str[0]
    city_nhl.loc[:, "NHL"] = city_nhl.loc[:, 'NHL'].replace(['', '—'], np.nan)
    c_df = city_nhl.dropna()

    c_df = c_df.rename(columns={"NHL": "team"})

    location_list = ["New York", "Tampa Bay", "New Jersey", "Carolina", "Minnesota", "Colorado", "Dallas", "Vegas",
                     "Anaheim", "San Jose", "Arizona", "Washington", "Florida"]
    city_team = []
    new_team_name = []
    for x in cities_city["Metropolitan area"]:
        for z in location_list:
            for y in nhl_wl["team"]:
                if x in y:
                    city_team.append(y)
                    new_name = y.replace(x, "")
                    new_team_name.append(new_name.strip())
                if z in y:
                    city_team.append(y)
                    new_name = y.replace(z, "")
                    new_team_name.append(new_name.strip())
    replace_dict = dict(zip(city_team, new_team_name))
    nhl_wl["team"] = nhl_wl["team"].replace(replace_dict)
    final_nhl_wl = nhl_wl.replace(to_replace=["Rangers", "Devils", "Islanders"], value="Rangers Islanders Devils")
    final_2 = final_nhl_wl.replace(to_replace=["Kings", "Ducks"], value="Kings Ducks")

    final3 = final_2.groupby("team", as_index=False).mean()
    corr_with_population(c_df, final3, "nhl")
    return final3


def nba_correlation():
    """
      calculates the win/loss ratio's correlation with the population of the city it is in for the NBA using 2018 data
     :return:
     """
    nba_2018 = nba_df[nba_df["year"] == 2018]
    nba_2018.loc[:, "team"] = [x.replace('*', "") for x in nba_2018["team"]]
    nba_2018.loc[:, "team"] = nba_2018.loc[:, "team"].str.replace(r'\s*\(.*\)\s*', '', regex=True)

    nba_18_winn = nba_2018[["team", "W", "L", "year"]]
    nba_wl = calculate_ratio(nba_18_winn, "nba")

    city_df = cities.rename(columns={"Population (2016 est.)[8]": "Population", 'Metropolitan area': "City"})
    city_nba = city_df[['City', 'Population', 'NBA']]
    city_nba.loc[:, "NBA"] = city_nba.loc[:, "NBA"].str.split("[").str[0]
    city_nba.loc[:, "NBA"] = city_nba.loc[:, 'NBA'].replace(['', '—'], np.nan)
    c_df = city_nba.dropna()
    c_df = c_df.rename(columns={"NBA": "team"})

    location_list = ["Indiana", "Miami", "Brooklyn", "Golden State", "Utah", "New York", "Tampa Bay", "New Jersey",
                     "Carolina", "Minnesota", "Colorado", "Dallas", "Vegas", "Anaheim", "San Jose", "Arizona",
                     "Washington", "Florida"]
    city_team = []
    new_team_name = []
    for x in cities_city["Metropolitan area"]:
        for z in location_list:
            for y in nba_wl["team"]:
                if x in y:
                    city_team.append(y)
                    new_name = y.replace(x, "")
                    new_team_name.append(new_name.strip())
                if z in y:
                    city_team.append(y)
                    new_name = y.replace(z, "")
                    new_team_name.append(new_name.strip())
    replace_dict = dict(zip(city_team, new_team_name))
    nba_wl["team"].replace(replace_dict, inplace=True)

    final_nba_wl = nba_wl.replace(to_replace=["Knicks", "Nets"], value="Knicks Nets")
    final_2 = final_nba_wl.replace(to_replace=["Lakers", "Clippers"], value="Lakers Clippers")
    final3 = final_2.groupby("team", as_index=False).mean()
    corr_with_population(c_df, final3, "nba")
    return final3


def mlb_correlation():
    """
      calculates the win/loss ratio's correlation with the population of the city it is in for the MLB using 2018 data
     :return:
     """
    mlb_2018 = mlb_df[mlb_df["year"] == 2018]
    mlb_2018.loc[:, "team"] = [x.replace('*', "") for x in mlb_2018.loc[:, "team"]]
    mlb_2018.loc[:, "team"] = mlb_2018.loc[:, "team"].str.replace(r'\s*\(.*\)\s*', '', regex=True)

    mlb_18_winn = mlb_2018[["team", "W", "L", "year"]]
    mlb_wl = calculate_ratio(mlb_18_winn, "mlb")

    city_df = cities.rename(columns={"Population (2016 est.)[8]": "Population", 'Metropolitan area': "City"})
    city_mlb = city_df[['City', 'Population', 'MLB']]
    city_mlb.loc[:, "MLB"] = city_mlb.loc[:, "MLB"].str.split("[").str[0]
    city_mlb.loc[:, "MLB"] = city_mlb.loc[:, 'MLB'].replace(['', '—'], np.nan)
    c_df = city_mlb.dropna()
    c_df = c_df.rename(columns={"MLB": "team"})

    location_list = ["Oakland", "Texas", "San Francisco", "Indiana", "Miami", "Brooklyn", "Golden State", "Utah",
                     "New York", "Tampa Bay", "New Jersey", "Carolina", "Minnesota", "Colorado", "Dallas", "Vegas",
                     "Anaheim", "San Jose", "Arizona", "Washington", "Florida"]
    city_team = []
    new_team_name = []
    for x in cities_city["Metropolitan area"]:
        for z in location_list:
            for y in mlb_wl["team"]:
                if x in y:
                    city_team.append(y)
                    new_name = y.replace(x, "")
                    new_team_name.append(new_name.strip())
                if z in y:
                    city_team.append(y)
                    new_name = y.replace(z, "")
                    new_team_name.append(new_name.strip())
    replace_dict = dict(zip(city_team, new_team_name))
    mlb_wl.loc[:, "team"].replace(replace_dict, inplace=True)

    final_2 = mlb_wl.replace(
        to_replace=["Dodgers", "Angels", "Yankees", "Mets", "Cubs", "White Sox", "Giants", "Athletics"],
        value=["Dodgers Angels", "Dodgers Angels", "Yankees Mets", "Yankees Mets", "Cubs White Sox", "Cubs White Sox",
               "Giants Athletics", "Giants Athletics"])

    final3 = final_2.groupby("team", as_index=False).mean()
    corr_with_population(c_df, final3, "mlb")
    return final3


def nfl_correlation():
    """
      calculates the win/loss ratio's correlation with the population of the city it is in for the NFL using 2018 data
     :return:
     """
    nfl_2018 = nfl_df[nfl_df["year"] == 2018]
    nfl_2018.loc[:, "team"] = [x.replace('+', "") for x in nfl_2018.loc[:, "team"]]
    nfl_2018.loc[:, "team"] = [x.replace('*', "") for x in nfl_2018.loc[:, "team"]]
    nfl_18_winn = nfl_2018[["team", "W", "L", "year"]]
    nfl_wl = calculate_ratio(nfl_18_winn, "nfl")

    city_df = cities.rename(columns={"Population (2016 est.)[8]": "Population", 'Metropolitan area': "City"})
    city_nfl = city_df[['City', 'Population', 'NFL']]
    city_nfl.loc[:, "NFL"] = city_nfl.loc[:, "NFL"].str.split("[").str[0]
    city_nfl.loc[:, "NFL"] = city_nfl.loc[:, 'NFL'].replace(['', '— '], np.nan)
    city_nfl.loc[:, "NFL"] = city_nfl.loc[:, 'NFL'].replace(['', '—'], np.nan)
    c_df = city_nfl.dropna()
    c_df = c_df.rename(columns={"NFL": "team"})

    location_list = ["New England", "Indianapolis", "Tennessee", "Oakland", "Texas", "San Francisco", "Miami",
                     "Brooklyn", "Golden State", "Utah", "New York", "Tampa Bay", "New Jersey", "Carolina", "Minnesota",
                     "Colorado", "Dallas", "Vegas", "Anaheim", "San Jose", "Arizona", "Washington", "Florida"]
    city_team = []
    new_team_name = []
    for x in cities_city["Metropolitan area"]:
        for z in location_list:
            for y in nfl_wl["team"]:
                if x in y:
                    city_team.append(y)
                    new_name = y.replace(x, "")
                    new_team_name.append(new_name.strip())
                if z in y:
                    city_team.append(y)
                    new_name = y.replace(z, "")
                    new_team_name.append(new_name.strip())
    replace_dict = dict(zip(city_team, new_team_name))
    nfl_wl.loc[:, "team"].replace(replace_dict, inplace=True)

    final_2 = nfl_wl.replace(to_replace=["Giants", "Jets", "Rams", "Chargers", "49ers", "Raiders"],
                             value=["Giants Jets", "Giants Jets", "Rams Chargers", "Rams Chargers", "49ers Raiders",
                                    "49ers Raiders"])

    final3 = final_2.groupby("team", as_index=False).mean()
    corr_with_population(c_df, final3, "nfl")
    return final3


def sports_team_performance():
    """
     explores the null hypothesis that sport teams in the same region perform the same within their respective sports (given
     that a region has at least 2 sport teams in different sports).
     This will be explored with a series of paired t-tests between all pairs of sports.
     Are there any sports where we can reject the null hypothesis?
     Where a sport has multiple teams in one region, values are averaged.

     The result shows that a high positive value (close to 1) indicates that the performance ratios between the two sports
     leagues are very similar (e.g. NBA-NFL 0.94 , or MLB-NBA 0.95, NFL-MLB 0.80), suggesting that teams in those leagues
     tend to perform similarly within their respective sports.
     On the opposite, for e.g. NHL-NFL (0.03) or NHl-NBA (0.02) or NHl-MLB (0.0007) the similarity in their
     performance ratio is quite low. The p-value is below the typical significance level of 0.05, indicating statistical
     significance. Therefore, the null hypothesis for those sport leagues can be rejected.

    :return:
    """
    # NHL
    final_nhl = nhl_correlation()
    final_nhl.rename(columns={"team": "NHL"}, inplace=True)
    nhl_clean = final_nhl[["NHL", "ratio_nhl"]]

    # NBA
    final_nba = nba_correlation()
    final_nba.rename(columns={"team": "NBA"}, inplace=True)
    nba_clean = final_nba[["NBA", "ratio_nba"]]

    # MLB
    final_mlb = mlb_correlation()
    final_mlb.rename(columns={"team": "MLB"}, inplace=True)
    mlb_clean = final_mlb[["MLB", "ratio_mlb"]]

    # NFL
    final_nfl = nfl_correlation()
    final_nfl.rename(columns={"team": "NFL"}, inplace=True)
    nfl_clean = final_nfl[["NFL", "ratio_nfl"]]

    # CITY
    city = cities.rename(columns={"Population (2016 est.)[8]": "Population", 'Metropolitan area': "City"})

    columns_sport = ["NFL", "MLB", "NBA", "NHL"]
    for col in columns_sport:
        city[col] = city[col].str.split("[").str[0]
        city[col] = city[col].replace(['', '— '], np.nan)
        city[col] = city[col].replace(['', '—'], np.nan)

    city['nr_nan'] = city.isna().sum(axis=1)
    city_df = city[city["nr_nan"] < 3]

    merge1 = pd.merge(city_df, nhl_clean, how="left", on="NHL")
    merge2 = pd.merge(merge1, mlb_clean, how="left", on="MLB")
    merge3 = pd.merge(merge2, nba_clean, how="left", on="NBA")
    merge4 = pd.merge(merge3, nfl_clean, how="left", on="NFL")
    columns = ["ratio_nfl", "ratio_mlb", "ratio_nba", "ratio_nhl"]
    final_df = merge4[columns]

    sports = ["ratio_nfl", "ratio_nba", "ratio_nhl", "ratio_mlb"]
    p_values = pd.DataFrame({k: np.nan for k in sports}, index=sports)

    for row in final_df:
        for sport in final_df:
            p_values.loc[row, sport] = stats.ttest_rel(final_df[row], final_df[sport], nan_policy="omit")[1]
    print(p_values)
    return p_values


sports_team_performance()