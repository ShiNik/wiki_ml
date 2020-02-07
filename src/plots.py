#user define imports

#python imports
import numpy as np
import matplotlib.pyplot as plt

def get_plot_size(num_items):
    num_col = 2
    num_row = int(np.ceil(num_items / num_col))
    return {"row_size": num_row, "col_size": num_col}


def scatter_plots(analysis_list, plot_title):
    plot_size = get_plot_size(len(analysis_list))

    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(plot_size["row_size"], plot_size["col_size"], figsize=(10, 10),
                            gridspec_kw={'wspace': 0.2, 'hspace': 0.55})
    fig.suptitle(plot_title, fontsize=15)
    axs = axs.flatten()
    for analysis, ax in zip(analysis_list, axs):
        x_value = analysis.data_info.x_values
        y_value = analysis.data_info.y_values
        x_title = analysis.data_info.x_label
        y_titel = analysis.data_info.y_label
        intercept = analysis.results_info.intercept
        coef = analysis.results_info.coef
        analysis_type = analysis.type

        ax.scatter(x_value, y_value, color='r')
        ax.set_title(analysis_type, size=10, color="g")
        ax.set_xlabel(x_title, size=7, color="y")
        ax.set_ylabel(y_titel, size=7, color="y")

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
    plt.show()


