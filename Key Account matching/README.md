# KEY ACCOUNT MATCHING PROJECT
This project implements a Key Matching System that uses *fuzzy matching techniques* to link *end customers* with *key accounts* based on textual similarity.
It proceses *customer names*, applies text cleaning and performs similarity analysis to find the best matches.

The project contains six (6) modules. These are:

1. main module: This module executes the process.
2. data_loader: Loads and prepares customer and key account data.
3. text_cleainig: Cleans and standardizes text for matching.
4. similarity_analysis: Performs similarity calculations.
5. fuzzy_matching: Custom fuzzy logic for text comparison.
6. config: Configurations (similarity treshold, paths, etc.).

And the Workflow steps are:

1️⃣ Data Loading (data_loader.py)
- Reads input files:
    - results_end_customer.csv (End Customers List)
    - Key_account_list_full.csv (Key Accounts List)
    - Geography.xlsx (Country Mapping)
- Maps country codes to country names for better consistency.
- Creates original_end_customer, a backup of the original customer name.

2️⃣ Text Cleaning (text_cleaning.py)
- Standardizes text (lowercase conversion).
- Removes special characters (e.g., @, #, !).
- Removes common commercial words (e.g., "service", "group", "solutions").
- Removes legal suffixes (e.g., "S.P.A", "GmbH", "Inc").
- Merges fragmented words ("A T A M S P A" → "ATAM").
- Removes accents ("Málaga" → "Malaga").

3️⃣ Similarity Analysis (similarity_analysis.py)
- Compares desc_end_customer to df_ka['Names'] using fuzzy matching.
- Computes similarity scores with FuzzyWuzzy library, specifically, the token_set_ratio method (fuzz.token_set_ratio).
- Filters out low similarity scores (similarity_threshold).
- Creates a structured output DataFrame (df_comparison_filtered).

4️⃣ Output Processing (create_df_stage())
- Stores original_end_customer along with the final matched key account.
- Ensures correct country-based filtering.
- Fixes indexing issues (roww vs row) to prevent errors.
