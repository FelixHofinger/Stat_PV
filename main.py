from gui import Gui

import os

import streamlit as st
import pandas as pd

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



            st.header('Verkehrsleistung')
            with st.expander('Verkehrsleistung'):

                st.header('2019')
                verkehrsleistung_car = st.number_input('Verkehrsleistung mIV 2019 [P-km/a]')
                verkehrsleistung_zug = st.number_input('Verkehrsleistung Zug 2019 [P-km/a]')

                st.header('2020')
                verkehrsleistung_car = st.number_input('Verkehrsleistung mIV 2020 [P-km/a]')
                verkehrsleistung_zug = st.number_input('Verkehrsleistung Zug 2020 [P-km/a]')

                st.header('2021')
                verkehrsleistung_car = st.number_input('Verkehrsleistung mIV 2021[P-km/a]')
                verkehrsleistung_zug = st.number_input('Verkehrsleistung Zug 2021 [P-km/a]')

            st.header('Modalsplit')
            with st.expander('Modal-Split'):
                st.header('2019')
                ms_car = st.slider('Modal Split - PKW 2019[%]', 0.0, 100.0, step=0.1)
                ms_train = st.slider('Modal Split - Zug 2019 [%]', 0.0, 100.0, step=0.1)

                st.header('2020')
                ms_car = st.slider('Modal Split - PKW 2020 [%]', 0.0, 100.0, step=0.1)
                ms_train = st.slider('Modal Split - Zug 2020 [%]', 0.0, 100.0, step=0.1)

                st.header('2021')
                ms_car = st.slider('Modal Split - PKW 2021 [%]', 0.0, 100.0, step=0.1)
                ms_train = st.slider('Modal Split - Zug 2021 [%]', 0.0, 100.0, step=0.1)

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
                print(chart_data_graz)

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