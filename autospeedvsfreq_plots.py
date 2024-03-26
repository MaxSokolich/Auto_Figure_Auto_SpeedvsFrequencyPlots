import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statistics

filename = "cellbotspeedvsfreqdata/6botcellbot7.xlsx"
trim_factor = 1

xlsx = pd.ExcelFile(filename)

# Get the sheet names
sheet_names = xlsx.sheet_names

# Iterate over each sheet and read it into a DataFrame
dfs = []
for sheet_name in sheet_names:
    df = pd.read_excel(filename, sheet_name=sheet_name)
    dfs.append(df)

magneticfield_df = dfs.pop(0)
rolling_freq = magneticfield_df["Rolling Frequency"]
plot_freq = []
for freq in rolling_freq:
    if freq != 0:
        plot_freq.append(freq)
plot_freq = list(set(plot_freq)) 

print(plot_freq)

my_data = {}
my_data["freq"] = plot_freq


for robot_index in range(len(dfs)):
#######
    robot = dfs[robot_index]
    robot_vel = robot["Vel Mag"]
    robot_vel_length = len(robot_vel)
 

    FINAL_VEL = []

    counter = 0
    for f in range(len(plot_freq)):  #loop through every frequency that was used
        current_speed_list_to_be_averaged = []
     
        for j in range(robot_vel_length):  #loop through each rows in robot velocity data
            freq = rolling_freq[j]
            vel = robot_vel[j]
       

            if freq == 0:
                counter = 0

            if freq == plot_freq[f]:
                counter +=1
                if counter > trim_factor:
                    current_speed_list_to_be_averaged.append(vel)
                    
        
        #now average it
        
        current_speed_list_to_be_averaged = current_speed_list_to_be_averaged[:-trim_factor]
        average_vel = statistics.mean(current_speed_list_to_be_averaged)    
        FINAL_VEL.append(average_vel)
        
    my_data["robot {} avg".format(robot_index+1)] = FINAL_VEL



individual_robot_average_vel_dataframe = pd.DataFrame(my_data)
individual_robot_average_vel_dataframe.to_excel('outputdata.xlsx', index=False) 





#plot output dataframe after grouping and analyzing file
df = pd.read_excel("6botcellbot_total.xlsx")



row_freq = df.iloc[:,0]
row_means = df.iloc[:, 1:].mean(axis=1)
row_std = df.iloc[:, 1:].std(axis=1)


coefficients = np.polyfit(row_freq, row_means, 1)
p = np.poly1d(coefficients)
equation = f'v = {coefficients[0]:.2f}f + {coefficients[1]:.2f}'

#plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
ax1.plot(row_freq, p(row_freq), color = "r", label = "linear fit")
ax1.errorbar(row_freq, row_means, yerr = row_std, fmt='-o', capsize = 5)
ax1.set_xlabel("frequency")
ax1.set_ylabel("velocity (um/s)")
ax1.set_title(f'Linear Curve Fitting\n{equation}')


for bot in df.columns[1:]:
    ax2.plot(row_freq, df[bot], label=str(bot), marker = "*")

ax2.set_xlabel("frequency")
ax2.set_ylabel("velocity (um/s)")
ax2.legend()
ax2.set_title("6 Bot Cellbot Speed (um/s) vs Rotating Magnetic Field Frequency")
    

plt.show()


xlsx.close()


