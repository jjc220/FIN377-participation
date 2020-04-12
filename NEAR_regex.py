{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "0\n",
      "1\n",
      "0\n",
      "0\n",
      "0\n",
      "1\n",
      "0\n",
      "0\n",
      "1\n"
     ]
    }
   ],
   "source": [
    "def NEAR_regex(list_of_words,max_words_between=5,partial=False,cases_matter=False):\n",
    "    '''\n",
    "    Parameters\n",
    "    ----------\n",
    "    list_of_words : list\n",
    "        A list of \"words\", each element is a string\n",
    "        \n",
    "        This program will return a regex that will look for times where word1 \n",
    "        is near word2, or word2 is near word 1.\n",
    "        \n",
    "        It works with multiple words: You can see if words1 is near word2 or\n",
    "        word3. \n",
    "        \n",
    "    max_words_between : int, optional\n",
    "        How many \"words\" are allowed between words in list_of_words. The default\n",
    "        is 5, but you should consider this carefully.\n",
    "        \n",
    "        \"words\" in between are chunks of characters. \"DON don don- don12 2454\" \n",
    "        is 5 words.\n",
    "        \n",
    "        This will not allow matches if the words are separated by a newline \n",
    "        (\"\\n\") character.\n",
    "        \n",
    "    partial : Boolean, optional\n",
    "        If true, will accept longer words than you give. For example, if one \n",
    "        word in your list is \"how\", it will match to \"howdy\". Be careful in \n",
    "        choosing this based on your problem. Partial makes more sense with \n",
    "        longer words. \n",
    "        The default is True.\n",
    "        \n",
    "    cases_matter: Boolean, optional bt IMPORTANT\n",
    "        If True, will return a regex string that will only catch cases where  \n",
    "        words in the string have the same case as given as input to this \n",
    "        function. For example, if one word here is \"Hi\", then the regex \n",
    "        produced by this function will not catch \"hi\".\n",
    "        \n",
    "        If false, will return a regex string that will only work if all letters\n",
    "        in search string are lowercase.\n",
    "        \n",
    "        The default is True.\n",
    "     \n",
    "        \n",
    "    Warning / Feature\n",
    "    -------\n",
    "    This WILL NOT \n",
    "    \n",
    "        \n",
    "    Unsure about speed\n",
    "    -------\n",
    "    I don't think this is a very \"fast\" function, but it should be robust. \n",
    "  \n",
    "    \n",
    "    Suggested use\n",
    "    -------\n",
    "    a_string_you_have = 'Jack and Jill went up the hill'\n",
    "    \n",
    "    # 1. define words and set up the regex\n",
    "    words = ['jack','hill']                         \n",
    "    rgx = NEAR_regex(words)                       \n",
    "    \n",
    "    # 2. convert the string to lowercase before searching!\n",
    "    a_string_you_have = a_string_you_have.lower()   \n",
    "    \n",
    "    # 3. len+findall+rgx = counts the number of times the word groups are close\n",
    "    count = len(re.findall(rgx,test))              \n",
    "    print(count)                                 \n",
    "    \n",
    "    Returns\n",
    "    -------\n",
    "    A string which is a regex that can be used to look for cases where all the \n",
    "    input words are near each other.\n",
    "    '''\n",
    "               \n",
    "    from itertools import permutations\n",
    "    \n",
    "    start = r'(?:\\b' # the r means \"raw\" as in the backslash is just a backslash, not an escape character\n",
    "    \n",
    "    if partial:\n",
    "        gap   = r'[A-Za-z]*\\b(?: +[^ \\n\\r]*){0,' +str(max_words_between)+r'} *\\b'\n",
    "        end   = r'[A-Za-z]*\\b)'\n",
    "    else:\n",
    "        gap   = r'\\b(?: +[^ \\n]*){0,' +str(max_words_between)+r'} *\\b'\n",
    "        end   = r'\\b)'\n",
    "        \n",
    "    regex_list = []\n",
    "    \n",
    "    for permu in list(permutations(list_of_words)):\n",
    "        # catch this permutation: start + word + gap (+ word + gap)... + end\n",
    "        if cases_matter: # case sensitive - what cases the user gives are given back\n",
    "              regex_list.append(start+gap.join(permu)+end)           \n",
    "        else: # the resulting search will only work if all words are lowercase\n",
    "            lowerpermu = [w.lower() for w in permu]\n",
    "            regex_list.append(start+gap.join(lowerpermu)+end)\n",
    "    \n",
    "    return '|'.join(regex_list)\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "import re\n",
    "\n",
    "test  = 'This is a partial string another break with words'\n",
    "words = ['part','with']\n",
    "rgx   = NEAR_regex(words)\n",
    "print(len(re.findall(rgx,test)))            # no match (partials not allowed) - good!\n",
    "\n",
    "rgx = NEAR_regex(words,partial=True)\n",
    "print(len(re.findall(rgx,test)))            # match (partials allowed) - good!\n",
    "\n",
    "rgx   = NEAR_regex(words,partial=True,max_words_between=1)\n",
    "print(len(re.findall(rgx,test)))            # no match (too far apart) - good!\n",
    "\n",
    "words = ['part','With']\n",
    "rgx   = NEAR_regex(words,partial=True,cases_matter=True)\n",
    "print(len(re.findall(rgx,test)))\n",
    "\n",
    "words = ['part','with','this']\n",
    "rgx = NEAR_regex(words,partial=True)\n",
    "print(len(re.findall(rgx,test)))           # no match - good! \"This\" != \"this\"\n",
    "print(len(re.findall(rgx,test.lower())))    # match - good!\n",
    "\n",
    "test  = 'This is a partial string \\n another break with words'\n",
    "words = ['part','with']\n",
    "rgx = NEAR_regex(words,partial=True)\n",
    "print(len(re.findall(rgx,test)))            # fails because of the \\n break\n",
    "\n",
    "test  = 'This is a partial string \\r another break with words'\n",
    "words = ['part','with']\n",
    "rgx = NEAR_regex(words,partial=True)\n",
    "print(len(re.findall(rgx,test)))            # fails with \\r too.\n",
    "\n",
    "test  = 'This is a partial string                      another break with words'\n",
    "words = ['part','with']\n",
    "rgx = NEAR_regex(words,partial=True)\n",
    "print(len(re.findall(rgx,test)))            # extra spaces don't affect"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
