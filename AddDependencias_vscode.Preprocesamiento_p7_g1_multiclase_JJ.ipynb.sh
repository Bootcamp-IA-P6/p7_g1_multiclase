# Añadir xgboost a las dependencias del proyecto
uv add xgboost

# Añadir ipykernel como dependencia de desarrollo (no va a producción)
uv add --dev ipykernel

# Instala todas las dependencias del pyproject.toml en el .venv
uv sync

# Registra el .venv del proyecto como kernel de Jupyter
# Sustituye "p7-g1-multiclase" por el nombre que quieras ver en el selector de VS Code
uv run ipython kernel install --user --name=p7-g1-multiclase

jupyter kernelspec list

#pyproject2.toml resultante