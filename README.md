# custom-data-openai-rest-api
OpenAI linked with custom data and REST API for questions

Installation:
`pip install langchain openai chromadb tiktoken unstructured`

### API:
POST: http://127.0.0.1:8000/question

### Examples:
Custom Data:
```
I was born in Italy on May 1996
I have two sisters and one brother
```

## Question 1:
Question:
```
{
    "text": "Where was i born?"
}
```
Answer:
```
{
    "text": "I was born in Italy."
}
```

## Question 2:
Question:
```
{
    "text": "How much sisters do i have?"
}
```
Answer:
```
{
    "text": "Based on the given information, you have two sisters."
}
```

## Question 3:
Question:
```
{
    "text": "Who is Obama?"
}
```
Answer:
```
{
    "text": "Barack Obama is an American politician who served as the 44th President of the United States from 2009 to 2017. He is not related to the context given."
}
```
