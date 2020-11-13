import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime
import pandas as pd
import alphavantage as av
import streamlit as st
import time


def do_portfolio_analysis(tickers, start_date, end_date, num_of_portfolios):

    #pull financial data from aplha vantage
    data = av.pull_data_from_av(tickers, "av-monthly-adjusted", start_date, end_date)
    table = av.clean_table(data)

    #Download data to CSV file for offline analysis
    table.to_csv('data/out.csv', sep=';')

    #Simulation of portfolios
    results_frame = av.simulation_without_active_management(table, num_of_portfolios, tickers)

    #find special portfolios and print weights
    max_sharpe_port = results_frame.iloc[results_frame['sharpe'].idxmax()]
    min_vol_port = results_frame.iloc[results_frame['stdev'].idxmin()]
    max_return = results_frame.iloc[results_frame['returns'].idxmax()]

    #print("\nMax Sharpe ratio\n",max_sharpe_port,"\n")
    #print("\nMax Volatility ratio\n",min_vol_port,"\n")
    #print("\nMax return ratio\n",max_return,"\n")

    plt.suptitle("Portfolio analysis")
    plt.title(str(tickers), fontdict = {'fontsize' : 10})
    plt.scatter(results_frame.stdev,results_frame.returns,c=results_frame.sharpe,cmap='RdYlBu')
    plt.xlabel('Volatility')
    plt.ylabel('Returns')
    plt.colorbar()
    plt.grid(color='b', linestyle='-')

    #plot markers
    sharpe_marker = plt.scatter(max_sharpe_port[1],max_sharpe_port[0],marker="x",color='r',s=200)
    vol_marker = plt.scatter(min_vol_port[1],min_vol_port[0],marker="x",color='b',s=200)
    return_marker = plt.scatter(max_return[1],max_return[0],marker="x",color='g',s=200)
    plt.legend((sharpe_marker, vol_marker, return_marker),("Max sharpe ratio","Min volatility", "Max returns"))
    fig = plt.gcf()
    plt.savefig("test.png")
    return fig, max_sharpe_port, max_return, min_vol_port



def main():
    
    # create local data
    if not os.path.exists("data"):
        os.mkdir("data")

    st.title("Portfolio analysis application")
    st.header("Calculates optimum portfolio allocation")
    user_input = st.text_input("Comma seperated stock ticker symbols", "")
    num_of_simulations = st.text_input("Number of simulations to run", 5000)
    start_date = st.date_input('Ignore stocks before', datetime(1999,1,1))
    end_date = st.date_input('Ignore stocks after', datetime.today())

    if st.button("Start analysis"):
        if user_input != "":
            user_input = user_input.split(",")
            st.write("Starting analysis for", str(user_input))
            st.write("Estimated time for completion:", len(user_input)*15, "seconds.")
            start = time.time()
            fig,sharpe,max_return,min_vol = do_portfolio_analysis(user_input, start_date,
                                                    end_date, int(num_of_simulations))
            st.write("Done, took" ,time.time()-start, "seconds.")
            st.title("Allocation in portfolio")
            col1, col2, col3 = st.beta_columns(3)
            col1.write("Highest sharpe ratio")
            col1.write(sharpe)
            col2.write("Maximum Return")
            col2.write(max_return)
            col3.write("Minimum Volatility")
            col3.write(min_vol)
            st.write(fig)

if __name__ == "__main__":
    main()