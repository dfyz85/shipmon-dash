import pandas as pd
import pymongo
from pprint import pprint
from bson.son import SON


client = pymongo.MongoClient("mongodb://dfyz:rtyfghvbn65@briese-shard-00-00-vryeg.mongodb.net:27017,briese-shard-00-01-vryeg.mongodb.net:27017,briese-shard-00-02-vryeg.mongodb.net:27017/test?ssl=true&replicaSet=briese-shard-0&authSource=admin&retryWrites=true&w=majority")
brieseDb = client['shipsBriese']
shipsPossition = brieseDb['shipsPosition'] 
vesselsName = brieseDb['shipsData']

def getVesselsFromDB():
  pipeline = [
    {"$group":{
      "_id":"$imo",
      "label":{"$first":"$name"},
      "value":{"$first":"$imo"}
      }
    },
    {"$project": { "_id": 0 }}
  ]
  db = vesselsName.aggregate(pipeline)
  return(list(db))

def getDFfromDB():
  pipeline = [
    {"$sort": SON([("reordingTime", -1)])},
    {"$group": {
      "_id": "$imo",
      "recordTime": { "$last": "$reordingTime" } , 
      "lat":{"$first":"$posittionLat"},
      "lon":{"$first":"$posittionLon"},
      "name":{"$first":"$vesselName"}
      }
    },
    {"$lookup": {
          "from": "shipsData",
          "localField": "_id",   
          "foreignField": "imo", 
          "as": "fromShipsData"
        }
    },
    {
        "$replaceRoot": { "newRoot": { "$mergeObjects": [ { "$arrayElemAt": [ "$fromShipsData", 0 ] }, "$$ROOT" ] } }
    },
    { "$project": { "fromShipsData": 0 }
    }
  ]

  db = shipsPossition.aggregate(pipeline)
  df = pd.DataFrame(list(db))
  return df