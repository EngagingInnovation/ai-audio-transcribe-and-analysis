# Personas
default = "You are an AI with expertise in language comprehension and summarization. You are trained to understand and analyze text, finding key points, action items, and sentiment. Your responses are clear, concise, and focused on the most important aspects of the text."

abby = "You are Abby the Analyst. You are a highly skilled data analyst with a keen eye for detail and a passion for numbers. You are detail-oriented, logical, and data-driven. Your work is focused on analyzing data, identifying trends, and providing actionable insights. You are known for your logical thinking, methodical approach, and ability to distill complex information into clear and concise summaries. You are focused on data, statistics, and concrete outcomes. You highlight factual information, action items, KPIs, and follow-up tasks. Your tone is precise, objective, and methodical."

bob = "You are Bob the Business Manager. You are a seasoned business professional with a wealth of experience in managing teams, projects, and operations. You are pragmatist with a results-driven, realistic, practical, and solution-oriented perspective. You emphasize actionable items, practical solutions, and immediate next steps. Your tone is direct, realistic, and practical."

ollie = "You are Ollie the Optimist. You are an enthusiastic and positive-minded individual with a focus on opportunities. You are known for your upbeat attitude, motivational spirit, and encouraging words. You emphasize successes, achievements, and future opportunities. Your tone is upbeat, inspirational, and supportive."

steve = "You are Steve the Skeptic. You are a critical thinker with a cautious and questioning approach. You are known to be critical, questioning and cautious. You look for potential issues, challenges assumptions, and stress the importance of thorough planning You highlight risks and areas needing more scrutiny. Your tone is analytical, cautious, and somewhat critical."

veronica = "You are Veronica the Visionary. You are a creative and forward-thinking strategist with a passion for innovation, creativity, and long-term vision. You are known for your ability to think outside the box, come up with innovative ideas, and set strategic directions. You focus on long-term goals, visionary projects, and potential game-changers. Your tone is inspirational, future-oriented, and strategic."

output_request = "Your must always remove lines that begin with a series of three backticks (```) from your response."

personas = {
    "default": default + " " + output_request,
    "analyst": abby + " " + output_request,
    "pragmatist": bob + " " + output_request,
    "optomist": ollie + " " + output_request,
    "skeptic": steve + " " + output_request,
    "visionary": veronica + " " + output_request,
}


# Response Template Setup - warms up the AI to produce the formatted output we desire
response_template_example_prompt = """
Provide three strategies for a successful meeting. Use this response-template to build your response. Only respond with the formatted content from within the response-template block


``` response-template
{{ FOR EACH STRATEGY IN LIST }}
{{ STRATEGY.NUMBER }}. **{{ STRATEGY.TOPIC }}:** 
{{ STRATEGY.DESCRIPTION }} 

```
"""

response_template_example_response = """
1. **Preparation and Planning:** 
Start by setting clear objectives for the meeting, determining what you aim to achieve by the end. Communicate these objectives to all participants in advance. Create a detailed agenda that outlines the topics to be covered, assigns time slots for each topic, and distribute the agenda before the meeting. This helps participants prepare and stay on topic. Additionally, invite only essential participants who can contribute to the objectives to keep the meeting focused and productive.

2. **Effective Facilitation:** 
Ensure that the meeting starts and ends on time to respect everyone's time and encourage punctuality. Foster an environment where participants feel comfortable contributing by encouraging active participation and using techniques like round-robin discussions or direct questions to involve quieter members. Keep the conversation on track by gently steering it back to the agenda when it goes off-topic and summarize key points and decisions as you go to ensure clarity.

3. **Follow-Up and Accountability:** 
Document key takeaways, decisions made, and assigned tasks during the meeting, and share these notes with all participants immediately after the meeting. Ensure that each action item has a designated owner and a clear deadline to maintain accountability and ensure tasks are completed. Plan for a follow-up meeting or check-in to review progress on action items and discuss any outstanding issues, keeping momentum and ensuring continuous progress.

"""

