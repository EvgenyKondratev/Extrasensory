import pickle
from typing import Optional
from flask import session


class HiddenNumbers:
    def __init__(self, numbers: list[int]):
        self.numbers: list[int] = numbers

    def save(self) -> None:
        pickled_data = pickle.dumps({'numbers': self.numbers})
        session['hidden_numbers'] = pickled_data

    @classmethod
    def load(cls) -> Optional['HiddenNumbers']:
        ret = None
        pickled_data = session.get('hidden_numbers')
        if pickled_data is not None:
            data = pickle.loads(pickled_data)
            ret = cls(data.get('numbers', []))
        return ret
