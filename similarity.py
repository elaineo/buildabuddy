from data import *
import math

BOTS = ["annefrank", "bierce", "bookerwashington", "buffalobill", "carnegie", 
        "carson", "cruz", "darwin", "hillaryclinton", "paul", "poehler", "roosevelt",
        "tinafey", "trump", "twain"]

# receive two JSON personality profiles
# determine euclidean distance
def similarity(origin, target):
  distance = 0.0
  target_traits = flat_traits(target)
  origin_traits = flat_traits(origin)
  for o, t in zip(origin_traits, target_traits):
    distance += math.pow(o.get("percentage") - p.get("percentage"), 2)
  return 1-(math.sqrt(distance/len(origin_traits)))

def flat_traits(person):
  traits = person.get("tree").get("children")[0].get("children")[0]
  return traits.get("children")

def find_bot(target):
    r = sort(map(similarity_file, BOTS))
    return r[0]