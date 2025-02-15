from terminaltables import AsciiTable
from random import randint
from os import system, name
from time import sleep
import functools

def clear():
  if name == "nt":
    _ = system("cls")
  else:
    _ = system("clear")

def saveroll(density, count, times):
  header_data = [
    ['Save Dice Information']
  ]
  body_data = [
    ['Option', 'Value'],
    ['Number of Sides', density],
    ['Number of Dice', count],
    ['Number of Rolls', times],
    ['Filename', "N/A"]
  ]
  header = AsciiTable(header_data)
  body1 = AsciiTable(body_data)
  clear()
  print(header.table)
  print(body1.table)
  print("Saving Dice information")
  print("Please enter a filename (Don't Include Extensions)")
  filename = input("save>")
  if filename == "":
    print("Please enter a filename!")
    input("retry>")
    saveroll(density, count, times)
    return
  body_data[4][1] = filename + ".dice"
  body2 = AsciiTable(body_data)
  clear()
  print(header.table)
  print(body2.table)
  print("Saving dice information to \"{}.dice\"".format(filename))
  file = open("{}.dice".format(filename), 'w')
  file.write("{}:{}:{}".format(density, count, times))
  file.close()
  sleep(3)
  print("Saved!")
  input("back>")
  return

def rolldice(density, count, times):
  print("Rolling {} {}-sided dice/s {} times".format(count, density, times))
  ccount = int(times) - 1
  sleep(3)
  header_data = [
    ['Dice Rolls']
  ]
  rolls = []
  i = 0
  while i <= int(ccount):
    roll = str(randint(1,int(density)))
    s = 1
    while s < int(count):
      roll += ":" + str(randint(1,int(density)))
      s += 1
    rolls.append(roll)
    i += 1
  #print(rolls)
  showresults(rolls, density, count, times)
  return

def showresults(rolls, density, count, times):
  q = 0
  menu_data = [
    ['Title', 'Value', 'Total', 'Average']
  ]

  while q < len(rolls):
    croll = rolls[q]
    crollsplit = croll.split(":")
    crollint = []
    for number in crollsplit:
      crollint.append(int(number))
    averageRoll = sum(crollint) / len(crollint)
    totalRoll = functools.reduce(lambda a, b: a+b, [int(number) for number in crollsplit])
    menu_data.append(['Roll {}'.format(str(int(q) + 1)), croll, totalRoll, averageRoll])
    q += 1

  header = AsciiTable(header_data)
  menu = AsciiTable(menu_data)
  clear()
  print(header.table)
  print(menu.table)
  print("To view advanced metrics, type \"metrics\"")
  print("To save the information of the current dice to a file, type \"save\" now")
  print("To roll again with the same settings, type \"reroll\"")
  choice = input("metrics/save/reroll/back>")
  if choice.upper() == "SAVE" or choice.upper() == "S" or choice.upper() == "SAVEROLL":
    saveroll(density, count, times)
    return
  elif choice.upper() == "REROLL" or choice.upper() == "R":
    confirmroll(density, count, times)
    return
  elif choice.upper() == "METRICS" or choice.upper() == "M":
    showmetrics(rolls) # TODO: Make the return after this function go back to the original results display (refactoring most of this code will likely be required)
    showresults(rolls, density, count, times)
    return
  else:
    return


def confirmroll(density, count, times):
  print("Is this data okay? [y/N]")
  print("{} {}-sided dice/s are to be rolled {} times".format(count, density, times))
  choice = input("confirm>")
  c = choice.upper()
  if c == "Y":
    rolldice(density, count, times)
  elif c == "N":
    return
  else:
    print("Invalid Option, exiting...")
    return

