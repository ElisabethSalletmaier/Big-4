Data Science Project: Analysing the Win/Loss Ratio of the "Big 4"

install requirements from poetry file,

run main.py file

Analysing the 4 biggest sport leagues in the USA:  the Major League Baseball (MLB), the National Basketball Association (NBA), the National Football League (NFL), and the National Hockey League (NHL).
For each sport the win/loss ratio's correlation with the population of the city is calculated using pearsonr. Only data from 2018 is used. 
Furthermore, the project explores the null hypothesis that sport teams in the same region perform the same within their respective sports (given that a region has at least 2 sport teams in different sports).
This will be explored with a series of paired t-tests between all pairs of sports. Where a sport has multiple teams in one region, values are averaged.
Are there any sports where we can reject the null hypothesis?

The result shows that a high positive value (close to 1) indicates that the performance ratios between the two sports leagues are very similar (e.g. NBA-NFL 0.94 , or MLB-NBA 0.95, NFL-MLB 0.80), suggesting that teams in those leagues
tend to perform similarly within their respective sports. On the opposite, for e.g. NHL-NFL (0.03) or NHl-NBA (0.02) or NHl-MLB (0.0007) the similarity in their performance ratio is quite low. 
The p-value is below the typical significance level of 0.05, indicating statistical significance. Therefore, the null hypothesis for those sport leagues can be rejected.

