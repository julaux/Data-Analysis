from data_loader import read_results_end_customer, read_ka
from text_cleaning import clean_text
from similarity_analysis import comparison
from config import similarity_threshold, output_file_csv, output_file_excel, output_dir

# ONLY FOR REVIEWING
from pandasgui import show

# ------------------------------------------ LOAD FILES TO BE MATCHED -----------------------------------------------------
# THE DATASETS ARE LOAD AND APPLIED THE CLEAN_TEXT FUNCTION FROM THE TEXT_CLEANING MODULE

# KA_ACCOUNT_LIST
df_ka = read_ka()
df_ka['Names'] = df_ka.apply(lambda row: clean_text(row['Names'], row['Country']), axis=1)

# RESULTS_END_CUSTOMER
df_end_customer = read_results_end_customer()
df_end_customer['desc_end_customer'] = df_end_customer.apply(lambda row: clean_text(row['desc_end_customer'], row['code_country']), axis=1)


# ----------------------------------------------  DICTIONARIES ----------------------------------------------------------------
# COMMON COUNTRIES
common_countries = list(set(df_end_customer['code_country'].unique()).intersection(df_ka['Country'].unique()))

# DICTIONARIES
# X FOR DF_END_CUSTOMER
x = df_end_customer[(df_end_customer['code_country'].isin(common_countries)) & (df_end_customer['code_country'] != '')]

# Y FOR DF_KA
y = df_ka[(df_ka['Country'].isin(common_countries)) & (df_ka['Country'] != '')]

# DF_END_CUSTOMER
df_dict1 = {nombre_grupo: datos for nombre_grupo, datos in x.groupby('code_country')}

# DF_KA
df_dict2 = {nombre_grupo: datos for nombre_grupo, datos in y.groupby('Country')}


#-------------------------------------------------- SAVE DECION_TRESHOLD FILE -----------------------------------------------------
df_comparison = comparison(df_dict1, df_dict2, similarity_threshold)

# SELECT THE SIMILARITY SCORE, ADJUST SIMILARITY_TRESHOLD VARIABLE
df_comparison_filtered = df_comparison[df_comparison['similarity_score'] >= similarity_threshold]

# SORT ID_SK_TAX AND SIMILARITY_SCORE (HIGHEST SCORE)
df_comparison_filtered.sort_values(by=["id_sk_tax", "similarity_score"], ascending=[True, False])

# DROP DUPLICATES
df_comparison_filtered = df_comparison_filtered.drop_duplicates(subset= ["id_sk_tax"], keep="first")

# SEPARATOR
separator = '\t' # TAB


## ------------------------------------------------- SEE THE FINAL DATAFRAME ------------------------------------------------------------
show(df_comparison_filtered)

## Save file --> Decision treshold.csv

# SAVE AS CSV FILE
# df_comparison_filtered.to_csv(output_file_csv, index=False, encoding="utf-8-sig", sep=separator)

# Save as Excel file
# df_comparison_filtered_excel = df_comparison_filtered.loc[:, ['id_sk_tax', 
#                                                               'country', 
#                                                               'end_customer',
#                                                               'key_account', 
#                                                               'desc_account_owner', 
#                                                               'desc_account_owner_manager']].rename(columns={'country':'desc_country', 
#                                                                                                             'key_account':'desc_key_account'})

# df_comparison_filtered_excel.to_excel(output_file_excel, index=False, engine="openpyxl")

print(f'\n---- THE FILE HAS BEEN SAVED -----------')
print(f'\nRoute:\n{output_dir}\n')