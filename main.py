from gui import Gui

import os

import streamlit as st
import pandas as pd
import numpy as np

from cross_section_data import Cross_Section_Data

#from symul8_sumo_simulator import Symul8SumoSimulator
#from symul8_vissim_simulator import Symul8VissimSimulator

__author__ = ("Felix Hofinger", "Florian Lammer")
__copyright__ = ""
__credits__ = ("Felix Hofinger", "Florian Lammer")
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = ("Felix Hofinger", "Florian Lammer")
__email__ = ("felix.hofinger@tugraz.at", "florian.lammer@tugraz.at")
__status__ = "Development"


class StatistikPV_Gui():
    def __init__(self, *, appbrandimage=None, appicon=None, apptitle="", appversion="", appcopyrightlogos=[]):
        self._appbrandimage = appbrandimage
        self._appicon = appicon
        self._apptitle = apptitle
        self._appversion = appversion
        self._appcopyrightlogos = appcopyrightlogos

    # def calc_cross_sections(self,year1,year2):
    #     try:
    #         cross_section_data = Cross_Section_Data(year1=year1, year2=year2)
    #         cross_data = cross_section_data.read_cross_data()
    #         cross_section_li = cross_section_data.cross_section_list(cross_data)
    #         cross_section_selected = st.selectbox("Querschnitt wählen", cross_section_li)
    #         return cross_section_selected
    #     except:
    #         st.write('No Data available')



    def create(self, data_cat):

        # default layout



        st.set_page_config(page_title=self._apptitle, page_icon=self._appicon, layout='wide', initial_sidebar_state='auto')
        if self._appbrandimage:
            for logo in self._appbrandimage:
                st.sidebar.image(logo)

        elif self._apptitle:
            st.sidebar.title(self._apptitle)

        if self._appversion:
            st.sidebar.text(f"Version {self._appversion}")

        for logo in self._appcopyrightlogos:
            st.sidebar.image(logo)


        datacat = st.sidebar.selectbox('Kategorie', data_cat)
        st.title(self._apptitle)
        if datacat == 'Mobilitätsdaten - Allgemein':

            st.header('Querschnittsdaten-Berechnung')

            st.session_state.year1 = st.selectbox("Vergleichsjahr - 1", np.arange(2010,2025))
            st.session_state.year2 = st.selectbox("Vergleichsjahr - 2", np.arange(2010,2025))

            cross_section_data = Cross_Section_Data(year1=st.session_state.year1, year2=st.session_state.year2)
            global cross_data
            st.session_state.cross_section_selected = False
            st.session_state.driving_direction_select = False

            if st.session_state.year2:
                try:
                    cross_data = cross_section_data.read_cross_data()
                    cross_section_li = cross_section_data.cross_section_list(cross_data)
                    st.session_state.cross_section_selected = st.selectbox("Querschnitt wählen", cross_section_li)
                except:
                    st.subheader(f'Keine Daten für das Jahr {st.session_state.year1} bzw. {st.session_state.year2} vorhanden!')

            if st.session_state.cross_section_selected:
                data_to_plot, driving_directions_li = cross_section_data.select_drivingdirection(cross_data,
                                                                                           st.session_state.cross_section_selected)
                st.session_state.driving_direction_select = st.selectbox("Fahrtrichtung wählen", driving_directions_li)
                st.session_state.agg_level = st.selectbox("Auswertungsintervall",['Monatlich','Quartalsweise'])
                st.session_state.weekday = st.selectbox("Wochentag", ['Montag-Freitag', 'Samstag','Sonn- und Feiertag'])

                plot_data = st.button("Vergleich Querschnittsdaten anzeigen")

                if plot_data:
                    #data_to_plot = cross_section_data.
                    fig = cross_section_data.plot_bar_chart(data_to_plot,
                                                                st.session_state.driving_direction_select,
                                                                st.session_state.agg_level,
                                                                st.session_state.weekday)
                    st.pyplot(fig)













                #calc_cross_data = st.button("Vergleich Querschnittsdaten anzeigen")

                #agg_intervall = st.selectbox("Auswertungsintervall",['Monatlich','Quartalsweise'])
                #weekday = st.selectbox("Wochentag", ['Montag-Freitag', 'Samstag','Sonn- und Feiertag'])
                #calc_cross_data = st.button("Vergleich Querschnittsdaten anzeigen")
                #if calc_cross_data:
                   # data_to_plot = cross_section_data.select_crosssection(cross_data, cross_section_select)



            #print(cross_data_select)
            #print(calc_cross_data)



            # st.header('Modalsplit')
            # with st.expander('Modal-Split'):
            #     st.header('2019')
            #     ms_car = st.slider('Modal Split - PKW 2019[%]', 0.0, 100.0, step=0.1)
            #     ms_train = st.slider('Modal Split - Zug 2019 [%]', 0.0, 100.0, step=0.1)
            #
            #     st.header('2020')
            #     ms_car = st.slider('Modal Split - PKW 2020 [%]', 0.0, 100.0, step=0.1)
            #     ms_train = st.slider('Modal Split - Zug 2020 [%]', 0.0, 100.0, step=0.1)
            #
            #     st.header('2021')
            #     ms_car = st.slider('Modal Split - PKW 2021 [%]', 0.0, 100.0, step=0.1)
            #     ms_train = st.slider('Modal Split - Zug 2021 [%]', 0.0, 100.0, step=0.1)

            st.header('Radverkehr')
            with st.expander('Radverkehr'):

                st.header('2019')
                graz_2019 = st.number_input('# Fahrradfahrer Graz 2019')
                wien_2019 = st.number_input('# Fahrradfahrer Wien 2019')

                st.header('2020')
                graz_2020 = st.number_input('# Fahrradfahrer Graz 2020')
                wien_2020 = st.number_input('# Fahrradfahrer Wien 2020')

                st.header('2021')
                graz_2021 = st.number_input('# Fahrradfahrer Graz 2021')
                wien_2021 = st.number_input('# Fahrradfahrer Wien 2021')

                chart_data_graz = pd.DataFrame([[graz_2019, wien_2019], [graz_2020, wien_2020], [graz_2021, wien_2021]], index=['2019', '2020', '2021'], columns=['Graz','Wien'])
                #print(chart_data_graz)

                st.line_chart(chart_data_graz)







def main():
    # Project consortium logos
    ag_logos = [
        r"./logos/bmk.png",  # TUGraz
        r"./logos/oebb.png",
        r"./logos/asfinag.png"# BMK

    ]

    an_logo = [
        r"./logos/TU_Graz.png",  # TUGraz
        #r"./logos/isv.png",
    ]

    data_cat = ['Mobilitätsdaten - Allgemein',
                'Mobilitätsdaten - Aktive Mobilität',
                'Mobilitätsdaten - ÖPNV',
                'Mobilitätsdaten - Flugverkehr',
                'Energieverbrauch']



    gui = StatistikPV_Gui(
        apptitle="Prototypisches Dashboard BMK Monitoring Personenverkehr",
        appbrandimage=ag_logos,
        appicon="./logos/bmk.png'",
        appcopyrightlogos=an_logo,
        appversion=__version__)
    gui.create(data_cat)


if __name__ == '__main__':
    main()