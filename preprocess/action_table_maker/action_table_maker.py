from FirstFollowPredict import FirstFollowPredict as ffp

with open('../first_follow_maker/c_minus_grammar.txt') as f:
    lines = f.read().splitlines()

n = len(ffp.non_terminals)
state_counter = 2 * len(ffp.non_terminals)

edges = []
grammars_states = []

for i in range(len(lines)):
    splitted = lines[i].replace(' $', '').split(' ')
    nt = splitted[0]
    nt_index = ffp.non_terminals.index(nt)

    # print("grammar for ", nt, ": ", splitted[2:])

    if len(splitted[2:]) == 1:
        # edges.append([nt_index, nt_index + n, splitted[2]])
        grammars_states.append([i, nt_index + n])

    else:
        # edges.append([nt_index, state_counter, splitted[2]])
        grammars_states.append([i, state_counter])
        state_counter += 1

        for symbol in splitted[3:-1]:
            edges.append([state_counter - 1, state_counter, symbol])
            state_counter += 1

        edges.append([state_counter - 1, nt_index + n, splitted[-1]])

    # print("state_counter = ", state_counter)
    # print(edges)
    # print(nt_grammars_states)
    # input()

action_table = [[[] for _ in range(len(ffp.terminals))] for _ in range(state_counter)]

######################################################################
# fill action table for start state of each non-terminal, based on which grammar to be used
######################################################################
for [grammar_id, grammar_state] in grammars_states:
    splitted = lines[grammar_id].split(' ')
    nt = splitted[0]
    symbol = splitted[2]
    nt_index = ffp.non_terminals.index(nt)

    for t in ffp.predicts[grammar_id]:
        if symbol in ffp.terminals:
            action_table[nt_index][ffp.terminals.index(t)] = ["get"
                , symbol
                , grammar_state]
        elif symbol in ffp.non_terminals:
            action_table[nt_index][ffp.terminals.index(t)] = ["go"
                , ffp.non_terminals.index(symbol)
                , grammar_state]
        else:
            action_table[nt_index][ffp.terminals.index(t)] = ["go"
                , "ε"
                , grammar_state]

for nt_index in range(len(ffp.non_terminals)):
    for terminal_index in range(len(ffp.follows[nt_index])):
        if len(action_table[nt_index][terminal_index]) == 0:
            action_table[nt_index][terminal_index] = ['sync']

######################################################################
# fill action table for final state of each non-terminal, based on its follow set
######################################################################
for nt_index in range(len(ffp.non_terminals)):
    # for t in ffp.follows[nt_index]:
    for t in ffp.terminals:
        action_table[nt_index + n][ffp.terminals.index(t)] = ['ACCEPT' if nt_index == 0 else 'return']

######################################################################
# fill action table for edges inside each grammar
######################################################################
for e in edges:
    source, target, label = e

    if label in ffp.terminals:
        action_table[source][ffp.terminals.index(label)] = ["get", label, target]

    elif label in ffp.non_terminals:
        nt_index = ffp.non_terminals.index(label)
        # for t in ffp.firsts[nt_index]:
        for t in ffp.terminals:
            if t != 'ε':
                action_table[source][ffp.terminals.index(t)] = ["go"
                    , ffp.non_terminals.index(label)
                    , target]
            # else:
            #     for t2 in ffp.follows[nt_index]:
            #         action_table[source][ffp.terminals.index(t2)] = ["go"
            #             , ffp.non_terminals.index(label)
            #             , target]

######################################################################

print("_____", ffp.terminals)
for i in range(len(action_table)):
    print(f'{i:3d}: ', action_table[i])

######################################################################
# write action table in ActionTable.py

with open("../../ActionTable.py", "w") as f:
    f.write("class ActionTable:")
    f.write("\n\tterminals = ")
    f.write(str(ffp.terminals))
    f.write("\n\tnon_terminals = ")
    f.write(str(ffp.non_terminals))
    f.write("\n\ttable = ")
    f.write(str(action_table).replace(']], [[', ']],\n\t\t\t[['))
