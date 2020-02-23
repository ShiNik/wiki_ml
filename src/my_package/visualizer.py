# user define imports
from my_package import TableIt as TableIt
from my_package import util as util
from my_package.log_manager import LogManager
import sklearn.metrics as metrics

# python imports
import numpy as np
import matplotlib.pyplot as plt
import seaborn as seabornInstance
import pylab
import scipy.stats as stats
import pandas as pd

def get_plot_size(num_items):
    num_col = 3
    num_row = int(np.ceil(num_items / num_col))
    return {"row_size": num_row, "col_size": num_col}


def scatter_plots(analysis_list, plot_title, silen_mode_enabled=True):
    plot_size = get_plot_size(len(analysis_list))

    fig, axs = plt.subplots(plot_size["row_size"], plot_size["col_size"], figsize=(20, 10),
                            gridspec_kw={'wspace': 0.5, 'hspace': 0.55})
    fig.suptitle(plot_title, fontsize=15)
    axs = axs.flatten()
    for analysis, ax in zip(analysis_list, axs):
        x_value = analysis.data_info.x_values
        y_value = analysis.data_info.y_values
        x_title = analysis.data_info.x_label
        y_title = analysis.data_info.y_label
        intercept = analysis.results_info.intercept
        coef = analysis.results_info.coefficient
        analysis_type = analysis.type

        ax.scatter(x_value, y_value, color='r')
        ax.set_title(analysis_type, size=10, color="g")
        ax.set_xlabel(x_title, size=7, color="y")
        ax.set_ylabel(y_title, size=7, color="y")

        intercept = intercept[0]
        coef = coef[0][0]
        # p5 = ax.plot([1, 2, 3], [1, 2, 3], "r--")
        xx = np.zeros(2)
        yy = np.zeros(2)
        xx[0] = 0
        yy[0] = intercept
        xx[1] = np.max(x_value)
        yy[1] = np.max(x_value) * coef + intercept

        eq_line = "y = " + "{:10.3f}".format(coef) + "x" + "{:10.3f}".format(intercept)
        ax.plot(xx, yy, linestyle="solid", label=eq_line)

    if not silen_mode_enabled:
        plt.show()

    logger = LogManager.instance()
    if logger.debug_enabled():
        from my_package import util as util

        file_name = plot_title + ".png"
        full_path = util.get_full_output_path(file_name)
        fig.savefig(full_path)

    plt.close(fig)


def plot_data(dataset, labels, silen_mode_enabled=True):
    axes_subplot = dataset.plot(x=labels["x"][0], y=labels["y"][0], style='o')
    plt.title(labels["x"][1] + ' vs ' + labels["y"][1])
    plt.xlabel(labels["x"][1])
    plt.ylabel(labels["y"][1])

    if not silen_mode_enabled:
        plt.show()

    fig = axes_subplot.get_figure()
    logger = LogManager.instance()
    if logger.debug_enabled():
        from my_package import util as util
        file_name = 'Scatter_Data_' + labels["x"][1] + 'vs' + labels["y"][1] + ".png"
        full_path = util.get_full_output_path(file_name)
        fig.savefig(full_path)

    plt.close(fig)


def plot_results(analysis, silent_mode_enabled=True):
    import pandas as pd

    y_test = analysis.data_info.y_test
    y_pred = analysis.results_info.prediction
    if y_test is not None and y_pred is not None:
        df = pd.DataFrame({analysis.data_info.y_label + ' Actual': y_test.flatten(),
                           analysis.data_info.y_label + ' Predicted': y_pred.flatten()})
        df1 = df.head(25)
        axes_subplot = df1.plot(title=analysis.data_info.x_label, kind='bar', figsize=(16, 10))
        plt.grid(which='major', linestyle='-', linewidth='0.5', color='green')
        plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
        if not silent_mode_enabled:
            plt.show()

        fig = axes_subplot.get_figure()
        logger = LogManager.instance()
        if logger.debug_enabled():
            from my_package import util as util
            file_name = 'Result_' + analysis.data_info.x_label + " _ " + analysis.data_info.y_label + ' Actual' + 'vs' + analysis.data_info.y_label + ' Predicted' + ".png"
            full_path = util.get_full_output_path(file_name)

            fig.savefig(full_path)

        plt.close(fig)


