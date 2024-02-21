import speech_recognition as sr
import os
import requests

from langchain. chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import (
    HumanMessage,
)
from langchain.chains import ConversationChain, LLMChain
from langchain.memory import ConversationBufferMemory
import openai
from typing import Any, Dict, List, Tuple
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser

class Evaluation(BaseModel):
    explainingWithCustomerFeedback: Tuple[int, str] = Field(description="Explaining while checking the customer's expressions and reactions.")
    clearCommunicationMinimalJargon: Tuple[int, str] = Field(description="Communicated clearly, using as little jargon as possible.")
    empathyOrCommonGroundGained: Tuple[int, str] = Field(description="Gained empathy or common ground.")
    negotiationContentPurposeConfirmed: Tuple[int, str] = Field(description="Confirmed the content and purpose of the negotiation.")
    negotiationTimeConfirmed: Tuple[int, str] = Field(description="Confirmed the negotiation time.")
    participantsConfirmed: Tuple[int, str] = Field(description="Confirmed the participants.")
    appointmentRequestReasonCommunicated: Tuple[int, str] = Field(description="Clearly communicated the reason for requesting the appointment.")
    preliminaryClosingStrategy: Tuple[int, str] = Field(description="Preliminary closing (aligning post-discussion images) e.g., \"If Mr./Ms. XX feels the value of our service, what kind of action would you expect?\"")
    discussionAgendaArticulated: Tuple[int, str] = Field(description="Articulated the agenda of the discussion.")
    completeCompanyIntroductionGiven: Tuple[int, str] = Field(description="Explained the company introduction without omissions, as per the template.")
    briefHearingReasonsQuestionsStated: Tuple[int, str] = Field(description="Stated the reasons and number of questions for the brief hearing, and confidently proceeded with the hearing.")
    allHearingItemsCovered: Tuple[int, str] = Field(description="Managed to ask all the pre-prepared hearing items without omissions.")
    questionsShowPriorResearch: Tuple[int, str] = Field(description="Asked in a manner that shows prior research has been done (or familiarity with the subject area).")
    storyFlowQuestioning: Tuple[int, str] = Field(description="Explained in a way that the questions flowed as a story without disruption.")
    postHearingThanksAndUtilityExplained: Tuple[int, str] = Field(description="After all questions, articulated thanks and how the content of the brief hearing would be useful in the subsequent service explanation.")

#retrieveで実際の営業の人のロールプレイを評価するデータから評価例を取ってきたい。
def evaluate(history):
    parser = PydanticOutputParser(pydantic_object=Evaluation)
    llm = ChatOpenAI(
        #model_name='gpt-4',
        temperature=0.2,
        streaming=True,
    )
    observer_temp = """Now, you should grade the salesperson's response on a 10-point scale across 15 key performance indicators.

    Then, explain why you gave those scores, referring to certain responses made by the salesperson.

    Finally, give specific advice or examples of action in certain situations in the given dialogue.
    """
    template = """You specialize in observing and evaluating sales role-play conversations between a customer and a salesperson. Upon receiving a conversational dialogue, you grade the salesperson's response on a 10-point scale across 15 key performance indicators related to communication skills, empathy, negotiation preparation, and effective closing techniques.

    Current Conversation
    {history}

    {observer_temp}

    {format_instructions}
    """
    prompt = PromptTemplate(
        input_variables=['observer_temp','history'],
        partial_variables={'format_instructions': parser.get_format_instructions()},
        template=template,
    )

    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True,
    )
    output = chain.predict(observer_temp=observer_temp, history=history)
    parsed_output = parser.parse(output)
    return parsed_output

def speach_to_text(AUDIO_FILE):
    #AUDIO_FILEはpathを指定
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)
        #text = r.recognize_google(audio)
        text = r.recognize_whisper(
                    audio,
                    model='medium.en',
                    show_dict=True,
                )['text']
        return text

#以下はテキストを音声ファイルに変換する関数
#streamに送りつける
SERVER_URL = "undefined"  # サーバーのURLをここに入力してください。

def text_to_speech(text, model='tts-1', voice='alloy', response_format="opus"):
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    api_url = "https://api.openai.com/v1/audio/speech"
    headers = {
        "Authorization": f'Bearer {api_key}',  # Replace with your API key
    }

    data = {
        "model": model,
        "input": text,
        "voice": voice,
        "response_format": response_format,
    }

    with requests.post(api_url, headers=headers, json=data, stream=True) as response:
        if response.status_code == 200:
            # サーバーに送信するための追加のHTTPヘッダーをここで定義します。
            # 例: 'Content-Type': 'audio/opus' など、サーバー側で期待される形式に合わせてください。
            upload_headers = {
                "Authorization": "Bearer <YOUR_SERVER_AUTH_TOKEN>",  # サーバー認証用トークン
                "Content-Type": f"audio/{response_format}"  # この部分は実際のaudio content typeに合わせてください。
            }
            # メモリ内の音声データをサーバーにアップロード
            files = {'audio': ('audio.opus', response.raw, 'audio/opus')}
            upload_response = requests.post(SERVER_URL, headers=upload_headers, files=files)
            if upload_response.status_code == 200:
                print("Audio data successfully sent to the server.")
            else:
                print("Failed to send audio data to the server.")
                upload_response.raise_for_status()
        else:
            response.raise_for_status()