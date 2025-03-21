'''
关于射门的分析
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


class Shoot(object):
    def __init__(self, teamA, teamB, the_match_id):
        self.teamA = teamA
        self.teamB = teamB
        events_df = sb.events(match_id=the_match_id)
        self.shots = events_df[(events_df['type'] == 'Shot') & (events_df['team'] == self.team)]


    # 统计射门次数, 并排序
    def sortShoots(self):
        # 加入到统计
        all_shoots_count = self.shots.groupby('player').size().reset_index(name='Shoots')
        # 排序
        all_shoots_count = all_shoots_count.sort_values(by='Shoots', ascending=False)
        return all_shoots_count


