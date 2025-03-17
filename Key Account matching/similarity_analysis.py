import numpy as np
import pandas as pd
from fuzzy_matching import similarity
from config import similarity_threshold

# CREATE THE DATAFRAME STRUCTURE 
def create_df_stage(scores_array,indexarray, df1, df2):
    """
    Function to iterate through DF df_end_customer (df1) and DF df_ka (df2)
    Args:
        - scores_array: A 2D array or matrix containing similarity scores between entities.
        - indexarray: This array seems to hold indices used to map between the rows of df1 and df2.
        - df1: End customer result DataFrame
        - df2: Key Account list DataFrame
    Return:
    """

    df_rows = []
    for roww in range(df1.shape[0]):
        
        idsktax = df1.iloc[roww, 0]                 # 'id_sk_tax'
        country = df1.iloc[roww, 1]                 # 'Code_country'
        kcc_name = df1.iloc[roww, 2]                # 'desc_end_customer'
        original_end_customer = df1.iloc[roww, 3]   # 'end_customer'
                
        for col in range(indexarray.shape[1]):   
            fila = indexarray[roww,col]
            
            # DATAFRAME KEY ACCOUNTS COLUMNS 
            key_account = df2['Key Account'].iloc[fila]
            ka_name = df2['Names'].iloc[fila]
            desc_account_owner = df2['KAM'].iloc[fila]

            similarity_score = scores_array[roww, fila]
            
            row = {
                'id_sk_tax': idsktax,
                'country' : country,
                'desc_account_owner': desc_account_owner,
                'desc_account_owner_manager': 'Patrice Chereau',
                'end_customer': original_end_customer,
                'kcc_name': kcc_name,
                'ka_name': ka_name,  
                'key_account': key_account, 
                'similarity_score': similarity_score
            }
            df_rows.append(row)
    return df_rows

def comparison(dict1: dict, dict2: dict, topmatches: int) -> pd.DataFrame:
    """
    Compares the desc_end_customer column in df_dict1 with the Names column in df_dict2 for each country.
    Calculates the similarity score and creates a DataFrame with the results.

    Args
        - dict1: Dictionary for df_end_customer
        - dict2: Dictionary for df_ka
        - topmatches: Cut off of similarity score

    Returns
        Creates a DataFrame    
    """
    print('\nPerforming comparison and creating DataFrame\n')
    rows = []
    for element in list(dict1.keys()):
        print(f'Each matrix for {element} will have this dimension {dict1[element].shape[0]} x {dict2[element].shape[0]}')   

        # LIST OF CUSTOMERS' NAMES AND KEY ACCOUNT NAMES
        end_customer = dict1[element]['desc_end_customer'].tolist()
        ka_names = dict2[element]['Names'].tolist()
        ka_accounts = dict2[element]['Key Account'].tolist()
        countries = dict1[element]['code_country'].tolist()

        # SIMILARITY MATRIX
        result = np.zeros((len(end_customer), len(ka_names)))

        # CALCULATE THE SIMILARITY
        for i, cust in enumerate(end_customer):
            for j, ka in enumerate(ka_names):
                country_code = countries[i]
                result[i, j] = similarity(cust, ka, ka_accounts[j], country_code)

        # SELECT THE INDICES WITH HIGH SIMILARITY SCORE
        indices_maximos = np.argsort(result, axis=1)[:, ::-1][:, :topmatches]

        # ROUND THE SIMILARITY VALUES TO TWO DIGITS AND CONVERT TO FLOAT
        result = np.round(result.astype(float), 2)
        rows += create_df_stage(result, indices_maximos, dict1[element], dict2[element])

    df = pd.DataFrame(rows)
    return df