'''
关于传球的分析：
聚焦于一场比赛的球员传球情况。
'''
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

# 传球分析类
class Pass:
    # 初始化
    def __init__(self, teamA, teamB, the_match_id):
        self.teamA = teamA
        self.teamB = teamB
        self.events_df = sb.events(match_id=the_match_id)

        # separate start and end locations from coordinates
        self.events_df[['x', 'y']] = self.events_df['location'].apply(pd.Series)
        self.events_df[['pass_end_x', 'pass_end_y']] = self.events_df['pass_end_location'].apply(pd.Series)
        self.events_df[['carry_end_x', 'carry_end_y']] = self.events_df['carry_end_location'].apply(pd.Series)

        self.passes = self.events_df[(self.events_df.team == self.teamA) & (self.events_df.team == self.teamB) & (self.events_df.type == 'Pass')]
        self.passesA = self.events_df[(self.events_df.team == self.teamA) & (self.events_df.type == 'Pass')]
        self.passesB = self.events_df[(self.events_df.team == self.teamB) & (self.events_df.type == 'Pass')]

    # 统计传球次数,并排序
    def sortPasses(self):
        # 加入到统计
        A_passes_count = self.passesA.groupby('player').size().reset_index(name='Passes')
        B_passes_count = self.passesB.groupby('player').size().reset_index(name='Passes')
        # Merge A_passes_count and B_passes_count
        all_passes_count = pd.concat([A_passes_count, B_passes_count], ignore_index=True)
        # Add a 'Team' column to identify the team for each player
        all_passes_count['Team'] = all_passes_count.index.map(lambda x: self.teamA if x < len(A_passes_count) else self.teamB)
        # Reorder the columns to match the requested format
        all_passes_count = all_passes_count[['player', 'Team', 'Passes']]
        # 排序
        all_passes_count = all_passes_count.sort_values(by='Passes', ascending=False)
        return all_passes_count
    
    # 绘制球员传球数排序
    # 堆叠条形图
    def passesStackBarChart(self):
        # 设置传球Bar的颜色
        pass_colour='red'
        # 统计传球次数, 并排序
        all_passes_count = self.sortPasses()
        # sort to get lowest values first (so that it plots in the correct order on our bar chart)
        all_passes_count.sort_values(by='Passes', ascending=True, inplace=True)
        # include only relevant columns
        barchart_df=all_passes_count[["player", "Passes"]]
        # create figure and set some style parameters
        # plt.figure(figsize = (12, 8))
        sns.set_theme(rc={'axes.facecolor':'white', 'figure.facecolor':'white'})
        sns.set_style("ticks")
        # create bar chart
        barchart_df.set_index('player').plot(kind='barh', stacked=True, color=[pass_colour], legend=True,figsize=(10,10))
        # add chart labels and title
        plt.xlabel(xlabel="All passes", fontdict = { 'fontsize': 12, 'weight':'semibold'})
        plt.ylabel(ylabel="Player",fontdict = { 'fontsize': 12, 'weight':'semibold'})
        plt.title(f'Passes of {self.teamA} & {self.teamB} Players', fontdict = { 'fontsize': 18, 'weight':'bold'})
        # keep two axes
        sns.despine(top=True, right=True, left=False, bottom=False)
        plt.autoscale()
        plt.show()

    # 绘制场上所有球员的传球路线
    # 主队或客队或两队
    def teamPassMap(self, team):
        # 绘制场地
        pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_zorder=2, line_color='black')
        fig, ax = pitch.draw(figsize=(16, 11), constrained_layout=True, tight_layout=False)
        fig.set_facecolor('white')
        # 选择主队或客队传球数据
        if team == self.teamA:
            passes = self.passesA
        elif team == self.teamB:
            passes = self.passesB
        # Plot the passes
        pitch.arrows(passes.x, passes.y, 
                     passes.pass_end_x, passes.pass_end_y, 
                     width=1, headwidth=6, headlength=3, 
                     color='red', ax=ax, zorder=2, label=f"{team} Passes")
        # Add legend and title
        ax.legend(facecolor='grey', handlelength=4, edgecolor='None', fontsize=16, loc='best')
        ax_title = ax.set_title(f'Passes by {team}', fontsize=20, color='black')
        # 显示
        plt.show()


    # 绘制特定球员的传球图
    def playerPassMap(self, player):
        # 绘制场地
        pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_zorder=2, line_color='black')
        fig, ax = pitch.draw(figsize=(16, 11), constrained_layout=True, tight_layout=False)
        fig.set_facecolor('white')
        # 选择特定球员的传球数据
        player_passes = self.events_df[self.events_df.player == player]
        # Plot the passes
        pitch.arrows(player_passes.x, player_passes.y, 
                     player_passes.pass_end_x, player_passes.pass_end_y, 
                     width=1, headwidth=6, headlength=3, 
                     color='red', ax=ax, zorder=2, label=f"{player} Passes")
        # Add legend and title
        ax.legend(facecolor='grey', handlelength=4, edgecolor='None', fontsize=16, loc='best')
        ax_title = ax.set_title(f'Passes by {player}', fontsize=20, color='black')
        # 显示
        plt.show()

    # 统计球队威胁进攻三区的传球
    def teamPassIntoFinalThirdMap(self, team):
        f3rd_passes=self.events_df[(self.events_df.team == team) & (self.events_df.type == "Pass") & 
                                (self.events_df.x<80) & (self.events_df.pass_end_x>80) & 
                                (self.events_df.pass_outcome.isna())]
        # 绘制场地
        pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_zorder=2, line_color='black')
        fig, ax = pitch.draw(figsize=(16, 11), constrained_layout=True, tight_layout=False)
        fig.set_facecolor('white')
        # Plot the passes
        pitch.arrows(f3rd_passes.x, f3rd_passes.y, 
                     f3rd_passes.pass_end_x, f3rd_passes.pass_end_y, 
                     width=1, headwidth=6, headlength=3, 
                     color='red', ax=ax, zorder=2, label=f"{team} Passes into Final Third")
        # Add legend and title
        ax.legend(facecolor='grey', handlelength=4, edgecolor='None', fontsize=16, loc='best')
        ax_title = ax.set_title(f'Passes into Final Third by {team}', fontsize=20, color='black')
        # 显示
        plt.show()
        
    # 统计球员威胁进攻三区的传球
    def playerPassIntoFinalThirdMap(self, player):
        f3rd_passes=self.events_df[(self.events_df.player == player) & (self.events_df.type == "Pass") & 
                                (self.events_df.x<80) & (self.events_df.pass_end_x>80) & 
                                (self.events_df.pass_outcome.isna())]
        # 绘制场地
        pitch = Pitch(pitch_type='statsbomb', pitch_color='white', line_zorder=2, line_color='black')
        fig, ax = pitch.draw(figsize=(16, 11), constrained_layout=True, tight_layout=False)
        fig.set_facecolor('white')
        # Plot the passes
        pitch.arrows(f3rd_passes.x, f3rd_passes.y, 
                     f3rd_passes.pass_end_x, f3rd_passes.pass_end_y, 
                     width=1, headwidth=6, headlength=3, 
                     color='red', ax=ax, zorder=2, label=f"{player} Passes into Final Third")
        # Add legend and title
        ax.legend(facecolor='grey', handlelength=4, edgecolor='None', fontsize=16, loc='best')
        ax_title = ax.set_title(f'Passes into Final Third by {player}', fontsize=20, color='black')
        # 显示
        plt.show()
















