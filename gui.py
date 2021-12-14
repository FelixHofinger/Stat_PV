import streamlit as st
import glob
import os

from streamlit.report_thread import add_report_ctx

class Gui():
    def __init__(self, *, appbrandimage=None, appicon=None, apptitle="", appversion="", appcopyrightlogos=[]):
        self._appbrandimage = appbrandimage
        self._appicon = appicon
        self._apptitle = apptitle
        self._appversion = appversion
        self._appcopyrightlogos = appcopyrightlogos


    def create(self):

        # default layout
        st.set_page_config(page_title=self._apptitle, page_icon=self._appicon, layout='wide', initial_sidebar_state='auto')
        if self._appbrandimage:
            for logo in self._appbrandimage:
                st.sidebar.image(logo)
            #st.sidebar.image(self._appbrandimage)
        elif self._apptitle:
            st.sidebar.title(self._apptitle)

        if self._appversion:
            st.sidebar.text(f"Version {self._appversion}")

        # # Scenario selection is usually done in the sidebar and either returns
        # # a string denoting the scenario, or a list of objects which describe the scenario
        # scenario = self.create_scenario_selection(scenarios)
        # if scenario and type(scenario) == str:
        #     st.title(f"{scenario}")
        #
        # # Streamlit calls us multiple times as it reloads the page. We create the configuration only until
        # # the user presses "start simulation"
        # #if not st.session_state.button_start_simulation:
        # self.create_scenario(scenario)
        #         # Add logos to the bottom (if any)
        for logo in self._appcopyrightlogos:
            st.sidebar.image(logo)
