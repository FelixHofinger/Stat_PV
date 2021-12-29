
import pandas as pd
import numpy as np
import time
from os import path
import matplotlib.pyplot as plt



class Cross_Section_Data:
    def __init__(self, year1=None, year2=None, agg_level=None):
        self._year1 = year1
        self._year2 = year2
        self._agg_level = agg_level
        self._comp_year = (self._year1, self._year2)
        self._month = {1 :('01', 'Jänner', 'Q1'),
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

    def read_cross_data(self):

        return_data = pd.DataFrame()
        for no, year in enumerate(self._comp_year):
            for month in self._month:
                cross_data = pd.read_excel(f"./cross_section_data/{str(year)[-2:]}{self._month[month][0]}_ASFINAG_Verkehrsstatistik_BW.xls", sheet_name='Daten')
                cross_data = self.prep_data(cross_data, month, year)
                return_data = return_data.append(cross_data)

        return return_data




    def prep_data(self,data,month,year):
        data_prep = data.tail(-2)
        data_prep = data_prep.drop(['Abschnitt (von - bis)', 'DTVMS', 'DTVMO', 'DTVDD', 'DTVFR', 'Datengüte', 'Legende'], axis =1)
        data_prep['Fahrzeugklasse'] = data_prep['Fahrzeugklasse'].replace({'Kfz': 'KFZ', 'Kfz > 3,5t hzG': 'LKW', 'Kfz <= 3,5t hzG': 'PKW', 'Kfz  > 3,5t hzG': 'LKW'})
        data_prep['Quartal'] = self._month[month][2]
        data_prep['Monat'] = self._month[month][0]
        data_prep['Jahr'] = year
        return data_prep

    def select_drivingdirection(self, cross_data, cross_section):

        cross_section_data = cross_data.loc[cross_data['Zählstellenname'] == cross_section]
        driving_directions = cross_section_data['Richtung'].unique()

        #data_to_plot = cross_data.loc[cross_data['Zählstellenname'] == cross_section]

        return cross_section_data, driving_directions

    def cross_section_list(self,data):
        cross_section = data['Zählstellenname'].unique()
        return cross_section

    def barplot_autolabel(self, ax, bar, text, height, bottom_height):
        """Attach a text label above each bar in *rects*, displaying its height."""

        for bars in bar:

           #

            ax.annotate('{}'.format(text),
                        xy=(bars.get_x() + bars.get_width(), height + bottom_height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', rotation=0, size=10)

    def plot_bar_chart(self,data_to_plot, driving_direction, agg_intervall, weekday):

        data_to_plot = data_to_plot.loc[data_to_plot['Richtung'] == driving_direction]
        y_max = []
        month_li = data_to_plot['Monat'].unique()
        plt.style.use('seaborn-darkgrid')
        fig,ax = plt.subplots()
        width = 0.28

        if weekday == 'Montag-Freitag':
            if agg_intervall =='Monatlich':
                print(data_to_plot['Fahrzeugklasse'].unique())
                print(data_to_plot['Monat'].unique())

                for no1, month in enumerate(month_li):
                    car_data_y1 = data_to_plot.loc[(
                                (data_to_plot['Monat'] == month) & (data_to_plot['Jahr'] == self._year1) & (
                                    data_to_plot['Fahrzeugklasse'] == 'PKW'))].reset_index().iloc[0]['DTVMF']
                    car_data_y2 = data_to_plot.loc[(
                                (data_to_plot['Monat'] == month) & (data_to_plot['Jahr'] == self._year2) & (
                                    data_to_plot['Fahrzeugklasse'] == 'PKW'))].reset_index().iloc[0]['DTVMF']
                    hgv_data_y1 = data_to_plot.loc[(
                                (data_to_plot['Monat'] == month) & (data_to_plot['Jahr'] == self._year1) & (
                                    data_to_plot['Fahrzeugklasse'] == 'LKW'))].reset_index().iloc[0]['DTVMF']
                    hgv_data_y2 = data_to_plot.loc[(
                                (data_to_plot['Monat'] == month) & (data_to_plot['Jahr'] == self._year2) & (
                                data_to_plot['Fahrzeugklasse'] == 'LKW'))].reset_index().iloc[0]['DTVMF']

                    y_max.append(round(max(car_data_y1+hgv_data_y1,car_data_y2+hgv_data_y2), -4))

                    bar_car_y1 = ax.bar(no1+1-width/2, int(car_data_y1), width, color='darkred',edgecolor='black',linewidth=1.5)
                    bar_hgv_y1 = ax.bar(no1 + 1 - width / 2, int(hgv_data_y1), width, color='lightblue', edgecolor='black', linewidth=1.5, bottom=int(car_data_y1))
                    bar_car_y2 = ax.bar(no1 + 1 + width / 2, int(car_data_y2), width, color='darkgreen', edgecolor='black', linewidth=1.5)
                    bar_hgv_y2 = ax.bar(no1 + 1 + width / 2, int(hgv_data_y2), width, color='darkorange', edgecolor='black',linewidth=1.5, bottom=int(car_data_y2))



                    abs_month_diff_car = int(car_data_y2) - int(car_data_y1)
                    rel_month_diff_car = round(((int(car_data_y2) - int(car_data_y1))/int(car_data_y1))*100, 2)

                    abs_month_diff_hgv = int(hgv_data_y2) - int(hgv_data_y1)
                    rel_month_diff_hgv = round(((int(hgv_data_y2) - int(hgv_data_y1)) / int(hgv_data_y1)) * 100, 2)

                    plot_height = max((car_data_y1+hgv_data_y1),(car_data_y2+hgv_data_y2))



                    self.barplot_autolabel(ax, bar_car_y1, f'PKW: {rel_month_diff_car} %', plot_height, 50)
                    self.barplot_autolabel(ax, bar_car_y1, f'LKW: {rel_month_diff_hgv} %', plot_height, plot_height*0.05)
                    # self.barplot_autolabel(ax, bar_car_y2, 0)
                    # self.barplot_autolabel(ax, bar_hgv_y1, car_data_y1)
                    # self.barplot_autolabel(ax, bar_hgv_y2, car_data_y2)

        y_max = max(y_max)
        ax.set_xticks(np.arange(1,len(month_li)+1))
        ax.set_xticklabels(np.arange(1,len(month_li)+1), size=13)
        ax.tick_params(axis='y', labelsize=13)
        ax.set_ylabel('[DTV Werktag]', size=15)
        ax.set_xlabel('Monat', size=15)
        ax.set_ylim(0, y_max*1.25)
        ax.grid(True)
        ax.set_title(f'Übersicht Verkehrsaufkommen', size=25, weight='bold', position=(0.5, 1.065))
        ax.legend((bar_car_y1, bar_car_y2, bar_hgv_y1, bar_hgv_y2), ('PKW pro Tag - 2019', 'PKW pro Tag - 2020', 'LKW pro Tag - 2019','LKW pro Tag - 2020'), fontsize=15)

        fig.set_size_inches(18, 8)
        fig.savefig(path.join(f"./results","first_barplot.pdf"))

        return fig




debug = 0
if debug:
    cross_section_data = Cross_Section_Data(year1=2019, year2=2020)
    cross_data = cross_section_data.read_cross_data()
    cross_section_li = cross_section_data.cross_section_list(cross_data)


    cross_data = cross_section_data.select_data(cross_data,'Pressbaum','monatlich','Montag-Freitag')

