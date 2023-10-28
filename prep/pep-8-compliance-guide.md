## Installing Pep 8 VS Code Extension

As Stian mentioned, **autopep8** has a few quirks. Danika recommended Black to me as well; instructions on how to install and enable are below.

1. Install Black extension for VS Code:  
https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter

2. Set Black to be the default formatter for Python Code:

    a.  Open the VS Code Command Palette by pressing <kbd>Ctrl</kbd> + <kbd>Sft</kbd> + <kbd>P</kbd> (Linux/Windows) or <kbd>Cmnd</kbd> + <kbd>Sft</kbd> + <kbd>P</kbd> (MacOS).

    b. Type in “settings.json” and press enter to open the settings file.

    c. Paste in the following lines of code and save the file.
    ```json
    "[python]": {
            "editor.defaultFormatter": "ms-python.black-formatter",
            "editor.formatOnSave": true
        }
    ```

3. To format your code, right click anywhere in the document and select “format document”, or press <kbd>Shft</kbd> + <kbd>Alt</kbd> + <kbd>F</kbd> (Linux/Windows) or <kbd>Shft</kbd> + <kbd>Opt</kbd> + <kbd>F</kbd> (MacOs).

    Saving a document will also automatically format it. To turn this off, set `editor.formatOnSave` to `false` in settings.json.   

---
Black will sort of most of the formatting, anything else that needs checking will be picked up by **flake8**, which will run automatically on pushing to GitHub.

### Exceptions

Black will not format commented out code, for instance, lines of code longer than 79 characters. This will still be raised by **flake8** in GitHub actions, causing the run to fail. For this reason, it is worth checking code in an online validator before pushing.

## Using PythonChecker To Validate Code

You can also use this site to validate Python code: https://www.pythonchecker.com/. Just copy and paste your Python into the online editor, and it will flag any lines that are not Pep 8 compliant.

### Exceptions

PythonChecker does not recognise that kwargs should not have whitespace around the assignment operator, as written below.

```python
def format_sales(stock=None, staff=None, sales=None):
    # function body...
```

There is more information on this in the Pep 8 style guide:  
https://peps.python.org/pep-0008/#other-recommendations

Please add any other exceptions here!