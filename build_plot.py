import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import plotly.graph_objects as go

def build_px_plot(graph1, graph2, v, vehicle):
    graph1_ax = graph1[0]
    graph1_y = graph1[1]

    graph2_ax = graph2[0]
    graph2_y = graph2[1]

    graph1_df = pd.DataFrame({'ax': graph1_ax, 'y': graph1_y, 'origin': ['graph1']*len(graph1_ax)})
    graph2_df = pd.DataFrame({'ax': graph2_ax, 'y': graph2_y, 'origin': ['graph2']*len(graph2_ax)})

    df = pd.concat([graph1_df, graph2_df])

    fig = px.scatter(df, x='ax', y='y', color='origin', title='{} at {} m/s'.format(vehicle.car_params['vehicleName'], v))
    
    return fig

def build_px_smooth(graph1, graph2, v, vehicle):
    graph1_ax = graph1[0]
    graph1_y = graph1[1]

    graph2_ax = graph2[0]
    graph2_y = graph2[1]

    graph1_df = pd.DataFrame({'ax': graph1_ax, 'y': graph1_y, 'origin': ['graph1']*len(graph1_ax)})
    graph2_df = pd.DataFrame({'ax': graph2_ax, 'y': graph2_y, 'origin': ['graph2']*len(graph2_ax)})

    df = pd.concat([graph1_df, graph2_df])

    fig = go.Figure()

    # graph 1 traces
    fig.add_trace(go.Scatter(x=graph1_ax, y=graph1_y, name='spline1',
                             line_shape='spline'))

    # graph 2 trace
    fig.add_trace(go.Scatter(x=graph2_ax, y=graph2_y, name='spline2',
                             line_shape='spline'))

    return fig


def build_plt_plot(graph1, graph2, v, vehicle): 
    graph1_ax = np.array(graph1[0])
    graph1_y = np.array(graph1[1])

    graph2_ax = np.array(graph2[0])
    graph2_y = np.array(graph2[1])

    graph1_df = pd.DataFrame({'ax': graph1_ax, 'y': graph1_y, 'origin': ['graph1']*len(graph1_ax)})
    graph2_df = pd.DataFrame({'ax': graph2_ax, 'y': graph2_y, 'origin': ['graph2']*len(graph2_ax)})

    df = pd.concat([graph1_df, graph2_df])

    idx = np.argsort(graph1_ax)

    graph1_ax = graph1_ax[idx]
    graph1_y = graph1_y[idx]

    idx2 = np.argsort(graph2_ax)
    graph2_ax = graph2_ax[idx2]
    graph2_y = graph2_y[idx2]

    graph1_ax_smooth = np.linspace(graph1_ax[0], graph1_ax[-1], 300)
    graph2_ax_smooth = np.linspace(graph2_ax[0], graph2_ax[-1], 300)

    graph1_y_smooth = make_interp_spline(graph1_ax, graph1_y)(graph1_ax_smooth)
    graph2_y_smooth = make_interp_spline(graph2_ax, graph2_y)(graph2_ax_smooth)

    fig, ax = plt.subplots()

    # ax.scatter(graph1_ax, graph1_y, label='Graph 1', s=3, alpha=0.5)
    # ax.scatter(graph2_ax, graph2_y, label='Graph 2', s=3, alpha=0.5)
    
    # ax.plot(graph1_ax, graph1_y, 'o')
    # ax.plot(graph2_ax, graph2_y, 'o')
    ax.plot(graph1_ax, graph1_y, label='Graph 1', alpha=0.3)
    ax.plot(graph2_ax, graph2_y, label='Graph 2', alpha=1)

    ax.set_xlabel("lateral acceleration Ay")
    ax.set_ylabel("yaw")
    ax.legend()
    ax.grid(True)
    return fig, ax

# CURRENT WORKING FUNCTION
def build_plot(graph_df, velocity, chosen_colors):
    # use plolty traces to build up the plot
    fig = go.Figure()

    # graph 1 first
    graph1_subset = graph_df[graph_df['graph_num'] == 1]
    unique_delta1 = list(graph1_subset['delta'].unique())
    unique_beta1 = list(graph1_subset['beta'].unique())
    
    if chosen_colors[0] is None:
        graph1_color = 'blue'
    else:
        graph1_color = chosen_colors[0]

    if chosen_colors[1] is None:
        graph2_color = 'red'
    else:
        graph2_color = chosen_colors[1]

    # should be auto sorted since we were interating through a for loop
    for delta in unique_delta1:
        delta_subset = graph1_subset[graph1_subset['delta'] == delta]
        fig.add_trace(go.Scatter(x=delta_subset['ay'], y=delta_subset['yaw'],
                                 mode='lines',
                                 marker=dict(color=graph1_color),
                                 line_shape='spline',
                                 showlegend=False))
    
    # graph 2

    graph2_subset = graph_df[graph_df['graph_num'] == 2]
    unique_delta2 = list(graph2_subset['delta'].unique())
    unique_beta2 = list(graph2_subset['beta'].unique())
    
    # should be auto sorted since we were interating through a for loop
    for beta in unique_beta2:
        beta_subset = graph2_subset[graph2_subset['beta'] == beta]
        fig.add_trace(go.Scatter(x=beta_subset['ay'], y=beta_subset['yaw'],
                                 mode='lines',
                                 marker=dict(color=graph2_color),
                                 line_shape='spline',
                                 showlegend=False))
    return fig

def add_plot_trace(current_fig, graph_df, velocity, chosen_colors):
    fig = current_fig
    graph1_subset = graph_df[graph_df['graph_num'] == 1]
    unique_delta1 = list(graph1_subset['delta'].unique())
    unique_beta1 = list(graph1_subset['beta'].unique())
   
    
    if chosen_colors[0] is None:
        graph1_color = 'blue'
    else:
        graph1_color = chosen_colors[0]

    if chosen_colors[1] is None:
        graph2_color = 'red'
    else:
        graph2_color = chosen_colors[1]

    for delta in unique_delta1:
        delta_subset = graph1_subset[graph1_subset['delta'] == delta]
        fig.add_trace(go.Scatter(x=delta_subset['ay'], y=delta_subset['yaw'],
                                 mode='lines',
                                 marker=dict(color=graph1_color),
                                 line_shape='spline',
                                 showlegend=False))
    
    graph2_subset = graph_df[graph_df['graph_num'] == 2]
    unique_delta2 = list(graph2_subset['delta'].unique())
    unique_beta2 = list(graph2_subset['beta'].unique())
    
    # should be auto sorted since we were interating through a for loop
    for beta in unique_beta2:
        beta_subset = graph2_subset[graph2_subset['beta'] == beta]
        fig.add_trace(go.Scatter(x=beta_subset['ay'], y=beta_subset['yaw'],
                                 mode='lines',
                                 marker=dict(color=graph2_color),
                                 line_shape='spline',
                                 showlegend=False))
    return fig 
