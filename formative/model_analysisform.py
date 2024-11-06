"""
Plotting the convergence of tip deflection size based on seeding choices
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from scipy.interpolate import make_interp_spline

plt.rcParams.update({'font.size': 20})  # Set global font size


def process_data():
    ### Importing data ###
    df = pd.read_csv("/Users/aronfinkelstein/Documents/GitHub/FEAcoursework/formative/modelparams.csv")
    tip_deflections = df["Tip_Deflection"].dropna()
    global_size = df["Global_Size"].dropna()
    memory_used = df['memory_used'].dropna()
    analytical_values_m = df['Analytical_Solution'].dropna()
    number_elements = df["num_elements"].dropna()

    # creating data arrays
    number_elements = np.array(number_elements)
    tip_deflections = np.array(tip_deflections)
    memory_used = np.array(memory_used)
    tip_def_mm = [deflection*1000 for deflection in tip_deflections]
    analytical_values = [deflection*1000 for deflection in analytical_values_m]

    print(number_elements)
    return number_elements, tip_def_mm, analytical_values, memory_used

def plot_data_graph(number_elements, tip_def_mm, analytical_values,memory_used):
    fig, ax1 = plt.subplots()

    # Plot tip deflection on the left y-axis
    ax1.scatter(number_elements, tip_def_mm, label='Tip Deflection Data Points', color='blue')
    ax1.plot(number_elements, tip_def_mm, label='Tip Deflection Curve', color='blue')
    ax1.set_xlabel('Number of Elements')
    ax1.set_ylabel('Tip Deflection (mm)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')  # Set the color of the y-axis labels to match the data color

    # Create a second y-axis that shares the same x-axis (for memory usage)
    ax2 = ax1.twinx()
    ax2.scatter(number_elements, memory_used, label='Memory Usage Data Points', color='green')
    ax2.plot(number_elements, memory_used, label='Memory Usage Curve', color='green')
    ax2.set_ylabel('Memory Usage (MB)', color='green')
    ax2.tick_params(axis='y', labelcolor='green')  # Set the color of the y-axis labels to match the data color

    # Plot the analytical values on the first axis
    ax1.plot(number_elements, analytical_values, color='red', linestyle='--', label='Calculated Value')

    # Combine the legends from both axes    
    fig.legend(loc='lower right', bbox_to_anchor=(1, 0), bbox_transform=ax1.transAxes)

    # Set the title
    plt.title('Number of Elements vs Tip Deflection and Memory Usage')

    # Show the plot
    plt.show()

def plot_difference(number_elements, tip_def_mm): 
    actual_differences = [abs(tip_def_mm[i] - tip_def_mm[i-1]) for i in range(1, len(tip_def_mm))]
    percentage_differences = [(abs(tip_def_mm[i] - tip_def_mm[i-1]) / tip_def_mm[i-1]) * 100 for i in range(1, len(tip_def_mm))]
    number_elements_diff = number_elements[1:]
    
    plt.plot(number_elements_diff, actual_differences, label = 'Absolute Difference')
    plt.scatter(number_elements_diff, actual_differences, label = 'Data Points')
    # plt.plot(number_elements_diff, percentage_differences, label = 'Percentage Absolute Difference')
    plt.legend()
    plt.show()

def plot_error_percent(number_elements, tip_def_mm, analytical_values):
    percentage_errors = []
    i = 0
    for deflection in tip_def_mm:
        percentage_error = (abs(deflection - analytical_values[i]) /deflection )* 100
        percentage_errors.append(round(percentage_error,4))
        i+=1
    
    plt.plot(number_elements, percentage_errors)
    plt.scatter(number_elements, percentage_errors)
    plt.title("Number of Elements in Model vs Error Between Analytical and FEA result")
    plt.xlabel("Number of Elements")
    plt.ylabel("Percentage Error between Analaytical Calculation and FEA (%)")
    plt.show()


def main():
    number_elements, tip_def_mm, analytical_values, memory_used = process_data()
    
    graph_choice = input("Choose graph, (1) for data, (2) for convergence:")

    if graph_choice == "1":
        plot_data_graph(number_elements, tip_def_mm, analytical_values, memory_used)
    
    if graph_choice == "2":
        plot_error_percent(number_elements, tip_def_mm, analytical_values)

if __name__ == "__main__":
    main()