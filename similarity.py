from data import *
import math

# receive two JSON personality profiles
# determine euclidean distance
def similarity(origin, target):
  distance = 0.0
  for p in origin:
    distance += math.pow(trait.percentage - target_big5[i].percentage, 2)
  return 1-(math.sqrt(distance/len(origin_big5)))

def flat_traits(person):
  traits = person.get("tree").get("children")[0].get("children")[0]
  return traits.get("children")