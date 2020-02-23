# Python Code for checking the number is 3 digit or not.... Written by Shiraz Musaddique
i=int(input("Enter your number:"))
if (i < 1000 and i > 99):
  print(i, "is a 3 digit number ")
else:
  print(i, "is not a 3 digit number ")
