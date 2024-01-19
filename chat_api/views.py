from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from chat_api.models import ChatResponse
from chat_api.serializers import ChatResponseSerializer
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

@api_view(['GET'])
def askChat(request):
    try:
        # Initialising and checking variables
        llm = ChatOpenAI()
        output_parser = StrOutputParser()
        codeSmell = request.GET["codeSmell"]
        quality = request.GET["quality"]
        code = request.GET["code"]
        startLine = int(request.GET["startLine"])
        endLine = int(request.GET["endLine"])
        # Comment this snippet out if the code coming in is an array
        codeLbyL = code.split('\n')
        extractedCode = '\n'.join(codeLbyL[startLine-1:endLine])

        # Using normal chat-gpt 3.5 turbo (switch to fine-tune when done)
        systemPrompt = """
        You are a teaching assistant who needs to explain the problem of the code given to the student.
        Use the following code smell, code and the software quality impacted to explain what is wrong with the code.
        Strictly answer in JSON format and follow the example given below
        ===
        {{
        "Explanation" : [Explanation of the code smell],
        "Solution" : [Brief Description of the solution],
        "Updated Code" : [Fix of the updated code]
        }}
        ===
        If you do not know the answer, just say that "I do not know" and do not try to make up an answer
        """
        defaultPrompt = """
        Please review this code
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
                      "code":extractedCode,})
        # serializer = ChatResponseSerializer(answer)

        return Response(answer)

    except Exception as e:
        print("Exception:",e)
        return Response(status=status.HTTP_404_NOT_FOUND)