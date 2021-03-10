## API instructions

Run the following commands to get started:
```
sh ./install.sh
sh ./run.sh
```

## POST /api/filter-bad-words/en-US

+ ### Request
```
/api/filter-bad-words/en-US
```

+ ### Body
Your key should be equal "message". 
Write your text in the value to filter.
```
  {
      "message": "What the HELL?!!"
  }
```
+ ### Response200
```
  {
      "filtered text": "What the ***?!!"
  }
```

##Adding new languages
In `filtering.py` create new class based on `BaseTextFiltering`.

```
class AnyLangTextFiltering(BaseTextFiltering):
    lang_code = "your language code"
    gram_endings = "grammatical endings of your language"

```


Open `updating.py` and add your language code as a key to `SOURCES_BY_LANG`. As a value you set the url. 
```
SOURCES_BY_LANG = {
    'en-US': "https://raw.githubusercontent.com/RobertJGabriel/Google-profanity-words/master/list.txt",
}
```
Add your key and value to the function below.
```
def dispatch_filtering_class(lang_code):
    return {
        'your language code': AnyLangTextFiltering,
    }[lang_code]()
```
Now you can send your requests like this.
```
/api/filter-bad-words/<lang_code>
```

