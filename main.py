from gui import Gui

import os

import streamlit as st

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


    def create(self):

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

        #

        data_categories = ['Mobilitätsdaten - Allgemein','Mobilitätsdaten - Aktive Mobilität','Mobilitätsdaten - ÖPNV','Mobilitätsdaten - Flugverkehr', 'Energieverbrauch']

        st.title(self._apptitle)
        st.header('2019')
        with st.expander('2019'):
            #

            st.header('Verkehrsleistung')
            verkehrsleistung = st.number_input('Verkehrsleistung [P-km/a]')
            st.header('Modalsplit')
            ms_car = st.slider('Modal Split - PKW [%]', 0.0, 100.0,step=0.1)



        #for cat in data_categories:
         #   st.header(cat)
          #  st.expander(cat)









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

    scenarios = [
        "",
        "Mobilitätsdaten-Allgemein",
        "Mobiltätsadaten-Schiene",
        "Auffahrt 2+1 RE",
        "Auffahrt 3+1 RE",
        "Verflechtungsstrecke 2+1",
        "Abfahrt 2-1 RE",
        "Baustelle 2-1",
        "Baustelle 4+0",
        "Tunnel 2-streifig"
    ]

    gui = StatistikPV_Gui(
        apptitle="Prototypisches Dashboard BMK Monitoring Personenverkehr",
        appbrandimage=ag_logos,
        appicon="./logos/bmk.png'",
        appcopyrightlogos=an_logo,
        appversion=__version__)
    gui.create()


if __name__ == '__main__':
    main()