import praw
import requests
import json
import os
import re
from tqdm import tqdm

from openai import OpenAI
from dotenv import load_dotenv
import argparse


load_dotenv()  # take environment variables from .env.


# Parse command-line arguments
parser = argparse.ArgumentParser(description='Process Reddit posts.')
parser.add_argument('--method', type=str, default='chat', choices=['translate', 'chat'],
                    help='Method to use for processing text. "translate" uses Deepl, "chat" uses GPT-3.5 Turbo.')
parser.add_argument('--lang', type=str, default='EN',
                    help='Target language for translation. Only used if method is "translate".')
args = parser.parse_args()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def chat_with_gpt3(prompt):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are an assistant that meaningfully translates English Reddit post texts into Language:{args.lang} and optimizes them for text-to-speech. The following is a Reddit post that you should translate and optimize for text-to-speech"},
            {"role": "user", "content": prompt}
        ]
    )
    # Extract the content attribute
    return completion.choices[0].message.content


def get_reddit_post(url):
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
    )
    post = reddit.submission(url=url)
    return post.title, post.selftext


def translate_to_german(text):
    # url = "https://api.deepl.com/v2/translate"
    url = "https://api-free.deepl.com/v2/translate"
    data = {
        "auth_key": os.getenv("DEEPL_AUTH_KEY"),
        "text": text,
        "target_lang": args.lang,
    }
    response = requests.post(url, data=data)
    response_json = response.json()
    return response_json['translations'][0]['text']


def process_text(title, text):
    if args.method == 'translate':
        title = translate_to_german(title)
        text = translate_to_german(text)
    elif args.method == 'chat':
        title = chat_with_gpt3(
            f"Translate the following title into Language: {args.lang} and adjust it so that it is optimized for a lecture by a text-to-speech program. Also remove all parentheses such as (29m) or (M23) or (M25) etc. Also remove all edits from the Reddit post so only the pure text remains:" + "\n\n" + "title" + "\n\n" + "Revised title:")
        text = chat_with_gpt3(
            f"Translate the following text into Language: {args.lang} and adjust it so that it is optimized for a lecture by a text-to-speech program. Also remove all parentheses such as (29m) or (M23) or (M25) or (19) etc. Also remove all edits from the Reddit post so only the pure text remains. Break off the text at the most exciting point to keep the readers very curious:" + "\n\n" + "text" + "\n\n" + "Revised text:")
    return title, text


def modify_json(title_text, part_text, outro_text, main_text):
    data = []
    for i in range(len(title_text)):
        data.append({
            "series": title_text[i],
            "part": part_text[i],
            "outro": outro_text[i],
            "text": main_text[i]
        })

    with open('./video.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def read_file_line_by_line(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            yield line


title_text = []
main_text = []

# Convert generator to list to get length
lines = list(read_file_line_by_line('./reddit-post.txt'))

for line in tqdm(lines, desc="Processing Reddit posts", unit="post"):
    title, text = get_reddit_post(line)
    title, text = process_text(title, text)

    title = title.replace('\n\n', '.')  # replace '\n\n' with ' ' in title
    text = text.replace('\n\n', '.')  # replace '\n\n' with ' ' in text

    title = title.replace('&#x200B', '')  # replace , with '' in title
    text = text.replace('&#x200B', '')  # replace , with '' in text

    # remove gender and age indications from title and text
    title = re.sub(r'\(?\d+\s*[mwMW]\)?', '', title)
    text = re.sub(r'\(?\d+\s*[mwMW]\)?', '', text)

    # remove gender and age indications where M/W is written before the number
    title = re.sub(r'\(?\s*[mwMW]\s*\d+\)?', '', title)
    text = re.sub(r'\(?\s*[mwMW]\s*\d+\)?', '', text)

    # remove characters not allowed in a Windows filename from title
    title = re.sub(r'[<>:"/\\|?*,]', '', title)

    text = text.replace('Edit:', '')
    text = text.replace('edit:', '')

    title_text.append(title)
    main_text.append(text)

# Initialize part_text and outro_text after the loop
part_text = [""] * len(title_text)
outro_text = [""] * len(title_text)


modify_json(title_text, part_text, outro_text, main_text)
