from app import BASE_DIR

lang_codes = {
    'en-US': "https://raw.githubusercontent.com/RobertJGabriel/Google-profanity-words/master/list.txt",
}


class TextFiltering:

    def filter_text(self, text, lang_code):
        from app.updating import DataUpdating

        special_symbols = ('!', '?', '.', ',', ':', ';', '-', '_', '%',)
        gram_endings = ('ing', 'ed', 'es', 's',)  # todo: use out of the box solution for lemmatization
        try:
            # fixme: preprocess banned words when you download not when you actually filter text
            bad_words = set(bw.strip("\n") for bw in open(f'{BASE_DIR}/data/words_{lang_code}.txt'))
        except:
            DataUpdating.get_data(lang_code)
            bad_words = set(bw.strip("\n") for bw in open(f'{BASE_DIR}/data/words_{lang_code}.txt'))

        words = text.split()
        filtered_text = []
        for word in words:  # type: str
            temp_val = ""
            while word.endswith(special_symbols):  # exclude special symbols
                temp_val += word[-1]
                word = word[:-1]

            if word.endswith(gram_endings) and word not in bad_words:  # exclude grammatical endings
                for ending in gram_endings:
                    if word.endswith(ending):
                        ending_len = len(ending)
                        temp_val += word[-ending_len:][::-1]
                        word = word[:-ending_len]
                        break

            if word in bad_words:
                line_length = len(word)
                word = '*' * line_length
            filtered_text.append(word + temp_val[::-1])  # add our endings back

        filtered_text = ' '.join(filtered_text)
        return {'filtered text': filtered_text}  # fixme: return just `filtered_text`, wrap in dict in view
