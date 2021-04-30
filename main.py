import logging
import plotly.express as px
import streamlit as st
import os
import pandas as pd
import base64
import numpy as np
import glob
import datetime
import utils

pd.options.mode.chained_assignment = None

st.set_page_config(
    layout="wide",
    initial_sidebar_state='collapsed',
    page_title='APEX Visualization',
    page_icon='icon2.png' 
    )

sim_file = st.file_uploader("Choose*.RCH file")
obd_file = st.file_uploader("Choose 'stf_mon.obd' file")

sims = st.text_input('Enter Reach IDs (e.g., 12, 16, 99):')
obds = st.text_input('Enter column names from the observation file:')
sims_list = sims.split(",")
obds_list = obds.split(",")
obds_list = [i.strip() for i in obds_list]
sims_list = [i.strip() for i in sims_list]
# sims_list


stdate = st.date_input(
    "Simulation Start Day",
    # datetime.date(1980, 1, 1)
    )
caldate = st.date_input(
    "Calibration Start Day",
    # datetime.date(1980, 1, 1)
    )
eddate = st.date_input("Calibration End Day")
st.write('Your birthday is:', stdate)

# d5 = st.date_input("date range without default", [datetime.date(1980, 1, 1), datetime.date(2019, 7, 8)])
# st.write(d5[0])


def main(df, sims_list):
    st.write(df)
    st.plotly_chart(utils.get_plot(df, sims_list), use_container_width=True)
    stats_df = utils.get_stats_df(df, sims_list)
    yscale = st.radio("Select Y-axis scale", ["Linear", "Logarithmic"])
    st.plotly_chart(utils.get_fdcplot(df, sims_list, yscale), use_container_width=True)
    stats_df = utils.get_stats_df(df, sims_list)
    st.dataframe(stats_df.T)



@st.cache
def load_data():
    # time_step = 'M'
    # caldate = '1/1/{}'.format(valstyr)
    # eddate = '12/31/{}'.format(valedyr)

    df = utils.get_sim_obd(sim_file, obd_file, obds_list, sims_list, stdate, caldate, eddate)
    # mfig = utils.viz_biomap()
    return df, sims_list


if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)
    if sim_file and obd_file is not None:
        df, sims_list = load_data()
        main(df, sims_list)



