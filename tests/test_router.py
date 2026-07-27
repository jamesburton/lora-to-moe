from __future__ import annotations

import unittest

from lora_moe.router import LinearRouter, routing_metrics


class RouterTests(unittest.TestCase):
    def test_router_learns_linearly_separable_experts(self) -> None:
        examples = [
            ([1.0, 0.0], 0),
            ([1.2, 0.1], 0),
            ([0.0, 1.0], 1),
            ([0.1, 1.2], 1),
            ([-1.0, -1.0], 2),
            ([-1.2, -1.1], 2),
        ]
        router = LinearRouter(input_size=2, experts=3, seed=3)
        losses = router.fit(examples, epochs=80, learning_rate=0.1)
        self.assertLess(losses[-1], losses[0])
        self.assertTrue(
            all(router.route(features).selected[0] == label for features, label in examples)
        )

    def test_top_two_weights_are_normalised(self) -> None:
        decision = LinearRouter(2, 3).route([0.3, -0.2], top_k=2)
        self.assertAlmostEqual(1.0, sum(decision.weights))

    def test_metrics_report_dead_experts(self) -> None:
        router = LinearRouter(1, 2)
        decisions = [router.route([1.0]) for _ in range(4)]
        self.assertEqual(1, routing_metrics(decisions)["dead_experts"])


if __name__ == "__main__":
    unittest.main()
