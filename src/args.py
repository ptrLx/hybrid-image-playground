import argparse


class ArgParser:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(description="Hybrid Image Playground")

        self.parser.parse_args()
