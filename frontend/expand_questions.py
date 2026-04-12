import json
import copy
import os

input_file = "src/data/GameQuestions.json"

with open(input_file, "r", encoding='utf-8') as f:
    data = json.load(f)

for game_key, levels_dict in data.items():
    if "beginner" not in levels_dict:
        continue
    
    base_questions = levels_dict["beginner"][:5] # Extract the base 5 templates
    
    for level_name in ["beginner", "medium", "hard"]:
        expanded_questions = []
        for i in range(25):
            # Clone the template
            template_index = i % len(base_questions)
            template = copy.deepcopy(base_questions[template_index])
            
            # Update specific IDs and Difficulty flags
            template["id"] = i + 1
            template["difficulty"] = level_name
            
            # Optionally add a small variant marker for UX differentiation during tests
            if i >= 5:
               template["questionText"] = template["questionText"] + f" (Variant {i+1})"
            
            expanded_questions.append(template)
            
        data[game_key][level_name] = expanded_questions

with open(input_file, "w", encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print("Successfully expanded questions to 25 per level!")
