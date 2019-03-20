# successful backtesting
back testing for what?
- Filtration
  - sift out the strategies which do not meet our demands
- Modelling
  - test our strategy under condition such as **transaction costs, order routing, latency, liquidity** 
- Optimisation
  - increase the performance of a strategy
- Verification
  - compare different strategies with their performance.
  
  
In general, as the frequency of the strategy **increases**, it becomes harder to correctly model the 
microstructure effects of the market and exchanges.

## BackTesting Bias
- Optimisation Bias 
  - also called curve fitting,means overly optimized for a attractive result but probably 
  not performe well in the living trading
  - source:parameters such as entry/exit criteria, look back periods, volatility mearurement
  - solving ways:
    - reduce the number of parameters as possible
    - perform a **sensitivity analysis**(I think its very useful!!)
      - This means **varying the parameters** incrementally and plotting a "surface" of performance.
      - smooter, **BETTER** 高维度的优化就比较复杂了，这里不表
- Look-Ahead Bias
  - means you could use the information after the point of the testing time
  - examples:
    - Technical Bugs: Incorrect index(offset) of the verctor(array) may introduce the future information
    - Parameter Calculation: Using the whole dataset to calculat the regression coeeficients
    - Maxima/Minima: since these maximal/minimal values can only be calculated at the end of a time period, a look-ahead 
    bias is introduced if these values are used -during- the current period.
- Survivorship Bias 
  - some instruments can not be trade at the latter time,so if you still trading the existing instruments
  the performance will be inflated
  - solving:
    - Using Survivorship Bias Free Dataset
    - Use More Recent Data
- Cognitive Bias 