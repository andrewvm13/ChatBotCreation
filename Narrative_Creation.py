import pandas as pd
import json

# Define the mapping of integers to descriptive modifiers
modifier_mapping = {
    0: "never",
    1: "sometimes",
    2: "often",
    3: "always"
}

# Load the small dataframe with answers
answers_df = pd.read_csv('Data/SRS_Adult_Data.csv')

# Load the questions and modifiers from the JSON file
with open('Data/SRS_Adult_Schema.json') as f:
    questions_data = json.load(f)

# Extract the relevant questions and their descriptions
questions = {k: v['description'] for k, v in questions_data['properties'].items() if k.startswith('Q')}
questions_list = sorted(questions.items())

# Extract the diagnosis for each row and create narratives for the rows
narratives = []



for idx, row in answers_df.iterrows():
    age = row['SRS_Adult:age']
    diagnosis = row['SRS_Adult:diagnosis']
    individual_narrative = [f"This child is {str(age)} months old and has {str(diagnosis).lower()} and "]

    responses = []
    for q_key, q_description in questions_list:
        q_answer = row[f'SRS_Adult:{q_key}']
        if pd.notna(q_answer):
            q_answer_text = modifier_mapping.get(int(q_answer), "unknown")
            responses.append(f"{q_description.lower()} {q_answer_text}")

    # Combine the responses into a single sentence
    individual_narrative.append(". ".join(responses) + ".")
    narratives.append(" ".join(individual_narrative))

# Combine all narratives into a single text block
full_narratives_text = "\n\n".join(narratives)


# Filter lines with 100 or more characters and save to another file
filtered_output_file = "Narratives_Created/SRS_Adult_Narratives.txt"
filtered_lines = [line for line in full_narratives_text.splitlines() if len(line.strip()) >= 100]

# Write the filtered lines to the output file
with open(filtered_output_file, "w") as file:
    file.write("\n".join(filtered_lines))

print(f"Filtered rows saved to: {filtered_output_file}")