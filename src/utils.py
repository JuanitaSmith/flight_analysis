import numpy as np
import pandas as pd
import os


def reduce_mem_usage(df):
    """ iterate through all the numerical columns of a dataframe and modify the data type
        to reduce memory usage.
    """

    print('\nTriggering memory optimization.......\n')

    start_mem = df.memory_usage().sum() / 1024 ** 2
    print('Memory usage of dataframe is {:.2f} MB'.format(start_mem))
    for col in df.columns:
        col_type = df[col].dtype
        if col_type != object:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)

    end_mem = df.memory_usage().sum() / 1024 ** 2
    print('Memory usage after optimization is: {:.2f} MB'.format(end_mem))
    print('Decreased by {:.1f}%'.format(100 * (start_mem - end_mem) / start_mem))
    return df


def create_folder(folder_name):
    """ Make directory if it doesn't already exist """

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        
        
def convert_time(col):

    # Convert column to string, remove any float decimals, pad with leading zero's and correct missing fields converstions
    col =  col.astype('str').str.replace('.0', '', regex=False).str.zfill(4).replace('0nan', None)

    # Some minute fields are incorrect, covert minute = 60 to minute = 59
    col  = np.where(col.str[-2:] == '60',  col .str[:2] + '59', col)

    # convert column to datetime
#     col = pd.to_datetime(col , format='%H%M', errors='raise')   
    col = pd.to_datetime(col, format='%H%M') - pd.to_datetime(col, format='%H%M').normalize()    
    
    return col        