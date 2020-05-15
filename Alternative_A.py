import math
import copy
import collections


#Inverted index A, input is the filename and output are 
#dictionary, size of the dictionar and sum of length of the posting lists.
def get_inverse_index(file):
    # Create an inverted index dictionary
    PostingDic = {}
    with open(file, "r", encoding="UTF-8")as f:
        terms = f.readlines()
        for term in terms:
            word, docID = term.split(" ")
            docID = int(docID.strip('\n'))
            if word not in PostingDic.keys():
                PostingDic[word] = [docID]
            else:
                PostingDic[word].append(docID)
    
    # Write the dictionat into a json file.
    save_name = file+".json"
    f = open(save_name,'w', encoding="UTF-8")
    f.write(str(PostingDic))
    f.close()
    
    return PostingDic, len(PostingDic.keys()), len_posting(PostingDic) 

# a function to return the length of
# the total length of posting lists in dictionary.
def len_posting(PostingDic):
    len_of_posting = 0
    for value in PostingDic.values():
        len_of_posting += len(value)
    return len_of_posting

# Save the posting lists in dictionaries and print the length and sum of lists. 
_, words_orig, sum_orig = get_inverse_index("index.txt")
lower_dict, words_lower, sum_lower = get_inverse_index("lower_index.txt")

print(f"Before lowering the terms: size of the dic and sum of lenght of postings are {words_orig}, {sum_orig}")
print(f"\nAfter lowering the terms: size of the dic and sum of lenght of postings are {words_lower}, {sum_lower}") 

# Find stop words and get the index number
# eliminating the stop words.
Sorted_dic = sorted(lower_dict.items(), key=lambda item: len(item[1]), reverse= True)
Stop_words = [word[0] for word in Sorted_dic][:10] 
for word in Stop_words:
    del lower_dict[word]

# Print the index with and without stop words.
print(f"The index with and without stop words are: {len_posting(lower_dict)}, {sum_lower}")

# Boolean queries A
# single word query for ’school’, 'kids' and 'really'.
school_query, kids_query, really_query = lower_dict["school"], lower_dict["kids"], lower_dict["really"]


# function to process two lists.
def intersect1(ls1, ls2):
    answer = []
    index1, index2 = 0, 0
    while compare(index1, len(ls1)-2) and compare(index2, len(ls2)-2):
        if is_equal(ls1[index1], ls2[index2]):
            answer.append(ls1[index1])
            index1 += 1
            index2 += 1
        elif compare(ls1[index1], ls2[index2]):
            index1 += 1
        else:
            index2 += 1
    return answer

#define two comparing functions which also account how many times 
# it is used.
counter = 0
def is_equal(value1, value2):
    global counter
    counter += 1
    return value1 == value2

def compare(value1, value2):
    global counter
    counter += 1
    return value1 <= value2

# a function which gets the interception of a word list.
def intersect_orig(term_ls):
    term = {}
    for word in term_ls:
        term[word] = lower_dict[word]
    result = term[list(term.keys())[0]]
    del term[list(term.keys())[0]]
    while len(term) != 0 and len(result)!= 0:
        result = intersect1(result, term[list(term.keys())[0]])
        del term[list(term.keys())[0]] 
    return result, counter

# An optimized function which gets the intercept of a word list based on your postings. 
def intersect_opt(term_ls):
    term = {}
    for word in term_ls:
        term[word] = lower_dict[word]
    term = sorted(term.items(), key=lambda item: len(item[1]))
    result = term[0][1]
    del term[0]
    while len(term) != 0 and len(result)!= 0:
        result = intersect1(result, term[0][1])
        del term[0]    
    return result, counter

print(intersect_orig(["really", "kids", "school"]))
# result is ([72, 224, 385], 498)

print(intersect_opt(["really", "kids", "school"]))

# resul is ([72, 224, 385], 809), -meaning the comparison time is (809-498) = 311.

# TF/IDF weighting 
# create a dictionary which stores the idf score for each term
idf_dic = copy.deepcopy(lower_dict)
with open("term_freq.txt", "r", encoding ="UTF-8") as f:
    lines = f.readlines()
    doc_num = lines[-1].split(" ")[-1]
    for key in idf_dic.keys():
        idf_dic[key] = math.log10(int(doc_num)/len(idf_dic[key]))


# create a tf_idf dictionary to store the different 
# tf-idf score of three term in different documents
ID_ls, _ = intersect_opt(["really", "kids", "school"])
word_tf_idf = {}
word_tf_idf["school"] = []
word_tf_idf["kids"] = []
word_tf_idf["really"] = []
with open("term_freq.txt", "r", encoding="UTF-8") as f:
    lines = f.readlines()
    for line in lines:
        count, word, doc_ID = line.strip().split(" ")
        if int(doc_ID) in ID_ls:
            if word == "school":
                word_tf_idf["school"].append((float(count)*idf_dic["school"], doc_ID))
            elif word == "kids":
                word_tf_idf["kids"].append((float(count)*idf_dic["kids"], doc_ID))
            elif word == "really":
                word_tf_idf["really"].append((float(count)*idf_dic["really"], doc_ID))

print(word_tf_idf)
