
import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as
    described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    dot_prod = 0
    for e in vec1:
        if e in vec2:
            dot_prod += vec1[e]*vec2[e]

    return dot_prod/(norm(vec1)*norm(vec2))


sentences = [["i", "am", "a", "sick", "man"],
["i", "am", "a", "spiteful", "man"],
["i", "am", "an", "unattractive", "man"],
["i", "believe", "my", "liver", "is", "diseased"],
["however", "i", "know", "nothing", "at", "all", "about", "my",
"disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]]



def build_semantic_descriptors(sentences):
    d = {}

    for e in sentences:
        d_sentence = {}
        for w in e:
            dd = {}
            for ww in e:
                if w == ww:
                    pass
                elif ww in dd:
                    dd[ww] += 1
                else:
                    dd[ww] = 1

            d_sentence[w] = dd

        for key in d_sentence:
            if key not in d:
                 d[key] = d_sentence[key]
            else:
                for keyy in d_sentence[key]:
                    if keyy not in d[key]:
                        d[key][keyy] = d_sentence[key][keyy]
                    else:
                        d[key][keyy] += d_sentence[key][keyy]


    return d


def build_semantic_descriptors_from_files(filenames):
     res = []
     for i in range(len(filenames)):

         text = open(filenames[i], "r", encoding="latin1").read()\
         .replace(".","#").replace("!","#").replace("?","#").lower().split("#")
         for i in range(len(text)):
             text[i]= text[i].replace(",", "").replace("-", " ").replace(":", "")\
             .replace(";", "").replace("--", " ").replace("\n"," ").split()
         res.extend(text)

     return build_semantic_descriptors(res)


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):

    max_similiar = -2
    vec_word = semantic_descriptors[word]

    x = False

    for choice in choices:
        if choice in semantic_descriptors:
            vec_choice = semantic_descriptors[choice]
        else:
            vec_choice = {}
        for e in vec_choice:
            if x == True:
                break
            if e in vec_word:
                x = True
        if x == False:
            score = -1
        if x == True:
            score = similarity_fn(vec_word,vec_choice)
        if score>max_similiar:
            chosen_word = choice
            max_similiar = score

    return chosen_word




def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    tot=0
    cur_right = 0
    lines = open(filename, "r", encoding="latin1").readlines()
    for i in range(len(lines)):
        all_words = lines[i].split()
        word = all_words[0]
        correct_ans = all_words[1]
        choices = all_words[2:]

        guess = most_similar_word(word,choices,semantic_descriptors,similarity_fn)
        if guess == correct_ans:
            tot +=1
            cur_right += 1
        else:
            tot +=1
    print(tot)
    print(cur_right)

    return cur_right/tot*100





if __name__ =="__main__":

    #vec1 = {"i": 3, "am": 3, "a": 2, "sick": 1, "spiteful": 1, "an": 1, "unattractive": 1}
    #vec2 = {"i": 1, "believe": 1, "my": 1, "is": 1, "diseased": 1}
    #print(cosine_similarity(vec1,vec2))

    #ddd = build_semantic_descriptors(sentences)

    semantic_descriptors = build_semantic_descriptors_from_files(["file1.txt","file2.txt"])

    print(run_similarity_test("test.txt", semantic_descriptors, cosine_similarity))
