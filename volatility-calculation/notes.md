# Developer notes:


## Volatility
$ volatility = std \times \sqrt{trading days}$
- Data provided is not daily returns -- how to handle?
- use same formula and last trade point as proxy for close price -- **CONSULT DOMAIN EXPERTISE**
	- alternatively use opening or mean price?
- https://www.educba.com/volatility-formula/


## Assumptions:
- All data is available for calculation, and speed is not a constraint (don't need to perform ongoing calculation and store values)
- Data will always be in a format matching the files given -- for automation, sanity checks should be performed.
- Temporal changes are outside the scope of the assignment, but probably have value. Need to discuss with domain experts. E.g. level shift (of mean) in stock D, and change in volatility behaviour over period. It is likely that more recent values are more relevant to the application.
- Volatility calculation is not defined -- there are many options for this. The choice to use the last observed trade as the closing price warrants further discussion with domain experts.


## ToDo:
- Implement level shift detection -- i.e. stock D -- **CONSULT DOMAIN EXPERTISE**
- Volatility shift detection -- i.e. stock D. Are latest values more useful? -- **CONSULT DOMAIN EXPERTISE**
- 3x std threshold is arbitrary, can test modifications of this based on extent of outlier trends.
- Store values for faster daily calculations if speed required by pipeline.
- Volatility measures 
	-- more ways to do this
	-- can use alternative proxy for daily price -- e.g. first trade or mean
- Date field validation -- easy to check whether trades fall on weekenends
- The one-week neighbourhood for median calculation is arbitrary and can be optimised. As can the 3-std threshold for outlier detection.

## References:
Automatic outlier detection for time series: an application to sensor data
	https://link.springer.com/article/10.1007/s10115-006-0026-6
	
A Survey of Methods for Time Series Change Point Detection
	https://link.springer.com/article/10.1007/s10115-016-0987-z
