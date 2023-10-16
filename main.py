from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from starlette.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError
from exception_handlers import request_validation_exception_handler, http_exception_handler, unhandled_exception_handler
from middleware import log_request_middleware
import multipart
import nltk


app = FastAPI()

app.middleware("http")(log_request_middleware)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

nltk.download('punkt')
nltk.download('stopwords')

# Mount static files (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates configuration
templates = Jinja2Templates(directory="templates")


def process_text(text):
    # Tokenize sentences
    sentences = sent_tokenize(text)

    # Tokenize words, remove stopwords, and apply stemming
    stop_words = set(stopwords.words("english"))
    ps = PorterStemmer()
    processed_sentences = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        filtered_words = [ps.stem(word.lower()) for word in words if word.isalnum() and word.lower() not in stop_words]
        processed_sentence = " ".join(filtered_words)
        processed_sentences.append(processed_sentence)

    return processed_sentences


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/answer", response_class=HTMLResponse)
async def answer_question(request: Request):
    form_data = await request.form()
    user_question = form_data["question"]

    # Process the user's question
    processed_question = process_text(user_question)

    # Placeholder: Provide a simple response for demonstration purposes
    response = "I am your chatbot. You asked: {}".format(user_question)

    return templates.TemplateResponse(
        "index.html", {"request": request, "question": user_question, "response": response}
    )

try:
    predict(...)
except Exception as e:
    print(e)

