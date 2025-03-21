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


# Pass.py
class Pass:
    def __init__(self, teamA, teamB, the_match_id):
        self.teamA = teamA
        self.teamB = teamB
        events_df = sb.events(match_id=the_match_id)
        self.passes = events_df[(events_df['type'] == 'Pass') & (events_df['team'] == self.team)]

    # 统计传球次数, 并排序
    def sortPasses(self):
        # 加入到统计
        all_passes_count = self.passes.groupby('player').size().reset_index(name='Passes')
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



