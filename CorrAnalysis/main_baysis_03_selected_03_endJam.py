#  Copyright (c) 2020. Jakob Erpf
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
#  and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of
#  the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
#  THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#  TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas_profiling import ProfileReport

from func_correlation import numerical_encoding, compute_correlations
from func_plot import plot_correlation, plot_statistic, set_size, tex_fonts, \
    plot_congestion_dist, plot_congestion_scatter
from func_utils import date_parser, print_welcome

if __name__ == '__main__':
    print_welcome()

    save_plot = True
    show_plot = False

    generate_report = True

    data_path = 'data/'
    work_path = data_path + 'BAYSIS/03_selected_03_endJam/'
    plot_path = work_path + 'plots/'
    tex_path = work_path + 'latex/'
    csv_path = work_path + 'csv/'

    work_file = 'BAYSIS_2019.csv'

    file_prefix = 'baysis_selected'
    file_plot_type = '.pdf'

    baysis_imported = pd.read_csv(data_path + 'BAYSIS/02_matched/' + work_file, sep=';', decimal=',', parse_dates=True,
                                  date_parser=date_parser)

    baysis_matched = baysis_imported[
        [
            # Congestion Data
            "TempMax",
            "TempAvg",
            "SpatMax",
            "SpatAvg",
            "TempDist",
            "SpatDist",
            "Coverage",
            # The temporal reference of if the incident to the congestion. The incident...
            # [-1] = Not Set
            # [1] = is before
            # [2] = is overlapping before
            # [3] = is during
            # [4] = is overlapping after
            # [5] = is after
            "TempGL",
            # The spatial reference of if the incident to the congestion. The incident...
            # [-1] = Not Set in case of congestion with no distance
            # [1] = is before
            # [2] = is during or overlapping
            # [3] = is after
            "SpatGL",
            # The temporal reference of if the incident is during the congestion. The incident is within...
            # [-1] = Not Set in case not during or overlapping
            # [1] = 10% to Beginning
            # [2] = 10% - 30% to Beginning
            # [3] = 30% - 70% (Middle)
            # [4] = 30% - 10% to Ending
            # [5] = 10% to Ending
            "TempIL",
            # The spatial reference of if the incident is during the congestion. The incident is within...
            # [-1] = Not Set in case not during or overlapping
            # [1] = 10% to Beginning
            # [2] = 10% - 30% to Beginning
            # [3] = 30% - 70% (Middle)
            # [4] = 30% - 10% to Ending
            # [5] = 10% to Ending
            "SpatIL",
            "TLCar",
            "TLHGV",
            # Accident Data
            "Strasse",
            "Kat", "Typ", "Betei",
            "UArt1", "UArt2",
            "AUrs1", "AUrs2",
            "AufHi",
            "Alkoh",
            "Char1", "Char2",
            "Lich1", "Lich2",
            "Zust1", "Zust2",
            "Fstf",
            "WoTag",
            "FeiTag"]].copy()

    # Manual data type conversion from str to datetime64
    baysis_imported['Date'] = pd.to_datetime(baysis_imported['Date'], format='%Y-%m-%d')

    # Manual data type conversion from str to int64
    baysis_matched["TLCar"] = pd.to_numeric(baysis_matched["TLCar"])
    baysis_matched["TLHGV"] = pd.to_numeric(baysis_matched["TLHGV"])
    baysis_matched["TLCar"] = baysis_matched["TLCar"].astype('int64')
    baysis_matched["TLHGV"] = baysis_matched["TLHGV"].astype('int64')

    # Add month of roadwork
    baysis_matched['Month'] = baysis_imported['Date'].dt.strftime('%b')
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Removing errors in WoTag
    days = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
    baysis_matched['WoTag'].loc[np.invert(baysis_matched['WoTag'].isin(days))] = ''

    # Removing whitespaces
    baysis_matched['Strasse'] = baysis_matched['Strasse'].str.replace(' ', '')

    #################
    ### Selection ###
    #################

    baysis_selected = baysis_matched.loc[
        (baysis_matched["TempGL"].isin([3, 4, 5]))
    ]

    baysis_selected = baysis_selected.loc[
        (baysis_matched["TempIL"].isin([-1, 4, 5]))
    ]

    baysis_selected = baysis_selected.loc[
        (baysis_matched["SpatGL"].isin([2, 3]))
    ]

    ##################
    ### Congestion ###
    ##################

    plot_congestion_dist(
        ["TempMax",
         "TempAvg",
         "SpatMax",
         "SpatAvg",
         "TempDist",
         "SpatDist",
         "Coverage",
         "TLCar",
         "TLHGV"],
        baysis_matched, plot_path, file_prefix, save_plot, show_plot)

    # plot_congestion_scatter(
    #     ["TempMax"],
    #     ["SpatMax"],
    #     baysis_matched, plot_path, file_prefix, save_plot, show_plot)
    #
    # plot_congestion_scatter(
    #     ["TempAvg"],
    #     ["SpatAvg"],
    #     baysis_matched, plot_path, file_prefix, save_plot, show_plot)
    #
    # plot_congestion_scatter(
    #     ["TempDist"],
    #     ["SpatDist"],
    #     baysis_matched, plot_path, file_prefix, save_plot, show_plot)
    #
    # plot_congestion_scatter(
    #     ["TLCar"],
    #     ["TLHGV"],
    #     baysis_matched, plot_path, file_prefix, save_plot, show_plot)
    #
    # locators = ["TempGL",
    #             "SpatGL",
    #             "TempIL",
    #             "SpatIL"]
    #
    # for atr in locators:
    #     plt.figure(figsize=set_size(418, 0.8))
    #     plt.style.use('seaborn')
    #     plt.rcParams.update(tex_fonts)
    #     plt.title('Distribution of ' + atr)
    #     plt.ylabel('Count')
    #     baysis_selected.plot.scatter(x='TempMax', y='SpatMax', c=atr, colormap='viridis')
    #     plt.xlabel(atr)
    #     if save_plot:
    #         plt.savefig(plot_path + file_prefix + '_scatter_E_' + atr + '.pdf')
    #         if not show_plot:
    #             plt.close()
    #     if show_plot:
    #         plt.show()
    #     else:
    #         plt.close()

    ##################
    ### Histograms ###
    ##################

    # Plot histogram of accidents over time / months
    plt.figure(figsize=(13, 6))
    plt.title('Histogram of accidents per month, with at least one adjacent congestion')
    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)
    plt.ylabel('Count')
    ax = sns.countplot(x='Month', data=baysis_selected, palette='Spectral', order=months)
    if save_plot:
        plt.savefig(plot_path + file_prefix + '_hist_month.pdf')
        if not show_plot:
            plt.close()
    if show_plot:
        plt.show()
    else:
        plt.close()

    # Remove month column
    # baysis_selected.drop('Month', axis='columns', inplace=True)

    # Plot histogram of accidents over highway
    plt.figure(figsize=(13, 6))
    plt.title('Histogram of accidents per highways, with at least one adjacent congestion')
    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)
    plt.ylabel('Count')
    ax = sns.countplot(x='Strasse', data=baysis_selected, palette='Spectral')
    if save_plot:
        plt.savefig(plot_path + file_prefix + '_hist_highway.pdf')
        if not show_plot:
            plt.close()
    if show_plot:
        plt.show()
    else:
        plt.close()

    ##############
    ### Counts ###
    ##############

    ###############
    ### Scatter ###
    ###############

    ###########
    ### Box ###
    ###########

    ##############
    ### Report ###
    ##############

    if generate_report:
        report = ProfileReport(baysis_selected, title='BAYSIS Selected Dataset Report')
        report.to_file(work_path + file_prefix + '_report.html')

    ###################
    ### Encoding ###
    ###################

    # define column types
    nominal_columns = ["Str", "Kat", "Typ",
                       "UArt1", "UArt2",
                       "AUrs1", "AUrs2",
                       "AufHi",
                       "Char1", "Char2",
                       "Lich1", "Lich2",
                       "Zust1", "Zust2",
                       "WoTag",
                       'Month']
    dichotomous_columns = ["Alkoh"]
    ordinal_columns = ["Betei", "Fstf", "FeiTag"]

    # Encode non numerical columns
    baysis_encoded, baysis_encoded_dict = numerical_encoding(baysis_selected,
                                                             ["Strasse",
                                                              "Fstf",
                                                              'Month'],
                                                             drop_single_label=False,
                                                             drop_fact_dict=False)
    baysis_encoded.to_csv(csv_path + 'encoded.csv', index=False, sep=';')

    with open(csv_path + 'encoded_dict.csv', 'w') as tf:
        for key in baysis_encoded_dict.keys():
            tf.write("%s, %s\n" % (key, baysis_encoded_dict[key]))

    ###################
    ### Correlation ###
    ###################

    baysis_encoded = baysis_encoded.rename(columns={"TempMax": "TMax",
                                                    "TempAvg": "TAvg",
                                                    "SpatMax": "SMax",
                                                    "SpatAvg": "SAvg",
                                                    "Coverage": "Cov",
                                                    "TempDist": "TDist",
                                                    "SpatDist": "SDist",
                                                    'Strasse': "Str"})

    baysis_encoded = baysis_encoded.drop(columns=["TempGL",
                                                  "SpatGL",
                                                  "TempIL",
                                                  "SpatIL"])

    # Calculate with Cramers 's V
    results = None  # To make sure that no old data is reused
    results = compute_correlations(
        baysis_encoded,
        columns_nominal=nominal_columns, columns_dichotomous=dichotomous_columns, columns_ordinal=ordinal_columns,
        bias_correction=False)

    # Plot correlation matrix
    plot_correlation(results.get('correlation'), results.get('columns'),
                     nominal_columns, dichotomous_columns, ordinal_columns,
                     results.get('inf_nan_corr'),
                     results.get('columns_single_value'),
                     save=save_plot, filepath=plot_path + file_prefix + '_corr_cramers.pdf',
                     show=show_plot, figsize=(18, 15))

    # Plot statistics/significant matrix
    # plot_statistic(results.get('significance'), results.get('columns'),
    #                nominal_columns, dichotomous_columns, ordinal_columns,
    #                results.get('inf_nan_corr'),
    #                results.get('columns_single_value'),
    #                save=save_plot, filepath=plot_path + file_prefix + '_sign_cramers.pdf',
    #                show=show_plot, figsize=(18, 15))

    # Export correlation/statistics/coefficients into latex tables
    with open(tex_path + file_prefix + '_corr_cramers.tex', 'w') as tf:
        tf.write(results.get('correlation').to_latex(float_format="{:0.2f}".format))

    with open(tex_path + file_prefix + '_sign_cramers.tex', 'w') as tf:
        tf.write(results.get('significance').to_latex(float_format="{:0.3f}".format))

    with open(tex_path + file_prefix + '_coef_cramers.tex', 'w') as tf:
        tf.write(results.get('coefficient').to_latex(escape=False))

    # Calculate with Theil's U
    results = None  # To make sure that no old data is reused
    results = compute_correlations(
        baysis_encoded,
        theils=True,
        columns_nominal=nominal_columns, columns_dichotomous=dichotomous_columns, columns_ordinal=ordinal_columns,
        bias_correction=False)

    # Plot correlation matrix
    plot_correlation(results.get('correlation'), results.get('columns'),
                     nominal_columns, dichotomous_columns, ordinal_columns,
                     results.get('inf_nan_corr'),
                     results.get('columns_single_value'),
                     save=save_plot, filepath=plot_path + file_prefix + '_corr_theils.pdf',
                     show=show_plot, figsize=(18, 15))

    # Plot statistics/significant matrix
    # plot_statistic(results.get('significance'), results.get('columns'),
    #                nominal_columns, dichotomous_columns, ordinal_columns,
    #                results.get('inf_nan_corr'),
    #                results.get('columns_single_value'),
    #                save=save_plot, filepath=plot_path + file_prefix + '_sign_theils.pdf',
    #                show=show_plot, figsize=(18, 15))

    # Export correlation/statistics/coefficients into latex tables
    with open(tex_path + file_prefix + '_corr_theils.tex', 'w') as tf:
        tf.write(results.get('correlation').to_latex(float_format="{:0.2f}".format))

    with open(tex_path + file_prefix + '_sign_theils.tex', 'w') as tf:
        tf.write(results.get('significance').to_latex(float_format="{:0.3f}".format))

    with open(tex_path + file_prefix + '_coef_theils.tex', 'w') as tf:
        tf.write(results.get('coefficient').to_latex(escape=False))

    ######################
    ### Scatter Matrix ###
    ######################

    # https://seaborn.pydata.org/examples/scatterplot_matrix.html
    # sns.set_theme(style='ticks')
    # sns.pairplot(baysis_selected, hue='Kat')
    # plt.show()

    print('Finished BAYSIS Selected Analysis')
