# Contributing

All contributions to are welcome!

## Getting Started

Before contributing to our project, we recommend that you familiarize yourself with our project's [code of conduct](CODE_OF_CONDUCT.md).

We also encourage you to review the [existing issues](https://github.com/MatteoFasulo/Whisper-TikTok/issues) and [pull requests](https://github.com/MatteoFasulo/Whisper-TikTok/pulls) to get an idea of what needs to be done and to avoid duplicating efforts.

## Contributing Code

Before contributing code, please make sure to do the following:

1. Fork the repository and clone it to your local machine.
2. Create a virtual environment with `conda`, `venv` or any other tool of your choice.
3. Install the required dependencies by running:

    ```bash
    uv pip install -e ".[dev, docs]" --torch-backend=auto
    ```

4. Make sure that all the tests pass by running:

    ```bash
    pytest
    ```

5. Make sure that formatting and linting checks pass. We use `pre-commit` to manage our hooks. You can run the hooks manually by executing:

    ```bash
    pre-commit install
    pre-commit run --all-files
    ```

6. Commit your changes and push your branch.
7. Create a merge request describing your changes and linking any relevant issues.

## Bug Reports and Feature Requests

If you encounter any bugs or have feature requests, please open an issue on our [GitHub Issues page](https://github.com/MatteoFasulo/Whisper-TikTok/issues).

When reporting a bug, please include as much detail as possible, including steps to reproduce the issue, expected behavior, and any relevant logs or screenshots.

## Releasing a New Version

We use semantic versioning for our project. To release a new version, follow these steps:

1. Make sure that all changes intended for the new release are merged into the `main` branch. Unstaged or staged changes should not be present but rather committed or stashed away.
2. Create a new branch from `main` for the release (e.g., `prepare-release`):

    ```bash
    git checkout main
    git pull origin main
    git checkout -b prepare-release
    ```

3. Ensure all tests pass and the code is properly formatted. Use `pre-commit` to check formatting and linting.

    ```bash
    pytest
    pre-commit install
    pre-commit run --all-files
    ```

4. Choose which kind of version bump you want to perform: `major`, `minor`, or `patch`:

    - Major: for incompatible API changes.
    - Minor: for adding functionality in a backward-compatible manner.
    - Patch: for backward-compatible bug fixes.

    Then run the following command to bump the version accordingly:

    ```bash
    bump-my-version bump <major|minor|patch>
    ```

5. Verify that the version has been updated and a new git tag has been created.
6. Update the `CHANGELOG.md` file with the changes included in this release. Run the following command to generate the changelog:

    ```bash
    generate-changelog
    ```

7. Commit the updated `CHANGELOG.md` file and push the changes along with the new tag to the remote repository:

    ```bash
    git add CHANGELOG.md
    git commit -m "chore: update CHANGELOG for new release"
    git push --tags && git push origin prepare-release
    ```

8. Create a pull request to merge the `prepare-release` branch into `main`. Once the pull request is approved and merged, the new version will be officially released.

9. Now give yourself a pat on the back for a job well done :)
