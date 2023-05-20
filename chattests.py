import openai
import json
import random
import time
import re

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

def parseStories(inputJson):
    stories = json.loads(response)
    storyEntries = stories.get('stories', [])

    for story in storyEntries:
        print(story.get('title', 'No Title'))

    return storyEntries

def find_and_parse_suggestions(text):
    # regex pattern to find suggestions JSON array
    pattern = r'suggestions:\s*(\[[^\]]*\])'
    
    match = re.search(pattern, text, re.DOTALL)
    if match is not None:
        suggestions_str = match.group(1)
        suggestions = json.loads(suggestions_str)
        return suggestions
    else:
        return None

# openai.api_key  = os.getenv('OPENAI_API_KEY')
openai.api_key = "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"
# gpt-4
# gpt-3.5-turbo
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model = model,
        messages = messages,
        temperature = 0.3, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

role = f"""
You take the role of a female, experienced dungeons and dragons master. You pay good attention to: 1. adhering the the DnD lore; 2. having balanced female and male NPCs; 3. reasoning well, how likely the players actions are to succeed. Give yourself a name. The user is the single player in your party. You will lead her through the game. It will be a one on one adventure. She will let you know what she wants to do and you will continue the game and story according her input.
"""

storyArc = """ Think of three stories, that the adventurer could undertake. Summarize each story in two paragraphs. Return your answer in JSON format. Each story summary should be in an entry array called `stories`. Each story should have an entry `title` and an entry `story`."""

possibleWaysToGoal = """ Think of three possible paths the adventurer could successfully finish this adventure. Write a summary for each. Return you answer in JSON format, each possible path as an entry in an array called `paths`. In an further entry called `winCondition` write in short plain text, what the player needs to accomplish to win the adventure. If applicable in an further entry called `looseCondition` write in short plain text, under which circumstances (besides the player's death) the adventure can not be won anymore."""

opening = """ Open the adventure with giving a short descripton of the setting. Then discribe what is asked of the adventure in this adventure. Then tell her where she is and give very brife introdurtion. """

characerSheet = """````
{
  "character": {
    "name": "",
    "gender": "",
    "race": "",
    "class": "",
    "level": "",
    "alignment": "",
    "experience_points": "",
    "hit_points": "",
    "armor_class": "",
    "speed": "",
    "attributes": {
      "strength": "",
      "intelligence": "",
      "wisdom": "",
      "dexterity": "",
      "constitution": "",
      "charisma": ""
    },
    "saving_throws": {
      "death_paralysis_poison": "",
      "wands": "",
      "petrification_polymorph": "",
      "breath": "",
      "spell": ""
    },
    "equipment": {
      "weapons": [
        {
          "name": "",
          "damage": "",
          "type": ""
        }
      ],
      "armor": {
        "name": "",
        "armor_class": ""
      },
      "items": [
        {
          "name": "",
          "quantity": ""
        }
      ]
    },
    "special_abilities": [""],
    "languages": [""],
    "backstory": ""
  }
}
```"""

answerOptions = """ In the end ask what she wants to do, give her 4 suggestions what to do next. Put each option as an entry in an JSON array at the end of your response. The JSON array should be called suggestions. """

activeStorySummary = ""

response = get_completion(role + storyArc)
print(response)
allStories = parseStories(response)
storyNumer = random.randint(0, len(allStories) - 1)
activeStorySummary = allStories[storyNumer]['story']
activeStoryTitle = allStories[storyNumer]['title']

print(activeStorySummary)

print("We are playing today: " + activeStoryTitle)

response = get_completion(role + possibleWaysToGoal)
print(response)



storyReminder = " The story of the adventure that you two are playing it given in three back ticks: ```" + activeStorySummary + "```Always give your answers according to this story. Lead the player towards the stroy given. Don't let her venture too far off that main story, but let her also export a bit of side stories. "
createCharacters = """ Make three characters level 1, that would be fit to go this adventure. Fill in the character sheet given in the tripple back ticks. For the entry backstory, write a 4 paragraphs long backstory. """

time.sleep(60)
response = get_completion(role + storyReminder + createCharacters + characerSheet)
print(response)

response = get_completion(role + storyReminder + opening + answerOptions)
print(response)

suggestions = find_and_parse_suggestions(response)