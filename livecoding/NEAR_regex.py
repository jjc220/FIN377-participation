def NEAR_regex(list_of_words,max_words_between=5,partial=False,cases_matter=False):
            
    from itertools import permutations
    
    start = r'(?:\b' # the r means "raw" as in the backslash is just a backslash, not an escape character
    
    if partial:
        gap   = r'[A-Za-z]*\b(?: +[^ \n\r]*){0,' +str(max_words_between)+r'} *\b'
        end   = r'[A-Za-z]*\b)'
    else:
        gap   = r'\b(?: +[^ \n]*){0,' +str(max_words_between)+r'} *\b'
        end   = r'\b)'
        
    regex_list = []
    
    for permu in list(permutations(list_of_words)):
        # catch this permutation: start + word + gap (+ word + gap)... + end
        if cases_matter: # case sensitive - what cases the user gives are given back
              regex_list.append(start+gap.join(permu)+end)           
        else: # the resulting search will only work if all words are lowercase
            lowerpermu = [w.lower() for w in permu]
            regex_list.append(start+gap.join(lowerpermu)+end)
    
    return '|'.join(regex_list)