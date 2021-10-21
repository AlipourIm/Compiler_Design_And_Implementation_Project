import json


def get_chars_by_symbol(symbl):
    symbol_dict = {
        "d": "0123456789",
        "l": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "s": ";:,[](){}+-<",
        "/": "/",
        "*": "*",
        "n": "\n",
        "z": "Ā",
        "=": "=",
        "w": " \r\t\v\f"
    }
    valid_chars = "".join(symbol_dict.values())

    if symbl != "o":
        return symbol_dict[symbl]
    else:
        chars = ""
        for i in range(257):
            if chr(i) not in valid_chars:
                chars += chr(i)
        return chars


if __name__ == "__main__":

    # Opening JSON file
    f = open("dfa.json", )
    data = json.load(f)

    # Create 2d-array for DFA table
    number_of_states = len(data["states"])
    number_of_chars = 257
    DFA_Table = [[-1 for i in range(number_of_chars)] for j in range(number_of_states)]

    # Print alphabet
    # my_string = ""
    # print(data["alphabet"])
    # for symbol in data["alphabet"]:
    #     print(f"symbols: {symbol}, chars matching: \"{get_chars_by_symbol(symbol)}\"")
    #     my_string += get_chars_by_symbol(symbol)
    # print(len(my_string))

    # Iterate through states
    final_states = []
    lookahead_states = []

    for state in data["states"]:
        if state["name"][-1] == "*":
            lookahead_states.append(state["id"])
        if state["end"]:
            final_states.append([state["id"], state["label"]])

    print(final_states)
    print(lookahead_states)

    # Closing file
    f.close()

    # with open('final_states.txt', 'w') as file2:
    #     for state in final_states:
    #         file2.write(str(state) + "\n")
    # with open('look_ahead_states.txt', 'w') as file3:
    #     for state in lookahead_states:
    #         file3.write('%s ' % state)
    #     file3.close()

    # Iterate through edges
    for edge in data["transitions"]:
        state_src_id = edge["state_src_id"]
        state_dst_id = edge["state_dst_id"]

        # print(f"{state_src_id} -> {state_dst_id} (", end="")
        for symbol in edge["symbols"]:
            # print(symbol, end=", ")
            for char in get_chars_by_symbol(symbol):
                # print(f"{state_src_id} , {ord(char)}")
                DFA_Table[state_src_id][ord(char)] = state_dst_id
        # print("\b\b)")

    # Save in file
    # with open("DFA_Table.txt", "w") as f:
    #     for s in DFA_Table:
    #         f.write(str(s) + "\n")

    with open("../DFA.py", "w") as f:
        f.write("class DFA:\n\tdfa_table = ")
        f.write(str(DFA_Table))
        f.write("\n\tfinal_states = ")
        f.write(str(final_states))
        f.write("\n\tlook_ahead_states = ")
        f.write(str(lookahead_states))
        f.write("\n")

    # Restore from file
    # DFA_Table = []
    # with open("DFA_Table.txt", "r") as f:
    #     for line in f:
    #         DFA_Table.append(line.strip('][').replace('"', '').split(','))
