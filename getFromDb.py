import sys
import pandas as pd
import pymongo
from pprint import pprint
from bson.son import SON
import certifi # for MacOS

MONGO_URI = "mongodb://dfyz:rtyfghvbn65@briese-shard-00-00-vryeg.mongodb.net:27017,briese-shard-00-01-vryeg.mongodb.net:27017,briese-shard-00-02-vryeg.mongodb.net:27017/test?ssl=true&replicaSet=briese-shard-0&authSource=admin&retryWrites=true&w=majority"
client = pymongo.MongoClient(MONGO_URI,tlsCAFile=certifi.where())
brieseDb = client['shipsBriese']
shipsPossition = brieseDb['shipsPositionNow'] 
#shipsPossition = brieseDb['shipsPosition'] 
vesselsName = brieseDb['shipsData']

try:
  clientLocal = pymongo.MongoClient("mongodb://127.0.0.1:27017/",serverSelectionTimeoutMS=90000)
except:
  print("Could not connect to MongoDB.")
  sys.exit(1)
brieseDbLocal = clientLocal['shipsBriese']
shipsPossitionLocal = brieseDbLocal['shipsPosition']
vesselsNameLocal = brieseDbLocal['shipsData']

def getVesselsFromDB(server='cloud'):
  pipeline = [
    {"$group":{
      "_id":"$imo",
      "label":{"$first":"$name"},
      "value":{"$first":"$imo"}
      }
    },
    {"$project": { "_id": 0 }},
    {"$sort":SON([("label", 1)])}
  ]
  if server == 'cloud':
    db = vesselsName.aggregate(pipeline)
  elif server == 'local':
    db = vesselsNameLocal.aggregate(pipeline)
  return(list(db))

def getDFfromDB(server='cloud'):
  # pipeline = [
  #   {"$sort": SON([("reordingTime", -1)])},
  #   {"$group": {
  #     "_id": "$imo",
  #     "recordTime": { "$last": "$reordingTime" } , 
  #     "lat":{"$first":"$posittionLat"},
  #     "lon":{"$first":"$posittionLon"},
  #     "name":{"$first":"$vesselName"},
  #     "status":{"$first":"$status"},
  #     "speed":{"$first":"$speed"},
  #     "course":{"$first":"$course"},
  #     "departure":{"$first":"$departure"},
  #     "arrival":{"$first":"$arrival"},
  #     "eta":{"$first":"$eta"},
  #     "draught":{"$first":"$draught"},
  #     "time":{"$first":"$time"}
  #     }
  #   },
  #   {"$lookup": {
  #         "from": "shipsData",
  #         "localField": "_id",   
  #         "foreignField": "imo", 
  #         "as": "fromShipsData"
  #       }
  #   },
  #   {
  #       "$replaceRoot": { "newRoot": { "$mergeObjects": [ { "$arrayElemAt": [ "$fromShipsData", 0 ] }, "$$ROOT" ] } }
  #   },
  #   { "$project": { "fromShipsData": 0 }
  #   }
  # ]
  pipeline = [
    {"$sort": SON([("reordingTime", -1)])},
    {"$group": {
      "_id": "$imo",
      "recordTime": { "$last": "$reordingTime" } , 
      "lat":{"$first":"$posittionLat"},
      "lon":{"$first":"$posittionLon"},
      "name":{"$first":"$vesselName"},
      "status":{"$first":"$status"},
      "speed":{"$first":"$speed"},
      "course":{"$first":"$course"},
      "departure":{"$first":"$departure"},
      "arrival":{"$first":"$arrival"},
      "eta":{"$first":"$eta"},
      "draught":{"$first":"$draught"},
      "time":{"$first":"$time"}
      }
    }
  ]
  if server == 'cloud':
    db = shipsPossition.aggregate(pipeline)
  elif server == 'local':
    db = shipsPossitionLocal.aggregate(pipeline)
  df = pd.DataFrame(list(db))
  return df

def getVesselReportDBLocal(vesselIMO):
  if vesselIMO:
    pipeline = [
      {"$match":{
        "imo":vesselIMO
      }
      },
      {"$group":{
        "_id":"$time",
        "time":{"$first":"$time"},
        "area":{"$first":"$area"},
        "status":{"$first":"$status"},
        "speed":{"$first":"$speed"},
        "course":{"$first":"$course"},
        "draugt":{"$first":"$draught"}
        }
      },
      {"$project": { "_id": 0} },
      {"$sort":SON([("time", -1)])}
    ]
    db = shipsPossitionLocal.aggregate(pipeline)
    df = pd.DataFrame(list(db))
    return(df)

def getVesselsPointsDBLocal():
  pipeline=[
    {"$group":
        {
          "_id": "$imo",
          "count":SON([("$sum",1)]),
          "vesselName":{"$first":"$vesselName"}
        } 
    },
    {"$sort":SON([("count", 1)])}
  ]
  db = shipsPossitionLocal.aggregate(pipeline)
  df = pd.DataFrame(list(db))
  return(df)

# x = getVesselReportDBLocal('9261994')
# x = 
#for i in x.columns:
  #print(i)

#x = getDFfromDB()
#print(x.loc[x.name.str.contains('BBC LIMA'),['name','lat','lon']])