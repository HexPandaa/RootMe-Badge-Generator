#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: HexPandaa
# Original idea from Podalirius (https://www.root-me.org/?page=forum&id_thread=12859)

import argparse
import textwrap
from rootme import *
from badge import Badge
from os.path import dirname, isdir, isfile, abspath
from os import makedirs, remove


def download_file(session: Session, url: str, save_path: str) -> None:
    save_path = abspath(save_path)
    response = session.get(url, stream=True)
    if response.status_code == 200:
        if not isdir(dirname(save_path)):
            makedirs(dirname(save_path))
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)


def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent("""
                                     Root-Me Badge Generator
                                     -----------------------
                                         A python script to generate badges from Root-Me profiles
                                         
                                         Author: HexPandaa
                                         Repo: https://github.com/HexPandaa/RootMe-Badge-Generator
                                         
                                     """),
                                     epilog="If you find a bug, please report it here: "
                                            "https://github.com/HexPandaa/RootMe-Badge-Generator/issues"
                                     )

    parser.add_argument("--theme", "-t", metavar="name", type=str,
                        choices=Badge.get_themes(), default="light",
                        help="The theme for the badge among " + ", ".join(Badge.get_themes()))
    parser.add_argument("--outfile", "-o", metavar="filepath", type=str,
                        default="badge.png",
                        help="The file to which the file will be saved (default: 'out/badge.png'")
    parser.add_argument("--show", "-s", action="store_true",
                        help="If the argument is present, shows the badge with the default viewer or the one specified"
                             " with --viewer/-V")
    parser.add_argument("--viewer", "-V", metavar="command",
                        help="The viewer to use to show the badge, to use in conjunction with --show/-s")
    parser.add_argument("--dont-save", "-d", action="store_false", dest="save",
                        help="If given, does not save the file, useful to only show the badge")
    parser.add_argument("pseudo", metavar="username", type=str,
                        help="The username of the user for which you want to create a badge")

    args = parser.parse_args()

    return args


def main(args: argparse.Namespace):
    pseudo = args.pseudo
    theme = args.theme
    rm = RootMe()
    try:
        data = rm.get_user_stats(pseudo)
    except UserNotFoundError as e:
        print("ERROR: This user does not exist")
        quit(1)
    if data["avatar_url"]:
        download_file(rm.get_session(), data["avatar_url"], "pp.png")
    badge = Badge(
        pseudo=data["username"],
        profile_picture="pp.png",
        score=data["score"],
        title=data["rank"],
        ranking=data["ranking"],
        total_users=data["total_users"],
        theme=theme
    )
    badge.create()
    if isfile("pp.png"):
        remove("pp.png")

    if args.save:
        badge.save(args.outfile)

    if args.show:
        badge.show(args.viewer)


if __name__ == "__main__":
    args = parse_args()
    main(args)
