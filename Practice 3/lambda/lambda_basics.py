#Lambda functions are powerful when used inside other functions.
#They can multiply a given value by an unknown number.
def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)

print(mydoubler(11))