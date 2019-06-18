import urllib.request
import json

"""
Takes a json file and converts it to a list, finds indexes of searched items, 
their values and prints them out  
"""

# FINAL VERSION: June 11, 2019

def user_input(prompt=None):
    return input(prompt)


def convert_json_to_list(url):
    if url > str(''):
        # Gets the webpage and reads its content
        doc_page = urllib.request.urlopen(url)
        webpage_text = doc_page.read()
        # Converts json file
        jsondata = json.loads(webpage_text)
        treedata = json.dumps(jsondata['tree'], indent=2)
        # split() method returns a list of strings after breaking the given string by the specified separator
        splitdat = treedata.split()

        return splitdat

    else:
        print("URL is missing. Exiting")
        exit()


def json_splits(splitdat, word):
    # gets the indexes of all required items
    matchedi = []
    i = 0
    length = len(splitdat)

    while i < length:
        if word == splitdat[i]:
            matchedi.append(i)
        i += 1

    return matchedi


def json_indexs(matchedi, splitdat, word):
    # calculates indexes of the item next to the above indexes and gets all their values
    mplus = []
    length2 = len(matchedi)
    index_values = []

    print(f'VALUES OF {word} INDEXES: \n')

    for j in range(length2):
        mplus.append(matchedi[j] + 1)

        index_values2 = splitdat[mplus[j]]

        index_values.append(splitdat[mplus[j]])

        print(index_values2)

    return index_values


def json_values(index_values, matchedi, splitdat, word):
    count = splitdat.count(word)

    if matchedi > [] or count > 0:
        print(' ')
        print(f'String >>{word}<< was found in the list >>{count}<< times')
        print(' ')

    elif word == str(''):
        print("String is missing. Exiting")
        exit()

    else:
        print('')
        print(f'!!! String >>{word}<< was not found in the list !!!')
        print('')


def main():
    url = input('Webapge address: ')
    print(" ")
    word = input('Search this string: ')
    print('')

    splitdats = convert_json_to_list(url)
    indexed_slugs = json_splits(splitdats, word)
    values_of_indexes = json_indexs(indexed_slugs, splitdats, word)
    counting = json_values(values_of_indexes, indexed_slugs, splitdats, word)

    # Prints the complete list created out of the json file
    # print("COMPLETE LIST: ", splitdats)
    # Prints the indexes of the searched items in the list
    # print("ITEM INDEXES: ", indexed_slugs)
    print("VALUES OF INDEXES: \n", values_of_indexes)

    return


if __name__ == "__main__":
    main()

