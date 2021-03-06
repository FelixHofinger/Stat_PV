import pandas as pd
import numpy as np
import time
from os import path
import matplotlib.pyplot as plt
import streamlit as st

class Cross_Section_Data:
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
        self._weekday = {'Montag-Freitag': 'DTVMF',
                         'Montag-Sonntag': 'DTVMS',
                         'Montag': 'DTVMO',
                         'Dienstag-Donnerstag': 'DTVDD',
                         'Freitag': 'DTVFR',
                         'Samstag': 'DTVSA',
                         'Sonn- und Feiertag': 'DTVSF'}
        self._cross_section = {}

    def read_cross_data(self):
        return_data = pd.DataFrame()
        for no, year in enumerate(self._comp_year):
            for month in self._month:
                cross_data = pd.read_excel(
                    f"./cross_section_data/{str(year)[-2:]}{self._month[month][0]}_ASFINAG_Verkehrsstatistik_BW.xls",
                    sheet_name='Daten')
                cross_data = self.prep_data(cross_data, month, year)
                return_data = return_data.append(cross_data)
        return return_data

    def read_raum_cross_data(self, raum_type, bl):
        return_data = pd.DataFrame()
        cross_data_info = pd.read_excel(f"./cross_section_data/ASFINAG_Zählstellenübersicht.xlsx", sheet_name='Tabelle2')
        cross_data_info_dict = cross_data_info.set_index('Messstelle').T.to_dict('list')

        for no, year in enumerate(self._comp_year):
            for month in self._month:
                cross_data = pd.read_excel(
                    f"./cross_section_data/{str(year)[-2:]}{self._month[month][0]}_ASFINAG_Verkehrsstatistik_BW.xls",
                    sheet_name='Daten')
                cross_data = self.prep_data(cross_data, month, year, raumtyp=True)
                cross_data['Bundesland'] = cross_data['Zählstellenname'].apply(lambda x: cross_data_info_dict[x][1] if x in cross_data_info_dict else None)
                cross_data['Bezirk'] = cross_data['Zählstellenname'].apply(lambda x: cross_data_info_dict[x][2] if x in cross_data_info_dict else None)
                cross_data['Raumtyp'] = cross_data['Zählstellenname'].apply(lambda x: cross_data_info_dict[x][3] if x in cross_data_info_dict else None)
                cross_data['Grenze'] = cross_data['Zählstellenname'].apply(lambda x: cross_data_info_dict[x][4] if x in cross_data_info_dict else None)

                if bl == 'Alle' and raum_type == 'Gesamt':
                    return_data = return_data.append(cross_data)
                elif bl == 'Alle':
                    cross_data = cross_data.loc[cross_data['Raumtyp'] == raum_type]
                    return_data = return_data.append(cross_data)
                elif raum_type == 'Gesamt':
                    cross_data = cross_data.loc[cross_data['Bundesland'] == bl]
                    return_data = return_data.append(cross_data)
                else:
                    cross_data = cross_data.loc[cross_data['Raumtyp'] == raum_type]
                    cross_data = cross_data.loc[cross_data['Bundesland'] == bl]
                    return_data = return_data.append(cross_data)

        return return_data

    def prep_data(self, data, month, year, raumtyp = False):
        data_prep = data.tail(-2)
        data_prep = data_prep.drop(
            ['Abschnitt (von - bis)', 'Datengüte', 'Legende'], axis=1)
        data_prep['Fahrzeugklasse'] = data_prep['Fahrzeugklasse'].replace(
            {'Kfz': 'KFZ', 'Kfz > 3,5t hzG': 'LKW', 'Kfz <= 3,5t hzG': 'PKW', 'Kfz  > 3,5t hzG': 'LKW'})
        data_prep['Quartal'] = self._month[month][2]
        data_prep['Monat'] = self._month[month][0]
        data_prep['Jahr'] = year
        if raumtyp:
            data_prep = data_prep.loc[data_prep['Richtung'] == 'gesamt']
        return data_prep

    def select_drivingdirection(self, cross_data, cross_section):
        cross_section_data = cross_data.loc[cross_data['Zählstellenname'] == cross_section]
        driving_directions = cross_section_data['Richtung'].unique()
        return cross_section_data, driving_directions

    def cross_section_list(self, data):
        cross_section = data['Zählstellenname'].unique()
        motorway_df = pd.DataFrame()
        mp_df = pd.DataFrame
        for mp in cross_section:
            motorway_temp_data = data[data['Zählstellenname'] == mp]
            cross_section_name = [str(motorway_temp_data.iloc[0]['Autobahn']) + str('_') + \
                                  str(motorway_temp_data.iloc[0]['Zählstellen-']) + str('_') + \
                                  str(motorway_temp_data.iloc[0]['Zählstellenname'])]
            motorway_df = motorway_df.append(cross_section_name)


        dict_zaehlstelle = dict(zip(list(motorway_df[0]), list(cross_section)))

        motorway_df.to_excel(path.join(f"./results", "zaehlstellenliste.xlsx"))

        return motorway_df, dict_zaehlstelle

    def barplot_autolabel(self, ax, bar, text, height, bottom_height):
        """Attach a text label above each bar in *rects*, displaying its height."""

        for bars in bar:
            ax.annotate('{}'.format(text),
                        xy=(bars.get_x() + bars.get_width(), height + bottom_height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', rotation=0, size=10)

    def plot_bar_chart(self, data_to_plot, driving_direction, agg_intervall, weekday):
        # ToDo: May add checkbox do streamlit plattform
        wd = self._weekday[weekday]
        relative = True
        data_to_plot = data_to_plot.loc[data_to_plot['Richtung'] == driving_direction]
        y_max = []
        abs_diff_car = []
        abs_diff_hgv = []
        total_car_y1 = []
        total_hgv_y1 = []
        month_li = data_to_plot['Monat'].unique()
        q_li = data_to_plot['Quartal'].unique()
        plt.style.use('seaborn-darkgrid')
        fig, ax = plt.subplots()
        width = 0.28

        if agg_intervall == 'Monatlich':
            for no1, month in enumerate(month_li):
                car_data_y1 = data_to_plot.loc[(
                        (data_to_plot['Monat'] == month) & (data_to_plot['Jahr'] == self._year1) & (
                        data_to_plot['Fahrzeugklasse'] == 'PKW'))].reset_index().iloc[0][wd]
                car_data_y2 = data_to_plot.loc[(
                        (data_to_plot['Monat'] == month) & (data_to_plot['Jahr'] == self._year2) & (
                        data_to_plot['Fahrzeugklasse'] == 'PKW'))].reset_index().iloc[0][wd]
                hgv_data_y1 = data_to_plot.loc[(
                        (data_to_plot['Monat'] == month) & (data_to_plot['Jahr'] == self._year1) & (
                        data_to_plot['Fahrzeugklasse'] == 'LKW'))].reset_index().iloc[0][wd]
                hgv_data_y2 = data_to_plot.loc[(
                        (data_to_plot['Monat'] == month) & (data_to_plot['Jahr'] == self._year2) & (
                        data_to_plot['Fahrzeugklasse'] == 'LKW'))].reset_index().iloc[0][wd]

                y_max.append(round(max(car_data_y1 + hgv_data_y1, car_data_y2 + hgv_data_y2), -4))

                bar_car_y1 = ax.bar(no1 + 1 - width / 2, int(car_data_y1), width, color='darkred',
                                    edgecolor='black', linewidth=1.5)
                bar_hgv_y1 = ax.bar(no1 + 1 - width / 2, int(hgv_data_y1), width, color='lightblue',
                                    edgecolor='black', linewidth=1.5, bottom=int(car_data_y1))
                bar_car_y2 = ax.bar(no1 + 1 + width / 2, int(car_data_y2), width, color='darkgreen',
                                    edgecolor='black', linewidth=1.5)
                bar_hgv_y2 = ax.bar(no1 + 1 + width / 2, int(hgv_data_y2), width, color='darkorange',
                                    edgecolor='black', linewidth=1.5, bottom=int(car_data_y2))

                plot_height = max((car_data_y1 + hgv_data_y1), (car_data_y2 + hgv_data_y2))
                if relative:
                    abs_month_diff_car = int(car_data_y2) - int(car_data_y1)
                    abs_month_diff_hgv = int(hgv_data_y2) - int(hgv_data_y1)

                    abs_diff_car.append(abs_month_diff_car)
                    abs_diff_hgv.append(abs_month_diff_hgv)
                    total_car_y1.append(int(car_data_y1))
                    total_hgv_y1.append(int(hgv_data_y1))

                    rel_month_diff_car = round(((int(car_data_y2) - int(car_data_y1)) / int(car_data_y1)) * 100, 2)
                    rel_month_diff_hgv = round(((int(hgv_data_y2) - int(hgv_data_y1)) / int(hgv_data_y1)) * 100, 2)
                    self.barplot_autolabel(ax, bar_car_y1, f'PKW: {rel_month_diff_car} %', plot_height, 50)
                    self.barplot_autolabel(ax, bar_car_y1, f'LKW: {rel_month_diff_hgv} %', plot_height,
                                           plot_height * 0.05)

            # calc yearly diffrence
            rel_car = round(sum(abs_diff_car) / sum(total_car_y1) * 100, 2)
            rel_hgv = round(sum(abs_diff_hgv) / sum(total_hgv_y1) * 100, 2)
            print(y_max)
            y_max = max(y_max)
            print(y_max, 'second')
            ax.set_xticks(np.arange(1, len(month_li) + 1))
            ax.set_xticklabels(np.arange(1, len(month_li) + 1), size=13)
            ax.tick_params(axis='y', labelsize=13)
            ax.set_ylabel(f'DTV {weekday}', size=15)
            ax.set_xlabel('Monat', size=15)
            ax.set_ylim(0, y_max * 1.25 + 7500)
            ax.grid(True)
            ax.set_title(f'Übersicht Verkehrsaufkommen', size=25, weight='bold', position=(0.5, 1.065))
            ax.legend((bar_car_y1, bar_car_y2, bar_hgv_y1, bar_hgv_y2),
                      ('PKW pro Tag - 2019', 'PKW pro Tag - 2020', 'LKW pro Tag - 2019', 'LKW pro Tag - 2020'),
                      fontsize=15)

            ax.text(0.025, 0.95, f'Veränderung Verkehrsaufkommen PKW: {rel_car} %', horizontalalignment='left',
                    verticalalignment='top', transform=ax.transAxes, fontsize=15, weight='bold')
            ax.text(0.025, 0.90, f'Veränderung Verkehrsaufkommen LKW: {rel_hgv} %', horizontalalignment='left',
                    verticalalignment='top', transform=ax.transAxes, fontsize=15, weight='bold')
            fig.set_size_inches(18, 8)
            fig.savefig(path.join(f"./results", "first_barplot.pdf"))
            return fig

        elif agg_intervall == 'Quartalsweise':
            for no1, quartal in enumerate(q_li):
                car_data_y1 = int(data_to_plot.loc[(
                        (data_to_plot['Quartal'] == quartal) & (data_to_plot['Jahr'] == self._year1) & (
                        data_to_plot['Fahrzeugklasse'] == 'PKW'))].reset_index()[wd].mean())

                car_data_y2 = int(data_to_plot.loc[(
                        (data_to_plot['Quartal'] == quartal) & (data_to_plot['Jahr'] == self._year2) & (
                        data_to_plot['Fahrzeugklasse'] == 'PKW'))].reset_index()[wd].mean())
                hgv_data_y1 = int(data_to_plot.loc[(
                        (data_to_plot['Quartal'] == quartal) & (data_to_plot['Jahr'] == self._year1) & (
                        data_to_plot['Fahrzeugklasse'] == 'LKW'))].reset_index()[wd].mean())
                hgv_data_y2 = int(data_to_plot.loc[(
                        (data_to_plot['Quartal'] == quartal) & (data_to_plot['Jahr'] == self._year2) & (
                        data_to_plot['Fahrzeugklasse'] == 'LKW'))].reset_index()[wd].mean())

                y_max.append(round(max(car_data_y1 + hgv_data_y1, car_data_y2 + hgv_data_y2), -4))

                bar_car_y1 = ax.bar(no1 + 1 - width / 2, int(car_data_y1), width, color='darkred',
                                    edgecolor='black', linewidth=1.5)
                bar_hgv_y1 = ax.bar(no1 + 1 - width / 2, int(hgv_data_y1), width, color='lightblue',
                                    edgecolor='black', linewidth=1.5, bottom=int(car_data_y1))
                bar_car_y2 = ax.bar(no1 + 1 + width / 2, int(car_data_y2), width, color='darkgreen',
                                    edgecolor='black', linewidth=1.5)
                bar_hgv_y2 = ax.bar(no1 + 1 + width / 2, int(hgv_data_y2), width, color='darkorange',
                                    edgecolor='black', linewidth=1.5, bottom=int(car_data_y2))

                plot_height = max((car_data_y1 + hgv_data_y1), (car_data_y2 + hgv_data_y2))
                if relative:
                    abs_month_diff_car = int(car_data_y2) - int(car_data_y1)
                    abs_month_diff_hgv = int(hgv_data_y2) - int(hgv_data_y1)

                    abs_diff_car.append(abs_month_diff_car)
                    abs_diff_hgv.append(abs_month_diff_hgv)
                    total_car_y1.append(int(car_data_y1))
                    total_hgv_y1.append(int(hgv_data_y1))

                    rel_month_diff_car = round(((int(car_data_y2) - int(car_data_y1)) / int(car_data_y1)) * 100, 2)
                    rel_month_diff_hgv = round(((int(hgv_data_y2) - int(hgv_data_y1)) / int(hgv_data_y1)) * 100, 2)
                    self.barplot_autolabel(ax, bar_car_y1, f'PKW: {rel_month_diff_car} %', plot_height, 50)
                    self.barplot_autolabel(ax, bar_car_y1, f'LKW: {rel_month_diff_hgv} %', plot_height,
                                           plot_height * 0.05)

            # calc yearly diffrence
            rel_car = round(sum(abs_diff_car) / sum(total_car_y1) * 100, 2)
            rel_hgv = round(sum(abs_diff_hgv) / sum(total_hgv_y1) * 100, 2)
            print(y_max)
            y_max = max(y_max)
            print(y_max, 'second')
            ax.set_xticks(np.arange(1, len(q_li) + 1))
            ax.set_xticklabels(np.arange(1, len(q_li) + 1), size=13)
            ax.tick_params(axis='y', labelsize=13)
            ax.set_ylabel(f'DTV {weekday}', size=15)
            ax.set_xlabel('Quartal', size=15)
            ax.set_ylim(0, y_max * 1.25 + 7200)
            ax.grid(True)
            ax.set_title(f'Übersicht Verkehrsaufkommen - Quartal', size=25, weight='bold', position=(0.5, 1.065))
            ax.legend((bar_car_y1, bar_car_y2, bar_hgv_y1, bar_hgv_y2),
                      (f'PKW pro Tag - {self._year1}', f'PKW pro Tag - {self._year2}', f'LKW pro Tag - {self._year1}',
                       f'LKW pro Tag - {self._year2}'),
                      fontsize=15)

            ax.text(0.025, 0.95, f'Veränderung Verkehrsaufkommen PKW: {rel_car} %', horizontalalignment='left',
                    verticalalignment='top', transform=ax.transAxes, fontsize=15, weight='bold')
            ax.text(0.025, 0.90, f'Veränderung Verkehrsaufkommen LKW: {rel_hgv} %', horizontalalignment='left',
                    verticalalignment='top', transform=ax.transAxes, fontsize=15, weight='bold')
            fig.set_size_inches(18, 8)
            fig.savefig(path.join(f"./results", "quartal_barplot.pdf"))
            return fig


    def calc_cross_veh_sum(self, data_y1, data_y2, wd):
        temp_data = pd.merge(data_y1, data_y2, on='Zählstellenname', how='inner')

        temp_data = temp_data[(temp_data.DTVMF_x != -1)]
        temp_data = temp_data[(temp_data.DTVMF_y != -1)]

        temp_data['Differenz_percentage'] = temp_data[f'{wd}_y'] - temp_data[f'{wd}_x']#(temp_data('DTVMF_y')+1)
        temp_data['Differenz_percentage'] = temp_data['Differenz_percentage'] / temp_data[f'{wd}_x'] * 100

        data_y1_sum = temp_data[f'{wd}_x'].sum()
        data_y2_sum = temp_data[f'{wd}_y'].sum()
        diff_percentage = temp_data['Differenz_percentage'].mean()
        return data_y1_sum, data_y2_sum, diff_percentage

    def plot_bar_chart_raum(self, data_to_plot, agg_intervall, weekday, relative=True):
        # ToDo: May add checkbox do streamlit plattform
        wd = self._weekday[weekday]

        y_max = []
        abs_diff_car = []
        abs_diff_hgv = []
        total_car_y1 = []
        total_hgv_y1 = []
        month_li = data_to_plot['Monat'].unique()
        q_li = data_to_plot['Quartal'].unique()
        plt.style.use('seaborn-darkgrid')
        fig, ax = plt.subplots()
        width = 0.28

        if agg_intervall == 'Monatlich':
            for no1, month in enumerate(month_li):

                car_data_y1 = data_to_plot.loc[(data_to_plot['Monat'] == month) & (data_to_plot['Jahr'] == self._year1)
                                               & (data_to_plot['Fahrzeugklasse'] == 'PKW')]
                car_data_y2 = data_to_plot.loc[(data_to_plot['Monat'] == month) & (data_to_plot['Jahr'] == self._year2)
                                               & (data_to_plot['Fahrzeugklasse'] == 'PKW')]

                car_sum_y1, car_sum_y2, car_diff_per = self.calc_cross_veh_sum(car_data_y1, car_data_y2, wd)

                hgv_data_y1 = data_to_plot.loc[(
                        (data_to_plot['Monat'] == month) & (data_to_plot['Jahr'] == self._year1) & (
                        data_to_plot['Fahrzeugklasse'] == 'LKW'))]
                hgv_data_y2 = data_to_plot.loc[(
                        (data_to_plot['Monat'] == month) & (data_to_plot['Jahr'] == self._year2) & (
                        data_to_plot['Fahrzeugklasse'] == 'LKW'))]

                hgv_sum_y1, hgv_sum_y2, hgv_diff_per = self.calc_cross_veh_sum(hgv_data_y1, hgv_data_y2, wd)

                y_max.append(round(max(car_sum_y1 + hgv_sum_y1, car_sum_y2 + hgv_sum_y2), -4))

                bar_car_y1 = ax.bar(no1 + 1 - width / 2, int(car_sum_y1), width, color='darkred',
                                    edgecolor='black', linewidth=1.5)
                bar_hgv_y1 = ax.bar(no1 + 1 - width / 2, int(hgv_sum_y1), width, color='lightblue',
                                    edgecolor='black', linewidth=1.5, bottom=int(car_sum_y1))
                bar_car_y2 = ax.bar(no1 + 1 + width / 2, int(car_sum_y2), width, color='darkgreen',
                                    edgecolor='black', linewidth=1.5)
                bar_hgv_y2 = ax.bar(no1 + 1 + width / 2, int(hgv_sum_y2), width, color='darkorange',
                                    edgecolor='black', linewidth=1.5, bottom=int(car_sum_y2))

                plot_height = max((car_sum_y1 + hgv_sum_y1), (car_sum_y2 + hgv_sum_y2))

                if relative:
                    rel_month_diff_car = round(car_diff_per, 2)
                    rel_month_diff_hgv = round(hgv_diff_per, 2)
                    self.barplot_autolabel(ax, bar_car_y1, f'PKW: {rel_month_diff_car} %', plot_height, 50)
                    self.barplot_autolabel(ax, bar_car_y1, f'LKW: {rel_month_diff_hgv} %', plot_height,
                                           plot_height * 0.05)
                    abs_diff_car.append(rel_month_diff_car)
                    abs_diff_hgv.append(rel_month_diff_hgv)

                else:
                    abs_month_diff_car = int(car_sum_y2) - int(car_sum_y1)
                    abs_month_diff_hgv = int(hgv_sum_y2) - int(hgv_sum_y1)

                    abs_diff_car.append(abs_month_diff_car)
                    abs_diff_hgv.append(abs_month_diff_hgv)
                    total_car_y1.append(int(car_sum_y1))
                    total_hgv_y1.append(int(hgv_sum_y1))

                    rel_month_diff_car = round(((int(car_sum_y2) - int(car_sum_y1)) / int(car_sum_y1)) * 100, 2)
                    rel_month_diff_hgv = round(((int(hgv_sum_y2) - int(hgv_sum_y1)) / int(hgv_sum_y1)) * 100, 2)
                    self.barplot_autolabel(ax, bar_car_y1, f'PKW: {rel_month_diff_car} %', plot_height, 50)
                    self.barplot_autolabel(ax, bar_car_y1, f'LKW: {rel_month_diff_hgv} %', plot_height,
                                           plot_height * 0.05)

            # calc yearly diffrence
            if relative:
                rel_car = round(sum(abs_diff_car) / 12, 2)
                rel_hgv = round(sum(abs_diff_hgv) / 12, 2)

            else:
                rel_car = round(sum(abs_diff_car) / sum(total_car_y1) * 100, 2)
                rel_hgv = round(sum(abs_diff_hgv) / sum(total_hgv_y1) * 100, 2)

            y_max = max(y_max)
            ax.set_xticks(np.arange(1, len(month_li) + 1))
            ax.set_xticklabels(np.arange(1, len(month_li) + 1), size=13)
            ax.tick_params(axis='y', labelsize=13)
            ax.set_ylabel(f'DTV {weekday}', size=15)
            ax.set_xlabel('Monat', size=15)
            ax.set_ylim(0, y_max * 1.25 + 7500)
            ax.grid(True)
            ax.set_title(f'Übersicht Verkehrsaufkommen', size=25, weight='bold', position=(0.5, 1.065))
            ax.legend((bar_car_y1, bar_car_y2, bar_hgv_y1, bar_hgv_y2),
                      ('PKW pro Tag - 2019', 'PKW pro Tag - 2020', 'LKW pro Tag - 2019', 'LKW pro Tag - 2020'),
                      fontsize=15)

            ax.text(0.025, 0.95, f'Veränderung Verkehrsaufkommen PKW: {rel_car} %', horizontalalignment='left',
                    verticalalignment='top', transform=ax.transAxes, fontsize=15, weight='bold')
            ax.text(0.025, 0.90, f'Veränderung Verkehrsaufkommen LKW: {rel_hgv} %', horizontalalignment='left',
                    verticalalignment='top', transform=ax.transAxes, fontsize=15, weight='bold')
            fig.set_size_inches(18, 8)
            fig.savefig(path.join(f"./results", "first_barplot.pdf"))
            return fig

        elif agg_intervall == 'Quartalsweise':
            for no1, quartal in enumerate(q_li):
                car_data_y1 = int(data_to_plot.loc[(
                        (data_to_plot['Quartal'] == quartal) & (data_to_plot['Jahr'] == self._year1) & (
                        data_to_plot['Fahrzeugklasse'] == 'PKW'))].reset_index()[wd].mean())

                car_data_y2 = int(data_to_plot.loc[(
                        (data_to_plot['Quartal'] == quartal) & (data_to_plot['Jahr'] == self._year2) & (
                        data_to_plot['Fahrzeugklasse'] == 'PKW'))].reset_index()[wd].mean())
                hgv_data_y1 = int(data_to_plot.loc[(
                        (data_to_plot['Quartal'] == quartal) & (data_to_plot['Jahr'] == self._year1) & (
                        data_to_plot['Fahrzeugklasse'] == 'LKW'))].reset_index()[wd].mean())
                hgv_data_y2 = int(data_to_plot.loc[(
                        (data_to_plot['Quartal'] == quartal) & (data_to_plot['Jahr'] == self._year2) & (
                        data_to_plot['Fahrzeugklasse'] == 'LKW'))].reset_index()[wd].mean())

                y_max.append(round(max(car_data_y1 + hgv_data_y1, car_data_y2 + hgv_data_y2), -4))

                bar_car_y1 = ax.bar(no1 + 1 - width / 2, int(car_data_y1), width, color='darkred',
                                    edgecolor='black', linewidth=1.5)
                bar_hgv_y1 = ax.bar(no1 + 1 - width / 2, int(hgv_data_y1), width, color='lightblue',
                                    edgecolor='black', linewidth=1.5, bottom=int(car_data_y1))
                bar_car_y2 = ax.bar(no1 + 1 + width / 2, int(car_data_y2), width, color='darkgreen',
                                    edgecolor='black', linewidth=1.5)
                bar_hgv_y2 = ax.bar(no1 + 1 + width / 2, int(hgv_data_y2), width, color='darkorange',
                                    edgecolor='black', linewidth=1.5, bottom=int(car_data_y2))

                plot_height = max((car_data_y1 + hgv_data_y1), (car_data_y2 + hgv_data_y2))
                if relative:
                    abs_month_diff_car = int(car_data_y2) - int(car_data_y1)
                    abs_month_diff_hgv = int(hgv_data_y2) - int(hgv_data_y1)

                    abs_diff_car.append(abs_month_diff_car)
                    abs_diff_hgv.append(abs_month_diff_hgv)
                    total_car_y1.append(int(car_data_y1))
                    total_hgv_y1.append(int(hgv_data_y1))

                    rel_month_diff_car = round(((int(car_data_y2) - int(car_data_y1)) / int(car_data_y1)) * 100, 2)
                    rel_month_diff_hgv = round(((int(hgv_data_y2) - int(hgv_data_y1)) / int(hgv_data_y1)) * 100, 2)
                    self.barplot_autolabel(ax, bar_car_y1, f'PKW: {rel_month_diff_car} %', plot_height, 50)
                    self.barplot_autolabel(ax, bar_car_y1, f'LKW: {rel_month_diff_hgv} %', plot_height,
                                           plot_height * 0.05)

            # calc yearly diffrence
            try:
                rel_car = round(sum(abs_diff_car) / sum(total_car_y1) * 100, 2)
            except:
                rel_car = -100
            try:
                rel_hgv = round(sum(abs_diff_hgv) / sum(total_hgv_y1) * 100, 2)
            except:
                rel_hgv = -100
            print(y_max)
            y_max = max(y_max)
            print(y_max, 'second')
            ax.set_xticks(np.arange(1, len(q_li) + 1))
            ax.set_xticklabels(np.arange(1, len(q_li) + 1), size=13)
            ax.tick_params(axis='y', labelsize=13)
            ax.set_ylabel(f'DTV {weekday}', size=15)
            ax.set_xlabel('Quartal', size=15)
            ax.set_ylim(0, y_max * 1.25 + 7200)
            ax.grid(True)
            ax.set_title(f'Übersicht Verkehrsaufkommen - Quartal', size=25, weight='bold', position=(0.5, 1.065))
            ax.legend((bar_car_y1, bar_car_y2, bar_hgv_y1, bar_hgv_y2),
                      ('PKW pro Tag - 2019', 'PKW pro Tag - 2020', 'LKW pro Tag - 2019', 'LKW pro Tag - 2020'),
                      fontsize=15)

            ax.text(0.025, 0.95, f'Veränderung Verkehrsaufkommen PKW: {rel_car} %', horizontalalignment='left',
                    verticalalignment='top', transform=ax.transAxes, fontsize=15, weight='bold')
            ax.text(0.025, 0.90, f'Veränderung Verkehrsaufkommen LKW: {rel_hgv} %', horizontalalignment='left',
                    verticalalignment='top', transform=ax.transAxes, fontsize=15, weight='bold')
            fig.set_size_inches(18, 8)
            fig.savefig(path.join(f"./results", "quartal_barplot.pdf"))
            return fig



debug = 0
if debug:
    cross_section_data = Cross_Section_Data(year1=2019, year2=2020)
    cross_data = cross_section_data.read_cross_data()
    cross_section_li = cross_section_data.cross_section_list(cross_data)
    cross_data = cross_section_data.select_data(cross_data, 'Pressbaum', 'monatlich', 'Montag-Freitag')
