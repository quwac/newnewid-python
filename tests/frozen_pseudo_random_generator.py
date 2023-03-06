from typing import List, Union

from newnewid.random.pseudo_random_generator import PseudoRandomGenerator


class FrozenPseudoRandomGenerator(PseudoRandomGenerator):
    def __init__(
        self,
        *,
        counter_reset: Union[int, List[int]] = 0,
        counter_increment: Union[int, List[int]] = 1,
        random_binary: Union[int, List[int]] = 0,
    ) -> None:
        if type(counter_reset) is int:
            counter_reset = [counter_reset]
        if type(counter_increment) is int:
            counter_increment = [counter_increment]
        if type(random_binary) is int:
            random_binary = [random_binary]

        self.counter_reset: List[int] = counter_reset  # type: ignore
        self.counter_increment: List[int] = counter_increment  # type: ignore
        self.random_binary: List[int] = random_binary  # type: ignore

        self.counter_reset_index = -1
        self.counter_increment_index = -1
        self.random_binary_index = -1

    def generate(self, bits: int, use: str) -> int:
        if use == "counter-reset":
            self.counter_reset_index = (self.counter_reset_index + 1) % len(self.counter_reset)
            return self.counter_reset[self.counter_reset_index]
        elif use == "counter-increment":
            self.counter_increment_index = (self.counter_increment_index + 1) % len(
                self.counter_increment
            )
            return self.counter_increment[self.counter_increment_index]
        elif use == "random-binary":
            self.random_binary_index = (self.random_binary_index + 1) % len(self.random_binary)
            return self.random_binary[self.random_binary_index]
        else:
            raise ValueError(f"Unknown use: {use}")
