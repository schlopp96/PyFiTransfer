# PyFiTransfer

## About

- **_PyFiTransfer_** is a python module/cli program that can easily transfer files of a given extension-type from their source directory to a destination directory.

- Intended as a part of an upcoming library I'm creating that will be based around basic file operations.

---

## Installing PyFiTransfer

### Using pip _(Recommended)_

- To install _**PyFiTransfer**_ using `pip`, enter the following:

  - ```shell
      python -m pip install PyFiTransfer
    ```

- Done!

---

### Manual Installation

1. Start by doing one of two things:

   - A. Download source code `*.zip` archive from the PyFiTransfer GitHub repo ["releases"](https://github.com/schlopp96/PyFiTransfer) tab, and extract the contents to your desired installation directory.
   - B. Clone the repo with the git client of your choice by entering the following command:
     - `git clone https://github.com/schlopp96/PyFiTransfer/releases/latest/`

2. Navigate to directory containing extracted contents, and open said directory within a terminal.

3. Install all dependencies for this package by entering the following command:
   - `pip install -r requirements.txt`

- **Optional:**

  - Move the `"PyFiTransfer-vx.x.x"` directory to your global Python 3rd-party package installation directory to be able to import `PyFileTransfer` like any other module:
    - `"path/to/python/Lib/site-packages/HERE"`

- Done!

---

## Usage

- In an open python environment, simply import the PyFiTransfer package and run the `main.py` script like so:

  ```python
  >>> import PyFiTransfer

  >>> PyFiTransfer.main()
  ```

- _If you have **NOT** installed **PyFiTransfer** using `pip`:_

  - Open the python script titled `main.py` located within the installation directory:
    - `"~PyFiTransfer/PyFiTransfer/main.py"`

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
