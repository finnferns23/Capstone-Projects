import json
import pandas as pd
import requests # you need this module to make an API call

api_url = "http://api.open-notify.org/astros.json" # this url gives use the astronaut data
response = requests.get(api_url) # Call the API using the get method and store the
                                # output of the API call in a variable called response.
if response.ok:             # if all is well() no errors, no network timeouts)
    data = response.json()  # store the result in json format in a variable called data
                            # the variable data is of type dictionary.

print(data)   # print the data just to check the output or for debugging
print(data.get('number'))
astronauts = data.get('people')
print("There are {} astronauts on ISS".format(len(astronauts)))
print("And their names are :")
for astronaut in astronauts:
    print(astronaut.get('name'))
#Import required libraries
api_url="http://127.0.0.1:5000/data"
def get_number_of_jobs_T(technology):
    
    #your code goes here
    return technology,number_of_jobs
get_number_of_jobs_T("Python")
def get_number_of_jobs_L(location):
    
    #your coe goes here
    return location,number_of_jobs
#your code goes here

#your code goes here

# your code goes here
# your code goes here
#your code goes here
#your code goes here
# your code goes here
