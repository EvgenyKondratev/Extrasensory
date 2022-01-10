import random
import pickle
from typing import Optional, List
from main_app import app
from flask import session


class Extrasensory:
    def __init__(self, name: str, accuracy: int, predictions: List[int]):
        self.name: str = name
        self.accuracy: int = accuracy
        self.predictions: List[int] = predictions

    def __repr__(self) -> str:
        return f'Экстрасенс {self.name}'

    def predict(self) -> None:
        random_number = random.randint(app.config.get('MIN_RANGE_HIDDEN_NUMBER'),
                                       app.config.get('MAX_RANGE_HIDDEN_NUMBER'))
        self.predictions.append(random_number)

    def recalc_accuracy(self, number: int) -> None:
        if number == self.predictions[-1]:
            self.accuracy += 1
        else:
            self.accuracy -= 1

    def save(self) -> None:
        pickled_data = pickle.dumps({'name': self.name, 'accuracy': self.accuracy, 'predictions': self.predictions})
        session[f'extrasensory:{self.name}'] = pickled_data

    @classmethod
    def load(cls, name: str) -> Optional['Extrasensory']:
        ret = None
        pickled_data = session.get(f'extrasensory:{name}')
        if pickled_data is not None:
            data = pickle.loads(pickled_data)
            ret = cls(data.get('name'), data.get('accuracy', 0), data.get('predictions', []))
        return ret
