import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.ticker as tick
import time
pd.options.mode.chained_assignment = None  # default='warn'
from scipy.signal import savgol_filter


phases = ['rhexis', 'phaco', 'cortex', 'core_vitr', 'memb_peel', 'laser']
pd.set_option("display.max_rows", None, "display.max_columns", None)
pd.options.display.width = None

df = pd.read_csv(r'all_experts_one_sheet_gaze_paper.csv')

fig,ax = plt.subplots(2)


def main():
    # Filter by user here if desired
    for i in range(11):
        df_gaze = df.query('user == ' + str(i+1))

        # To plot the gaze path of each user:
        ax.plot(df_gaze.x, df_gaze.y, label = 'Surgeon ' + str(i+1))
        # To plot the variantion in speed for each user:
        ax.plot((df_gaze.frame)/60, df_gaze.dist, label = i+1)


        #to plot changes in x/y
        x = savgol_filter(df_gaze.x, 55, 2)
        y = savgol_filter(df_gaze.y, 55, 2)
        ax[0].plot((df_gaze.frame)/60, x, label = 'Surgeon: ' + str(i+1))
        ax[1].plot((df_gaze.frame)/60, y, label = 'Surgeon: ' + str(i+1))


        # Plot the heatmap of gaze attention
        plt.hist2d(df_gaze.x, df_gaze.y,
                   bins=300,
                   norm=colors.LogNorm(),
                   cmap="RdYlGn_r")


    formatter = tick.FuncFormatter(lambda ms, x: time.strftime('%M:%S', time.gmtime(ms)))
    ax[0].xaxis.set_major_formatter(formatter)
    ax[1].xaxis.set_major_formatter(formatter)
    ax[0].set_title('Gaze behavior of all participants - x axis')
    ax[1].set_title('Gaze behavior of all participants - y axis')
    ax[0].legend(fancybox=True, shadow=True)

    # Optional - To select individual surgeons from the legend
    lines = ax.get_lines()
    leg = ax.legend(fancybox=True, shadow=True)
    lined = {}  # Will map legend lines to original lines.
    for legline, origline in zip(leg.get_lines(), lines):
        legline.set_picker(True)  # Enable picking on the legend line.
        lined[legline] = origline
    
    def on_pick(event):
        # On the pick event, find the original line corresponding to the legend
        # proxy line, and toggle its visibility.
        legline = event.artist
        origline = lined[legline]
        visible = not origline.get_visible()
        origline.set_visible(visible)
        # Change the alpha on the line in the legend so we can see what lines
        # have been toggled.
        legline.set_alpha(1.0 if visible else 0.2)
        fig.canvas.draw()
    
    fig.canvas.mpl_connect('pick_event', on_pick)

    plt.show()


if __name__ == "__main__":
    main()

