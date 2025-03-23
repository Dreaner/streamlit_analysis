# 传球数据分析
任务目标：写一个库，这个库能够包含几个类，每个类负责一种动作。

每种动作

#call statsbombpy API to get all free competitions
#free_comps = sb.competitions()

#call the statsbombpy API to get a list of matches for a given competition
#competition_id=9, season_id=281
leverkusen_2024_matches = sb.matches(competition_id=9, season_id=281)

#print a list of columns available in the event data
#print(events_df.columns)

## 要写的类

### Pass
统计传球次数，并排序

绘制球员传球数排序，堆叠条形图

### Shoot
统计射门次数, 并排序


### Touch
统计一些触球情况

一个球员在球场上的热点图



