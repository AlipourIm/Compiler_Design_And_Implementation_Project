import bs4


def get_tables(html_doc):
    soup = bs4.BeautifulSoup(html_doc, features="html.parser")
    return soup.findAll('table')


with open('grammar_first_follow_set.html', 'r') as f:
    webpage = f.read()
    tables = get_tables(webpage)


def make_list(table):
    result = []
    all_rows = table.findAll('tr')
    for row in all_rows:
        result.append([])
        all_cols = row.findAll('td')
        for col in all_cols:
            the_strings = [str(s) for s in col.findAll(text=True)]
            the_text = ' '.join(the_strings)
            result[-1].append(the_text)
    return result


first_table = make_list(tables[0])
follow_table = make_list(tables[1])
predict_table = make_list(tables[2])

first = []
follow = []
predict = []
non_terminals = []
# terminals = ['ID', ';', '[', 'NUM', ']', '(', ')', 'int', 'void', ',', '{', '}', 'break', 'if', 'endif', 'else',
# 'repeat', 'until', 'return', '=', '<', '==', '+', '-', '*', '$']

for i in range(1, len(first_table)):
    first.append(first_table[i][1].split())
    follow.append(follow_table[i][1].split())
    non_terminals.append(first_table[i][0])

for i in range(len(follow)):
    for j in range(len(follow[i])):
        if follow[i][j] == '┤':
            follow[i][j] = '$'

for i in range(1, len(predict_table)):
    predict.append(predict_table[i][1].split())

for i in range(len(predict)):
    for j in range(len(predict[i])):
        if predict[i][j] == '┤':
            predict[i][j] = '$'

terminals = sorted(set().union(*first).union(*follow))
terminals.remove('ε')

with open("../../FirstFollowPredict.py", "w") as f:
    f.write("class first_follow_predict:\n\tfirsts = ")
    f.write(str(first))
    f.write("\n\tfollows = ")
    f.write(str(follow))
    f.write("\n\tpredicts = ")
    f.write(str(predict))
    f.write("\n\tnon_terminals = ")
    f.write(str(non_terminals))
    f.write("\n\tterminals = ")
    f.write(str(terminals))
    f.write("\n")
