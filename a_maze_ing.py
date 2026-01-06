#!/usr/bin/env python3

import sys
import argparse


def display_errors(message: str) -> None:
    print(f"[ERROR]: {message}")


def check_flags() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--algo", choices=["medium", "complex"], default="medium")
    args = parser.parse_args()
    mapping = {"medium": 0, "complex": 1}

    return mapping[args.algo]


def medium():
    print("medium")


def complex():
    print("complex")


def generate_maze(algo: int) -> bool:
    algo_list = [medium, complex]
    print(algo)
    return (algo_list[algo])


def main():
    _algo = 0
    if len(sys.argv) <= 1:
        return display_errors("Not enough arguments")
    _algo = check_flags()
    generate_maze(_algo)


if __name__ == "__main__":
    main()
