# Development

## Prerequisites
Make sure Python 3, pip, PyCharm and Poetry are installed on your system.

## Setup
1. Clone this repository.
2. Open the folder in PyCharm.
3. Go to `Settings > Project > Python Interpreter`.
4. Go to the settings next to `Python Interpreter` and click `Add...`.
5. Select `Poetry environment` on the left side.
6. Make sure the `Base interpreter` and `Poetry executable` are correct.
7. Make sure `Install packages from pyproject.toml` is checked.
8. Click `Ok`. PyCharm will now install the dependencies.
9. Close the settings.
10. Copy `.env.example` to `.env` and change the environment variables. Only `DATABASE_*` variables have to be changed for development.
11. Open PyCharm's terminal (bottom left).
12. Run the migrations with `python manage.py migrate`.
13. Seed the database with `python manage.py loaddata **/fixtures/*.json`.
14. Run the cache migrations with `python manage.py createcachetable`.
15. Create an admin user with `python manage.py createsuperuser`.
16. Close PyCharm's terminal.

## Running
PyCharm should have automatically detected Django and created a run configuration for the project.
You can now run the project by clicking the green arrow (`Run`) or green bug (`Debug`) in the top right corner.

Alternatively, you can manually add a configuration.
1. Go to `Run/debug configurations` or click `Add configuration...` in the top right corner.
2. Click `Add new...` and select `Django Server`.
3. Give it the name of the project, the defaults can be left unchanged.
4. Click `Ok` to close the configurations.
