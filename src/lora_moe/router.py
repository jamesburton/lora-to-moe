"""Small reference router with deterministic SGD and observable routing."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Iterable, Sequence


def _softmax(logits: Sequence[float]) -> list[float]:
    maximum = max(logits)
    values = [math.exp(value - maximum) for value in logits]
    total = sum(values)
    return [value / total for value in values]


@dataclass(frozen=True)
class RoutingDecision:
    probabilities: tuple[float, ...]
    selected: tuple[int, ...]
    weights: tuple[float, ...]


class LinearRouter:
    """A sequence-level softmax router used as an executable specification."""

    def __init__(self, input_size: int, experts: int, seed: int = 0) -> None:
        if input_size < 1 or experts < 2:
            raise ValueError("input_size >= 1 and experts >= 2 are required")
        generator = random.Random(seed)
        self.weights = [
            [generator.uniform(-0.01, 0.01) for _ in range(input_size + 1)]
            for _ in range(experts)
        ]

    def probabilities(self, features: Sequence[float]) -> list[float]:
        if len(features) + 1 != len(self.weights[0]):
            raise ValueError("feature width does not match the router")
        augmented = [*features, 1.0]
        return _softmax(
            [sum(a * b for a, b in zip(row, augmented)) for row in self.weights]
        )

    def route(self, features: Sequence[float], top_k: int = 1) -> RoutingDecision:
        if not 1 <= top_k <= len(self.weights):
            raise ValueError("top_k must select at least one available expert")
        probabilities = self.probabilities(features)
        selected = tuple(
            sorted(range(len(probabilities)), key=probabilities.__getitem__, reverse=True)[
                :top_k
            ]
        )
        selected_total = sum(probabilities[index] for index in selected)
        mixture_weights = tuple(
            probabilities[index] / selected_total for index in selected
        )
        return RoutingDecision(tuple(probabilities), selected, mixture_weights)

    def fit(
        self,
        examples: Iterable[tuple[Sequence[float], int]],
        epochs: int = 100,
        learning_rate: float = 0.1,
    ) -> list[float]:
        dataset = list(examples)
        if not dataset:
            raise ValueError("at least one training example is required")
        losses: list[float] = []
        for _ in range(epochs):
            total_loss = 0.0
            for features, label in dataset:
                probabilities = self.probabilities(features)
                total_loss -= math.log(max(probabilities[label], 1e-12))
                augmented = [*features, 1.0]
                for expert, row in enumerate(self.weights):
                    error = probabilities[expert] - (1.0 if expert == label else 0.0)
                    for column, value in enumerate(augmented):
                        row[column] -= learning_rate * error * value
            losses.append(total_loss / len(dataset))
        return losses


def routing_metrics(decisions: Sequence[RoutingDecision]) -> dict[str, object]:
    if not decisions:
        raise ValueError("at least one routing decision is required")
    expert_count = len(decisions[0].probabilities)
    counts = [0] * expert_count
    entropy = 0.0
    for decision in decisions:
        counts[decision.selected[0]] += 1
        entropy -= sum(
            probability * math.log(max(probability, 1e-12))
            for probability in decision.probabilities
        )
    total = len(decisions)
    utilisation = [count / total for count in counts]
    return {
        "mean_entropy": entropy / total,
        "utilisation": utilisation,
        "dead_experts": sum(value == 0.0 for value in utilisation),
        "max_to_mean_load": max(counts) / (sum(counts) / expert_count),
    }
