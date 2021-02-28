import json
import time


class Switch(dict):
    def __getitem__(self, item):
        for key in self.keys():  # iterate over the intervals
            if item in key:  # if the argument is part of that interval
                return True  # super().__getitem__(key)   # return its associated value
            else:
                return False
        raise KeyError(item)  # if not in any interval, raise KeyError


def getProfiles():
    with open('matchProfiles.json') as json_file:
        data = json.load(json_file)

        profiles = list()

        for person in data:
            p = Profile(
                person['index'],
                person['name'],
                person['age'],
                person['gender'],
                person['lookingfor'],
                person['agePreferences'] if person['agePreferences'] != ["None"] else None,
                person['qualities'],
                person['preferences'],
            )
            """
            {
            "index":0,
            "name":"Frankie Olsson",
            "age":36,
            "gender":"Male",
            "lookingfor":"Male",
            "agePreferences": [
                "Older",
                "Very young",
                "Ancient"
            ],
            "qualities": [
                {"eyecolor":"Black"},
                {"financialStatus":"Middle Class"},
                {"height":"Standard"},
                {"occupation":"Food"},
                {"animals":"Spider"}
            ],
            "preferences": [
                {"eyecolor":["Brown","Red"]},
                {"financialStatus":["Very poor"]},
                {"height":["Standard","Tall"]},
                {"occupation":["Party animal"]},
                {"animals":["None"]}
            ]
            }
            """

            profiles.append(p)

        return profiles


class Profile:

    def __init__(self, index, name, age, gender, lookingfor, agePreferences, qualities, preferences):
        self.index = index
        self.name = name
        self.age = age
        self.gender = gender
        self.lookingfor = lookingfor
        self.agePreferences = self.makeAgeList(agePreferences) if agePreferences else None
        self.qualities = self.combineDict(qualities)
        self.preferences = self.combineDict(preferences)

    def matchScore(self, profile):
        # Scoring wrong on (1:713), (0:54) and probably more.
        if not self.validMatch(profile):
            return 0
        tot = 0
        for pref in self.preferences:
            if profile.qualities[pref] in self.preferences[pref] or "None" in self.preferences[pref]:
                if self.qualities[pref] in profile.preferences[pref] or "None" in profile.preferences[pref]:
                    tot += 1

        return tot/5

    def likesAge(self, age):
        if not self.agePreferences:
            return True

        for gap in self.agePreferences:
            if age in gap:
                return True

        return False
        # switch = Switch({
        #     range(1, 21): True,
        #     range(21, 31): True,
        #     range(0,1000): False
        # })

    def likesGender(self, gender):
        if self.lookingfor == "Either":
            return True
        else:
            return gender == self.lookingfor

    def validMatch(self, profile):
        if self == profile:
            return False
        return self.likesGender(profile.gender) and \
               self.likesAge(profile.age) and \
               profile.likesGender(self.gender) and \
               profile.likesAge(self.age)

    def makeAgeList(self, agePreferences):
        pref = []
        if "Very young" in agePreferences:
            pref.append(range(-1000, self.age - 9))
        if "Younger" in agePreferences:
            pref.append(range(self.age - 10, self.age - 4))
        if "Same age" in agePreferences:
            pref.append(range(self.age - 5, self.age + 6))
        if "Older" in agePreferences:
            pref.append(range(self.age + 5, self.age + 11))
        if "Much Older" in agePreferences:
            pref.append(range(self.age + 10, self.age + 16))
        if "Ancient" in agePreferences:
            pref.append(range(self.age + 15, 1000))

        return pref

    def combineDict(self, dictlist):
        retdict = {}
        for pref in dictlist:
            retdict.update(pref)

        return retdict

start_time = time.time()

profiles = getProfiles()


# # Let's figure out how many of each match score there are
# scoredist = {}
# for i in range(0,6):
#     scoredist[i/5] = 0
# for user in profiles:
#     for profile in profiles:
#         if user.validMatch(profile):
#             score = user.matchScore(profile)
#             scoredist[score] += 1
# print(scoredist)
# # Output:
# # {0.0: 539888, 0.2: 3396834, 0.4: 8724799, 0.6: 11264840, 0.8: 7029685, 1.0: 1685768}
# # --- 130.44158387184143 seconds ---

# # Now lets figure out how many users have potential 1.0 matches
matchlist = []
total = 0
total_sum = 0
for user in profiles:
    if user.index % 100 == 0:
        print("User: {}".format(user.index))
    highscore = 0
    bestmatchindex = -1
    for profile in profiles:
        if user.validMatch(profile):
            score = user.matchScore(profile)
            if score >= highscore:
                highscore = score
                bestmatchindex = profile.index
            if score == 1:
                total += 1
                break
    if(bestmatchindex != -1):
        total_sum += highscore
        matchlist.append("({}:{}),".format(user.index, bestmatchindex))
    else:
        print(user.index)

print(total)
print(total_sum)
# Output:
# 9247
# --- 10.60509467124939 seconds ---
#
# for match in matchlist:
#     print(match, end="")
# print()
# # Output:
# # (0:481),(1:4233),(2:2005),(3.... was entered to the website and we scored 1631
# # --- 5.687190771102905 seconds ---

# print(profiles[54].matchScore(profiles[0]))  # Should be 0.4 points
# print(profiles[0].matchScore(profiles[54]))  # Should be 0.4 points
# print(profiles[713].matchScore(profiles[1]))  # Should be 0 points
# print(profiles[2].matchScore(profiles[559]))  # Should be 0.4 points
# print(profiles[4].matchScore(profiles[193]))  # Should be 0.8 points
# print(profiles[5].matchScore(profiles[60]))  # Should be 0.8 points
# (6:224) # 0.2
# (11:292) # 1

# All matches seem to be symmetrical: (A:B) gives same score as (B:A)
print("--- %s seconds ---" % (time.time() - start_time))


arlene = {"index": 1, "name": "PhD. Arlene Karlsson", "age": 54, "gender": "Female", "lookingfor": "Female",
     "agePreferences": ["Younger"],
     "qualities": [{"eyecolor": "Red"}, {"financialStatus": "Middle Class"}, {"height": "Tall"}, {"occupation": "None"},
                   {"animals": "Cat"}],
     "preferences": [{"eyecolor": ["Brown"]}, {"financialStatus": ["Very poor"]}, {"height": ["Short"]},
                     {"occupation": ["Military", "Party animal"]}, {"animals": ["Spider", "Cat", "Snakes"]}]}

tyrone = {"index": 713, "name": "Tyrone Gustafsson Jr.", "age": 48, "gender": "Female", "lookingfor": "Female",
          "agePreferences": ["Much Older", "Older", "Younger"],
          "qualities": [{"eyecolor": "Blue"}, {"financialStatus": "Rich"}, {"height": "Standard"}, {"occupation": "IT"},
                        {"animals": "Rats"}],
          "preferences": [{"eyecolor": ["Black", "Red"]}, {"financialStatus": ["Very poor", "Poor", "Middle Class"]},
                          {"height": ["Short", "Tall"]}, {"occupation": ["None"]}, {"animals": ["None"]}]}
