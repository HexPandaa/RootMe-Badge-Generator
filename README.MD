# Root-Me Badge Generator

## Description

**Root-Me Badge Generator** is a Python 3 script that generates badges from Root-me profiles.

The original idea came from *Podalirius* on the Root-Me forums (https://www.root-me.org/?page=forum&id_thread=12859)

Example badges:

![HexPandaa light theme](https://i.imgur.com/ghiDNUg.png)

![das dark theme](https://i.imgur.com/mviu4Pn.png)


## Features

The script can generate badges with differents themes, I might add more of these over time.


## Requirements

In order to run the script, you will need at least Python 3.6, and the following modules:

- [Requests](https://2.python-requests.org/en/master/) *(To make requests to the Root-Me website)*
- [Pillow](https://pillow.readthedocs.io/en/stable/index.html) *(This is the imaging library that I used to generate the badge)*

To install them, simply run this command in your terminal:

On Linux:
````bash
python3 -m pip install requests pillow
````


On Windows:
`````cmd
pip3 install requests pillow
`````


## Usage

To generate a badge, a few options are available, but to try the default you can simply use this command and replace `<username>` with your Root-Me username:

On Linux:
````
python3 generate.py <username>
````

On Windows:
`````
python generate.py <username>
`````

To know which options are possible, use the flag `--help`, for example you can add `--theme dark` to use a dark theme for your badge.


Here's the script help: `python generate.py --help`

````
usage: generate.py [-h] [--theme name] [--outfile filepath] [--show]
                   [--viewer command] [--dont-save]
                   username

Root-Me Badge Generator
-----------------------
    A python script to generate badges from Root-Me profiles

    Author: HexPandaa
    Repo: https://github.com/HexPandaa/RootMe-Badge-Generator

positional arguments:
  username              The username of the user for which you want to create
                        a badge

optional arguments:
  -h, --help            show this help message and exit
  --theme name, -t name
                        The theme for the badge among dark, light
  --outfile filepath, -o filepath
                        The file to which the file will be saved (default:
                        'badge.png'
  --show, -s            If the argument is present, shows the badge with the
                        default viewer or the one specified with --viewer/-V
  --viewer command, -V command
                        The viewer to use to show the badge, to use in
                        conjunction with --show/-s
  --dont-save, -d       If given, does not save the file, useful to only show
                        the badge

If you find a bug, please report it here: https://github.com/HexPandaa/RootMe-Badge-Generator/issues


````

## About the author


I'm really interested in cybersecurity, that's why I wanted to create something for one of the website I like.

You can find me here:


- https://github.com/HexPandaa
- https://root-me.org/HexPandaa
- https://www.hackthebox.eu/home/users/profile/125471


![My avatar](https://files.catbox.moe/qu71em.jpg "A cute panda I made")