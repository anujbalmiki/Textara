from sre_parse import Tokenizer
import tokenize
from django.shortcuts import render
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer, pipeline

# Create your views here.


def translator(request):
    text = request.POST['rec_text3']
    return render(request, 'translator.html', {'text': text})


def translate(request):
    text2 = request.POST['rec_text4']
    lang = request.POST['langs']

    # Creating a Text2TextGenerationPipeline for language translation
    pipe = pipeline(task='text2text-generation', model='facebook/m2m100_418M')

    # Converting
    translated = pipe(text2, forced_bos_token_id=pipe.tokenizer.get_lang_id(
        lang=lang))[0]['generated_text']
    return render(request, 'translator.html', {'text': text2, 'text2': translated})
