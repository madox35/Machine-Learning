import pandas

import matplotlib.pyplot as plt
import numpy as np

path_data_set    = './Data/DataSet/bank/bank.csv'

path_Categorical = './Data/Results/group7-DQR-Continuous.csv'
path_Continuous  = './Data/Results/group7-DQR-Categorical.csv'

path_Categorical_features = './Data/Results/group7-DQR-Continuous.csv'
path_Continuous_features  = './Data/Results/group7-DQR-Categorical.csv'



# Try to read csv file
try:
    file_ds = pandas.read_csv(path_data_set,delimiter = ';', header=0, index_col=0)
except:
    print("Error when reading csv file")
    exit(1)

continuous_columns = file_ds.select_dtypes(include=[np.number])    
continuous_header = ["Features","Count","% Miss", "Card", "Min", "1st Qrt", "Mean","Median","3rd Qrt", "std" ]
continuous_features_table = []

for col in continuous_columns:
    feature = [col]
    feature.append(file_ds[col].size)
    feature.append((file_ds[col].isnull().sum()/file_ds[col].size) * 100)
    feature.append(file_ds[col].unique().size)
    feature.append(np.min(file_ds[col]))
    feature.append(np.percentile(file_ds[col],25))
    feature.append(np.mean(file_ds[col]))
    feature.append(np.percentile(file_ds[col],50))
    feature.append(np.percentile(file_ds[col],75))
    feature.append(np.std(file_ds[col]))
        
    continuous_features_table.append(feature)
    
categorical_columns = file_ds.select_dtypes(exclude=[np.number])                     
categorical_header = ["Features","Count","% Miss", "Card", "Mode", "Mode Freq", "Mode %","2nd Mode"," 2nd Mode Fréq", "2nd Mode %" ]
categorical_features_table = []
           
for col in categorical_columns:
    feature = [col]
    feature.append(file_ds[col].size)
    feature.append((file_ds[col].isnull().sum()/file_ds[col].size) * 100)
    feature.append(file_ds[col].unique().size)
    mode = []
    mode = file_ds[col].value_counts()
    feature.append(np.min(file_ds[col]))
    feature.append(np.percentile(file_ds[col],25))
    feature.append(np.mean(file_ds[col]))
    feature.append(np.percentile(file_ds[col],50))
    feature.append(np.percentile(file_ds[col],75))
    feature.append(np.std(file_ds[col]))

    continuous_features_table.append(feature)
#file_ds.drop('id',1)
'''
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

columns = file_ds.columns

print(columns)

print(file_ds._get_numeric_data().columns)

for column in file_ds.columns:
    
    
    
    
    
    
    count = file_ds[column].value_counts(sort=1)
    
    try:
        val = count.loc[' ?']
    except :
        val = 0
    
    if file_ds[column].dtype != numpy.int64:
        file_categorical_features.ix[column, '% Miss'] = val/file_ds[column].count()
        file_categorical_features.ix[column, 'Mode %'] = count.irow(0)/file_ds[column].count()
        
        try:
            file_categorical_features.ix[column, '2nd Mode'] = count.keys()[1]
            file_categorical_features.ix[column, '2nd Mode freq'] = count[1]
            file_categorical_features.ix[column, '2nd Mode %'] = count[1]/file_ds[column].count()
        except:
            file_categorical_features.ix[column, '2nd Mode'] = 0
            file_categorical_features.ix[column, '2nd Mode freq'] = 0
            file_categorical_features.ix[column, '2nd Mode %'] = 0

    else:
        file_continuous_features.ix[column, '% Miss'] = val
        
        
        '''
# Write files to csv
pandas.DataFrame(file_continuous_features,columns=['HeadersTable']).to_csv(path_Continuous)
pandas.DataFrame(file_categorical_features).to_csv(path_or_buf=path_Categorical)

# Generating plots, 
for column in file_ds.columns:
    #if the column is continuous and that they have a cardinality higher than 10, histogram !
    if file_ds[column].unique.size >= 10:
        file_ds[column].plot().hist()
        plt.show()
    # Otherwise, it's just bar plot
    else:
        data = [
            go.Bar(
                x=file_ds[column].value_counts().keys(),
                y=file_ds[column].value_counts().values
            )
        ]
        plot_url = py.plot(data, filename='Data/HTML/'+column+".html")
