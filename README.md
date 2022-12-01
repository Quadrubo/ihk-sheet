# IHKSheet

Easily manage your Berichtshefte :)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

To get started you need:
- google sheets file setup in the required layout
- google service account with credentials file

### Installing

A step by step series of examples that tell you how to get a development env running


First clone the repository to your local system.

```shell
git clone https://github.com/Quadrubo/ihk-sheet
```

After that install the requirements.

```shell
pip install -r requirements.txt
```
Start the `main.py` file to get started.

### Troubleshooting

## Copy to Clipboard not working

If you get an error, stating `It seems like there is no copy/paste mechanism installed on your system. Please follow the link in the error.`, your system may be missing a copy/paste mechanism.
Follow the instructions at [Pyperclip - Not Implemented Error](https://pyperclip.readthedocs.io/en/latest/index.html#not-implemented-error) to install a copy/paste mechanism on your system.
On my system, installing `xclip` solved the issue.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* **Billie Thompson** - *README Template* - [PurpleBooth](https://github.com/PurpleBooth)
