import os
import pandas as pd
import numpy as np
import pickle

def get_df(file_name = 'data/uploaded_data.csv'):    
    df = pd.read_csv(file_name, index_col=None)
    return df    

def pickle_save(filename,element):
    with open(filename+'.pkl', 'wb') as file:
       pickle.dump(element, file)

def pickle_load(filename):
    pickle_off = open(filename+".pkl", "rb")
    return pickle.load(pickle_off)

def get_null_options():
    null_options = pickle_load("options/null-options")
    null_options = ", ".join(null_options)
    return null_options                                     # Reurns String

def save_custom_null_options(custom_null_options):
    custom_null_options = custom_null_options.split(",")      
    custom_null_options = [x.strip() for x in custom_null_options]        
    pickle_save("options/null-options",custom_null_options)

#########3############################# START NULL ################################################################

def get_handle_null_options():
    options = pickle_load("options/remove_null-options")
    return options

def save_handle_null_options(handle_null_option):
    handle_null = get_handle_null_options()
    
    other_option = "Remove Nulls" if  "Fill with Mean/Mode" == handle_null_option else "Fill with Mean/Mode"


    new_handle_null ={"selected":handle_null_option,"not-selected":other_option}
    

    pickle_save("options/remove_null-options",new_handle_null)

def fill_nulls(df,stats,column_=None,float_method='mean', category_method='Mode'):
    columns = df.columns
    stat = stats['float_stats']
    stat.update(stats['category_stats'])        
    dtypes = stats['dtypes']

    # if column_ is not None:        
    #     columns = [column_]

    for column in columns:        
        if dtypes[column] in ['nominal','ordinal','flag']:
            mode = stat[column]['Mode']
            df[column].fillna(mode,inplace=True)
        elif dtypes[column] == 'float':
            mean = stat[column]['mean']
            df[column].fillna(mean,inplace=True)
    return df

#########3############################# END NULL ################################################################
def initialize_global_vars():
    global no_of_var, missing_cells, no_of_observations ,categorical_dtype, dtype
    df = get_df()
    no_of_var = (df.columns)
    #missing_cells = 




def change_custom_symbols_to_null(df): #Change Values like " ?, undefined " to null
    null_options = get_null_options().split(", ")
    #Change IRIS VALUE
    for nulls in null_options:
        df = df.replace(nulls,np.nan)        
    #print(change_custom_null_options_to_null())
    return df        

'''
def get_column_wise_null_values():
    #Change IRIS VALUE    
    df = change_custom_null_options_to_null()
    columns =  df.columns    
    columns_nulls = {}
    for column in columns:
        columns_nulls.update({column:pd.isna(df[column]).sum()})
    #print(get_column_wise_null_values())
    return columns_nulls
'''

def get_faulty_records(df,columns_dtypes):
    column_false_records = {}
    
    for column in columns_dtypes:
        rows_list = []
        dtype = columns_dtypes[column]

        for count,row in enumerate(df[column]):
                if dtype == 'float':
                    try:
                        row = float(row)                                # It has been Identified as Float previously not changed to float 
                    except:
                        pass
                    if type(row) != type(1.0) and row not in ["\"\"","\'\'",np.nan]:
                        rows_list.append(row)
                elif dtype == 'string' or dtype == 'nominal' or dtype == 'ordinal' or dtype == 'flag':
                    try:
                        row = float(row)                                # To check if any Float value has not been added
                    except:
                        pass                    
                    if type(row) != type('abc') and row not in [np.nan]:
                        rows_list.append(row)

        if len(rows_list) > 0:
            column_false_records.update({column:rows_list})
    return column_false_records


def check_ordinal(keys):
    all_keys = 0
    key_length = len(keys)
    example_index = False
    ordinal_examples  = [["zero","one","two","three","four"],["first","second","third","fourth","fifth","sixth","seventh","eighth"],["a","b","c","d","e","f"],["extremely dislike", "dislike", "neutral", "like", "extremely like"]]
    for name in keys:
        if example_index != False:
            break
        for count,example in enumerate(ordinal_examples):
            if name in example:
                example_index = count
                break    
    if example_index != False: #It means ordinal possibility
        for name in keys:
            if name in ordinal_examples[example_index]:
                all_keys += 1
    
    if all_keys == key_length:
        return True
    else:
        False
#print(check_ordinal(['a','b','c']))        
def get_category_dtype(df,columns_dtypes,categories_count):
    # nomial or Ordinal or flag
    columns = df.columns
    for column in columns:
        if columns_dtypes[column] == 'string':            
            keys = categories_count[column].keys()
            if len(keys) == 2:
                columns_dtypes.update({column:'flag'})            
            elif check_ordinal(keys):
                columns_dtypes.update({column:'ordinal'})            
            else:
                columns_dtypes.update({column:'nominal'})            
    return columns_dtypes

def get_categories_count(df,columns_dtypes):            
    column_categories_count = {}
    categories_count = {}
    columns = df.columns

    for column in columns:
        categories_count = {}
        if columns_dtypes[column] == 'string': #nominal ke ordinal
            for category in df[column]:
                try:
                    category = category.lower()
                except:
                    #for null valeus dont have lower
                    pass
                if category in categories_count and category:
                    count = categories_count[category]
                    categories_count.update({category:count+1})
                else:
                    # New Category
                    if category not in ["\"\"","\'\'",np.nan]:
                        categories_count.update({category:1})

            column_categories_count.update({column:categories_count})
    return column_categories_count

