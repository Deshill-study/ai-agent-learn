from ..llm import ask


def Refine():
    # reference https://github.com/andrewyng/translation-agent
    print('Refine:')
    source_text = """
    Last week, I spoke about AI and regulation at the U.S. Capitol at an event that was attended by legislative and business leaders. I’m encouraged by the progress the open source community has made fending off regulations that would have stifled innovation. But opponents of open source are continuing to shift their arguments, with the latest worries centering on open source's impact on national security. I hope we’ll all keep protecting open source!

    Based on my conversations with legislators, I’m encouraged by the progress the U.S. federal government has made getting a realistic grasp of AI’s risks. To be clear, guardrails are needed. But they should be applied to AI applications, not to general-purpose AI technology.
    """
    ## system prompt
    first_translate_system_message = f"You are an expert linguist, specializing in translation from English to Chinese."

    ## user prompt

    first_user_translation_prompt = f"""This is an English to Chinese translation, please provide the Chinese translation for this text. \
    Do not provide any explanations or text apart from the translation.
    English: {source_text}

    Chinese:"""

    ## 将 source text 作为参数传入，构造好完整的输入
    first_user_prompt = first_user_translation_prompt

    print(first_user_prompt)
    ## system prompt
    first_translate_system_message = f"You are an expert linguist, specializing in translation from English to Chinese."

    ## user prompt

    first_user_translation_prompt = f"""This is an English to Chinese translation, please provide the Chinese translation for this text. \
    Do not provide any explanations or text apart from the translation.
    English: {source_text}

    Chinese:"""

    ## 将 source text 作为参数传入，构造好完整的输入
    first_user_prompt = first_user_translation_prompt.format(source_text=source_text)

    print(first_user_prompt)
    messages = [
    {"role":"system", "content": first_translate_system_message},
    {"role":"user", "content": first_user_prompt}
    ]

    first_response = ask(messages=messages)

    translation_1 = first_response.choices[0].message.content
    print(translation_1)

    reflect_system_prompt = "You are an expert linguist specializing in translation from English to Chinese. \
    You will be provided with a source text and its translation and your goal is to improve the translation."

    reflect_prompt = f"""Your task is to carefully read a source text and a translation from English to Chinese, and then give constructive criticism and helpful suggestions to improve the translation. \

    The source text and initial translation, delimited by XML tags <SOURCE_TEXT></SOURCE_TEXT> and <TRANSLATION></TRANSLATION>, are as follows:

    <SOURCE_TEXT>
    {source_text}
    </SOURCE_TEXT>

    <TRANSLATION>
    {translation_1}
    </TRANSLATION>

    When writing suggestions, pay attention to whether there are ways to improve the translation's \n\
    (i) accuracy (by correcting errors of addition, mistranslation, omission, or untranslated text),\n\
    (ii) fluency (by applying Chinese grammar, spelling and punctuation rules, and ensuring there are no unnecessary repetitions),\n\
    (iii) style (by ensuring the translations reflect the style of the source text and takes into account any cultural context),\n\
    (iv) terminology (by ensuring terminology use is consistent and reflects the source text domain; and by only ensuring you use equivalent idioms Chinese).\n\

    Write a list of specific, helpful and constructive suggestions for improving the translation.
    Each suggestion should address one specific part of the translation.
    Output only the suggestions and nothing else."""

    feedback_user_prompt = reflect_prompt.format(
            source_text=source_text,
            translation_1=translation_1,
        )

    print(feedback_user_prompt)
    message2 = [
    {"role":"system", "content": reflect_system_prompt},
    {"role":"user", "content": feedback_user_prompt}
    ]

    response = ask(messages=message2)

    reflection = response.choices[0].message.content
    print(reflection)
    # system prompt
    refiner_system_prompt = f"You are an expert linguist, specializing in translation editing from English to Chinese."

    # user content
    refined_translate_user_prompt = f"""Your task is to carefully read, then edit, a translation from English to Chinese, taking into
    account a list of expert suggestions and constructive criticisms.

    The source text, the initial translation, and the expert linguist suggestions are delimited by XML tags <SOURCE_TEXT></SOURCE_TEXT>, <TRANSLATION></TRANSLATION> and <EXPERT_SUGGESTIONS></EXPERT_SUGGESTIONS> \
    as follows:

    <SOURCE_TEXT>
    {source_text}
    </SOURCE_TEXT>

    <TRANSLATION>
    {translation_1}
    </TRANSLATION>

    <EXPERT_SUGGESTIONS>
    {reflection}
    </EXPERT_SUGGESTIONS>

    Please take into account the expert suggestions when editing the translation. Edit the translation by ensuring:

    (i) accuracy (by correcting errors of addition, mistranslation, omission, or untranslated text),
    (ii) fluency (by applying Chinese grammar, spelling and punctuation rules and ensuring there are no unnecessary repetitions), \
    (iii) style (by ensuring the translations reflect the style of the source text)
    (iv) terminology (inappropriate for context, inconsistent use), or
    (v) other errors.

    Output only the new translation and nothing else."""

    refined_user_prompt = refined_translate_user_prompt.format(
            source_text=source_text,
            translation_1=translation_1,
            reflection=reflection,
        )

    message3 = [
        {"role":"system", "content": refiner_system_prompt},
        {"role":"user", "content": refined_user_prompt}
    ]

    response = ask(messages=message3)

    translation_2 = response.choices[0].message.content
    print(translation_2)

    
