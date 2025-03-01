formatted_string = f"""
+---------------------+--------------------------------+
| Field               | Value                          |
+---------------------+--------------------------------+
| Item ID             | asdf                           |
| Product ID          | item                           |
| Product Name        | item                           |
| Product Price       | item                           |
| Product Image URL   | item                           |
| Quantity            | item                           |
| Digital             | item                           |
| Total               | item                           |
| Available Quantity  | item                           |
+---------------------+--------------------------------+
"""

print(formatted_string)






# Write a function that sorts an array card ranks in ascending order
# based on standard playing card ranks. (from lowest to highest) 
cards = ['Jack', 8, 2, 2, 6, 'King', 5, 3, 'Queen', 'King', 'Queen']
# output = [2,2,5,6 8, 3, 'Jack', 'Queen', 'Queen', 'King', 'King']

def sort_deck(cards):
    deck = {2:[], 3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],'Jack':[],'Queen':[],'King':[]
            ,'Ace':[]}
    d_set =set()
    for card in cards:
        deck[card].append(card)
        d_set.add(card)
    output=[]
    
    for k, v in deck.items():
        if k in d_set:
            output += v

    print(output)

sort_deck(cards)

d = {'watermelon': 3, 'apple': 2, 'banana': 1}   
dv = {k: v for k, v in sorted(d.items(), key=lambda item: item[1])}
print(f'dv: {dv}')  


dd = dict(sorted(d.items(), key= lambda item: item[1]))

print(dd)