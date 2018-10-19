# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 12:36:30 2018

Description: Public version of the signal visualization tool

Last update: 
Version: 1.0
Author: ale.fcanosa@gmail.com
"""


import pandas as pd
import numpy as np
import os
import glob
from scipy.signal import savgol_filter
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_table_experiments as dt


cwd = os.getcwd()
files = glob.glob(os.path.join(cwd,"*.csv"))

def process_dataset(df):
    df = df.select_dtypes(include = ['float64', 'int'])
    if 'Time (abs)' in df.index:
        time = df['Time (abs)']
        time = time - time.iloc[0]
        Ts = round(max(time)/len(df),2)
    else:
        time = np.arange(0,len(df),1)
        Ts = 1
    return df, time, Ts

app = dash.Dash()
app.title = 'Public version - Signal Visualization Tool'

app.config['suppress_callback_exceptions']=False

# Boostrap CSS
app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

app.layout = html.Div([
       
    # Heading: Title, Logo, and author
    html.Div([
        # Title of the app
        html.Div([
            html.H1('Public version - Signal Visualization Tool', 
                style = {
                        'textAlign': 'center',
                        'fontSize': 30,
                        'fontWeight': 'bold',
                        'position': 'relative',
                        'padding-top': 12
                }
            ),
        ], className = 'eight columns'), 
        # Argonne National Laboratory Logo
        html.Div([
            html.Img(src = 'https://img.autobytel.com/car-reviews/autobytel/11694-good-looking-sports-cars/2016-Ford-Mustang-GT-burnout-red-tire-smoke.jpg',
                style = {
                    'textAlign': 'center',
                    'height': '30%',
                    'width': '30%',
                    'position': 'relative',
                    'padding-top': 12
                }
            ),            
        ], className = 'four columns'),   
    ], className = 'row'),

    # Signal detector - controls
    html.Div([
        html.Div([         
            # Signal detector for the main viz
            html.Div([   
                html.Div([
                    html.Label('Signals:'),
                    dcc.Dropdown(
                        id = 'signal_selector',
                        options = [{'label': None, 'value': None}],
                        value = (None,),
                        multi = True
                    ),                        
                ], className = 'nine columns'),
                html.Div([
                    html.Label('Path:'),
                    dcc.Input(
                        id = 'path_selector',
                        placeholder = 'Enter the path....',
                        type = 'text',
                        value = cwd,
                        style = {
                            'width': '700px',
                        }
                    ),                    
                ], className = 'three columns'),
            ], className = 'row'), 

                    
            # Rest of the controls: normalization and filtering
            # Normalize signals
            html.Div([ 
                html.Div([ 
                    html.Label('Normalized signals around 0:'),
                    dcc.RadioItems(
                        id = 'normalized',
                        options = [
                                {'label': 'Yes', 'value': 'norm'},
                                {'label': 'No', 'value': 'signal'}
                                ],
                        value = 'signal',
                        labelStyle={'display': 'inline-block'}
                    ),
                ], className = 'three columns'),
                
                # Filter signals
                html.Div([ 
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Label('Filtered signals:'),
                                dcc.RadioItems(
                                    id = 'filtered',
                                    options = [
                                            {'label': 'Yes', 'value': 'filt'},
                                            {'label': 'No', 'value': 'no_filt'}
                                            ],
                                    value = 'no_filt',
                                    labelStyle={'display': 'inline-block'}
                                ),
                            ], className = 'three columns'),
                            html.Div([
                                dcc.Input(
                                    id = 'filter',
                                    placeholder='Enter the length of the filter...',
                                    type = 'number',
                                    value = '',
                                    style = {
                                        'width': '300px',
                                        'position': 'absolute',
                                        'left': -20
                                    }
                                ),
                            ], 
                            style = {'position': 'relative',
                                     'padding-top': 5},
                            className = 'nine columns'),
                        ], className = 'row')
                    ], className = 'row'),     
                ], className = 'six columns'),
                                
                # Files selector              
                html.Div([
                    html.Label('Files:'),
                    dcc.Dropdown(
                        id = 'files_selector',
                        options = [{'label': os.path.basename(i), 'value': i} for i in files],
                        value = None,
                        multi = False,
                        style = {
                            'width': '700px',
                        }
                    ), 
                ], className = 'three columns'),  
            ], className = 'row'),                
        ], className = 'seven columns'),
    ], className = 'row'),
        
    # Main part of the app                         
    html.Div([
         # Signal visualizator
         html.Div([
            html.Div([
                dcc.Graph(id = 'graph-with-multiple-selection',
                          style = {'height': '500',
    #                     'width': '1200'
                         }
                    )
            ], className = 'row'),
             html.Div([
                 dcc.RangeSlider(
                    id = 'time-slider',
                    marks = {i: '{}'.format(i) for i in range(0, 100, 10)},
                    min = 0,
                    max = 100,
                    step = 1,
                    value = [0, 100]    
                )        
            ], className = 'row'),
        ], className = 'seven columns'),
        html.Div([               
            html.Div([
                html.Div([
                    html.Div([
                        html.Label('x Axis: '),
                        ], className = 'two columns'),
                    html.Div([
                        dcc.Dropdown(
                            id = 'x_axis',
                            options = [{'label': None, 'value': None}],
                                value = None,
                                style = {
                                'width': '300px',
                            }
                        ),
                    ], className = 'ten columns'),
                ], className = 'row'),
                html.Div([
                    html.Div([
                        html.Label('y Axis: '),
                    ], className = 'two columns'),
                    html.Div([
                        dcc.Dropdown(
                            id = 'y_axis',
                            options = [{'label': None, 'value': None}],
                                value = None,
                                style = {
                                'width': '300px',
                            }
                        )
                    ], className = 'ten columns'),
                ], className = 'row'),
            ], className = 'row'),
                 
            # Initialize plot relationships
            html.Div([
                dcc.Graph(id = 'graph-relations',
                    ),
            ], className = 'row')
                    
        ], className = 'five columns'),             
    ], className = 'row'),
           
    # Dynamic table with metrics
    html.Div([
        html.Div([
            html.Label('Metrics:',
                style = {
                    'textAlign': 'center',
                    'fontSize': 18,
                    'fontWeight': 'bold',
                    'fontColor': '#0000ff',
                    'position': 'relative',
                    'padding-top': 12
                }
            ),
            dt.DataTable(
                id = 'table_with_metrics',
                rows = [{'Signal': None,
                         'Mean': None,
                         'Max': None,
                         'Min': None,
                         'Std': None}],
                columns = ('Signal', 'Mean', 'Max', 'Min', 'Std'),
                sortable = True
            )
        ], className = 'seven columns'),
    ], className = 'row')

])

"""
Callbacks of the app: interactive part of the app
"""

@app.callback(
    dash.dependencies.Output('files_selector', 'options'),
    [dash.dependencies.Input('path_selector', 'value')])
def update_file_selector(pathname):
    path_sel = os.path.normpath(pathname)
    files = glob.glob(os.path.join(path_sel,"*.csv"))
    return [{'label': os.path.basename(i), 'value': i} for i in files]

@app.callback(
    dash.dependencies.Output('signal_selector', 'options'),
    [dash.dependencies.Input('files_selector', 'value')])
def update_options_signal_visualizator(filename):        
    df, time, Ts = process_dataset(pd.read_csv(filename))       
    return [{'label': i, 'value': i} for i in df.columns]

@app.callback(
    dash.dependencies.Output('x_axis', 'options'),
    [dash.dependencies.Input('files_selector', 'value')])
def update_options_x_axis(filename):        
    df, time, Ts = process_dataset(pd.read_csv(filename))       
    return [{'label': i, 'value': i} for i in df.columns]

@app.callback(
    dash.dependencies.Output('y_axis', 'options'),
    [dash.dependencies.Input('files_selector', 'value')])
def update_options_y_axis(filename):        
    df, time, Ts = process_dataset(pd.read_csv(filename))       
    return [{'label': i, 'value': i} for i in df.columns]

@app.callback(
    dash.dependencies.Output('time-slider', 'marks'),
    [dash.dependencies.Input('files_selector', 'value')])
def update_options_time_slider_marks(filename):        
    df, time, Ts = process_dataset(pd.read_csv(filename))       
    return {i: '{}'.format(i) for i in range(int(min(time)), int(max(time)), int((int(max(time)) - int(min(time)))/15))}

@app.callback(
    dash.dependencies.Output('time-slider', 'value'),
    [dash.dependencies.Input('files_selector', 'value')])
def update_options_time_slider_values(filename):        
    df, time, Ts = process_dataset(pd.read_csv(filename))       
    return [min(time), max(time)] 

@app.callback(
    dash.dependencies.Output('time-slider', 'min'),
    [dash.dependencies.Input('files_selector', 'value')])
def update_options_time_slider_min(filename):        
    df, time, Ts = process_dataset(pd.read_csv(filename))       
    return min(time)

@app.callback(
    dash.dependencies.Output('time-slider', 'max'),
    [dash.dependencies.Input('files_selector', 'value')])
def update_options_time_slider_max(filename):        
    df, time, Ts = process_dataset(pd.read_csv(filename))       
    return max(time)

@app.callback(
    dash.dependencies.Output('time-slider', 'step'),
    [dash.dependencies.Input('files_selector', 'value')])
def update_options_time_slider_step(filename):        
    df, time, Ts = process_dataset(pd.read_csv(filename))       
    return Ts

@app.callback(
    dash.dependencies.Output('graph-with-multiple-selection', 'figure'),
    [dash.dependencies.Input('signal_selector', 'value'),
     dash.dependencies.Input('normalized', 'value'),
     dash.dependencies.Input('filtered', 'value'),
     dash.dependencies.Input('filter', 'value'),
     dash.dependencies.Input('time-slider', 'value'),
     dash.dependencies.Input('files_selector', 'value')])
def update_figure(selected_signals, normalized, filtered, degree, time_range, filename):
    
    df, time, Ts = process_dataset(pd.read_csv(filename))
    
    time_sel = time[int(time_range[0]/Ts):int(time_range[1]/Ts)]
    filtered_df = df[selected_signals]
    filtered_df = filtered_df.iloc[int(time_range[0]/Ts):int(time_range[1]/Ts)]
    traces = []
    
    if selected_signals == None:
        pass
    
    if normalized == 'signal':
        for key in filtered_df:
            traces.append(go.Scatter(
                x = time_sel, 
                y = filtered_df[key],
                mode = 'lines',
                name = key
            )
        )
        if filtered == 'filt':
            if degree % 2 == 0:
                degree = degree + 1
            for key in filtered_df:
                traces.append(go.Scatter(
                        x = time_sel,
                        y = savgol_filter(filtered_df[key], degree, 0),
                        mode = 'lines',
                        name = 'filtered ' + key
                )
            )
        
    elif normalized == 'norm':
        for key in filtered_df:
            traces.append(go.Scatter(
                x = time_sel, 
                y = 2*(filtered_df[key] - filtered_df[key].min())/(filtered_df[key].max() - filtered_df[key].min()) - 1,
                mode = 'lines',
                name = key
            )
        )
        if filtered == 'filt':
            if degree % 2 == 0:
                degree = degree + 1
            for key in filtered_df:
                traces.append(go.Scatter(
                        x = time_sel,
                        y = savgol_filter(2*(filtered_df[key] - filtered_df[key].min())/(filtered_df[key].max() - filtered_df[key].min()) - 1, degree, 0),
                        mode = 'lines',
                        name = 'filtered ' + key
                )
            )
        
    return {
            'data': traces,
            'layout': go.Layout(
                title = 'Signals vs Time (sec)',
                titlefont=dict(
                    family = 'Times',
                    size = 20,
                    color = 'black'
                ),
                plot_bgcolor = '#e6e6e6',
                xaxis=dict(
                    title='Time (sec)',
                    titlefont=dict(
                        family = 'Times',
                        size = 18,
                        color = 'black'
                    )
                ),
                yaxis=dict(
                    title='Signals',
                    titlefont=dict(
                        family ='Times',
                        size = 18,
                        color='black'
                    )
                )
            )
        }
 
@app.callback(
    dash.dependencies.Output('table_with_metrics', 'rows'),
    [dash.dependencies.Input('signal_selector', 'value'),
     dash.dependencies.Input('files_selector', 'value')])
def update_table(selected_signals, filename):
    
    df = pd.read_csv(filename)
    df, time, Ts = process_dataset(df)
    
    if selected_signals == None:
        pass
    else:
        table_df = df[selected_signals]
        
        print([{'Signal': key,
                 'Mean': round(table_df[key].mean(),2),
                 'Max': round(table_df[key].max(),2),
                 'Min': round(table_df[key].min(),2),
                 'Std': round(table_df[key].std(),2)} for key in table_df])
        return [{'Signal': key,
                 'Mean': round(table_df[key].mean(),2),
                 'Max': round(table_df[key].max(),2),
                 'Min': round(table_df[key].min(),2),
                 'Std': round(table_df[key].std(),2)} for key in table_df]               
                
@app.callback(
    dash.dependencies.Output('graph-relations', 'figure'),
    [dash.dependencies.Input('x_axis', 'value'),
     dash.dependencies.Input('y_axis', 'value'),
     dash.dependencies.Input('time-slider', 'value'),
     dash.dependencies.Input('files_selector', 'value')])
def update_relations(x_axis, y_axis, time_range, filename):
    
    
    df = pd.read_csv(filename)
    df, time, Ts = process_dataset(df)
    
    if x_axis == None or y_axis == None:
        pass
    else:     
        df_time_filt = df.iloc[int(time_range[0]/Ts):int(time_range[1]/Ts)] 
        x = df_time_filt[x_axis]
        y = df_time_filt[y_axis]
        
        traces = []
        traces.append(go.Scatter(
            x = x,
            y = y,
            mode = 'markers',
            name = 'test',
        ))
        return {
            'data': traces,
            'layout': go.Layout(
                title = 'Signal 1 vs Signal 2',
                titlefont=dict(
                    family = 'Times',
                    size = 20,
                    color = 'black'
                ),
                plot_bgcolor = '#e6e6e6',
                xaxis=dict(
                    title=x_axis,
                    titlefont=dict(
                        family = 'Times',
                        size = 18,
                        color = 'black'
                    )
                ),
                yaxis=dict(
                    title=y_axis,
                    titlefont=dict(
                        family ='Times',
                        size = 18,
                        color='black'
                    )
                )
            )
        }


                

if __name__ == '__main__':
    app.run_server(debug=False)
    
    

    