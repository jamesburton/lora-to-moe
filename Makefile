.PHONY: check demo test

check:
	python -m compileall -q src examples tests
	PYTHONPATH=src python -m unittest discover -s tests -v
	PYTHONPATH=src python -m lora_moe.cli validate examples/catalog/code-expert.json
	PYTHONPATH=src python -m lora_moe.cli validate-graph examples/graphs/phase-a.json

demo:
	PYTHONPATH=src python examples/phase_a_toy.py

test:
	PYTHONPATH=src python -m unittest discover -s tests -v
