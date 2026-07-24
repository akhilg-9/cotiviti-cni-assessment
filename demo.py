"""
One-shot scripted demo — no arguments.

    python demo.py

Runs the full Past -> Present -> Future extraction on the bundled sample note.
A convenient entry point for the video screen-share; the same thing as
`cni run`. Set ANTHROPIC_API_KEY for live Claude calls.
"""

from src.cli import run

if __name__ == "__main__":
    run(None)