# Abstract Summary Prompt
abstract_summary_prompt = """
You will read the following meeting transcript text and summarize it into two or three abstract paragraphs. Each paragraph should be between 2 and 4 sentences long. You will also come up with a short title that describes the transcription. Aim to retain the most important points, providing a coherent and readable summary that could help a person understand the main points of the discussion without needing to read the entire text. Please avoid unnecessary details or tangential points, and do not include bullet points or lists. Use the response-template to build your respone. Only respond with the formatted content from inside the response-template block.


``` response-template
## {{ TITLE }}  
{{ ABSTRACT PARAGRAPHS }}
```

--- TRANSCRIPT ---
{transcription}
"""


# Key Points Extraction Prompt
key_points_prompt = """
Base your response on the following meeting transcript text. There are multiple phases to this request.

## PHASE 1 ##
Your first responsibility is to identify each of the main points that were discussed or brought up in the discussion and create a list of these points. These points should be the most important ideas, findings, or topics that are crucial to the essence of the discussion. Your goal is to provide a list that someone could read to quickly understand what was talked about. 

## PHASE 2 ##
After you have created your list, you have a second responsibility. This is important, you must sort the list you created such that the most discussed topic is at the top of the list. Each additional topic should follow in order, so that the second most discussed topic is second in the list, the third most discussed is third, until the end of the list. Your answer should be formatted using the response-template below with each KEY_POINT aligning to your ordered list, where KEY_POINT number one aligns with your top most list item. Please return the formatted list in this order. 

Each item in the ordered list should include a heading followed by a list of the details of that point. Use the response-template to build your respone. Only respond with the formatted content from inside the response-template block.


``` respnose-template
{{ FOR EACH POINT IN KEY_POINT LIST }}
### {{ POINT.NAME }}
- {{ POINT.DETAIL }}
- {{ POINT.DETAIL }}
- {{ POINT.DETAIL }}
- {{ POINT.DETAIL }}
- {{ POINT.DETAIL }}
```

--- TRANSCRIPT ---
{transcription}
"""

# Action Items Extraction Prompt
action_items_prompt = """
Please review the meeting transcript text and identify any tasks, assignments, or actions that were agreed upon or mentioned as needing to be done. These could be tasks assigned to specific individuals, or general actions that the group has decided to take. Please list these action items clearly and in detail. Each item in the ordered list should include a title in bold following by a list of the tasks, assignments or actions items. Use the response-template to build your respone. Only respond with the formatted content from inside the response-template block.


``` response-template
{{ FOR EACH ITEM IN ACTION_ITEM LIST }}
### {{ ITEM.NUMBER }}. {{ ITEM.NAME }}  
- {{ ITEM.DETAIL }}
- {{ ITEM.DETAIL }}
- {{ ITEM.DETAIL }}
- {{ ITEM.DETAIL }}
- {{ ITEM.DETAIL }}
```

--- TRANSCRIPT ---
{transcription}
"""

# Key Quotes Prompt
key_quotes_prompt = """
Please review the meeting transcript text and identify any significant statements or key quotes that capture important points, decisions, or memorable phrases. This list should be limited to 5 or fewer selections. These should be quotes that stand out due to their impact, clarity, or importance in the context of the meeting. Each quote should be presented in a clearly formatted manner. Use the response-template to build your respone. Only respond with the formatted content from inside the response-template block.


``` response-template
{{ FOR EACH QUOTE IN KEY_QUOTES LIST }}
**Quote {{ QUOTE.NUMBER }}**
> "{{ QUOTE.TEXT }}"
```

--- TRANSCRIPT ---
{transcription}
"""


# Sentiment Analysis Prompt
sentiment_analysis_prompt = """
Please use your expertise in language and emotion analysis for this task. Review the following meeting transcript text and provide an analysis of the overall sentiment. Please consider the overall tone of the discussion, the emotion conveyed by the language used, and the context in which words and phrases are used. Indicate whether the sentiment is generally positive, negative, or neutral, and provide brief explanations for your analysis where possible. Please include bullet points and subheadings for specific explanations or examples and any additional formatting as needed. Your answer should be concise, consisting of no more than three paragraphs in length. 

--- TRANSCRIPT ---
{transcription}
"""


prompts = {
    "example_prompt": response_template_example_prompt,
    "example_response": response_template_example_response,
    "abstract_summary": abstract_summary_prompt,
    "key_points": key_points_prompt,
    "action_items": action_items_prompt,
    "key_quotes": key_quotes_prompt,
    "sentiment_analysis": sentiment_analysis_prompt,
}
