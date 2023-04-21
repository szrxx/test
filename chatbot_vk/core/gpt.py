import openai

def get_gpt_response(api_key, prompt):
    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        n=1,
        stop=None,
        temperature=0.3
    )

    answer_text = response.choices[0].message['content'].strip()
    answer_length = len(answer_text)
    return answer_text, answer_length

