import xmlrpc.client
from datetime import datetime

proxy = xmlrpc.client.ServerProxy("http://localhost:8000")

def createNewNote():
  try:
    # Get data as user input
    topic = input("Topic: ")
    title = input("Title: ")
    text = input("Text: ")
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Initiate the remote procedure call and handle response
    success = proxy.createNewNote(topic, title, text, timestamp)
    if(success == True):
      print("Note '{}' created".format(title))
    else:
      raise Exception("Internal server error")
  except:
    print("Something went wrong, try again")

def getNotes():
  try:
    # User input
    topic = input("Topic to get notes from: ")
    while(len(topic) == 0):
      topic = input("Topic can not be empty! Enter topic again: ")

    # Initiate the remote procedure call and print notes
    notes = proxy.getNotes(topic)
    if(notes == False):
      raise Exception("Internal server error")
    elif(len(notes) == 0):
      print("No notes found")
    else:
      for note in notes:
        print()
        print("Title: {}".format(note[0].strip()))
        print(note[1].strip())
        print(note[2].strip())
  except:
    print("Something went wrong, try again")

# Menu loop
while True:
  try:
    print("1. Create new note")
    print("2. Get notes")
    print("3. Exit")
    choice = input("What you want to do: ")
    if choice == "1":
      createNewNote()
      print()
    elif choice == "2":
      getNotes()
      print()
    elif choice == "3":
      break
    else:
      print("Invalid choice. Enter 1, 2 or 3\n")
  except KeyboardInterrupt:
    print("Canceling...\n")
    continue
