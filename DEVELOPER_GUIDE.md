# Developer Guide

ALL LINKS ARE PLACEHOLDERS

## Introduction

Welcome to the developer guide for the JSON configuration file editor. This guide provides information on setting up the development environment, contributing to the project, and understanding the codebase.

## Setup

1. **Clone the repository**:
    ```sh
    git clone https://github.com/TerribleTurtle/turtles-serverconfig.git
    cd turtles-serverconfig
    ```

2. **Create a virtual environment and activate it**:
    ```sh
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

## Code Structure

- `config.json`: Configuration file containing paths and logging settings.
- `config_manager.py`: Manages loading and accessing configuration settings.
- `directory_validator.py`: Validates the directory structure.
- `change_tracker.py`: Tracks changes in memory.
- `batch_apply.py`: Applies changes and creates backups.
- `logger_setup.py`: Configures logging.

## Contributing

1. **Create a new branch** for your feature or bug fix:
    ```sh
    git checkout -b feature/your_feature_name
    ```

2. **Make your changes** and commit them with a clear message:
    ```sh
    git add .
    git commit -m "Add your clear commit message"
    ```

3. **Push to your branch**:
    ```sh
    git push origin feature/your_feature_name
    ```

4. **Create a pull request** on GitHub.

## Testing

- Tests are written using the `unittest` framework.
- To run tests, execute the following command:
    ```sh
    python -m unittest discover tests
    ```

## Code of Conduct

Please follow the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/0/code_of_conduct/).

## License

This project is licensed under the [CC BY-NC](LICENSE).

## Support

For support, please create an issue on the [GitHub repository](https://github.com/TerribleTurtle/turtles-serverconfig/issues).
