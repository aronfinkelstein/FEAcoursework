"""
Plotting the convergence of tip deflection size based on seeding choices
"""
print("beginning program")
import time
start = time.time()
import matplotlib.pyplot as plt
print(f"matplotlib imported in {time.time() - start:.4f} seconds")
start = time.time()
import numpy as np
print(f"numpy imported in {time.time() - start:.4f} seconds")
start = time.time()
import pandas as pd
print(f"matplotlib imported in {time.time() - start:.4f} seconds")
import math


def process_data():
    '''
    Process Data from the mesh convergence study
    '''
    print("processing data")
    df = pd.read_csv("/Users/aronfinkelstein/Documents/GitHub/FEAcoursework/summative/modelparams.csv")
    mesh_type = df["CSType"].unique()
    geom_orders = df["Geom_Order"].unique()

    separated_data = {mesh: {geom: {'seed_size': [], 'stress': [], 'deflection': []}
                                for geom in geom_orders}
                        for mesh in mesh_type}

    for index, row in df.iterrows():
        cstype = row['CSType']
        geom_order = row['Geom_Order']
        
        separated_data[cstype][geom_order]['seed_size'].append(row['Global_Size'])
        separated_data[cstype][geom_order]['stress'].append(row['Max_Mises_Stress'])
        separated_data[cstype][geom_order]['deflection'].append(row['Max_Deflection'])

    # Convert lists to numpy arrays for each entry
    for mesh in separated_data:
        for geom in separated_data[mesh]:
            separated_data[mesh][geom]['seed_size'] = np.array(separated_data[mesh][geom]['seed_size'])
            separated_data[mesh][geom]['stress'] = np.array(separated_data[mesh][geom]['stress'])
            separated_data[mesh][geom]['deflection'] = np.array(separated_data[mesh][geom]['deflection'])

    return separated_data


def plot_data(separated_data: dict):
    '''
    Plot deflection against seed size for each CSType, with line style based on Geometric_Order
    '''
    plt.figure(figsize=(10, 6))
    line_styles = {'Linear': 'solid', 'Quadratic': 'dotted'}
    plotted_geom_orders = set()  # Track plotted orders for legend purposes

    for cstype, geom_data in separated_data.items():
        for geom_order, data in geom_data.items():
            if len(data['seed_size']) > 0:
                # Normalize and transform seed size for plotting
                relative_seed_sizes = data['seed_size'] / np.max(data['seed_size'])
                transformed_seed_sizes = np.sqrt(relative_seed_sizes)

                # Plot each combination with the specified line style
                line_style = line_styles.get(geom_order, 'solid')
                plt.plot(transformed_seed_sizes, data['deflection'], label=f"{cstype} - {geom_order}",
                         linestyle=line_style, marker='o', markersize=5)

                # Only add each geom_order once for the legend
                if geom_order not in plotted_geom_orders:
                    plt.plot([], [], label=geom_order, linestyle=line_style, color='black')  # Dummy plot for legend
                    plotted_geom_orders.add(geom_order)

    plt.xscale('log')
    plt.gca().invert_xaxis()
    plt.xlabel('Relative Seed Size (Normalized)')
    plt.ylabel('Max Deflection (Max_Deflection)')
    plt.title('Mesh Convergence for Lug with 1MPa applied Pressure')
    plt.legend()
    plt.grid()
    plt.show()
    plt.xscale('log')
    plt.gca().invert_xaxis()

def main():
    plot_data(process_data())

if __name__ == "__main__":
    main()