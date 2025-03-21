#install relevant packages
#pip install statsbombpy
#pip install mplsoccer
#pip install highlight_text

import json

# import packages
from statsbombpy import sb
import pandas as pd
from mplsoccer import VerticalPitch, Pitch
from highlight_text import ax_text, fig_text
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import seaborn as sns

import streamlit as st

# import the analysis_soccer package
# 自己写的库
import analysis_soccer

#call statsbombpy API to get all free competitions
#free_comps = sb.competitions()

#call the statsbombpy API to get a list of matches for a given competition
#competition_id=9, season_id=281
leverkusen_2024_matches = sb.matches(competition_id=9, season_id=281)

#print the first 5 matches listed
print(leverkusen_2024_matches.head(5))

# 分析赛季最后一场德甲比赛 Bayer Leverkusen - Werder Bremen
# 比赛时间 2024-04-14 17:30
the_match_id = 3895302
teamA = 'Bayer Leverkusen'
teamB = 'Werder Bremen'

# 提取比赛数据
events_df = sb.events(match_id=the_match_id)
print(events_df.head(5))

#print a list of columns available in the event data
print(events_df.columns)

#separate start and end locations from coordinates
events_df[['x', 'y']] = events_df['location'].apply(pd.Series)
events_df[['pass_end_x', 'pass_end_y']] = events_df['pass_end_location'].apply(pd.Series)
events_df[['carry_end_x', 'carry_end_y']] = events_df['carry_end_location'].apply(pd.Series)


class Pass(object):
    def __init__(self, team):
        self.team = team
        self.passes = events_df[(events_df['type'] == 'Pass') & (events_df['team'] == self.team)]

    # 统计传球次数, 并排序
    def sortPasses(self):
        # 调取所有"传球"数据
        all_passes = events_df[(events_df.team == self.team) & (events_df.type == 'Pass')]
        # 加入到统计
        all_passes_count = all_passes.groupby('player').size().reset_index(name='Passes')
        # 排序
        all_passes_count = all_passes_count.sort_values(by='Passes', ascending=False)
        return all_passes_count
    
    # 绘制球员传球数排序 堆叠条形图
    def passesStackBarChart(self):
        # 统计传球次数, 并排序
        all_passes_count = self.sortPasses()
        # 绘制
        fig, ax = plt.subplots(figsize=(12, 8))
        # 绘制堆叠条形图
        sns.barplot(x='Passes', y='player', data=all_passes_count, palette='viridis')
        # 添加标题
        fig_text(0.5, 0.95, f'{self.team} Passes', color='black', fontsize=18, ha='center', va='center')
        # 添加标签
        ax_text(0, 1.02, 'Top 10 Players by Passes', color='black', fontsize=14, ha='left', va='center', ax=ax)
        # 显示
        plt.show()

'''
    # 绘制特定球员的传球图
    def PassMap(self, player):
        player = player

        # 选择当前球员的传球数据
        passes = all_passes[(all_passes["player"] == player)]

        # 调用足球场
        pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_color='black',line_zorder=2)

        fig, ax = pitch.draw(figsize=(16, 11), constrained_layout=True, tight_layout=False)
        fig.set_facecolor('white')

        # 绘制传球箭头
        pitch.arrows(passes.x, passes.y, passes.pass_end_x, passes.pass_end_y, width=1,
                    headwidth=6, headlength=3,
                    color='red', ax=ax, zorder=2, label = "Passes")
    
        #etiquetas de color
        ax.legend(facecolor='grey', handlelength=4, edgecolor='None', fontsize=16, loc='best')

        #titulo
        ax_title = ax.set_title('Pases de ' f'{player}', fontsize=30, color='black')

        plt.show()
'''


# 以勒沃库森为例
pass_Leverkusen = Pass('Bayer Leverkusen')
pass_sort = pass_Leverkusen.sortPasses()

#print(pass_sort)
#pass_Leverkusen.passesStackBarChart()




if __name__ == "__main__":
    main()

    