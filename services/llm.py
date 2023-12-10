import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

client = openai.OpenAI(
    organization=os.environ["OPENAI_ORG_ID"],
)


def get_email_prompt(email):
        email_prompt = f"""
        You are an assistant to a Software Engineer.
        For the given email body, try to fill out the following template.
        All output should be in JSON format.
        If dates/days are mentioned in the email, prioritise mentioning them.

        EMAIL: {email}

        TEMPLATE: {{
            "subject": <subject>,
            "body: "Associated Email Summary"
        }}

        For body, write in third person. Limit your response to 30 words

        For subject, you also must also add one of these three choices : ImpGPT, UrgGPT, ResLtrGPT.
        Add ImpGPT to subject if email is important.
        Add UrgGPT to subject if email is urgent.
        Add ResLtrGPT to subject if email can be read later and is not important.

        All are in context to Software Engineers. 

        Your output should look like:
        OUTPUT: {{"subject": <ImpGPT/UrgGPT/ResLtrGPT : SUBJECT_DATA>, "body": "<EMAIL_SUMMARY>"}}
        """

        return email_prompt

def make_oai_call(email, model="gpt-3.5-turbo-1106"):
    completion = client.chat.completions.create(
        model=model,
        temperature=0.5,
        max_tokens=2000,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a meeting assistant to a Software Engineer who reviews and summarises emails into 30 words or less.",
            },
            {"role": "user", "content": get_email_prompt(email)},
        ],
    )

    return completion.choices[0].message.content


if __name__ == "__main__":
    prompt = "Whats the value of pi?"
    print(make_oai_call(prompt))
