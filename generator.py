from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"


def generate_post(description: str) -> str:
    """
    Generate a AITA post based on user description
    """
    prompt = f"""You are a creative writer who specializes in AITA (Am I The Asshole) Reddit posts.

Write a dramatic, entertaining AITA post based on this situation: "{description}"

Rules:
- Start with "AITA for..." as the title on the first line
- Write in first person, casual Reddit style
- Include specific details, ages, and fake names
- Build up the drama naturally with context and backstory
- End with "So, AITA?"
- Length: 150-250 words
- Do NOT include a verdict or update yet

Write only the post, nothing else."""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.9,
    )

    return response.choices[0].message.content.strip()


def generate_update(
    original_post: str,
    user_verdict: str,
    user_comment: str,
) -> str:
    """
    Generate an update that subtly acknowledges the user's comment.
    """
    prompt = f"""You are writing an UPDATE to an AITA post. The original poster is coming back with new information.

Original post:
{original_post}

The top comment on this post was verdict: {user_verdict}
The comment said: "{user_comment}"

Write an update (150-250 words) that:
- Starts with "UPDATE:" 
- Begins with "Wow, this blew up." or similar
- Subtly references the comment (without directly quoting it) in a natural way — like "to everyone who said [paraphrase]..."
- Reveals a dramatic new development or resolution
- Ends with whether OP thinks they were the asshole or not
- Keeps the casual Reddit tone

Write only the update, nothing else."""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600,
        temperature=0.9,
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    print("Testing post generation...\n")
    post = generate_post("I told my sister her homemade cake tasted terrible at our mom's birthday")
    print(post)
    print("\n" + "─"*50 + "\n")
    print("Testing update generation...\n")
    update = generate_update(
        original_post=post,
        user_verdict="YTA",
        user_comment="Dude, just lie sometimes. Not everything needs brutal honesty.",
    )
    print(update)