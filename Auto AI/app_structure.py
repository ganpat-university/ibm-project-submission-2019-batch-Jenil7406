import streamlit as st
import os
import pandas as pd
import pandas_profiling as pp
import streamlit.components.v1 as components
import re
import stats


if True:# 'file_upload_state' not in st.session_state:
    st.session_state.file_upload_state = False    
    st.session_state.stats_state = False                # Will reset to False after every Action eg. remove nulls for new stats
    st.session_state.stats_value = {}    
    st.session_state.custom_state = False

saved_file_name = 'data/uploaded_data.csv'
if os.path.exists(saved_file_name):     
    df = pd.read_csv(saved_file_name, index_col=None)

with st.sidebar: 
    st.image("https://www.onepointltd.com/wp-content/uploads/2020/03/inno2.png")
    st.title("Auto ML")
    choice = st.radio("Navigation", ["Upload","Stats","Profiling","Cleaning","Modelling","Options"])
    st.info("This project application helps you build your ML Model")    





if choice == "Upload" :    
    st.title("Upload Your Dataset")
    
    file = st.file_uploader("Upload Your Dataset")
    is_header_check = True if st.checkbox("Include Header") else None

    if file:
        file_name = file.name
        upload_format = re.search("csv",file_name) or re.search("xlsx",file_name)         #Format Error if Other Format

        if upload_format:   
            if file and not st.session_state.file_upload_state: # Which means that New File Upload and File state is False
                st.session_state.file_upload_state = True

                is_csv = re.search(".csv",file_name)        #True if file is CSV else XLSX 
                if is_header_check:
                    df = pd.read_csv(file, index_col=None) if is_csv else pd.read_excel(file, index_col=None)
                else:
                    df = pd.read_csv(file, index_col=None, header=None) if is_csv else pd.read_excel(file, index_col=None, header=None)
                df.to_csv(saved_file_name, index=None)
                df.to_csv('data/modified_data.csv', index=None)
                st.dataframe(df)    
   
        else:
            st.error("Available Format (CSV / XLSX)")
      
        if not is_header_check and upload_format:
            col_length = len(df.columns)            
            col_name = st.text_input("Write the Column name from Column_0 to Column_{} Eg. colA,colB, colC ".format(str(col_length)))
            if (st.button('Submit')):
                col_name = col_name.split(",")            
                col_name = [x.strip() for x in col_name]
                df = pd.read_csv(saved_file_name, index_col=None, names=col_name)        
                st.dataframe(df)    
                df.to_csv(saved_file_name, index=None)
                df.to_csv('data/modified_data.csv', index=None)


    if st.session_state.file_upload_state and not file: # File state is True and Upload button not Pressed
        st.write("Uploaded Dataset")
        df = pd.read_csv(saved_file_name, index_col=None)        
        st.dataframe(df) 



if choice == "Profiling": 
    df = pd.read_csv(saved_file_name, index_col=None)        
    st.title("Exploratory Data Analysis")
    #profile = pp.ProfileReport(df)
    #profile.to_file("report/output.html")    
    profile_contents = open("report/output.html", "rt").read()
    components.html(profile_contents, width=900, height=20000)

if choice == "Options" :          
    null_options = stats.get_null_options()
    custom_null_options = st.text_input("Write Custom Null values",null_options)
    
    options = stats.get_handle_null_options()
    remove_null_option = st.radio("Select how to handle Null Values: ", (options['selected'], options['not-selected']))

    # Not Now
    st.text_input("Max Categories Criteria",50)
    st.text_input("Data Type Consideration Criteria",0.95)

    if (st.button('Update')):
        stats.save_custom_null_options(custom_null_options)                
        stats.save_handle_null_options(remove_null_option)
        st.success("Updated")

if choice == "Stats" :
    if st.session_state.stats_state == False:
        st.session_state.stats_state = True
        df = stats.get_df('data/modified_data.csv')
        stats = stats.get_stats(df)
        st.session_state.stats_value = stats


        stats = st.session_state.stats_value 
        st.title("Exploratory Data Analysis")
        st.dataframe(df)

        total = stats['Total Records']
        null_records = stats['total_null']
        total_columns = len(stats['columns'])
        st.header("Overview")
        dataset_describe = {"Total Records":total, "Null Records":null_records,"Total Columns":total_columns}        
        st.table(dataset_describe)

        st.header("Columns")
        st.table(stats['dtypes'])        

        stats['float_stats'].update(stats['category_stats'])        
        st.header("Column Details")    
        
        for column in stats['columns']:
            if stats['dtypes'][column] != 'object':             # No details for Object Column
                st.write(column.upper())
                if stats['dtypes'][column] == 'float':
                    st.table(stats['float_stats'][column])
                else:   #String Category                    
                    st.write("Categories Count")                    
                    mode = stats['float_stats'][column]['Mode']
                    null_values =  stats['float_stats'][column]['Null Values']
                    st.table(stats['float_stats'][column]['count'])                
                    st.table({"Mode Value":mode,"Null Value Count":null_values})

        st.header("Faulty Records")    
        st.table(stats['faulty_values'])
    else:        
        stats = st.session_state.stats_value 
        st.title("Exploratory Data Analysis")
        st.dataframe(df)

        total = stats['Total Records']
        null_records = stats['total_null']
        total_columns = len(stats['columns'])
        st.header("Overview")
        dataset_describe = {"Total Records":total, "Null Records":null_records,"Total Columns":total_columns}        
        st.table(dataset_describe)

        st.header("Columns")
        st.table(stats['dtypes'])        

        stats['float_stats'].update(stats['category_stats'])        
        st.header("Column Details")    
        
        for column in stats['columns']:
            if stats['dtypes'][column] != 'object':             # No details for Object Column
                st.write(column.upper())
                if stats['dtypes'][column] == 'float':
                    st.table(stats['float_stats'][column])
                else:   #String Category                    
                    st.write("Categories Count")                    
                    mode = stats['float_stats'][column]['Mode']
                    null_values =  stats['float_stats'][column]['Null Values']
                    st.table(stats['float_stats'][column]['count'])                
                    st.table({"Mode Value":mode,"Null Value Count":null_values})

        st.header("Faulty Records")    
        st.table(stats['faulty_values'])
            
        #st.write(stats)
        