def scatter_plot_results(analysis, silent_mode_enabled=True):
    y_test = analysis.data_info.y_test
    y_pred = analysis.results_info.prediction
    x_test = analysis.data_info.x_test
    if y_test is not None and y_pred is not None:
        fig = plt.figure(figsize=(10, 10))
        plt.scatter(x_test, y_test, color='gray')
        plt.plot(x_test, y_pred, color='red', linewidth=2)
        plt.title(analysis.data_info.x_label + ' vs ' + analysis.data_info.y_label)
        plt.xlabel(analysis.data_info.x_label)
        plt.ylabel(analysis.data_info.y_label)
        if not silent_mode_enabled:
            plt.show()

        logger = LogManager.instance()
        if logger.debug_enabled():
            from my_package import util as util
            file_name = 'Scatter_Results_' + analysis.data_info.x_label + " _ " + analysis.data_info.y_label + ' Actual' + 'vs' + analysis.data_info.y_label + ' Predicted' + ".png"
            full_path = util.get_full_output_path(file_name)
            fig.savefig(full_path, dpi=fig.dpi, bbox_inches='tight', pad_inches=0.5)

        plt.close(fig)


def print_result(analysis):
    print("============= " + analysis.get_name() + " ===============")
    analysis.print()


def print_results(analysis_list):
    for analysis in analysis_list:
        print_result(analysis)


def print_smart_table(analysis_list, title):
    table = []
    header = ["Analysis Name", "eq_line", "Pearson_correlation_coefficient"]
    table.append(header)
    for analysis in analysis_list:
        row = [analysis.get_name(), analysis.results_info.get_eq_line(),
               str(analysis.results_info.Pearson_correlation_coefficient)]

        table.append(row)

    TableIt.printTable(table, title, useFieldNames=True, color=(26, 156, 171))


def print_regression_results(analysis_list, formated_enabled):
    table = []
    header = ["Analysis Name", "EV", "intercept", "coefficient", "PCC", "MSLE", "r2", "MAE", "MSE", "RMSE"]
    table.append(header)
    title = "results"

    for analysis in analysis_list:
        y_true = analysis.data_info.y_test
        y_pred = analysis.results_info.prediction
        if y_true is not None and y_pred is not None:
            # Regression metrics
            explained_variance = metrics.explained_variance_score(y_true, y_pred)
            mean_absolute_error = metrics.mean_absolute_error(y_true, y_pred)
            mse = metrics.mean_squared_error(y_true, y_pred)
            mean_squared_log_error = metrics.mean_squared_log_error(y_true, y_pred)
            median_absolute_error = metrics.median_absolute_error(y_true, y_pred)
            r2 = metrics.r2_score(y_true, y_pred)
            if formated_enabled:
                name = analysis.data_info.x_label + " vs " + analysis.data_info.y_label
                name = name.replace("City", "C.")
                name = name.replace("Museum", "M.")
                name = name.replace("Visitors", "V.")
                name = name.replace("Population", "P.")
                intercept = round(analysis.results_info.intercept[0], 4)
                coefficient = round(analysis.results_info.coefficient[0][0], 4)
                row = [name, str(round(explained_variance, 4)),
                       str(intercept), str(coefficient),
                       str(round(analysis.results_info.Pearson_correlation_coefficient, 4)),
                       str(round(mean_squared_log_error, 4)),
                       str(round(r2, 4)), str(round(mean_absolute_error, 4)),
                       str(round(mse, 4)), str(round(np.sqrt(mse), 4))]

                table.append(row)

            else:
                print("\n", analysis.data_info.x_label + ' vs ' + analysis.data_info.y_label)
                print('explained_variance: ', round(explained_variance, 4))
                print('mean_squared_log_error: ', round(mean_squared_log_error, 4))
                print('r2: ', round(r2, 4))
                print('MAE: ', round(mean_absolute_error, 4))
                print('MSE: ', round(mse, 4))
                print('RMSE: ', round(np.sqrt(mse), 4))

    if formated_enabled:
        table_in_string = TableIt.printTable(table, title, useFieldNames=True, color=(26, 156, 171))
        from my_package import util as util
        file_name = title + ".txt"
        full_path = util.get_full_output_path(file_name)
        text_file = open(full_path, "w", encoding="utf-8")
        text_file.write(table_in_string)
        text_file.close()


