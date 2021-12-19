import pandas as pd

class Print():

    def __init__(self, dataset=None):
        if type(dataset) != pd.core.frame.DataFrame:
            self.dataset = pd.DataFrame()
            
        else:
            self.dataset = dataset

    def print_null_values(self):
        for column in self.dataset:
            if self.dataset[column].isnull().any():
                print('{0} has {1} null values'.format(column, self.dataset[column].isnull().sum()))

    def print_column_missing_values(self,column):
        x = len(self.dataset)
        if self.dataset[column].isnull().any():
            print('{0} has total of {1} null values'.format(column, self.dataset[column].isnull().sum()))
            print ('In the column {0}'.format(column), round(100-(self.dataset[column].count()/x * 100), 3), '% of the cells have missing values')
    