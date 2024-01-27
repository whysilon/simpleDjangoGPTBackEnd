from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from chat_api.models import ChatResponse
from chat_api.serializers import ChatResponseSerializer
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json

@api_view(['POST'])
def askChat(request):
    try:
        # Initialising and checking variables
        llm = ChatOpenAI(model_name="ft:gpt-3.5-turbo-0613:personal::8lainp5L")
        output_parser = StrOutputParser()
        
        data = json.loads(request.body)
        codeSmell = data["codeSmell"]
        quality = data["quality"]
        code = data["code"]
        startLine = data["startLine"]
        langauge = data["language"]
        # Using normal chat-gpt 3.5 turbo (switch to fine-tune when done)
        systemPrompt = """
        You are a teaching assistant who needs to explain the problem of the code given to the student.
        Use the following code smell, code and the software quality impacted to explain what is wrong with the code.
        If you do not know the answer, just say that "I do not know" and do not try to make up an answer
        """
        defaultPrompt = f"""
        Please review this {langauge} code snippet which starts at {startLine}
        """

        prompt = ChatPromptTemplate.from_messages([
        ("system", systemPrompt),
        ("user", defaultPrompt),
        ("user", "{codeSmell}"),
        ("user","{quality}"),
        ("user","{code}"),
        ])
        chain = prompt | llm | output_parser
        answer = chain.invoke({"codeSmell":codeSmell,
                      "quality":quality,
                      "code":code,
                      })
        # serializer = ChatResponseSerializer(answer)

        return Response(answer)

    except Exception as e:
        print("Exception:",e)
        return Response(e, status=status.HTTP_400_BAD_REQUEST)
