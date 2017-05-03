import collections
import pandas as pd
machines=collections.OrderedDict()
orders=collections.OrderedDict()
sequence=[]
queue_machines=[]
running=True
results_table=pd.DataFrame()
view=None
events=0
