import json


result = 1
json_obj = { "result": result} 


#print(json_str)

print( json.dumps({ "result": result}))