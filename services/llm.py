import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

client = openai.OpenAI(
    organization=os.environ["OPENAI_ORG_ID"],
)


def make_oai_call(prompt, model="gpt-3.5-turbo-1106"):
    completion = client.chat.completions.create(
        model=model,
        temperature=0.5,
        max_tokens=2000,
        messages=[
            {
                "role": "system",
                "content": "You are a meeting assistant which reviews and summarises emails into 10 words or less.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    return completion.choices[0].message.content


if __name__ == "__main__":
    prompt = "Whats the value of pi?"
    print(make_oai_call(prompt))