def plot_data_distribution(data, file_name, silent_mode_enabled=True):
    if silent_mode_enabled:
        return

    plt.figure(figsize=(15, 10))
    plt.tight_layout()
    seaborn_plot = seabornInstance.distplot(data)
    plt.show()

    logger = LogManager.instance()
    if logger.debug_enabled():
        full_path = util.get_full_output_path(file_name)
        fig = seaborn_plot.get_figure()
        fig.savefig(full_path)


def quantile_quantile_plot(data, silent_mode_enabled=True):
    if silent_mode_enabled:
        return

    stats.probplot(data, dist="norm", plot=pylab)
    pylab.show()


def residual_plot(analysis, silent_mode_enabled=True):
    x_train = analysis.data_info.x_train
    x_test = analysis.data_info.x_test
    y_train = analysis.data_info.x_train
    y_test = analysis.data_info.x_test
    model = analysis.results_info.model

    if x_train is not None and x_test is not None and \
            y_train is not None and y_test is not None and \
            model is not None:
        fig = plt.figure(figsize=(10, 10))
        plt.scatter(model.predict(x_train), model.predict(x_train) - y_train, color='blue', s=40, alpha=0.5)
        plt.scatter(model.predict(x_test), model.predict(x_test) - y_test, color='green', s=40)
        plt.hlines(y=0, xmin=0, xmax=9000000)
        plt.title(
            "Residual plot using training(blue) and test(green) data; " + analysis.data_info.x_label + ' vs ' + analysis.data_info.y_label)
        plt.ylabel("Residuals")
        if not silent_mode_enabled:
            plt.show()

        logger = LogManager.instance()
        if logger.debug_enabled():
            from my_package import util as util
            file_name = 'Residual_' + analysis.data_info.x_label + "_" + analysis.data_info.y_label + ".png"
            full_path = util.get_full_output_path(file_name)
            fig.savefig(full_path, dpi=fig.dpi, bbox_inches='tight', pad_inches=0.5)

        plt.close(fig)

def missingdata_plot(dataframe, silent_mode_enabled=True):
    museum_name = dataframe["museum"].tolist()  # ----------x-axis
    dataframe = dataframe.drop(columns=["museum", "id", "city_id"])  # ----------Independent Features
    features = dataframe.head()
    ##
    df_size = dataframe.shape
    missingdata_matrix = np.zeros(dataframe.shape)

    ##
    df = pd.isna(dataframe)
    df_array = df.to_numpy()
    for i in range(df_array.shape[0]):
        for j in range(df_array.shape[1]):
            if df_array[i][j]:
                missingdata_matrix[i][j] = int(0)
            else:
                missingdata_matrix[i][j] = int(1)
    missingdata_matrix = missingdata_matrix.T
    fig = plt.matshow(missingdata_matrix)
    plt.xlabel('Museum')
    plt.ylabel('Features')
    x = list(range(0, 46))
    y = list(range(0, 12))
    plt.yticks(y, features)
    plt.xticks(x, museum_name, rotation=90)
    plt.colorbar()

    if not silent_mode_enabled:
        plt.show()

    logger = LogManager.instance()
    if logger.debug_enabled():
        from my_package import util as util
        file_name = "missingdata.png"
        full_path = util.get_full_output_path(file_name)
        plt.savefig(full_path)

    plt.close()
