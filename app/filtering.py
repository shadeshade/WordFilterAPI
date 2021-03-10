import os
from abc import ABC, abstractmethod

from app.updating import get_data_from_set

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.dirname(CUR_DIR)


class AbstractTextFiltering(ABC):
    lang_code = None
    special_symbols = None
    gram_endings = None

    def __init__(self) -> None:
        if self.special_symbols is None or self.gram_endings is None or self.lang_code is None:
            raise AssertionError('`self.special_symbols` and `self.gram_endings` and `lang_code` must be initialised')

    @abstractmethod
    def filter_text(self, text):
        """Filter text from banned words"""
        pass


class BaseTextFiltering(AbstractTextFiltering):

    def __init__(self) -> None:
        super().__init__()

        self.data_set = get_data_from_set(self.lang_code)

    def filter_text(self, text):
        words = text.split()
        filtered_text = []
        for word in words:  # type: str
            temp_val = ""
            while word.endswith(self.special_symbols):  # exclude special symbols
                temp_val += word[-1]
                word = word[:-1]

            if word.lower().endswith(self.gram_endings) and word not in self.data_set:  # exclude grammatical endings
                for ending in self.gram_endings:
                    if word.endswith(ending):
                        ending_len = len(ending)
                        temp_val += word[-ending_len:][::-1]
                        word = word[:-ending_len]
                        break

            if word.lower() in self.data_set:
                line_length = len(word)
                word = '*' * line_length
            filtered_text.append(word + temp_val[::-1])  # add our endings back

        filtered_text = ' '.join(filtered_text)
        return filtered_text


class EngTextFiltering(BaseTextFiltering):
    lang_code = 'en-US'
    special_symbols = ('!', '?', '.', ',', ':', ';', '-', '_', '%',)
    gram_endings = ('ing', 'ed', 'es', 's',)


def dispatch_filtering_class(lang_code):
    return {
        'en-US': EngTextFiltering,
    }[lang_code]()