#df = change_custom_null_options_to_null().dropna()
#get_categories(df['species'])
#def get_categories_type(column)

def get_null_count(df,column):
    return pd.isna(df[column]).sum()


def get_float_stats(df,columns_dtypes):
    float_stats = {}
    columns = df.columns
    for column in columns:    
        null_count = get_null_count(df,column)        
        if columns_dtypes[column] == 'float':
            mean      = df[column].describe()['mean']
            min_value = df[column].describe()['min']
            max_value = df[column].describe()['max']
            std       = df[column].describe()['std']
            nulls     = get_null_count(df,column)
            float_stats.update({column:{"mean":mean,"min":min_value,"max":max_value,"std":std,"Nulls":nulls}})
    return float_stats

def get_category_stats(df,columns_dtypes):
    categories_count = get_categories_count(df,columns_dtypes)
    columns_dtypes   = get_category_dtype(df,columns_dtypes,categories_count)
    category_stats   = {}


    for column in categories_count.keys():                    
        mode_max = 0
        mode_category = ''
        nulls = get_null_count(df,column)
        for category in categories_count[column]:
            if categories_count[column][category] > mode_max:
                mode_max = categories_count[column][category]
                mode_category = category
        category_stats.update({column:{"count":categories_count[column],"Mode":mode_category,"Null Values":nulls}})                    
    return (columns_dtypes,category_stats)


################################################# MAIN #########################################

def get_stats(df):
    total_records = len(df)
    columns = df.columns
    total_null = df.isna().sum().sum()
    columns_dtypes = {}       # Categorical, Object , Float

    # Start Dtypes    
    category_float_criteria = 1
    category_criteria       = 0.9
    object_dtype_criteria = 1 - category_float_criteria     # Object means Moslty Contains Both values and cannot take decision on own probably will also be discarded in AutoML    

    for column in columns:
        float_values_count = 0
        string_values_count = 0                
        for count,row in enumerate(df[column]):            
            try:                
                # If not Float then String
                row = float(row)
            except:                
                pass

            if type(row) == type(1.0):
                float_values_count+=1
            else:
                string_values_count+=1                        
        
        if float_values_count > string_values_count:
            if float_values_count/total_records >= category_float_criteria:                
                columns_dtypes.update({column:"float"})

            else:                
                columns_dtypes.update({column:"object"})
        else:
            if string_values_count/total_records > category_criteria:                
                columns_dtypes.update({column:"string"})
            else:
                columns_dtypes.update({column:"object"})                        
    
    float_stats      = get_float_stats(df,columns_dtypes)    
    columns_dtypes,category_stats   = get_category_stats(df,columns_dtypes)
    faulty_values = get_faulty_records(df,columns_dtypes)
    return {"Total Records":total_records,"columns":columns,"total_null":int(total_null),"dtypes":columns_dtypes,"float_stats":float_stats,"category_stats":category_stats,"faulty_values":faulty_values}   

#print(get_stats(get_df('iris.csv')))



    
def auto_clean():
    df = change_custom_symbols_to_null()
    handle_null = get_handle_null_options()['selected']
    if handle_null == 'Remove Nulls':
        df = df.dropna
    else:
        df = fill_nulls(df)

    #drop column        



'''
df = get_df('iris.csv')
print(df.info())
print(df.describe())
print(df.count())
print(change_custom_null_options_to_null().dropna())
print(change_custom_null_options_to_null().dropna().dtypes)
#print(pd.isna(df['sepal_length']).sum())
#print(df.columns[0])

#df = get_df('iris.csv')
#print(df.replace('Null',np.nan))

def get_dtypes():
    df = change_custom_null_options_to_null()
    df = df.dropna()
    
    total_records = len(df)
    columns = df.columns
    columns_dtypes = {}       # Categorical, Object , Float

    category_float_criteria = 0.9
    object_dtype_criteria = 1 - category_float_criteria     # Object means Moslty Contains Both values and cannot take decision on own probably will also be discarded in AutoML
    max_categories = 10  #Get from Options    to discard column after max_categories    or Make it object Dtype after max categories

    for column in columns:
        float_values_count = 0
        string_values_count = 0                
        for count,row in enumerate(df[column]):            

            try:                
                # If not Float then String
                row = float(row)
            except:                
                pass

            if type(row) == type(1.0):
                float_values_count+=1
            else:
                string_values_count+=1                        
        
        if float_values_count > string_values_count:
            if float_values_count/total_records > category_float_criteria:                
                columns_dtypes.update({column:"float"})

            else:                
                columns_dtypes.update({column:"object"})
        else:
            if string_values_count/total_records > category_float_criteria:                
                columns_dtypes.update({column:"string"})
            else:
                columns_dtypes.update({column:"object"})                
        
    print(columns_dtypes)
    false_records = get_false_records(df,columns_dtypes)
    print(get_categories_count(df,columns_dtypes))
#print(get_dtypes())

'''



