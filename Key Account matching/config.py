import os

base_dir = os.path.dirname(os.path.abspath(__file__))

# INPUT FILE PATH
input_dir = os.path.join(base_dir, "Input")

key_account_total_path = os.path.join(input_dir, 'key_account_list_total.csv')
#key_account_sfdc_path = os.path.join(base_dir, 'view_dim_sfdc_rename.csv')
#key_account_list_path = os.path.join(base_dir, 'Key_account_list_full.csv')

results_end_customer_path = os.path.join(input_dir, 'Results End Customer POS.xlsx')

geography_path = os.path.join(input_dir, 'Geography.xlsx')

# OUTPUT FILE PATH
output_dir = os.path.join(base_dir, 'Output')
output_file_csv = os.path.join(output_dir, "decision_treshold_key_account_Total_v2.csv")
output_file_excel = os.path.join(output_dir, "decision_treshold_key_account_Total_v2.xlsx")

# ENSURE BOTH DIRECTORIES EXIST
os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

# SIMILARITY TRESHOLD
similarity_threshold = 90