#  Copyright (c) 2020. Jakob Erpf
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the 'Software'), to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
#  and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of
#  the Software.
#
#  THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
#  THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#  TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from func_correlation import numerical_encoding, compute_correlations
from func_plot import plot_correlation, plot_statistic, plot_boxplot_logscale
from func_utils import date_parser, print_welcome

if __name__ == '__main__':
    print_welcome()

    save_plot = True
    show_plot = False

    data_path = 'data/'
    work_path = data_path + 'ArbIS/dataset/'
    plot_path = work_path + 'plots/'
    tex_path = work_path + 'latex/'
    csv_path = work_path + 'csv/'
    work_file = 'ArbIS_2019.csv'

    arbis_imported = pd.read_csv(work_path + work_file, sep=';', decimal=',', parse_dates=True, date_parser=date_parser)

    arbis_selected = arbis_imported[
        [
            # Roadwork Data
            # 'Von', 'Bis',  # Not correlate able
            'Strasse',
            'AnzGesperrtFs',
            'Einzug',
            # 'VonKilometer', # Not correlate able
            # 'BisKilometer', # Not correlate able
            'Richtung',
            # 'VonKilometerBlock', # Not correlate able
            # 'BisKilometerBlock', # Not correlate able
            # 'VonStation', 'BisStation', # Not correlate able
            # 'VonAbschnitt', 'BisAbschnitt', # Not correlate able
            # 'SperrungID', 'StreckeID' # Not correlate able
            # 'StreckeID'
        ]].copy()

    # Manual data type conversion from str to datetime64
    arbis_imported['Von'] = pd.to_datetime(arbis_imported['Von'], format='%Y-%m-%d %H:%M:%S')
    arbis_imported['Bis'] = pd.to_datetime(arbis_imported['Bis'], format='%Y-%m-%d %H:%M:%S')

    # Add month of roadwork
    arbis_selected['Month'] = arbis_imported['Von'].dt.month_name()
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']

    # TODO https://stackoverflow.com/questions/33179122/seaborn-countplot-with-frequencies

    # Plot histogram of roadworks over time / months
    plt.figure(figsize=(13, 6))
    plt.title('Histogram of roadworks per month')
    plt.ylabel('Count')
    plt.xlabel('Month of 2019')
    sns.set_theme(style='darkgrid')
    # https://seaborn.pydata.org/generated/seaborn.countplot.html
    ax = sns.countplot(x='Month', data=arbis_selected, palette='Spectral', order=months)
    if save_plot:
        plt.savefig(plot_path + 'arbis_dataset_hist_month.pdf')
    if show_plot:
        plt.show()
    else:
        plt.close()

    # Remove month column
    # arbis_selected.drop('Month', axis='columns', inplace=True)

    # Plot histogram of accidents over highway
    plt.figure(figsize=(13, 6))
    plt.title('Histogram of roadworks per highways')
    plt.ylabel('Count')
    plt.xlabel('Highway')
    sns.set_theme(style='darkgrid')
    # https://seaborn.pydata.org/generated/seaborn.countplot.html
    ax = sns.countplot(x='Strasse', data=arbis_selected, palette='Spectral')
    if save_plot:
        plt.savefig(plot_path + 'arbis_dataset_hist_highway.pdf')
    if show_plot:
        plt.show()
    else:
        plt.close()

    # Add length of roadwork fragment in kilometers
    arbis_selected['Length'] = abs((arbis_imported['VonKilometer'] - arbis_imported['BisKilometer']))
    # Add duration of roadwork fragment in minutes
    arbis_selected['Duration'] = abs((arbis_imported['Von'] - arbis_imported['Bis'])).dt.total_seconds() / 60

    # Plot boxplots for visual relation testing
    plot_boxplot_logscale(arbis_selected, 'Strasse', 'Length', save_plot, show_plot,
                          plot_path + 'arbis_dataset_box_street2length.pdf')

    plot_boxplot_logscale(arbis_selected, 'Strasse', 'Duration', save_plot, show_plot,
                          plot_path + 'arbis_dataset_box_street2duration.pdf')

    plot_boxplot_logscale(arbis_selected, 'AnzGesperrtFs', 'Length', save_plot, show_plot,
                          plot_path + 'arbis_dataset_box_agfs2length.pdf')

    plot_boxplot_logscale(arbis_selected, 'AnzGesperrtFs', 'Duration', save_plot, show_plot,
                          plot_path + 'arbis_dataset_box_agfs2duration.pdf')

    plot_boxplot_logscale(arbis_selected, 'Einzug', 'Length', save_plot, show_plot,
                          plot_path + 'arbis_dataset_box_einzug2length.pdf')

    plot_boxplot_logscale(arbis_selected, 'Einzug', 'Duration', save_plot, show_plot,
                          plot_path + 'arbis_dataset_box_einzug2duration.pdf')

    plot_boxplot_logscale(arbis_selected, 'Richtung', 'Length', save_plot, show_plot,
                          plot_path + 'arbis_dataset_box_direction2length.pdf')

    plot_boxplot_logscale(arbis_selected, 'Richtung', 'Duration', save_plot, show_plot,
                          plot_path + 'arbis_dataset_box_direction2duration.pdf')

    # define column types
    nominal_columns = ['Strasse', 'StreckeID', 'Month']
    dichotomous_columns = ['Richtung']
    ordinal_columns = ['AnzGesperrtFs', 'Einzug']

    # Encode non numerical columns
    arbis_encoded, arbis_encoded_dict = numerical_encoding(arbis_selected,
                                                           ['Strasse',
                                                            'StreckeID',
                                                            'Month'],
                                                           drop_single_label=False,
                                                           drop_fact_dict=False)
    arbis_encoded.to_csv(csv_path + 'encoded.csv', index=False, sep=';')

    with open(csv_path + 'encoded_dict.csv', 'w') as tf:
        for key in arbis_encoded_dict.keys():
            tf.write("%s, %s\n" % (key, arbis_encoded_dict[key]))

    # Calculate with Cramers 's V
    results = None  # To make sure that no old data is reused
    results = compute_correlations(
        arbis_encoded,
        columns_nominal=nominal_columns, columns_dichotomous=dichotomous_columns, columns_ordinal=ordinal_columns,
        bias_correction=False)

    # Plot correlation matrix
    plot_correlation(results.get('correlation'), results.get('columns'),
                     nominal_columns, dichotomous_columns, ordinal_columns,
                     results.get('inf_nan_corr'),
                     results.get('columns_single_value'),
                     save=save_plot, filepath=plot_path + 'arbis_dataset_corr_cramers.pdf',
                     show=show_plot, figsize=(18, 15))

    # Plot statistics/significant matrix
    plot_statistic(results.get('significance'), results.get('columns'),
                   nominal_columns, dichotomous_columns, ordinal_columns,
                   results.get('inf_nan_corr'),
                   results.get('columns_single_value'),
                   save=save_plot, filepath=plot_path + 'arbis_dataset_sign_cramers.pdf',
                   show=show_plot, figsize=(18, 15))

    # Export correlation/statistics/coefficients into latex tables
    with open(tex_path + 'arbis_dataset_corr_cramers.tex', 'w') as tf:
        tf.write(results.get('correlation').to_latex(float_format="{:0.2f}".format))

    with open(tex_path + 'arbis_dataset_sign_cramers.tex', 'w') as tf:
        tf.write(results.get('significance').to_latex())

    with open(tex_path + 'arbis_dataset_coef_cramers.tex', 'w') as tf:
        tf.write(results.get('coefficient').to_latex())

    # Calculate with Theil's U
    results = None  # To make sure that no old data is reused
    results = compute_correlations(
        arbis_encoded,
        theils=True,
        columns_nominal=nominal_columns, columns_dichotomous=dichotomous_columns, columns_ordinal=ordinal_columns,
        bias_correction=False)

    # Plot correlation matrix
    plot_correlation(results.get('correlation'), results.get('columns'),
                     nominal_columns, dichotomous_columns, ordinal_columns,
                     results.get('inf_nan_corr'),
                     results.get('columns_single_value'),
                     save=save_plot, filepath=plot_path + 'arbis_dataset_corr_theils.pdf',
                     show=show_plot, figsize=(18, 15))

    # Plot statistics/significant matrix
    plot_statistic(results.get('significance'), results.get('columns'),
                   nominal_columns, dichotomous_columns, ordinal_columns,
                   results.get('inf_nan_corr'),
                   results.get('columns_single_value'),
                   save=save_plot, filepath=plot_path + 'arbis_dataset_sign_theils.pdf',
                   show=show_plot, figsize=(18, 15))

    # Export correlation/statistics/coefficients into latex tables
    with open(tex_path + 'arbis_dataset_corr_theils.tex', 'w') as tf:
        tf.write(results.get('correlation').to_latex(float_format="{:0.2f}".format))

    with open(tex_path + 'arbis_dataset_sign_theils.tex', 'w') as tf:
        tf.write(results.get('significance').to_latex())

    with open(tex_path + 'arbis_dataset_coef_theils.tex', 'w') as tf:
        tf.write(results.get('coefficient').to_latex())

    # https://seaborn.pydata.org/examples/scatterplot_matrix.html
    # sns.set_theme(style='ticks')
    # sns.pairplot(arbis_selected, hue='XXX')
    # plt.show()

    print('Finished ArbIS Dataset Analysis')