if choice == "Cleaning" :    
    st.title("Clean the Data")

    if (st.button("Change Custom Symbols to Null")):
        df = stats.get_df('data/modified_data.csv')
        df = stats.change_custom_symbols_to_null(df)
        df.to_csv('data/modified_data.csv', index=None)
        st.session_state.stats_state = False                   # So that it can again Recalculate
        st.success("Changed")

    st.header("Handle Null Values")
    if (st.button("Drop Na")):
        df = df.dropna()
        df.to_csv('data/modified_data.csv', index=None)
        st.session_state.stats_state = False                   
        st.success("Dropped")
        pass
    if (st.button("Fill NA")):
        df = stats.get_df('data/modified_data.csv')
        stats_data = stats.get_stats(df)
        df = stats.fill_nulls(df,stats_data)
        df.to_csv('data/modified_data.csv', index=None)
        st.session_state.stats_state = False                   
        st.success("Success")

    if (st.button("Custom NA")) or st.session_state.custom_state:
        st.session_state.custom_state = True
        print("Press")
        df = stats.get_df('data/modified_data.csv')
        stats = stats.get_stats(df)        
        columns = df.columns
        count = 0
        for x in columns:
            try:
                if stats['category_stats'][x]:
                    nulls =  stats['category_stats'][x]['Null Values']
                    if str(nulls) != '0':
                        st.write("Column Names",x)
                        st.write("Null Values: ",nulls)
                        choice = st.selectbox('Select the Fill Null Method',('mode','drop'))                        
                        if (st.button("Null Action {}".format(x))):
                            if choice == 'drop':
                                pass
                            else:
                                df = stats.fill_nulls(df=df,stats=stats_data,column_=x)
                            df.to_csv('data/modified_data.csv', index=None)
                            st.session_state.stats_state = False                   
                            st.success("Success")
                            st.session_state.custom_state = False            
                        count += 1                
            except:     
                try:               # Beecause Obect Type Column has no Stats
                    if stats['float_stats'][x]:
                        nulls = stats['float_stats'][x]['Nulls']
                        if str(nulls) != '0':
                            st.write("Column Names",x)
                            st.write("Null Values: ",nulls)
                            choice = st.selectbox('Select the Fill Null Method',('mean','min','max','drop'))
                            if (st.button("Null Action {}".format(x))):
                                if (st.button("Fill Null")):
                                    if choice == 'drop':
                                        pass
                                    else:
                                        df = stats.fill_nulls(df=df,stats=stats_data,column_=x,float_method=choice)
                                    df.to_csv('data/modified_data.csv', index=None)
                                    st.session_state.stats_state = False                   
                                    st.success("Success")       
                                    st.session_state.custom_state = False                                 
                            count += 1                            
                except:
                    pass
        if count == 0:
            st.write("No Null Values")
            st.session_state.custom_state = False                                 
        


    if (st.button("Auto Clean")):        
        df = stats.get_df('data/modified_data.csv')
        
        df = stats.change_custom_symbols_to_null(df)
        stats_data = stats.get_stats(df)

        df = stats.fill_nulls(df,stats_data)
        df.to_csv('data/modified_data.csv', index=None)

        st.session_state.stats_state = False                   
        st.success("Success")



        


if choice == "Modelling" :    
    from autokeras import StructuredDataRegressor
    from sklearn.model_selection import train_test_split
    st.title("Modelling")
    df = stats.get_df('data/modified_data.csv')    
    
    columns = list(df.columns)
    
    target_col = st.selectbox("Select Target Column",columns)
    # columns.remove(target_column)
    if(st.button("Train")):
        X = df.loc[:, df.columns != target_col]
        y = df.loc[:, target_col]
        print(X)
        X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.20, 
                                                    random_state=2021)
    
        search = StructuredDataRegressor(max_trials=1, loss='mean_absolute_error')
        search.fit(x=X_train, y=y_train)
        search.export_model()






