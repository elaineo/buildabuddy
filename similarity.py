from data import *
import math

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