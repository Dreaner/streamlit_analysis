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
import json

# import the "analysis_soccer" package
import analysis_soccer.Pass as apa
import analysis_soccer.Shoot as asho
import analysis_soccer.Touch as ato

# 分析赛季最后一场德甲比赛
# 比赛时间 2024-04-14 17:30:00
# 比赛id 3895302
# 球队 Bayer Leverkusen - Werder Bremen
teamA = 'Bayer Leverkusen'
teamB = 'Werder Bremen'
the_match_id = 3895302

def main():
    # 分析传球
    pass_last_game = apa.Pass(teamA, teamB, the_match_id)
    #print(pass_last_game.sortPasses())
    #pass_last_game.passesStackBarChart()
    #pass_last_game.teamPassMap('Bayer Leverkusen')
    #pass_last_game.playerPassMap('Robert Andrich')
    #pass_last_game.teamPassIntoFinalThirdMap('Bayer Leverkusen')
    pass_last_game.playerPassIntoFinalThirdMap('Florian Wirtz')


if __name__ == "__main__":
    main()

