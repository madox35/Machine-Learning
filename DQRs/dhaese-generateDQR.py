import pandas

import plotly.offline as py
import plotly.graph_objs as go

import numpy

path_data_set    = './Data/DataSet.csv'
path_Categorical = './Data/dhaese-DQR-CategorialFeatures.csv'
path_Continuous  = './Data/dhaese-DQR-ContinuousFeatures.csv'

# Try to read csv file
try:
    file_ds = pandas.read_csv(path_data_set) 
except:
    print("Error when reading csv file")
    exit(1)

    
file_ds.drop('id',1)

# Feature, count, %miss, card, min, 1st quart, mean, median, 3rd quart, max, Std dev
# Describe() returns only count, mean, std, min, 25%, 50%, 75%, and max
# Therefore we have to include others features
file_continuous_features = file_ds.describe().transpose()
file_categorical_features = file_ds.describe(include=['O']).transpose()


file_continuous_features['% Miss'] = 0
file_categorical_features['% Miss'] = 0
file_categorical_features['Mode %'] = 0
file_categorical_features['2nd Mode'] = 0
file_categorical_features['2nd Mode freq'] = 0
file_categorical_features['2nd Mode %'] = 0


for column in file_ds.columns:
    count = file_ds[column].value_counts(sort=1)

    try:
        val = count.loc[' ?']
    except :
        val = 0

    print()
    
    if file_ds[column].dtype != numpy.int64:
        file_categorical_features.ix[column, '% Miss'] = val/file_ds[column].count()
        file_categorical_features.ix[column, 'Mode %'] = count.irow(0)/file_ds[column].count()
        
        try:
            file_categorical_features.ix[column, '2nd Mode'] = count.index[1]
            file_categorical_features.ix[column, '2nd Mode freq'] = count.irow(1)
            file_categorical_features.ix[column, '2nd Mode %'] = count.irow(1)/file_ds[column].count()
        except:
            file_categorical_features.ix[column, '2nd Mode'] = 0
            file_categorical_features.ix[column, '2nd Mode freq'] = 0
            file_categorical_features.ix[column, '2nd Mode %'] = 0

    else:
        file_continuous_features.ix[column, '% Miss'] = val
        
# Write files to csv
pandas.DataFrame(file_continuous_features).to_csv(path_or_buf=path_Continuous)
pandas.DataFrame(file_categorical_features).to_csv(path_or_buf=path_Categorical)

# Generating plots, 
for column in file_ds.columns:
    #if the column is continuous and that they have a cardinality higher than 10, histogram !
    if file_ds[column].dtypes == 'int64' and file_ds[column].value_counts().__len__() >= 10:
        tab=file_ds[column].value_counts().sort_index()
        data = [
            go.Scatter(
                x=tab.keys(),
                y=tab.values
            )
        ]
        plot_url = py.plot(data, filename='Data/HTML/'+column+".html")
    # Otherwise, it's just bar plot
    else:
        data = [
            go.Bar(
                x=file_ds[column].value_counts().keys(),
                y=file_ds[column].value_counts().values
            )
        ]
        plot_url = py.plot(data, filename='Data/HTML/'+column+".html")