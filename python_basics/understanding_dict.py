sample_dict = {"name": "aryan","exp": 9,"location": "india"}
#print(sample_dict)
#print(type(sample_dict))

# NO INDEXING ON A DICT OBJECT
#print(sample_dict['location'])

#NESTED DICT
complex_data = {"name": "john","info":{"exp": 5, "location": "usa"}}
#print(complex_data['info']['location'])

# DICT WITH LIST
complex_data = {"org": "networknuts","employees":["john","jane","aryan"]}
print(complex_data['employees'][1])