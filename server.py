from xmlrpc.server import SimpleXMLRPCServer
import xml.etree.ElementTree as ET

server = SimpleXMLRPCServer(("localhost", 8000))
print("XMLRPC server is running on port 8000")
      
def createNewNote(topic, title, text, timestamp):
  try:
    tree = ET.parse("db.xml")
    root = tree.getroot()

    # Check if topic exists and create it if not
    topicElement = root.find("topic[@name='{}']".format(topic))
    if topicElement is None:
      topicElement = ET.SubElement(root, "topic", name=topic)

    # Create new note
    noteElement = ET.SubElement(topicElement, "note", name=title)
    ET.SubElement(noteElement, "text").text = text.strip()
    ET.SubElement(noteElement, "timestamp").text = timestamp.strip()
    tree.write("db.xml")
    print("createNewNote: Note '{}' created".format(title))
    return True
  except:
    print("createNewNote: Something went wrong")
    return False

def getNotes(topic):
  try:
    tree = ET.parse("db.xml")
    root = tree.getroot()
    
    # Find topic and return all notes
    topicElement = root.find("topic[@name='{}']".format(topic))
    if topicElement is None:
      print("getNotes: No notes found for topic '{}'".format(topic))
      return []
    else:
      notes = []
      for note in topicElement.findall("note"):
        title = note.get("name")
        text = note.find("text").text
        timestamp = note.find("timestamp").text
        notes.append((title, text, timestamp))
      print("getNotes: Found {} notes for topic '{}'".format(len(notes), topic))
      return notes
  except:
    print("getNotes: Somethings went wrong")
    return False

server.register_function(createNewNote, "createNewNote")
server.register_function(getNotes, "getNotes")
server.serve_forever()