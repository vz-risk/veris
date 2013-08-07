require 'mongo'
require 'json'
require 'rubygems'
include Mongo

SERVER = 'localhost'
DATABASE = 'kevin'
COLLECTION = 'vcdb'

server = MongoClient.new(SERVER)
db = server.db(DATABASE)
col = db.collection(COLLECTION)

Dir.glob('../vcdb/*.json') do |filename|
    infile = open(filename, 'r')
    incident = JSON.parse(infile.read())
    col.insert(incident)
end

