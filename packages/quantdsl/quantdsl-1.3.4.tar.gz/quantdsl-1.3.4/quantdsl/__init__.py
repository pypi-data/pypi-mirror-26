__version__ = '1.3.4'

# Todo: Finish off support for yearly periodisation, and also hourly.
# Todo: Command line support, so QuantDSL can be written and executed without knowing Python.
# Todo: Price process as DSL (included in module directly or by import, module named as arg to calc()).
# Todo: Price process as DSL, either calibration params, or args for calibration with e.g. data from quandl).
# Todo: More price processes (jumps, heston).
# Todo: Better report object: separate out the delta hedging.
# Todo: Better deltas (dx sometimes uses average of prices in month, when not all prices may be used in expression).
# Todo: Tidy up how args are passed into evaluate(), it seems correct, but also a bit ad hoc.
# Todo: Support names in expressions being resolved by evaluation args (e.g. like 'observation_date' but more general).
# Todo: StockMarket element.
# Todo: Warning when a built-in is being overridden by a user defined function. Or perhaps that would be useful? In any case, make sure this is handled properly (currently the user defined function will just be ignore?).
# Todo: Make price process create calibration params from market observations, as well as consume the calibration parameters.
# Todo: Develop a PriceProcess object that works as a network service client object, and as a server object (so price simulation is available over network).
# Todo: Change all names from lower camel case to underscore separated style.
# Todo: Develop multi-factor PriceProcess model (e.g. Schwartz-Smith)?
# Todo: Develop the multiprocessing code into a stack runner object, which can be replaced with a network-based runner?
# Todo: Develop call requirement dependency graph store, so call requirements can be retrieved over the network.
# Todo: Improve the multiprocessing code - currently it runs slower that the single threaded, and seems to grind to a halt for stacks > 5000 expressions (IPC bandwidth? rounding errors?).
# Todo: Improve separation of expression stack/dependency graph from results and notifications, so results from different runs can be reused when calculating greeks.
# Todo: Separate multiprocessing from ExpressionStack, self-evaluation of ExpressionStack can just be single threaded.
# Todo: Figure out how best to make alternative set of DSL classes available to workers (module commodity_name that is imported, rather than a dict of classes).
# Todo: Optimization for parallel execution, so if there are four cores, then it might make sense only to stub four large branches?
# Todo: Optimize network traffic by creating a single message containing all data required to evaluate a stubbed expression.
# Todo: Decouple the cli from the runner more, make the workers put things directly on the queue, so that the cli just waits for the final result and clocks the intermediate results as they occur in an event stream.
# Todo: Separate more clearly the syntax parsing (the Parser methods) from the semantic model the DSL objects.
# Todo: Separate more clearly a general function language implementation, which could be extended with any set of primitive elements.
# Todo: Use function arg annotation to declare types of DSL function args (will only work with Python 3).
# Todo: Develop closures, function defs within function defs may help to reduce call argument complexity.
# Todo: Think about other possibility of supporting another syntax? Perhaps there is a better syntax than the Python based syntax?
# Todo: Develop natural language "skin" for Quant DSL expressions (something like how Gherkin syntax maps to functions?)?
# Todo: Support list comprehensions, for things like a strip of options?
# Todo: Develop a GUI that shows the graph being evaluated, allowing results to be examined, allows models to be developed. Look at the "language workbench" ideas from Martin Fowler (environment which shows example results, with editable code reachable from the results, and processing built-in)?
# Todo: Better stats available on number of call requirements, number of leaves in dependency graph, depth of graph?
# Todo: Prediction of cost of evaluating an expression, cost of network data requests, could calibrate by running sample stubbed expressions (perhaps complicated for LongstaffSchwartz cos the LeastSqaures routine is run different numbers of times).
# Todo: Support plotting.
# Todo: Clean up the str, repr, pprint stuff?
# Todo: Raise Quant DSL-specific type mismatch errors at run time (ie e.g. handle situation where datetime and string can't be added).
# Todo: Anyway, identify when type mismatches will occur - can't multiply a date by a number, can't add a date to a date or to a number, can't add a number to a timedelta. Etc?
# Todo: (Long one) Go through all ways of writing broken DSL source code, and make sure there are sensible errors.
# Todo: Figure out behaviour for observation_date > any fixing date, currently leads to a complex numbers (square root of negative time delta).
# Todo: Think/talk about regressing on correlated brownian motions, rather than uncorrelated ones - is there actually a difference? If no difference, there is no need to keep the uncorrelated Brownian motions.
# Todo: Review the test coverage of the code.
# Todo: Review the separation of concerns between the various test cases.
# Todo: Move these todos to an issue tracker.

# Note on how to install matplotlib in virtualenv: http://www.stevenmaude.co.uk/2013/09/installing-matplotlib-in-virtualenv.html

































