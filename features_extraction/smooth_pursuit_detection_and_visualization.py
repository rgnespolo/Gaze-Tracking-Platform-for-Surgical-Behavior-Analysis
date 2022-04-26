import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
import time
pd.options.mode.chained_assignment = None  # default='warn'
from scipy.signal import savgol_filter

subspecialty = ['retina', 'cataract', 'other']
subspecialty_user = [1, 1, 1, 1, 3, 2]
years_oph = [20, 4, 4, 8, 7, 4]
years_sub = [10, 1, 1, 2, 2, 1]
phases = ['rhexis', 'phaco', 'cortex', 'core_vitr', 'memb_peel', 'laser']
attendings = [1,2,9]
residents = [4,5,6]
fellows = [3,7,8,10,11]

pd.set_option("display.max_rows", None, "display.max_columns", None)
pd.options.display.width = None

df = pd.read_csv(r'all_experts_one_sheet_gaze_paper.csv')
df_tooltip = pd.read_csv(r'detections_vitrector_gaze_paper.csv', usecols=['frame_tooltip','x_tooltip', 'y_tooltip'])
# detections_vitrector_gaze_paper detections_membranectomy_gaze_paper detections_endolaser_gaze_paper


fig,ax = plt.subplots()

def main():
    # select user here
    for i in range(1):
        df_gaze = df.query('phase == 4 & user == ' + str(i+1))
        # add column to match frame from df_gaze with frame with tooltip detections
        df_gaze.insert(loc=0, column='frame_gaze_per_user', value=np.arange(len(df_gaze)))
        #sync frame of gaze with frame of detection
        df_merged = df_gaze.set_index('frame_gaze_per_user').join(df_tooltip.set_index('frame_tooltip'))
        df_merged_notna = df_merged[df_merged['x_tooltip'].notna()]
        df_merged_notna['l2_dist_gaze_tooltip'] = df_merged_notna.apply(
            lambda row: (np.sqrt(((row.x-row.x_tooltip)**2 + (row.y-row.y_tooltip)**2))), axis=1)
        #speed of tooltip
        df_merged_notna['prev_x_tooltip'] = df_merged_notna['x_tooltip'].shift()
        df_merged_notna['prev_y_tooltip'] = df_merged_notna['y_tooltip'].shift()
        df_merged_notna['dist_tooltip'] = df_merged_notna.apply(
            lambda row: (np.sqrt(((row.x_tooltip-row.prev_x_tooltip)**2 + (row.y_tooltip-row.prev_y_tooltip)**2))), axis=1)
        #is overlap when <130 (3 degree)
        df_merged_notna['is_overlap'] = df_merged_notna.apply(
            lambda row: (np.sqrt(((row.x-row.x_tooltip)**2 + (row.y-row.y_tooltip)**2)) < 130), axis=1) #add condition for true or false ie < 130

        df_merged_notna = df_merged_notna.astype(float)
        #convert to seconds
        df_merged_notna['frame'] = df_merged_notna['frame'].div(60)
        #filtered
        w = savgol_filter(df_merged_notna.l2_dist_gaze_tooltip, 55, 2)
        #surgeon gaze
        ax.plot(df_merged_notna.frame, w, label= 'Surgeon 1 - Distance to tooltip')


        # # #speed of gaze movement per frame
        # ax.plot((df_merged_notna.frame), df_merged_notna.dist, label = 'Speed of gaze')
        # ax.plot((df_merged_notna.frame), df_merged_notna.dist_tooltip, label = 'tooltip_speed')


        #speed of gaze movement - sliding window 100ms
        df_merged_notna['rolling_speed_gaze'] = df_merged_notna['dist'].rolling(60).mean()
        df_merged_notna['rolling_speed_tooltip'] = df_merged_notna['dist_tooltip'].rolling(60).mean()
        ax.plot((df_merged_notna.frame), df_merged_notna.rolling_speed_gaze, label = 'Speed of gaze - px/s')
        ax.plot((df_merged_notna.frame), df_merged_notna.rolling_speed_tooltip, label = 'Speed of tooltip - px/s')


        #surgeon gaze
        #identifying potential smooth pursuit when speed of gaze < 72px/frame or 100 deg/s
        df_merged_notna['potential_pursuit'] = np.where((df_merged_notna.dist < 72) &
                                                        # (df_merged_notna.rolling_speed_tooltip > 1) &
                                                        # (df_merged_notna.rolling_speed_gaze > 1) &
                                                        (df_merged_notna.is_overlap == True), -20, 0)

        df_merged_notna['potential_pursuit'].replace(0, np.nan, inplace=True)
        ax.scatter(df_merged_notna.frame, df_merged_notna.potential_pursuit, label = 'Potential smooth pursuit')





        #
        # #speed of tooltip
        #ax.plot((df_merged_notna.frame), df_merged_notna.x_tooltip)
    # line
    print(df_merged_notna.head(10))
    plt.axhline(y=130, color='r', linestyle='-', label = 'Overlap w/ tooltip - threshold')
    plt.axhline(y=72, color='b', linestyle='-', label = 'Smooth pursuit threshold')
    #plt.axhline(y=433, color='b', linestyle='-', label = 'Smooth pursuit threshold (433 px/s)')

    #plt.title('Distance to AoI - Vitrector tooltip')
    plt.title('Identification of smooth pursuit movements - Core vitrectomy', fontsize = 22, fontweight = 'bold')
    plt.rcParams.update({'font.size': 15})
    formatter = tick.FuncFormatter(lambda ms, x: time.strftime('%M:%S', time.gmtime(ms)))
    ax.xaxis.set_major_formatter(formatter)

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
    plt.ylabel('Pixels', fontsize = 18)
    plt.xlabel('Time (mm:ss)', fontsize = 18)
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=15)

    plt.show()


if __name__ == "__main__":
    main()

