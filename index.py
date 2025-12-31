"""
a program to aid in decision-making
"""
from my_python_package_custom_package import my_module
def eisenhower_matrix(): 
    urgent = my_module.yn("is this task urgent?")
    important = my_module.yn("is this task important?")
    if urgent and important:
        print("Do it now.")
    elif not urgent and important:
        print("Schedule a time to do it.")
        call_when = yn("would you like me to helo you schedule a time?")
        if call_when:
            when()
    elif urgent and not important:
        print("Delegate it if possible.")
    else:
        print("Eliminate it.")

def when():


def read_logs():


while True:
    print("how may i help you? ")
    print("""1 - """) 