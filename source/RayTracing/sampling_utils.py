from random import random

class SamplingUtils:
    @staticmethod
    def get_regular_sampling(n_divisions: int) -> list[float]:
        return [i / n_divisions for i in range(n_divisions)]

    @staticmethod
    def get_uniform_sampling(n_samples : int) -> list[float]:
        return [random() for _ in range(n_samples)]

    @staticmethod
    def get_stratified_sampling(n_divisions: int) -> list[float]:       
        return [ (i + random()) / n_divisions for i in range(n_divisions)]