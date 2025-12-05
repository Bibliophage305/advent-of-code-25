#!/usr/bin/env python3

from manage import create, get_day_from_args


def main():
    day = get_day_from_args()
    create(day)


if __name__ == "__main__":
    main()
