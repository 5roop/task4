from transliterate import translit
from typing import Set, List
chars_to_remove = {
    '!',
    '"',
    '#',
    '%',
    '&',
    "'",
    '(',
    ')',
    '*',
    '+',
    ',',
    '-',
    '.',
    '/',
    ':',
    ';',
    '<',
    '=',
    '>',
    '?',
    '[',
    ']',
    '_',
    '`',
    '«',
    '°',
    '²',
    '³',
    'µ',
    '·',
    '»',
    '½',
    '‑',
    '–',
    '‘',
    '’',
    '“',
    '”',
    '„',
    '•',
    '…',
    '‰',
    '″',
    '₂',
    '₃',
    '€',
    '™',
    '→',
    '−',
    '∕',
    '😀',
    '😉',
    '🙁',
    '🙂'

}

def remove_chars(input_text: str, chars_to_remove: Set[str] = chars_to_remove) -> str:
    for c in chars_to_remove:
        input_text = input_text.replace(c, "")
    return input_text


def transliterate(input_text: str) -> str:
    from transliterate import translit
    return translit(input_text, "sr", reversed=True)

def is_alpha(token:str) -> bool:
    import re
    pattern = "^[a-zšđčćž]+$"
    compiled_pattern = re.compile(pattern)
    return bool(compiled_pattern.match(token))



def get_N_tokens(N=5000, path="/home/peterr/macocu/taskB/task4/toy_tokens.csv") -> set:
    """Loads tokens from CSV and returns as set of N most important for every language.

    Args:
        N (int, optional): Number of token per language to include. Defaults to 5000.
        path (str, optional): CSV file with token numbers per language. 
            Has columns (token,bswac_head_pp,cnrwac_head_pp,hrwac_head_pp,srwac_head_pp).
            Defaults to "/home/peterr/macocu/taskB/task4/toy_tokens.csv".

    Returns:
        set: set of most important N tokens for every language combination.
    """
    df = pd.read_csv(path, index_col=0)
    NUM_FEATS = N

    for column in df.columns:
        new_column_name = column + "_f"
        corpus_size = df[column].sum()
        df[new_column_name] = df[column] * 1e6 / corpus_size

    N = 1

    df["HR_SR"] = (df["hrwac_head_pp_f"] + N) / (df["srwac_head_pp_f"] + N)
    df["SR_HR"] = (df["srwac_head_pp_f"] + N) / (df["hrwac_head_pp_f"] + N)

    df["HR_CNR"] = (df["hrwac_head_pp_f"] + N) / (df["cnrwac_head_pp_f"] + N)
    df["CNR_HR"] = (df["cnrwac_head_pp_f"] + N) / (df["hrwac_head_pp_f"] + N)

    df["HR_BS"] = (df["hrwac_head_pp_f"] + N) / (df["bswac_head_pp_f"] + N)
    df["BS_HR"] = (df["bswac_head_pp_f"] + N) / (df["hrwac_head_pp_f"] + N)

    df["BS_SR"] = (df["bswac_head_pp_f"] + N) / (df["srwac_head_pp_f"] + N)
    df["SR_BS"] = (df["srwac_head_pp_f"] + N) / (df["bswac_head_pp_f"] + N)

    df["BS_CNR"] = (df["bswac_head_pp_f"] + N) / (df["cnrwac_head_pp_f"] + N)
    df["CNR_BS"] = (df["cnrwac_head_pp_f"] + N) / (df["bswac_head_pp_f"] + N)

    df["CNR_SR"] = (df["cnrwac_head_pp_f"] + N) / (df["srwac_head_pp_f"] + N)
    df["SR_CNR"] = (df["srwac_head_pp_f"] + N) / (df["cnrwac_head_pp_f"] + N)

    combos = ['HR_SR', 'SR_HR', 'HR_CNR', 'CNR_HR', 'HR_BS', 'BS_HR',
              'BS_SR', 'SR_BS', 'BS_CNR', 'CNR_BS', 'CNR_SR', 'SR_CNR']

    important_features = set()

    for lang_comb in combos:
        s = df[lang_comb].sort_values(ascending=False)
        current_features = s.index[:NUM_FEATS].values
        important_features = important_features.union(set(current_features))
    try:
        important_features.remove(np.nan)
    except KeyError:
        pass
    return important_features


def read_and_split_file(path: str) -> List[str]:
    """Reads a text file and returns a list of strings. Every string is a document.
    Expects the input to be corpus where documents are separated with empty lines.
    Returns only the words that are lowercase alpha.

    Args:
        path (str): path of the text file to read.

    Returns:
        List[str]: list of filtered documents.
    """    
    texts = list()
    chunk = ""
    with open(path, "r") as f:
        content = f.readlines()
    for line in content:
        # Handle splits
        if line == "\n":
            texts.append(chunk)
            chunk = ""
        # Filter only lowercase alphabetical words:
        from utils import is_alpha
        line = line.replace("\n", " ")
        words = [w if is_alpha(w) else " " for w in line.split(" ")]
        chunk += " ".join(words)
    return texts

