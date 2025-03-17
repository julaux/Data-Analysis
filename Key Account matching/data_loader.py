import pandas as pd
from config import key_account_total_path, results_end_customer_path, geography_path

def read_results_end_customer():
    """
    Read Results End Customer POS, 
    """
    df_results = pd.read_excel(results_end_customer_path, usecols=['id_sk_tax', 
                                                                   'code_country', 
                                                                   'desc_end_customer'], 
                                                                   dtype=str)
    
    # TO STANDARDIZE TO LOWERCASE
    df_results['desc_end_customer'] = df_results['desc_end_customer'].str.lower()
    
    ### ------ ERROR DEBUGGING
    # df_results = df_results[df_results['code_country'].str.lower() == 'it']

    ### ------ SAMPLING
    # df_results = df_results.sample(n=1000)
    
    # LOAD GEOGRAPHY ISO CODES INFO, AND REPLACE ISOCODE BY COUNTRY NAME
    geography = pd.read_excel(geography_path, usecols=['code_country', 'desc_country'], dtype=str)
    geography.drop_duplicates(inplace=True)
    geography['code_country'] = geography['code_country'].str.strip().str.upper()
    geography['desc_country'] = geography['desc_country'].str.strip().str.upper()

    # REPLACES COUNTRY ISO CODES BY FULL COUNTRY NAME
    df_results['code_country'] = df_results['code_country'].map(dict(zip(geography['code_country'], geography['desc_country'])))

    # CLEAN NaN AND EMPTY VALUES
    df_results = df_results[df_results['desc_end_customer'].notna() & (df_results['desc_end_customer'].str.strip() != "")]
    
    # COPY OF THE COLUMN 'DESC_END_CUSTOMER'
    df_results['original_end_customer'] = df_results['desc_end_customer']
    
    return df_results

def read_ka():
    """
    Read key account total (Key names + SFDC customers)
    """
    try:
        df_ka = pd.read_csv(key_account_total_path, encoding="utf-8")
    
    except UnicodeDecodeError:
        df_ka = pd.read_csv(key_account_total_path, encoding="ISO-8859-1")

    df_ka['Key Account'] = df_ka['Key Account'].astype(str).apply(lambda x: x.replace("�", "ä"))
    df_ka['Country'] = df_ka['Country'].str.strip().str.upper()

    # STANDARDIZING TO LOWERCASE
    df_ka['Names'] = df_ka['Names'].str.lower()

    return df_ka