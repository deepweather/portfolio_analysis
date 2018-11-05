import matplotlib.pyplot as plt
import numpy as np

import os
from datetime import datetime
import pandas as pd
import alpha_vantage as av


tickers = ['VUSTX', 'VISVX']
start_date = datetime(1999,1,1)
end_date = datetime.today()

#pull financial data from aplha vantage
data = av.pull_data_from_av(tickers, "av-monthly-adjusted", start_date, end_date)
table = av.clean_table(data)

#Download data to CSV file for offline analysis
table.to_csv('Data/out.csv', sep=';')

# set the number of portfolios to be simluated
num_of_portfolios = 500


#Simulation of portfolios
results_frame = av.simulation_without_active_management(table, num_of_portfolios, tickers)

#find special portfolios and print weights
max_sharpe_port = results_frame.iloc[results_frame['sharpe'].idxmax()]
min_vol_port = results_frame.iloc[results_frame['stdev'].idxmin()]
max_return = results_frame.iloc[results_frame['returns'].idxmax()]

print max_sharpe_port
print min_vol_port
print max_return

#create scatter plot coloured by Sharpe Ratio
plt.scatter(results_frame.stdev,results_frame.returns,c=results_frame.sharpe,cmap='RdYlBu')
plt.xlabel('Volatility')
plt.ylabel('Returns')
plt.colorbar()
plt.grid(color='b', linestyle='-')
#plot red star to highlight position of portfolio with highest Sharpe Ratio
plt.scatter(max_sharpe_port[1],max_sharpe_port[0],marker=(5,1,0),color='r',s=200)
#plot green star to highlight position of minimum variance portfolio
plt.scatter(min_vol_port[1],min_vol_port[0],marker=(5,1,0),color='b',s=200)
plt.scatter(max_return[1],max_return[0],marker=(5,1,0),color='g',s=200)
plt.show()
