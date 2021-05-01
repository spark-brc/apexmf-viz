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
from io import StringIO

pd.options.mode.chained_assignment = None

LINE = """<style>
.vl {
  border-left: 2px solid gray;
  height: 400px;
  position: absolute;
  left: 50%;
  margin-left: -3px;
  top: 0;
}
</style>
<div class="vl"></div>"""




st.set_page_config(
    layout="wide",
    initial_sidebar_state='collapsed',
    page_title='APEX Visualization',
    page_icon='icon2.png' 
    )
st.title('APEX Model - Streamflow Analysis')
st.markdown("## User Inputs:")


col1, line, col2 = st.beta_columns([0.4,0.1,0.4])

with col1:
    cont_file = st.file_uploader("Provide 'APEXCONT.DAT' file")
    sim_file = st.file_uploader("Provide *.RCH file")
    obd_file = st.file_uploader("Provide 'stf_mon.obd' file")

### 
if cont_file:
    stdate, eddate, start_year, end_year = utils.define_sim_period2(cont_file)
    with line:
        st.markdown(LINE, unsafe_allow_html=True)
    with col2:
        stdate = st.date_input(
            "Simulation Start Day",
            stdate
            )
        val_range = st.slider(
            "Set Analysis Period:",
            min_value=int(start_year),
            max_value=int(end_year), value=(int(start_year),int(end_year)))
        sims = st.text_input('Enter Reach IDs (e.g., 12, 16, 99):')
        obds = st.text_input('Enter column names from the observation file:')
    sims_list = sims.split(",")
    obds_list = obds.split(",")
    obds_list = [i.strip() for i in obds_list]
    sims_list = [i.strip() for i in sims_list]
    caldate = datetime.datetime(val_range[0], 1, 1)
    eddate = datetime.datetime(val_range[1], 12, 31)
###

def main(df, sims_list):
    with st.beta_expander('Dataframe for Simulated and Observed Stream Discharge'):
        st.dataframe(df, height=500)
        st.markdown(utils.filedownload(df), unsafe_allow_html=True)
    stats_df = utils.get_stats_df(df, sims_list)
    with col2:
        st.markdown(
            """
            ### Objective Functions
            """)
        st.dataframe(stats_df.T)
    st.markdown("## Hydrographs for stream discharge")
    st.plotly_chart(utils.get_plot(df, sims_list), use_container_width=True)
    tcol1, tcol2 = st.beta_columns([0.55, 0.45])
    with tcol1:
        st.markdown("## Flow Duration Curve")
    pcol1, pcol2= st.beta_columns([0.1, 0.9])
    with pcol1:
        yscale = st.radio("Select Y-axis scale", ["Linear", "Logarithmic"])
    with pcol2:
        st.plotly_chart(utils.get_fdcplot(df, sims_list, yscale), use_container_width=True)


@st.cache
def load_data():
    df = utils.get_sim_obd(sim_file, obd_file, obds_list, sims_list, stdate, caldate, eddate)
    return df, sims_list


if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)
    if sim_file and obd_file and sims and obds:
        df, sims_list = load_data()
        main(df, sims_list)



