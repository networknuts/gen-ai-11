def say_hello():
    print("hello world")
    print("hello python")
    print("hello ai")

def say_goodbye():
    print("goodbye world")

def greetings(name):
    print(f"hello {name}")

def add_together(n1=0,n2=0):
    return n1+n2

def create_data(user_name,user_location,user_job):
    return {
        "name": user_name,
        "job": user_job,
        "location": user_location
    }

result = create_data("aryan","india","instructor")
print(result)