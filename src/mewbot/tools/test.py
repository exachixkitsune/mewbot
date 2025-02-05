#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2021 - 2023 Mewbot Developers <mewbot@quicksilver.london>
#
# SPDX-License-Identifier: BSD-2-Clause

from __future__ import annotations

from typing import List, Generator

import argparse
import os

from mewbot.tools import Annotation, ToolChain


class TestToolchain(ToolChain):
    coverage: bool = False

    def run(self) -> Generator[Annotation, None, None]:
        args = self.build_pytest_args()

        result = self.run_tool("PyTest (Testing Framework)", *args)

        if result.returncode < 0:
            yield Annotation("error", "test-harness", 1, 1, "Tests Failed", "")

    def build_pytest_args(self) -> List[str]:
        """Builds out the `pytest` command

        This varies based on what output types are requested (human vs code
        readable), and whether coverage is enabled.
        Due to issues with pytest-cov handling, parallelisation is disabled
        when coverage is enabled
        https://github.com/nedbat/coveragepy/issues/1303#issuecomment-1014915146
        """

        args = [
            "pytest",
            "--new-first",  # Do uncached tests first -- likely to be more relevant.
            "--durations=0",  # Report all tests that take more than 1s to complete
            "--durations-min=1",
            "--junitxml=reports/junit.xml",
        ]

        if not self.coverage:
            args.append("--dist=load")  # Distribute between processes based on load
            args.append("--numprocesses=auto")  # Run processes equal to CPU count
            return args

        args.append("--cov=src")  # Enable coverage tracking for code in the './src'
        args.append("--cov-report=xml:reports/coverage.xml")  # Record coverage summary in XML

        if self.is_ci:
            # Simple terminal output
            args.append("--cov-report=term")
        else:
            # Output to terminal, showing only lines which are not covered
            args.append("--cov-report=term-missing")
            # Output to html, coverage is the folder containing the output
            args.append("--cov-report=html:coverage")

        return args


def parse_options() -> argparse.Namespace:
    default = "GITHUB_ACTIONS" in os.environ

    parser = argparse.ArgumentParser(description="Run tests for mewbot")
    parser.add_argument("--ci", dest="is_ci", action="store_true", default=default)
    parser.add_argument("--cov", dest="coverage", action="store_true", default=False)

    return parser.parse_args()


if __name__ == "__main__":
    options = parse_options()

    testing = TestToolchain("tests", in_ci=options.is_ci)
    testing.coverage = options.coverage
    testing()