def newroll():
  header_data = [
    ['New Dice Roll']
  ]
  header = AsciiTable(header_data)
  body_data = [
    ['Option', 'Value'],
    ['Number of Sides','N/A'],
    ['Number of Dice', 'N/A'],
    ['Number of Rolls', 'N/A']
  ]
  body1 = AsciiTable(body_data)
  clear()
  print(header.table)
  print(body1.table)
  print("How many sides should each dice have?")
  sides = input("setup[1/3]>")
  if sides == "":
    print("Please enter a value!")
    input("back>")
    return
  elif int(sides) is None:
    print("Please enter a Number!")
    input("back>")
    return
  else:
    density = str(int(sides))
    body_data[1][1] = density
    body2 = AsciiTable(body_data)
    clear()
    print(header.table)
    print(body2.table)
    print("How many Dices should be rolled?")
    nod = input("setup[2/3]>")
    if nod == "":
      print("Please enter a value!")
      input("back>")
      return
    elif int(nod) is None:
      print("Please enter a number!")
      input("back>")
      return
    else:
      dice = str(int(nod))
      body_data[2][1] = dice
      body3 = AsciiTable(body_data)
      clear()
      print(header.table)
      print(body3.table)
      print("How many times should the dice be rolled?")
      ttr = input("setup[3/3]>")
      if ttr == "":
        print("Please enter a value!")
        input("back>")
        return
      elif int(ttr) is None:
        print("Please enter a number!")
        input("back>")
        return
      else:
        times = str(int(ttr))
        body_data[3][1] = times
        body4 = AsciiTable(body_data)
        clear()
        print(header.table)
        print(body4.table)
        confirmroll(density, dice, times)

def importroll():
  print("Type the filename of the dice data you would like to import (don't include any extensions)")
  filename = input("file>") + ".dice"
  print("Opening file!")
  try:
    file = open(filename, "r")
  except FileNotFoundError:
    print("ERROR: The file specified could not be found!")
    input("back>")
    return
  except Exception as e:
    print("An unexpected error has ocurred! Please try again. If you file a bug report please include this text: \"{}\"".format(e))
  if file is None:
    print("Invalid file name!")
    input("back>")
  else:
    info = file.readlines()[0]
    data = info.split(':')
    dicedensity = data[0]
    dicecount = data[1]
    dicetimes = data[2].strip("\n")
    confirmroll(dicedensity, dicecount, dicetimes)

def showmetrics(rolls):
  title_data = [
    ["Advanced Metrics"]
  ]
  body_data = [
    ["Metric", "Best roll", "Value"]
  ]
  definedmetrics = ["Highest Total", "Highest Average"]
  definedresults = []
  splitrolls = []
  rolltotals = []
  rollaverages = []
  for roll in rolls:
    croll = roll.split(":")
    splitrolls.append(croll)
    introll = []
    for number in croll:
      introll.append(int(number))
    rolltotals.append(sum(introll))
    rollaverages.append(sum(introll) / len(introll))
  
  besttotal = {"idx": -1, "val": 0}
  bestaverage = {"idx": -1, "val": 0}
  
  currentIndex = 0

  while currentIndex < len(rolltotals):
    total = rolltotals[currentIndex]
    if total > besttotal["val"]:
      besttotal = {"idx": currentIndex, "val": total}
    currentIndex += 1
  
  currentIndex = 0

  while currentIndex < len(rollaverages):
    average = rollaverages[currentIndex]
    if average > bestaverage["val"]:
      bestaverage = {"idx": currentIndex, "val": average}
    currentIndex += 1
  
  definedresults.append(besttotal)
  definedresults.append(bestaverage)

  cI = 0
  while cI < len(definedmetrics):
    metric = definedmetrics[cI]
    metricresult = definedresults[cI]
    toadd = [metric, "Roll {}".format(metricresult["idx"] + 1), str(metricresult["val"])]
    body_data.append(toadd)
    cI += 1
  
  titletable = AsciiTable(title_data)
  bodytable = AsciiTable(body_data)
  clear()
  print(titletable.table)
  print(bodytable.table)
  input("back>")

menuoptions = {
  "1": newroll,
  "2": importroll,
  "q": quit
}

def choicerror():
  print("That is not a valid option!")
  input("back>")
  return

while True:
  clear()
  header_data = [
    ['Main Menu']
  ]
  menu_data = [
    ['Option', 'Function'],
    ['1', 'New Dice Roll'],
    ['2', 'Import Dices from File'],
    ['q', 'quit']
  ]
  header = AsciiTable(header_data)
  menu = AsciiTable(menu_data)
  print(header.table)
  print(menu.table)
  choice = input("menu>")
  func = menuoptions.get(choice, choicerror)
  func()
