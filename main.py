import streamlit as st
import pandas as pd
import numpy as np

from cross_section_data import Cross_Section_Data
from air_traffic_data import Air_Traffic_Data

__author__ = "Felix Hofinger"
__copyright__ = ""
__credits__ = "Felix Hofinger"
__license__ = ""
__version__ = "0.0.9"
__maintainer__ = "Felix Hofinger"
__email__ = "felix.hofinger@tugraz.at"
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

        # Querschnittsdaten (Segmentbezogen)
        if datacat == 'Querschnittsdaten (Segment)':
            st.header('Querschnittsdaten-Berechnung (Segmentbezogen)')
            st.session_state.year1 = st.selectbox("Vergleichsjahr - 1", np.arange(2015, 2023), index=4)
            st.session_state.year2 = st.selectbox("Vergleichsjahr - 2", np.arange(2015, 2023), index=5)
            cross_section_data = Cross_Section_Data(year1=st.session_state.year1, year2=st.session_state.year2)
            global cross_data
            st.session_state.cross_section_selected = False
            st.session_state.driving_direction_select = False
            if st.session_state.year2:
                try:
                    cross_data = cross_section_data.read_cross_data()

                    cross_section_li, cross_section_dict = cross_section_data.cross_section_list(cross_data)
                    st.session_state.cross_section_selected = st.selectbox("Querschnitt w??hlen", cross_section_li)
                except:
                    st.warning(f'Keine Daten f??r das Jahr {st.session_state.year1} bzw. {st.session_state.year2} vorhanden!')
            if st.session_state.cross_section_selected:
                data_to_plot, driving_directions_li = cross_section_data.select_drivingdirection(cross_data, cross_section_dict[st.session_state.cross_section_selected])
                st.session_state.driving_direction_select = st.selectbox("Fahrtrichtung w??hlen", driving_directions_li)
                st.session_state.agg_level = st.selectbox("Auswertungsintervall", ['Monatlich','Quartalsweise'])
                st.session_state.weekday = st.selectbox("DTV-Wert", ['Montag-Freitag', 'Dienstag-Donnerstag',
                                                                     'Montag-Sonntag', 'Sonn- und Feiertag', 'Montag',
                                                                     'Samstag'])

                plot_data = st.button("Vergleich Querschnittsdaten anzeigen")
                if plot_data:
                    with st.spinner("Auswertung Querschnittsdaten l??uft"):
                        fig = cross_section_data.plot_bar_chart(data_to_plot,
                                                                    st.session_state.driving_direction_select,
                                                                    st.session_state.agg_level,
                                                                    st.session_state.weekday)
                        st.pyplot(fig)

        elif datacat == 'Querschnittsdaten (Raum)':
            st.header('Querschnittsdaten - Berechnung (Raumbezogen)')
            st.session_state.y1_raum = st.selectbox("Vergleichsjahr - 1 ", np.arange(2015, 2023), index=4)
            st.session_state.y2_raum = st.selectbox("Vergleichsjahr - 2 ", np.arange(2015, 2023), index=5)
            st.session_state.raumtyp = st.selectbox("Raumtyp", ['Gesamt', 'Wien', 'Gro??stadt (ohne Wien)',
                                                                'zentrale Bezirke', 'peripherer Bezirk'])
            st.session_state.bundesland = st.selectbox("Bundesland", ['Alle', 'Wien','Nieder??sterreich', 'Burgenland',
                                                                      'Steiermark' , 'Ober??sterreich', 'Salzburg',
                                                                      'K??rnten', 'Tirol', 'Vorarlberg'])
            st.session_state.agg_level_raum = st.selectbox("Auswertungsintervall", ['Monatlich', 'Quartalsweise'])
            st.session_state.weekday_raum = st.selectbox("DTV-Wert", ['Montag-Freitag', 'Dienstag-Donnerstag',
                                                                     'Montag-Sonntag', 'Sonn- und Feiertag', 'Montag',
                                                                     'Samstag'])
            plot_data_raum = st.button("Vergleich Querschnittsdaten anzeigen")

            cross_section_data_raum = Cross_Section_Data(year1=st.session_state.y1_raum, year2=st.session_state.y2_raum)

            if plot_data_raum:
                with st.spinner("Auswertung Querschnittsdaten l??uft"):
                    try:
                        data_to_plot_raum = cross_section_data_raum.read_raum_cross_data(st.session_state.raumtyp, st.session_state.bundesland)
                        fig = cross_section_data_raum.plot_bar_chart_raum(data_to_plot_raum,
                                                                        st.session_state.agg_level_raum,
                                                                        st.session_state.weekday_raum, relative=False)
                        st.pyplot(fig)
                    except:
                        st.warning(f'Keine Daten f??r das Jahr {st.session_state.y1_raum} bzw. {st.session_state.y2_raum} vorhanden!')

        elif datacat == 'Flugverkehr':
            st.header('Auswertung Flugverkehr')
            st.session_state.year1 = st.selectbox("Vergleichsjahr - 1", np.arange(2015, 2023), index=4)
            st.session_state.year2 = st.selectbox("Vergleichsjahr - 2", np.arange(2015, 2023), index=5)
            st.session_state.airport = st.selectbox("Flughafen", ['Alle', 'Wien', 'Graz', 'Linz', 'Salzburg', 'Innsbruck', 'Klagenfurt'])
            st.session_state.indicator = st.selectbox("Indikator", ['Anzahl Passagiere', 'Anzahl Fl??ge', 'Flugkilometer', 'Personenkilometer'])
            st.session_state.agg_level_raum = st.selectbox("Auswertungsintervall", ['Quartalsweise', 'Monatlich (nicht unters??tzt)'])

            plot_data = st.button("Flugverkehrsdaten auswerten")
            if plot_data:
                with st.spinner("Auswertung Flugverkehrsdaten l??uft"):
                    air_traffic = Air_Traffic_Data()
                    data_dict_type, data_dict_year = air_traffic.read_air_tr_data(st.session_state.airport)

                    if st.session_state.year1 not in data_dict_year.keys() or st.session_state.year2 not in data_dict_year.keys():
                        st.warning('Jahr ist nicht in Datensatz enthalten - K??nnen im Statistik Austria Statcube heruntergeladen werden')
                    else:
                        fig = air_traffic.plot_air_tr_data(data_dict_type,
                                                           st.session_state.year1,
                                                           st.session_state.year2,
                                                           st.session_state.indicator,
                                                           st.session_state.airport)

                        st.info('Exemplarische Testanwendung - Die Daten beziehen sich nur auf den Binnenflugverkehr in ??sterreich!')
                        st.pyplot(fig)

        elif datacat == 'st??dtischer Verkehr (dummy)':
            st.header('St??dtischer Verkehr')

            st.header('2019')
            oev_graz_2019 = st.number_input('# ??V-Fahrgastzahlen Graz 2019')
            oev_wien_2019 = st.number_input('# ??V-Fahrgastzahlen Wien 2019')

            st.header('2020')
            oev_graz_2020 = st.number_input('# ??V-Fahrgastzahlen Graz 2020')
            oev_wien_2020 = st.number_input('# ??V-Fahrgastzahlen Wien 2020')
            st.header('2021')

            oev_graz_2021 = st.number_input('# ??V-Fahrgastzahlen Graz 2021')
            oev_wien_2021 = st.number_input('# ??V-Fahrgastzahlen Wien 2021')

            chart_data_graz = pd.DataFrame([[oev_graz_2019, oev_wien_2019], [oev_graz_2020, oev_wien_2020], [oev_graz_2021, oev_wien_2021]], index=['2019', '2020', '2021'], columns=['Graz','Wien'])

            st.line_chart(chart_data_graz)


        elif datacat == 'aktive Mobilit??t (dummy)':
            st.header('Radverkehr')

            st.header('2019')
            rf_graz_2019 = st.number_input('# Fahrradfahrer Graz 2019')
            rf_wien_2019 = st.number_input('# Fahrradfahrer Wien 2019')

            st.header('2020')
            rf_graz_2020 = st.number_input('# Fahrradfahrer Graz 2020')
            rf_wien_2020 = st.number_input('# Fahrradfahrer Wien 2020')
            st.header('2021')

            rf_graz_2021 = st.number_input('# Fahrradfahrer Graz 2021')
            rf_wien_2021 = st.number_input('# Fahrradfahrer Wien 2021')

            chart_data_graz = pd.DataFrame([[rf_graz_2019, rf_wien_2019], [rf_graz_2020, rf_wien_2020], [rf_graz_2021, rf_wien_2021]], index=['2019', '2020', '2021'], columns=['Graz','Wien'])
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
    data_cat = ['Querschnittsdaten (Raum)',
                'Querschnittsdaten (Segment)',
                'Flugverkehr',
                'st??dtischer Verkehr (dummy)',
                'aktive Mobilit??t (dummy)']

    gui = StatistikPV_Gui(
        apptitle="Prototypisches Dashboard BMK Monitoring Personenverkehr",
        appbrandimage=ag_logos,
        appicon="./logos/bmk.png'",
        appcopyrightlogos=an_logo,
        appversion=__version__)
    gui.create(data_cat)

if __name__ == '__main__':
    main()