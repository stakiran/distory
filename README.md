# distory
Diary of your browser History.

## Requirement
- Windows 7+
- Python 3.6+
- Firefox Quantum

## Preparation
- (1) Prepare `sqlite3.exe` from [SQLite Download Page](https://www.sqlite.org/download.html)
  - Ex. sqlite-tools-win32-x86-3280000.zip
- (2) Get your Firefox profile name
  - See `%appdata%\Mozilla\Firefox\Profiles`
  - Ex1. `tvsczp3y.default`
  - Ex2. `iotcz7up.stakiran`

## How to use
Firstly, output .csv file.

Secondly, output .md file from .csv file.

For example, if you want to get between 19/05/13 and 19/05/14, like this:

```
$ python distory.py -p iotcz7up.stakiran -d 190513

$ python distory.py -p iotcz7up.stakiran -d 190513 --md
```

And, files like this:

190513.csv

```
...
"stakiran (stakiran)",https://github.com/stakiran,1557748668694000
"Create a New Repository",https://github.com/new,1557748673761000
```

190513.md

```
# 2019/05/13(月) 77 counts
...
- 2019/05/13(月) 20:57:48 ["stakiran (stakiran)"](https://github.com/stakiran)
- 2019/05/13(月) 20:57:53 ["Create a New Repository"](https://github.com/new)
```

## How to use about bookmark data with date added
Use `--bookmark` option.

```
$ python distory.py --bookmark -p iotcz7up.stakiran -d 190513

$ python distory.py --bookmark -p iotcz7up.stakiran -d 190513 --md
```

## License
[MIT License](LICENSE)

## Author
[stakiran](https://github.com/stakiran)
