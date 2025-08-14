import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from market_overview.funcs import title_to_filename

colors = [
    '#E74C3C',  # Red
    '#3498DB',  # Blue  
    '#2ECC71',  # Green
    '#F39C12',  # Orange
    '#9B59B6',  # Purple
    '#1ABC9C',  # Teal
    '#E67E22',  # Dark Orange
    '#cccccc',  # Light Gray
    '#F1C40F',  # Golden Yellow
    '#E91E63',  # Pink
    '#8E44AD'   # Dark Purple
]

line_styles = ['-', '--', '-.', ':', '-', '--', '-.', ':', '-', '--', '-.']
markers = ['o', 's', '^', 'D', 'v', 'p', '*', 'h', 'H', '+', 'x']

def multi_line_chart(title: str, path: str, png: str, period: int | None=None,  show: bool=True) -> None:
    """
    args:
        title : title of chart
        path : csv file path
        png : png file path
        period : lookback
    """
    # path check
    if path[-1] != '/' or png[-1] != '/':
        raise ValueError("Path must end with '/'")

    plt.figure(figsize=(12, 8), facecolor='black')
    plt.style.use('dark_background')
    plt.title(title)

    for i, file in enumerate(os.listdir(path)):
        name = file[:-4]
        df = pd.read_csv(f'{path}{file}')

        # Normalize
        df['Close'] = ((df['Close'] / df['Close'].iloc[0]) - 1) * 100

        if period != None:
            df = df.tail(period)

        if name == 'SPY':
            plt.plot(df.Date, df['Close'],
                    label=name,
                    color='white',
                    linestyle=':',
                    linewidth=3,
                    marker='x',
                )

        else:
            plt.plot(df.Date, df['Close'], 
                    label=name, 
                    color=colors[i-1], 
                    linestyle=line_styles[i-1], 
                    linewidth=1,
                    marker=markers[i-1],
                    markersize=4, 
                    markevery=10, 
                    alpha=0.85) 

    plt.legend(loc='upper left')

    if period == None:
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())

    plt.xticks(rotation=45)

    if show == True:
        plt.show()

    filename_str = title_to_filename(title)
    plt.savefig(f'{png}{filename_str}.png')