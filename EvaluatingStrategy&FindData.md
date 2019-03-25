## Evaluating Trading Strategies
criteria for judging a strategy:
 - Methodology
   - The intrinsic of the strategy, trading logic based on the momentum or mean_reverting or else
   - does the strategy rely on complex statistical or ML algorithm
   - does the strategy works with a long list of **PARAMETERS**,danger for optimisation bias
 - Sharpe Ratio
   - reward/risk, with the different way of measurement of volatility
 - Leverage
   - strategy require significant leverage(future,options,swaps)
 - Frequency
   - higher frequency require more capital
 - Volatility
 - Win/Loss, Average Profit/Loss
   - it's a very profitable strategy even the num of loss exceed the num of winning
   - momentum: rely on large numbers of loss and small num of **BIG** winning
   - mean-reverting: more winners but losing can be quite severe 
 - Maximum Drawdown
   - largest overall peak to trough percentage drop on the equity curve
 - Capacity/Liquidity
   - retail trader and small fund do not need consider this too much
 - Parameters
   - more parameters, more vulnerable to **optimisation bias**
 - Benchmark
   - another view angle of the alpha and beta
## Find History Data
- Fundamental Data
  - data about the macroeconomic trends
    - interest rates
    - inflation figures
    - corporate actions
    - ......
  - fundamental data focus on value companies
- News Data
  - including articles,blog posts,microblog post(twitter,weibo)
  - ML techniques convert the infos into **SENTIMENT**
  - usually stored in NoSQL
- Asset Price Data
  - most traditonal data
  - consists of time series of asset prices(daily OHLC)
  - require significant storage when intrady trading is included
- Financial Instruments
  - equities,bonds,futures,options
  - differernt assest demand different structure of DATABASE
- Frequency
  - higher frequency demand more storage and more technique backgroud
- Benchmarks
  - often for comparing usage
- Technology
  - data storage:SQL,NoSQL
  - business logic:C++,Java,Python,MATLAB,R