#!/usr/bin/env python3

import argparse
import dataclasses
import re
import sys
from typing import TextIO


@dataclasses.dataclass
class Signature:
    function_name: str
    flag_name: str
    argument: str
    argument_name: str


def to_camel_case(s: str) -> str:
    result = ""

    capitalize = False
    for c in s:
        if c == "_":
            capitalize = True
        else:
            result += c.upper() if capitalize else c.lower()
            capitalize = False

    return result


def flag_to_function_name(s: str) -> str:
    return to_camel_case("SET_" + s.removeprefix("CURLOPT_"))


def read_signatures(sigs: TextIO) -> list[Signature]:
    result = []
    for sig in sigs:
        match = re.search(
            r"^CURLcode curl_easy_setopt\(CURL \*handle, ([^,]+), ([^)]+)\);$", sig
        )
        assert match

        flag_name, argument = match[1], match[2]
        function_name = flag_to_function_name(flag_name)
        argument_name = argument.split(" ")[-1]

        result.append(
            Signature(
                function_name=function_name,
                flag_name=flag_name,
                argument=argument,
                argument_name=argument_name,
            )
        )

    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="path to input file with signatures")
    parser.add_argument(
        "-t",
        "--type",
        choices=["declarations", "definitions"],
        required=True,
        help="type of members to generate: 'declarations' or 'definitions'",
    )
    parser.add_argument(
        "-n", "--namespace", help="name to prepend to function definitions"
    )
    args = parser.parse_args()

    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            signatures = read_signatures(f)
    else:
        signatures = read_signatures(sys.stdin)

    if args.type == "declarations":
        for sig in signatures:
            print(f"void {sig.function_name}({sig.argument});")
    elif args.type == "definitions":
        prefix = ""
        if args.namespace:
            prefix = f"{args.namespace}::"

        for sig in signatures:
            print(f"void {prefix}{sig.function_name}({sig.argument})")
            print("{")
            print("    curl_easy_setopt(_curl, {sig.flag_name}, {sig.argument_name});")
            print("}")
    else:
        raise RuntimeError("unknown type: " + args.type)


if __name__ == "__main__":
    main()
