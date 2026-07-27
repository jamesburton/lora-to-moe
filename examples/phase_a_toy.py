"""Dependency-free smoke proof: freeze experts, train only the router."""

from __future__ import annotations

import json
import random

from lora_moe.router import LinearRouter, routing_metrics


def build_data(seed: int, samples: int) -> list[tuple[list[float], int]]:
    random_source = random.Random(seed)
    centres = ((1.5, 0.0), (0.0, 1.5), (-1.5, -1.5))
    data: list[tuple[list[float], int]] = []
    for label, centre in enumerate(centres):
        for _ in range(samples):
            data.append(
                (
                    [
                        centre[0] + random_source.gauss(0.0, 0.3),
                        centre[1] + random_source.gauss(0.0, 0.3),
                    ],
                    label,
                )
            )
    random_source.shuffle(data)
    return data


def main() -> None:
    # The fixed specialists return the right answer only inside their own domain.
    # The router never observes the label at inference time.
    train = build_data(seed=17, samples=40)
    test = build_data(seed=29, samples=20)
    router = LinearRouter(input_size=2, experts=3, seed=7)
    losses = router.fit(train, epochs=30, learning_rate=0.08)
    decisions = [router.route(features) for features, _ in test]
    correct = sum(
        decision.selected[0] == label
        for decision, (_, label) in zip(decisions, test)
    )
    report = {
        "kind": "smoke",
        "router_frozen_expert_accuracy": correct / len(test),
        "uniform_random_baseline": 1 / 3,
        "first_loss": losses[0],
        "final_loss": losses[-1],
        **routing_metrics(decisions),
    }
    print(json.dumps(report, indent=2))
    if report["router_frozen_expert_accuracy"] < 0.95:
        raise SystemExit("smoke gate failed: router accuracy below 0.95")


if __name__ == "__main__":
    main()
