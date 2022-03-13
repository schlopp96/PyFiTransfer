# PyFiTransfer

## About

- **_PyFiTransfer_** is a simple program developed as a way to easily transfer files of a given extension-type from one directory to a destination directory.

- Originally created as a personal solution for easily moving gaming screenshots to my primary "pictures" folder without having to manually _copy-and-paste_ various screenshots after each time playing a game.

---

## Installing PyFiTransfer

### Using pip

> Coming Soon!

---

### Manual Installation

1. Download source code from the [PyFiTransfer GitHub repo](https://github.com/schlopp96/PyFiTransfer).

2. Extract contents of the containing `**.zip` file to desired install location.

3. Navigate to directory containing extracted contents, and open said folder within a terminal.

4. Enter `pip install -r requirements.txt` to install all dependencies for this package.

5. Finally, move the `"PyFiTransfer-vx.x.x"` directory to your global Python 3rd-party package installation directory to be able to import `PyFileTransfer` like any other module:

   - `"path/to/python/Lib/site-packages/PyFiTransfer-vx.x.x"`

6. Done!

---

## Usage

- _If you've already installed **PyFiTransfer** using pip:_

  - In an open python environment, simply import the PyFiTransfer package and run the `main.py` script like so:

    ```python
    import PyFiTransfer

    >>> PyFiTransfer.main()
    ```

- _If you have **NOT** already installed **PyFiTransfer** to your Python environment:_

  - Start by opening the python script located within the installation directory:
    - `"path/to/PyFiTransfer/PyFiTransfer/main.py"`

1. Enter the file-path to the directory acting as the file transfer's destination.

2. Enter the file-type of the files you wish to transfer **_(not including the "." that proceeds the file type)_**.

   - Example:
     - You would enter (without the quotations) `"exe"` when needing to migrate files with the `".exe"` extension.

3. If everything is correctly validated, a success message is returned to the console, alongside a list of files that were successfully transferred.

   - If an error occurs, the program will display an error message before exiting.

4. Finally, the user is prompted to press the `[ENTER]` key to exit the process.

---

![CLI Screenshot](img/Screenshot%202022-01-24%20010344.png)

---

## Contact

- If you have any questions, comments, or concerns that cannot be alleviated through the [project's GitHub repository](https://github.com/schlopp96/PyFiTransfer), please feel free to contact me through my email address:

  - `schloppdaddy@gmail.com`

---
