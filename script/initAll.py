import initDB as initdb
import initBot as initbot

filename = input("Path to resource.ini: ")

initdb.init(filename)
initbot.init(filename)
