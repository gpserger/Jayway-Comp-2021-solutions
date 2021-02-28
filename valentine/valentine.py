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
        tot1 = 0
        for pref in self.preferences:
            if "None" in self.preferences[pref] or profile.qualities[pref] == "None":
                tot1 += 1
            elif profile.qualities[pref] in self.preferences[pref]:
                tot1 += 1
        tot2 = 0
        for pref in profile.preferences:
            if "None" in profile.preferences[pref] or self.qualities[pref] == "None":
                tot2 += 1
            elif self.qualities[pref] in profile.preferences[pref]:
                tot2 += 1
        tot = tot1 + tot2
        return tot2/5

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
# matchlist = []
# total = 0
# for user in profiles:
#     for profile in profiles:
#         if user.validMatch(profile):
#             score = user.matchScore(profile)
#             if score == 1:
#                 total += 1
#                 matchlist.append("({}:{}),".format(user.index, profile.index))
#                 break
# print(total)
# # Output:
# # 9247
# # --- 10.60509467124939 seconds ---
# for match in matchlist:
#     print(match, end="")
# print()
# # Output:
# # (0:481),(1:4233),(2:2005),(3.... was entered to the website and we scored 1631
# # --- 5.687190771102905 seconds ---

print(profiles[54].matchScore(profiles[0]))
print("--- %s seconds ---" % (time.time() - start_time))