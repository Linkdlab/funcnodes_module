# FuncNodes Module

A tool for creating and managing modules for the [Funcnodes](https://github.com/Linkdlab/funcnodes) framework.

## 📌 Features

- 🚀 Quick module setup with predefined templates.
- 🔌 Optional React plugin for frontend integration.
- 🛠 Automatic Git initialization (optional).
- ✅ Pre-configured testing using pytest.
- 📂 Python packaging support with pyproject.toml.

## 📦 Installation

```sh
python -m pip install funcnodes-module
```

Ensure you have Python 3.11+ installed.

## 🎯 Usage

General Syntax

```sh
funcnodes-module <command> [options]
```

### 1️⃣ Creating a New Module

```sh
funcnodes-module new <name> [options]
```

| Argument           | Description                                  |
| ------------------ | -------------------------------------------- |
| name               | The name of the new module.                  |
| --with_react       | Adds React plugin templates.                 |
| --nogit            | Skips Git initialization.                    |
| --path <directory> | Specifies a custom directory for the module. |

Example:

```sh
funcnodes-module new my_module --with_react --nogit --path ~/projects
```

### 2️⃣ Updating an Existing Module

```sh
funcnodes-module update [options]
```

| Argument              | Description                                  |
| --------------------- | -------------------------------------------- |
| --nogit               | Skips Git initialization.                    |
| --path                | <directory> Specifies the project directory. |
| --force               | Forces overwriting of certain files.         |
| --project_name <name> | Manually specify the project name.           |
| --module_name <name>  | Manually specify the module name.            |
| --package_name <name> | Manually specify the package name.           |

### 3️⃣ Generating a Third-Party Notice File

```sh
funcnodes-module gen_third_party_notice [options]
```

| Argument           | Description                      |
| ------------------ | -------------------------------- |
| --path <directory> | Specifies the project directory. |

**IMPORTANT**: This is not legally valid as it may not cover every package and/or license. [IANAL](https://en.wikipedia.org/wiki/IANAL) applies here.

### 4️⃣ Running a Demo Worker

```sh
funcnodes-module demoworker
```

This command:

Creates a demo worker if it doesn’t exist.
Starts the worker and a FuncNodes server.
📁 Folder Structure

```sh
my_module/
│── src/
│ ├── my_module/ # Python package
│ │ ├── **init**.py
│ │ ├── main.py
│ ├── tests/
│ │ ├── test_my_module.py
│ ├── react_plugin/ # Optional React Plugin
│ ├── pyproject.toml # Python packaging
│ ├── README.md
│ ├── LICENSE
│ ├── .gitignore
```

🛠 Development & Testing
Run Tests

```sh
pytest
```

Build & Install Locally

```sh
pip install .
```

## 📜 License

This project is licensed under the MIT License.
