#!/usr/bin/env bash
# =============================================================================
# push_rama_2-feature_eda_jj.sh
# Sube todo el trabajo de JJ a la rama 2-feature_eda_jj en GitHub
# Uso: bash push_rama_2-feature_eda_jj.sh
# Ejecutar desde la raíz del proyecto: ~/Proyectos/p7_g1_multiclase/
# =============================================================================

set -e   # abortar si cualquier comando falla
set -u   # abortar si se usa una variable no definida

RAMA="2-feature_eda_jj"
FICHERO_COMMIT="commit_message_2-feature_eda_jj.txt"

echo ""
echo "========================================================"
echo "  push_rama_2-feature_eda_jj.sh"
echo "  Proyecto: p7_g1_multiclase"
echo "  Rama destino: $RAMA"
echo "========================================================"
echo ""

# ─── 0. Verificaciones previas ────────────────────────────────────────────────
echo "[0/6] Verificando entorno..."

# Comprobar que estamos en la raíz correcta del proyecto
if [ ! -f "pyproject.toml" ]; then
    echo "ERROR: No se encuentra pyproject.toml."
    echo "       Ejecuta este script desde la raíz del proyecto p7_g1_multiclase."
    exit 1
fi

# Comprobar que el fichero de commit existe
if [ ! -f "$FICHERO_COMMIT" ]; then
    echo "ERROR: No se encuentra el fichero de commit: $FICHERO_COMMIT"
    echo "       Colócalo en la raíz del proyecto junto a este script."
    exit 1
fi

echo "  ✓ pyproject.toml encontrado"
echo "  ✓ Fichero de commit encontrado: $FICHERO_COMMIT"

# ─── 1. Asegurar que estamos en la rama correcta ──────────────────────────────
echo ""
echo "[1/6] Comprobando rama actual..."

RAMA_ACTUAL=$(git branch --show-current)

if [ "$RAMA_ACTUAL" != "$RAMA" ]; then
    echo "  Rama actual: $RAMA_ACTUAL → cambiando a $RAMA"
    git checkout "$RAMA"
else
    echo "  ✓ Ya estamos en la rama $RAMA"
fi

# ─── 2. Crear / actualizar .gitignore ─────────────────────────────────────────
echo ""
echo "[2/6] Configurando .gitignore..."

cat > .gitignore << 'GITIGNORE'
# ─── Entorno virtual uv ───────────────────────────────────────────────────────
.venv/

# ─── Python cache ─────────────────────────────────────────────────────────────
__pycache__/
*.py[cod]
*.pyo

# ─── Jupyter artefactos de sesión ─────────────────────────────────────────────
.ipynb_checkpoints/
*.ipynb_checkpoints

# ─── Word / Office ficheros temporales ────────────────────────────────────────
~$*
~WRL*.tmp

# ─── Sistema operativo ────────────────────────────────────────────────────────
.DS_Store
Thumbs.db
desktop.ini
GITIGNORE

echo "  ✓ .gitignore creado/actualizado"

# ─── 3. Eliminar del índice lo que ahora ignora .gitignore ────────────────────
echo ""
echo "[3/6] Limpiando del índice git los ficheros ignorados..."

# Elimina del índice (no del disco) lo que .gitignore excluye
# --cached → solo del índice, no borra los archivos físicos
git rm -r --cached .venv/              2>/dev/null && echo "  · .venv/ eliminado del índice" || echo "  · .venv/ ya no estaba en el índice"
git rm -r --cached __pycache__/        2>/dev/null || true
git rm -r --cached .ipynb_checkpoints/ 2>/dev/null || true

# ─── 4. Añadir todo al stage ──────────────────────────────────────────────────
echo ""
echo "[4/6] Añadiendo ficheros al stage (git add)..."

git add .

echo ""
echo "  Ficheros en stage:"
git status --short

# ─── 5. Confirmar antes de commitear ──────────────────────────────────────────
echo ""
echo "========================================================"
echo "  ¿Confirmas el commit y push a '$RAMA'? (s/n)"
echo "========================================================"
read -r CONFIRMAR

if [ "$CONFIRMAR" != "s" ] && [ "$CONFIRMAR" != "S" ]; then
    echo "Operación cancelada por el usuario."
    exit 0
fi

# ─── 6. Commit ────────────────────────────────────────────────────────────────
echo ""
echo "[5/6] Realizando commit..."

# -F lee el mensaje desde el fichero de texto
git commit -F "$FICHERO_COMMIT"

echo "  ✓ Commit realizado"

# ─── 7. Push ──────────────────────────────────────────────────────────────────
echo ""
echo "[6/6] Subiendo a GitHub (git push)..."

# --set-upstream la primera vez que se sube la rama
# Si ya existe el upstream, simplemente hace push
git push --set-upstream origin "$RAMA"

echo ""
echo "========================================================"
echo "  ✓ Push completado correctamente"
echo "  Rama: $RAMA"
echo "  Repositorio remoto: $(git remote get-url origin)"
echo "========================================================"
echo ""
echo "Próximos pasos:"
echo "  · Abre un Pull Request desde $RAMA → develop en GitHub"
echo "  · Cuando el equipo decida qué incluir, crea una nueva rama desde develop"
