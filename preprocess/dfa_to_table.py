# Python program to read
# json file
 
 
import json
 
# Opening JSON file
f = open('dfa.json',)
 
# returns JSON object as
# a dictionary
data = json.load(f)
 
# Iterating through the json list

number_or_states = len(data['states'])

print(number_or_states)
#for state in data['states']:
    #print(state['end'])
 
# Closing file
f.close()