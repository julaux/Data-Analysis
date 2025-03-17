from rapidfuzz import fuzz
import re


def full_word_in_text(word, text):
    """
    Ensures that a word appears fully in the text, not as a substring.
    """
    # ENSURE THE WORD LIMITS
    pattern = rf'\b{re.escape(word)}\b'
    return bool(re.search(pattern, text))

def similarity(a, b, ka_account, country_code):
    """
    Calculates similarity using fuzz.token_set_ratio but penalizes cases where
    only one word is common and the rest are different.
    Takes into account the key account name.

    If ka_name is entirely in the kcc_nanme column -> score = 100
    If generic words match but the key account name is different -> penalizes the score.

    Args:
        - a: Is the variable for the Dataset from Results End Customer name (desc_end_customer / kcc_name)
        - b: The variable for the KA name (ka_name)
        - ka_account: Key Account Name (Se remueve el "KA-")

    Returns:
        Return a penalized score if is necessary.
    """
    # EXTRACT THE KEY ACCOUNT NAME, REMOVE THE LETTERS "KA-"
    core_ka_name = ka_account.replace("KA-", "").strip().lower()

    # VERIFY THAT ka_name AND THE VALUE OF THE COLUMN key_account APPEAR COMPLETELY IN in kcc_name
    if full_word_in_text(a, b) and full_word_in_text(core_ka_name, a):
        return 100


    # CALCULATING THE SIMILARITY SCORE 
    base_score = fuzz.token_set_ratio(a, b)

    # TOKENYZE THE WORDS
    words_a = set(a.split())
    words_b = set(b.split())

    # IF THE KEY ACCOUNT NAME APPEARS BOTH STRINGS OF a AND b, KEEP THE FULL SCORE
    if core_ka_name in words_a and core_ka_name in words_b:
        return round(base_score, 2)
    
    # WORDS IN COMMON (EXCLUDE KA-Account name)
    common_words = words_a.intersection(words_b) - {core_ka_name}

    return round(base_score, 2)