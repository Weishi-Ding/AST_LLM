# -*- coding: utf-8 -*-
"""main.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DvHi0b21l_trIid5ShtB-9iuWK0T5t9v
"""

# %load_ext autoreload
# %autoreload 2
# %autosave 180
# from google.colab import drive
# drive.mount('/content/drive')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from torch.nn import Sequential
from torch.utils.data import Dataset, DataLoader
from torch.optim import optimizer
from collections import namedtuple
import math
import os

# sys.path.append("/content/drive/MyDrive/cs138")

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print(device)

gamma = 0.9
num_episode = 100
target_update = 3
lr = 0.001
epsilon = 0.1
batch_size = 256
# action_space = [-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75 ,1]
action_space = [-1, 0.25, 0.5,0.75, 1]
# action_space = [-1, -0.5, 0, 0.5, 1]
# action_space = [-1, 0, 1]
input_dim = 19
output_dim = len(action_space)
cost_rate = 0.2 / 100 ##broker fee
stamp_duty_rate = 0.1 / 100 ##stamp duty rate for sales
uptrend_factor = 1.2
downtrend_factor = 0.8
train_start_date_str = '20150101'
train_end_date_str = '20200101'
test_start_date_str = '20200102'
test_end_date_str = '20230901'

"""# Process Data"""

train_data = pd.read_csv("data/train_data.csv")
val_data = pd.read_csv("data/val_data.csv")
test_data = pd.read_csv("data/test_data.csv")

from data_process import process_data

train_data = process_data(train_data).iloc[:, 1:]
val_data = process_data(val_data).iloc[:, 1:]
test_data = process_data(test_data, test=True).iloc[:, 1:]

"""# Train the Agent"""

from env import Environment
from agent import Agent

train_env = Environment(train_data)
val_env = Environment(val_data)
agent = Agent()

agent.train(train_env, val_env, 50, batch_size, epsilon, gamma, lr, device)

### load the best module
# model = torch.load('policy_net(single_sell_option).sav')
# agent = Agent(model)

"""# BackTest"""

##backtest
from backtest import Backtest
test_env = Environment(test_data)
backtest = Backtest(0, agent, test_env)
backtest.execute()
backtest.show_result()

##calculate mean metrics
mean_total_r = []
mean_annual_r = []
mean_alpha = []
mean_beta = []
mean_sharpe_ratio = []
mean_win_rate = []
mean_max_drawdown = []
mean_IR = []
mean_return_volatility=[]
mean_PLR = []
test_stock_list = test_data['ts_code'].unique()
for i in range(len(test_stock_list)):
    temp = test_data[test_data['ts_code'] == test_stock_list[i]]
    test_env = Environment(temp)
    backtest = Backtest(0, agent, test_env)
    backtest.execute()
    backtest.evaluate()
    mean_total_r.append(backtest.total_returns[-1])
    mean_annual_r.append(backtest.annualized_return)
    mean_alpha.append(backtest.alpha)
    mean_beta.append(backtest.beta)
    mean_sharpe_ratio.append(backtest.sharpe_ratio)
    mean_win_rate.append(backtest.win_rate)
    mean_max_drawdown.append(backtest.max_drawdown)
    mean_IR.append(backtest.information_ratio)
    mean_return_volatility.append(backtest.return_volatility)
    mean_PLR.append(backtest.profit_loss_ratio)

result_metrics = {
       'Average total return': np.mean(mean_total_r),
       'Average annualized return': np.mean(mean_annual_r),
       'Average Alpha': np.mean(mean_alpha),
       'Average Beta': np.mean(mean_beta),
       'Average Sharpe Ratio': np.mean(mean_sharpe_ratio),
       'Average Win Rate': np.mean(mean_win_rate),
       'Average Max Drawdown': np.mean(mean_max_drawdown),
       'Average IR:': np.mean(mean_IR),
       'Average Return Volatility': np.mean(mean_return_volatility),
       'Average Profit-Loss Ratio': np.mean(mean_PLR)}
result_metrics

"""# Build Portfolio"""

from portfolio import Portfolio

##calculate mean metrics
pool = list(test_data['ts_code'].unique())
mean_total_r = np.zeros(889)
mean_annual_r = []
mean_alpha = []
mean_beta = []
mean_sharpe_ratio = []
mean_win_rate = []
mean_max_drawdown = []
mean_IR = []
mean_return_volatility=[]
mean_PLR = []
num_stocks = 10
for i in range(10):
    model = torch.load('policy_net(single_sell_option).sav',map_location=torch.device('cpu'))
    np.random.shuffle(pool)
    stock_list = pool[:num_stocks]
    print(stock_list)
    p = Portfolio(stock_list)
    p.initialize()
    p.run()
    p.evaluate()
    mean_total_r += (np.array(p.mean_total_returns))
    mean_annual_r.append(p.mean_metrics[-1])
    mean_alpha.append(p.mean_metrics[-2])
    mean_beta.append(p.mean_metrics[-3])
    mean_sharpe_ratio.append(p.mean_metrics[1])
    mean_win_rate.append(p.mean_metrics[2])
    mean_max_drawdown.append(p.mean_metrics[5])
    mean_IR.append(p.mean_metrics[6])
    mean_return_volatility.append(p.mean_metrics[4])
    mean_PLR.append(p.mean_metrics[3])

    print(f"End of {i+1}th loop, mean return is {p.mean_total_returns[-1]}")

result_metrics = {'Average total return': mean_total_r[-1]/10,
       'Average annual return': np.mean(mean_annual_r),
       'Average Alpha': np.mean(mean_alpha),
       'Average Beta': np.mean(mean_beta),
       'Average Sharpe Ratio': np.mean(mean_sharpe_ratio),
       'Average Win Rate': np.mean(mean_win_rate),
       'Average Max Drawdown': np.mean(mean_max_drawdown),
       'Average IR:': np.mean(mean_IR),
       'Average Return Volatility': np.mean(mean_return_volatility),
       'Average Profit-Loss Ratio': np.mean(mean_PLR)}
result_metrics