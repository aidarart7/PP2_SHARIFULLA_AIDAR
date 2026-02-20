#Functions can send data back to the code that called them using the return statement.
#When a function reaches a return statement, it stops executing and sends the result back:
def get_greeting():
  return "Hello from a function"

message = get_greeting()
print(message)