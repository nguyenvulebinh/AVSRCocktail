import re

def format_text(word, w_type):
    def norm_transform(word, w_type):
        word = word.upper()
        strip_list = '.,!?;:\'"-][~+'    
        if w_type == "special_whisper":
            word = word.split("<")[0]
            return word.strip(strip_list)
        
        word = word.strip(strip_list)
        
        if w_type == "word_end_with_punct":
            return word
        elif w_type == "word_with_contractions":
            return word
        elif w_type == "word_with_hyphen":
            return word.replace("-", " ")
        elif w_type == "number_and_percentage":
            if ',' in word:
                word = word.replace(',', '')
            if '.' in word:
                word = word.replace('.', ' point ')
            word = word.replace('%', ' percent')
            return word
        elif w_type == "number_and_dollar":
            word = word.replace('$', '')
            if ',' in word:
                word = word.replace(',', '')
            if '.' in word:
                word = word.replace('.', ' point ')
            return word + " dollar"
            
        elif w_type == "pound_and_number":
            word = word.replace('£', '')
            if ',' in word:
                word = word.replace(',', '')
            if '.' in word:
                word = word.replace('.', ' point ')
            return word + " pound"
        elif w_type == "float_number":
            if '.' in word:
                word = word.replace('.', ' point ')
            if ',' in word:
                word = word.replace(',', '')
            return word
        elif w_type == "domain_name":
            return word.replace('.', ' dot ')
        elif w_type == "abbreviation":
            return word.replace('.', '')        
        else:
            return re.sub(r"[^a-zA-Z0-9' ]", " ", word)
    norm_word = norm_transform(word, w_type)
    norm_word = re.sub(r"\s+", " ", norm_word).upper()
    return norm_word

def is_valid_word(word):
    word = word.lower()
    # Define the regex pattern
    pattern = r'^\w+[.,!?;:]+$'
    word_end_with_punct = bool(re.match(pattern, word))
    if word_end_with_punct:
        return True, "word_end_with_punct"
    
    strip_list = '.,!?;:\'"-][~+'
    
    # words with contractions
    pattern = r"^[A-Za-z]?[a-z]+(?:['’](?:[a-z]{1,2}|m|re|ve|ll|s|t))?$"
    word_with_contractions = bool(re.match(pattern, word.strip(strip_list)))
    if word_with_contractions:
        return True, "word_with_contractions"
    
    # words connect by '-'
    pattern = r"^[a-zA-Z]+(?:-[a-zA-Z]+)+$"
    word_with_hyphen = bool(re.match(pattern, word.strip(strip_list)))
    if word_with_hyphen:
        return True, "word_with_hyphen"
    
    # number and percentage
    pattern = r"^[0-9]+(?:\.[0-9]+)?%$"
    number_and_percentage = bool(re.match(pattern, word.strip(strip_list)))
    if number_and_percentage:
        return True, "number_and_percentage"
    
    # number with 000 and dollar
    number_and_dollar = bool(re.match(r"\d{1,10}[\.,]*(?:,\d{3})*\d*\$$", word.strip(strip_list))) or bool(re.match(r"\$\d{1,10}[\.,]*(?:,\d{3})*\d*$", word.strip(strip_list)))
    if number_and_dollar:
        return True, "number_and_dollar"
    
    # pound and number
    pound_and_number = bool(re.match(r"\d{1,10}[\.,]*(?:,\d{3})*\d*\£$", word.strip(strip_list))) or bool(re.match(r"\£\d{1,10}[\.,]*(?:,\d{3})*\d*$", word.strip(strip_list)))
    if pound_and_number:
        return True, "pound_and_number"
    
    # pattern [a-zA-Z]+<|ru|><|translate|><|en|><|transcribe|>
    pattern = r"^[a-zA-Z]+[.,?!']*<\|\w+\|><\|(translate|transcribe)\|>$"
    special_whisper = bool(re.match(pattern, word.strip(strip_list)))
    if special_whisper:
        return True, "special_whisper"
    
    # float number
    pattern = r"^[0-9]+[\.,]+[0-9]+$"
    float_number = bool(re.match(pattern, word.strip(strip_list)))
    if float_number:
        return True, "float_number"
    
    # abbreviation p.m a.m U.S.A
    pattern = r"[a-z]{1}(\.[a-z]{1})+$"
    abbreviation = bool(re.match(pattern, word.strip(strip_list)))
    if abbreviation:
        return True, "abbreviation"
    
    # domain name
    pattern = r"^[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)+$"
    domain_name = bool(re.match(pattern, word.strip(strip_list)))
    if domain_name:
        return True, "domain_name"
    
    return False, "unknown"

def norm_string(text):
    words = text.strip().split()
    norm_words = []
    
    norm_set = set(['%', '$', '!', '"', '&', '*', '+', ':', '£', '|', '<', '>', '/', ']', ')', '~', '[', '_', '(', '-', '.', ',', '\'', ';', '?', '=', '@', '#', '^', '\\', '`', '{', '}', '}', '’'])
    
    for word in words:
        if set(word) & norm_set:
            _, w_type = is_valid_word(word)
            norm_word = format_text(word, w_type)
        else:
            norm_word = format_text(word, "unknown")
        norm_words.append(norm_word)
    return " ".join(norm_words)

if __name__ == "__main__":
    
    print(norm_string("t_qua ng'_123"))
    
    test_cases = [
        ["I'm Binh i'm 25 years old i'm a AI researcher. It's a good day.", "I'M BINH I'M 25 YEARS OLD I'M A AI RESEARCHER IT'S A GOOD DAY"],   
    ]
    
    for text, ref in test_cases:
        assert norm_string(text) == ref