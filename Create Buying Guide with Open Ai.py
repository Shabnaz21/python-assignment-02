import os
import openai
from requests import post
import base64
from dotenv import load_dotenv
load_dotenv()

wp_user = os.getenv('wp_user')
wp_pass = os.getenv('wp_pass')
wp_credential = f'{wp_user}:{wp_pass}'
token = base64.b64encode(wp_credential.encode())
header = {'Authorization': 'Basic '+token.decode('utf-8')}

openai.api_key = os.getenv('openai.api_key')
url = os.getenv('url')

# keyword collection
keywords = open('Keyword.txt').readlines()
for key in keywords:
    keyword = key.strip("\n")

    # Openai Part
    def openai_answers(text):
        response = openai.Completion.create(
          model="text-davinci-002",
          prompt=text,
          temperature=0.7,
          max_tokens=462,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
        )
        data = response.get("choices")[0].get('text').strip('\n')
        return data

    #Content Structure Section

    def intro_part(keyword):
        '''
        This function will write:  A short description on(key) within 150 words
        '''
        intro = f"Write an introduction on “best{keyword}” within 150 words."
        return intro

    def important_part(keyword):
        '''
        This function will write:  Why {key} is important?
        '''

        second_part = f'Why {keyword} is important within 200 words?'
        return second_part

    def choose_part (keyword):
        '''
        This function will write:  How to choose best (key)?
        '''
        third_part = f'How to choose best{keyword} within 300 words?'
        return third_part

    def consider_part(keyword):
        '''
        This function will write:  What features should be considered while buying{key) within 200 words?
        '''
        four_part = f'What features should be considered while buying{keyword} within 250 words?'
        return four_part

    def wrapped_up_part(keyword):
        '''
         This function will write a eye-catching conclusion/wrapped up on (key) within 150 words.
        '''
        last_part = f'Write a eye-catching conclusion/wrapped up on{keyword} within 150 words'
        return last_part

    intro = intro_part(keyword)
    important = important_part(keyword)
    choose = choose_part(keyword)
    consider = consider_part(keyword)
    conclusion = wrapped_up_part(keyword)

# Wp Section
    def wp_paragraph(text):
        '''
        this function will convert paragraph to HTML in wp.
        '''
        codes = f'<!--wp:paragraph --><p>{text}</p><!-- /wp:paragraph -->'
        return codes

    def first_h2(keyword):
        '''
        this function will make first heading : Why (key) important?
        '''
        code = f'<!-- wp:heading --><h2>Why {keyword}is important?</h2><!-- /wp:heading -->'
        return code

    def second_h2(keyword):
        '''
        this function will make second heading : How to choose (key)?

        '''
        code = f'<!-- wp:heading --><h2>How to choose best {keyword}?</h2><!-- /wp:heading -->'
        return code

    def third_h2(text):
        '''
        this function will make third heading : What features should be considered while buying(key)?
        '''
        code = f'<!-- wp:heading --><h2>What features should be considered while buying {keyword}?</h2>' \
               f'<!-- /wp:heading -->'
        return code

    def last_h2(keyword):
        '''
        this function will make a conclusion heading
        '''
        code = f'<!-- wp:heading --><h2>Conclusion: Best {keyword} </h2><!-- /wp:heading -->'
        return code

    def slugify(text):
        '''
        This function will make text to slug
        '''
        code = text.strip().replace(' ', '-')
        return code

    title = f'Best {keyword} Reviews'
    slug = slugify(keyword)

    introduction = openai_answers(intro)
    why_important = openai_answers(important)
    how_to_choose = openai_answers(choose)
    what_consider = openai_answers(consider)
    conclusion = openai_answers(conclusion)

# Wp content Post section
    wp_title = title.title()
    wp_intro = wp_paragraph(introduction)
    wp_first_h2 = first_h2(keyword)
    wp_why_important = wp_paragraph(why_important)
    wp_second_h2 = second_h2(keyword)
    wp_how_to_choose = wp_paragraph(how_to_choose)
    wp_third_h2 = third_h2(keyword)
    wp_what_consider = wp_paragraph(what_consider)
    wp_conclusion_h2 = last_h2(keyword)
    wp_conclusion = wp_paragraph(conclusion)
    wp_slug = slug

    wp_content = f'{wp_intro}{wp_first_h2}{wp_why_important}{wp_second_h2}{wp_how_to_choose}{wp_third_h2}{wp_what_consider}' \
                 f'{wp_conclusion_h2}{wp_conclusion}'

    def wp_posting(wp_title, slug, wp_content):
        api_url = url
        data = {
            'title': wp_title,
            'slug': slug,
            'content': wp_content,
            'categories': '7'
        }
        res = post(api_url, data=data, headers=header, verify=False)
        if res.status_code == 201:
            print('Post Successful')
        else:
            print(' Wrong')

    wp_posting(wp_title, slug, wp_content)


