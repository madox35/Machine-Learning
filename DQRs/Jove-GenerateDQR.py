import plotly
import numpy
import pandas



class DataTreatment:
    
    def __init__(self):
        self.pathData = './data/bank/bank.csv'
        self.__continuous = []
        self.__categories = []
        self.__missingFeatures = []
        self.__missingFeaturesCategories = []
        self.__dataRecovered = False
    
    def getCSV(self):
        print("Getting CSV data...")
        filecsv = pandas.read_csv(filepath_or_buffer=self.pathData, delimiter = ';', header=0, index_col=0)
        self.__continuous = filecsv.select_dtypes(include=[numpy.number])
        self.__categories = filecsv.select_dtypes(exclude=[numpy.number])
        self.__dataRecovered = True
        print("CSV Data loaded")
    
    def getContinuous(self):
        return self.__continuous
    
    def setContinuous(self,feature,value):
        self.__continuous[feature].append(value)
        
    def getCategories(self):
        return self.__categories
    
    def setCategories(self,feature,value):
        self.__categories.append(value)
    
    def getMissingFeatures(self):
        return self.__missingFeatures
    
    def setMissingFeatures(self,feature,value):
        self.__missingFeatures[feature].append(value)
        
    def getMissingFeaturesCategories(self):
        return self.__missingFeaturesCategories
    
    def setMissingFeaturesCategories(self,feature,value):
        self.__missingFeaturesCategories[feature].append(value)
        
    def drawGraphics(self):
        """
        Continuous features
        """
#       continuousDescribes = (self.getContinuous().describe()).transpose()
        #print(continuousDescribes)

        tableContinuous = self.getContinuous()
#        print(self.getContinuous())
        #pandas.DataFrame(tableContinuous).to_csv(path_or_buf='./data/results/continuous.csv')
        
        for feature,value in tableContinuous.items():                
            
#            count = len(value)
#            ERROR HERE TO FIX TO SAVE DATA IN CSV IN FUTUR
#            nbMiss = 0
#            for i in range(count):
#                val = value[i]
#                if val == ' ?':
#                    nbMiss += 1
#                    self.setMissingFeatures('Miss',value)
#            #print((nbMiss / count) * 100)
#            
#
            unique_value = len(set(self.getContinuous()))
            #print(unique_value)
            # Create & save plots
            
            if unique_value >= 10:
                
                plotly.offline.plot({
                    "data": [
                        plotly.graph_objs.Histogram(
                            x=tableContinuous[feature]
                        )
                    ],
                    "layout": plotly.graph_objs.Layout(
                        title="Histogram of feature \"" + feature + "\" - cardinality >=10"
                    )
                }, filename="./data/%s.html" % feature)
            else:
                plotly.offline.plot({
                    "data": [
                        plotly.graph_objs.Bar(
                            x=tableContinuous[feature].value_counts().keys(),
                            y=tableContinuous[feature].value_counts().values
                        )
                    ],
                    "layout": plotly.graph_objs.Layout(
                        title="Bar plot for feature \"" + feature + "\" - cardinality <10"
                    )
                }, filename="./data/html/%s.html" % feature)
        

        """
        Categories features
        """
        
#        categoriesDescribes = self.getCategories().describe().transpose()
#        desc_categories_dict = categoriesDescribes.to_dict()
        
        tableCategories = self.getCategories()
        pandas.DataFrame(tableCategories).to_csv(path_or_buf='./data/results/categories.csv')
        
        for feature,value in tableCategories.items():
            
#            count = len(value)
            
#            print(feature+'='+value)
#            ERROR HERE TO FIX TO SAVE DATA IN CSV IN FUTUR
#            first_mode_freq = desc_categories_dict['freq'][feature]
#            
#            
#            nbMiss = 0
#            for i in range(count):
#                val = value[i]
#                
#                if val == ' ?':
#                    nbMiss += 1
#            
#            percent = ( nbMiss / count) * 100
                      
#            self.setMissingFeaturesCategories('% Miss', percent)
#            self.setMissingFeaturesCategories('Mode %',(float(first_mode_freq) / count) * 100)
#            self.setMissingFeaturesCategories('2d Mode',0)
#            self.setMissingFeaturesCategories('2d Mode Freq.',0)
#            self.setMissingFeaturesCategories('2d Mode %',0)
            
            data = [
                plotly.graph_objs.Bar(
                    x=tableCategories[feature].value_counts().keys(),
                    y=tableCategories[feature].value_counts().values
                )
            ]
            layout = plotly.graph_objs.Layout(
                title="Bar plot for categorical feature \"" + feature + "\""
            )
            figure = plotly.graph_objs.Figure(data=data, layout=layout)
            name = "./data/html/" + feature + ".html"
            plotly.offline.plot(figure, filename=name)


# Main process 
    
x = DataTreatment()
x.getCSV();
#x.drawGraphics()

#print(x.getCategories())
#print(x.getContinuous())