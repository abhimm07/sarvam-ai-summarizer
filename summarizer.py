import argparse
import os
import sys
from typing import Optional
from dotenv import load_dotenv
from sarvamai import SarvamAI

# Ensure UTF-8 output on Windows terminals
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

load_dotenv()


def get_sarvam_client() -> SarvamAI:
    api_key = os.getenv("SARVAM_API_KEY")
    if not api_key:
        raise ValueError("SARVAM_API_KEY is not set. Please add it to your .env file.")
    return SarvamAI(api_subscription_key=api_key)


def summarize_text(
    text: str,
    summary_type: str = "bullet_points",
    language: str = "English",
    max_tokens: int = 1000,
    model: str = "sarvam-105b-conversations",
) -> str:
    """
    Summarize input text using Sarvam AI models.

    :param text: The input text to summarize.
    :param summary_type: Style ('bullet_points', 'concise', 'detailed', 'key_takeaways').
    :param language: Output language (e.g. 'English', 'Hindi', 'Bengali', 'Tamil', etc.).
    :param max_tokens: Maximum tokens for the generated summary.
    :param model: Sarvam model ('sarvam-105b-conversations' or 'sarvam-105b').
    :return: Generated summary.
    """
    client = get_sarvam_client()

    style_prompts = {
        "bullet_points": "Provide a clear, well-structured summary using bullet points highlighting the most essential ideas.",
        "concise": "Provide a single concise paragraph capturing the core message without losing critical context.",
        "detailed": "Provide an in-depth summary with sections covering the context, key details, and implications.",
        "key_takeaways": "Extract the top 3-5 high-impact actionable takeaways from the text.",
    }

    style_instruction = style_prompts.get(summary_type, style_prompts["bullet_points"])

    system_prompt = (
        f"You are a helpful and accurate text summarization assistant. "
        f"{style_instruction} "
        f"Generate the summary strictly in {language}. Keep the tone objective and faithful to the source material."
    )

    response = client.chat.completions(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Summarize the following text:\n\n{text}"},
        ],
        max_tokens=max_tokens,
    )

    choice = response.choices[0]
    return choice.message.content.strip() if choice.message and choice.message.content else "No summary generated."


def main():
    parser = argparse.ArgumentParser(description="Summarize text using Sarvam AI")
    parser.add_argument("--text", type=str, help="Text to summarize")
    parser.add_argument("--file", type=str, help="Path to text file to summarize")
    parser.add_argument(
        "--style",
        choices=["bullet_points", "concise", "detailed", "key_takeaways"],
        default="bullet_points",
        help="Summary format style",
    )
    parser.add_argument(
        "--lang",
        default="English",
        help="Language of the summary (e.g. English, Hindi, Tamil, Telugu, etc.)",
    )
    parser.add_argument(
        "--model",
        default="sarvam-105b-conversations",
        help="Sarvam model name",
    )

    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
    elif args.text:
        content = args.text
    else:
        # Default demonstration sample
        content = (
            "Sarvam AI is an Indian artificial intelligence startup building foundational AI models "
            "specifically tailored for Indian languages and use cases. They have developed sovereign "
            "large language models like Sarvam-105B, along with state-of-the-art voice models (speech-to-text "
            "and text-to-speech), document intelligence, translation, and transliteration APIs. "
            "Their mission is to make advanced AI accessible and effective across India's linguistic diversity."
        )
        print("Using demo text (use --text or --file for custom input):\n")
        print(f"Original ({len(content)} chars):\n{content}\n")

    summary = summarize_text(
        text=content,
        summary_type=args.style,
        language=args.lang,
        model=args.model,
    )

    print(f"=== Summary ({args.style} in {args.lang}) ===")
    print(summary)


if __name__ == "__main__":
    main()
