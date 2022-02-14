################################################################################
# File: binnenflug_matrix.py
#
# Date: 14.1.2022
# Author: Florian Lammer <florian.lammer@tugraz.at>
#
# Description:
#   Plottet eine Heatmap für alle Binnenflüge in Österreich zwischen den 6 Flughäfen.
#   Zahlen werden vom ankommenden und abgehenden Flughafen berichtet. Nach Statistik
#   Austria ist hier der Mittelwert zu bilden, da es zu Abweichungen kommen kann.
#
#   Plots können mittels der Parameter YEAR und Q für jedes Quartal jedes Jahres erstellt
#   werden. Siehe die Code-Sektion "plot data".
################################################################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Air_Traffic_Data:
    def __init__(self, year1=None, year2=None, agg_level=None):
        self._year1 = year1
        self._year2 = year2
        self._agg_level = agg_level
        self._comp_year = (self._year1, self._year2)
        self._month = {1: ('01', 'Jänner', 'Q1'),
                       2: ('02', 'Februar', 'Q1'),
                       3: ('03', 'März', 'Q1'),
                       4: ('04', 'April', 'Q2'),
                       5: ('05', 'Mai', 'Q2'),
                       6: ('06', 'Juni', 'Q2'),
                       7: ('07', 'Juli', 'Q3'),
                       8: ('08', 'August', 'Q3'),
                       9: ('09', 'September', 'Q3'),
                       10: ('10', 'Oktober', 'Q4'),
                       11: ('11', 'November', 'Q4'),
                       12: ('12', 'Dezember', 'Q4')}
        self._cross_section = {}

    # read and preprocess data
    def read_air_tr_data(self, airport):
        path = f"./air_traffic_data/"
        flug_ab = pd.read_excel(f'{path}Binnenflug_aut_abgehend.xlsx', engine='openpyxl', sheet_name='aufbereitet').replace('-',0)
        flug_an = pd.read_excel(f'{path}Binnenflug_aut_ankommend.xlsx', engine='openpyxl', sheet_name='aufbereitet').replace('-',0)



        # create a list of all existing airports and years
        flughafen_list = list(flug_ab['Berichtshafen'].unique())
        year_list = list(flug_ab['Jahr'].unique())

        # create dictionarys to store values from nested loops
        # some nested dictionaries are created in the nested loops
        # data structure: dict_type --> dict_year --> dict_quarter --> matrix with data
        dict_type = dict()

        # maximum values in all data to set plot color bar always to same boundaries
        list_v_max_plot = list()

        for TYPE in ['Passagiere nach Streckenzielen', 'Flüge']:
            # initialise values
            dict_year = dict()
            pass_max = 0
            for YEAR in year_list:
                # initialise values
                print(YEAR)
                dict_quarter = dict()
                for Q in range(1, 5):
                    print(Q)
                    # create a emtpy matrix for this year-quarter combination
                    matrix = pd.DataFrame(0, columns=flughafen_list, index=flughafen_list)

                    # loop thorugh all airports
                    for i in range(0, len(flughafen_list)):
                        for j in range(0, len(flughafen_list)):
                            berichtshafen = flughafen_list[i] #[1] # Graz
                            starthafen = flughafen_list[j] #[0] # Wien

                            # ankommend Berichtshafen
                            val_1 = flug_an[(flug_an['Jahr'] == YEAR ) & (flug_an['Quartal'] == Q) & (flug_an['Berichtshafen'] == berichtshafen) & (flug_an['Starthafen'] == starthafen)][TYPE].item()
                            # abgehend Starthafen
                            val_2 = flug_ab[(flug_ab['Jahr'] == YEAR ) & (flug_ab['Quartal'] == Q) & (flug_ab['Berichtshafen'] == starthafen) & (flug_ab['Landehafen'] == berichtshafen)][TYPE].item()
                            # create mean value between data reported from both airports
                            if airport == 'Alle':
                                val = int(np.round((val_1+val_2)/2))
                            elif berichtshafen == airport or starthafen == airport:
                                val = int(np.round((val_1+val_2)/2))
                            else:
                                val = 0
                            # fill matrix at the current cell
                            matrix.loc[starthafen,berichtshafen] = val
                            # if a new maximum value is found, update max value for plot
                            if val > pass_max:
                                pass_max = val
                            else:
                                pass

                    # print(matrix)
                    # write matrix to dictonary data storing structure
                    dict_quarter[Q] = matrix.copy()
                    del matrix
                dict_year[YEAR] = dict_quarter
            dict_type[TYPE] = dict_year
            # append list with max value for each type (passengers or flights
            list_v_max_plot.append(pass_max)

        return dict_type, dict_year

    def barplot_autolabel(self, ax, bar, text, height, bottom_height):
        """Attach a text label above each bar in *rects*, displaying its height."""

        for bars in bar:
            ax.annotate('{}'.format(text),
                        xy=(bars.get_x() + bars.get_width(), height + bottom_height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', rotation=0, size=15)

    def plot_air_tr_data(self, data, year1, year2, indicator, airport):
        dict_indicator = {'Anzahl Passagiere': 'Passagiere nach Streckenzielen',
                          'Anzahl Flüge': 'Flüge',
                          'Flugkilometer': 'Flüge',
                          'Personenkilometer':'Passagiere nach Streckenzielen'}

        path = f"./air_traffic_data/"
        dist_mat = pd.read_excel(f'{path}Distanzmatrix_Binnenflugverkehr.xlsx', engine='openpyxl').iloc[:, 1:].set_index('Flughafen')

        plot_data_li = []
        for YEAR in [year1, year2]:
            df_leistung = pd.DataFrame({'flug/pers/km': [0, 0, 0, 0]}, index=['Q1', 'Q2', 'Q3', 'Q4'])
            for Q_i in range(1, 5):
                plot_data = data[dict_indicator[indicator]][YEAR][Q_i]

                if indicator in ['Flugkilometer', 'Personenkilometer']:
                    data_value = (dist_mat * plot_data).sum().sum().round()
                else:
                    data_value = (1 * plot_data).sum().sum().round()
                df_leistung.loc[f'Q{Q_i}', 'flug/pers/km'] = data_value

            df_leistung.reset_index(inplace=True, drop=True)
            plot_data_li.append(df_leistung)

        y_max = max(plot_data_li[0]['flug/pers/km'].max(), plot_data_li[1]['flug/pers/km'].max())

        abs_diff =  []
        total = []
        plt.style.use('seaborn-darkgrid')
        fig, ax = plt.subplots()
        width = 0.28

        for no in range(len(plot_data_li[0])):
            data_y1 = plot_data_li[0].iloc[no]['flug/pers/km']
            data_y2 = plot_data_li[1].iloc[no]['flug/pers/km']
            bar_1 = ax.bar(no + 1 - width / 2, data_y1, width, color='darkred',
                           edgecolor='black', linewidth=1.5)
            bar_2 = ax.bar(no + 1 + width / 2, data_y2, width, color='darkgreen',
                           edgecolor='black', linewidth=1.5)

            plot_height = max(data_y1, data_y2)
            rel_month_diff_car = round(((int(data_y2) - int(data_y1)) / int(data_y1)) * 100, 2)
            abs_diff.append((int(data_y2) - int(data_y1)))
            total.append(int(data_y1))
            self.barplot_autolabel(ax, bar_1, f'{rel_month_diff_car} %', plot_height, plot_height/20)

        # 4 Quartale
        ax.set_xticks(np.arange(1, 5))
        ax.set_xticklabels(np.arange(1, 5), size=13)

        ax.tick_params(axis='y', labelsize=13)
        ax.set_ylabel(f'{indicator}', size=15)
        ax.set_xlabel('Quartal', size=15)
        ax.set_ylim(0, y_max * 1.25)
        ax.grid(True)
        ax.set_title(f'Auswertung Flugverkehr', size=25, weight='bold', position=(0.5, 1.065))
        ax.legend((bar_1, bar_2),
                (f'{indicator} - {year1}', f'{indicator} - {year2}'), fontsize=15)
        rel = round(sum(abs_diff) / sum(total) * 100, 2)
        ax.text(0.025, 0.95, f'Veränderung {indicator}: {rel} %', horizontalalignment='left',
                verticalalignment='top', transform=ax.transAxes, fontsize=15, weight='bold')
        fig.set_size_inches(18, 8)
        return fig


            #bar_car_y1 = ax.bar(no1 + 1 - width / 2, int(car_data_y1), width, color='darkred',
                    #                     edgecolor='black', linewidth=1.5)
                    # bar_hgv_y1 = ax.bar(no1 + 1 - width / 2, int(hgv_data_y1), width, color='lightblue',
                    #                     edgecolor='black', linewidth=1.5, bottom=int(car_data_y1))
                    # bar_car_y2 = ax.bar(no1 + 1 + width / 2, int(car_data_y2), width, color='darkgreen',
                    #                     edgecolor='black', linewidth=1.5)
                    # bar_hgv_y2 = ax.bar(no1 + 1 + width / 2, int(hgv_data_y2), width, color='darkorange',
                    #                     edgecolor='black', linewidth=1.5, bottom=int(car_data_y2))
                    #


        return plot_data_li





