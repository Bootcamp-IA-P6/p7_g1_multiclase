#!/usr/bin/env bash
# =============================================================================
# commit_cambios_preprocesamiento_20260319121638.sh
#
# Commitea únicamente el notebook modificado:
#   notebooks/Preprocesamiento_p7_g1_multiclase_JJ.ipynb
#
# El fichero de commit se nombra con timestamp para diferenciar versiones:
#   commit_message_<rama>_<YYYYMMDDHHmmss>.txt
#
# Uso: bash commit_cambios_preprocesamiento_20260319121638.sh
# Ejecutar desde la raíz del proyecto: ~/Proyectos/p7_g1_multiclase/
# =============================================================================

set -e
set -u

RAMA="2-feature_eda_jj"

# ─── Timestamp en el momento de ejecutar el script ────────────────────────────
# Así el nombre del fichero de commit refleja CUÁNDO se hizo, no cuándo se creó
TIMESTAMP=$(date +%Y%m%d%H%M%S)
FICHERO_COMMIT="commit_message_${RAMA}_${TIMESTAMP}.txt"
NOTEBOOK="notebooks/Preprocesamiento_p7_g1_multiclase_JJ.ipynb"

echo ""
echo "========================================================"
echo "  commit_cambios_preprocesamiento"
echo "  Rama    : $RAMA"
echo "  Fichero : $FICHERO_COMMIT"
echo "========================================================"
echo ""

# ─── 0. Verificaciones previas ────────────────────────────────────────────────
echo "[0/5] Verificando entorno..."

if [ ! -f "pyproject.toml" ]; then
    echo "ERROR: Ejecuta desde la raíz del proyecto (donde está pyproject.toml)."
    exit 1
fi

RAMA_ACTUAL=$(git branch --show-current)
if [ "$RAMA_ACTUAL" != "$RAMA" ]; then
    echo "ERROR: Estás en la rama '$RAMA_ACTUAL', se esperaba '$RAMA'."
    echo "       Ejecuta: git checkout $RAMA"
    exit 1
fi

if [ ! -f "$NOTEBOOK" ]; then
    echo "ERROR: No se encuentra $NOTEBOOK"
    exit 1
fi

echo "  ✓ Rama correcta        : $RAMA"
echo "  ✓ Notebook encontrado  : $NOTEBOOK"

# ─── 1. Generar fichero de commit con timestamp ───────────────────────────────
echo ""
echo "[1/5] Generando fichero de commit: $FICHERO_COMMIT"

cat > "$FICHERO_COMMIT" << ENDOFCOMMIT
feat(jj): ejecución verificada de Preprocesamiento_p7_g1_multiclase_JJ.ipynb · ${TIMESTAMP}

TIPO DE CAMBIO
==============
El código fuente del notebook NO ha cambiado.
Se ha ejecutado el notebook completo registrando los outputs reales
de las 8 celdas de código (antes vacíos).

FICHERO MODIFICADO
==================
${NOTEBOOK}

OUTPUTS REGISTRADOS (resumen)
==============================
Celda 1 · Dataset cargado: 2087 filas x 17 columnas
          FAVC verificado: ['no', 'yes'] — CSV de entrada correcto

Celda 2 · Columnas clasificadas por tipo correctamente

Celda 3 · Mapeo clínico 7 clases sin NaN:
          0→Insufficient_Weight (267)  1→Normal_Weight (282)
          2→Overweight_Level_I (276)   3→Overweight_Level_II (290)
          4→Obesity_Type_I (351)       5→Obesity_Type_II (297)
          6→Obesity_Type_III (324)     TOTAL=2087

Celda 3b· df.head() verificado: binarias 0/1, target_encoded 0-6

Celda 4 · Encoding completado: todas columnas numéricas, ningún object

Celda 5 · Split: train=1669 / test=418
          Distribución estratificada coherente entre ambos conjuntos

Celda 6 · StandardScaler: mean≈0.00, std≈1.00 en columnas numéricas

Celda 7 · Artefactos guardados en data/processed/ y models/

VERIFICACIÓN GLOBAL
===================
· Sin errores ni excepciones en ninguna celda
· assert NaN no saltó — mapeo clínico correcto
· 1669 + 418 = 2087 registros — split coherente
· Notebook listo como entrada del notebook de modelado

CONVENCIÓN DE FICHEROS DE COMMIT
==================================
commit_message_<rama>_<YYYYMMDDHHmmss>.txt
ENDOFCOMMIT

echo "  ✓ Fichero de commit creado"

# ─── 2. Stage del notebook y del fichero de commit ────────────────────────────
echo ""
echo "[2/5] Añadiendo al stage..."

git add "$NOTEBOOK"
git add "$FICHERO_COMMIT"

echo ""
echo "  Ficheros en stage:"
git status --short

# ─── 3. Confirmación ──────────────────────────────────────────────────────────
echo ""
echo "========================================================"
echo "  ¿Confirmas el commit? (s/n)"
echo "========================================================"
read -r CONFIRMAR

if [ "$CONFIRMAR" != "s" ] && [ "$CONFIRMAR" != "S" ]; then
    echo "Operación cancelada."
    git restore --staged "$NOTEBOOK" "$FICHERO_COMMIT" 2>/dev/null || true
    rm -f "$FICHERO_COMMIT"
    exit 0
fi

# ─── 4. Commit ────────────────────────────────────────────────────────────────
echo ""
echo "[3/5] Realizando commit..."
git commit -F "$FICHERO_COMMIT"
echo "  ✓ Commit realizado"

# ─── 5. Push ──────────────────────────────────────────────────────────────────
echo ""
echo "[4/5] Push a GitHub..."
git push origin "$RAMA"

echo ""
echo "========================================================"
echo "  ✓ Push completado"
echo "  Fichero de commit guardado: $FICHERO_COMMIT"
echo "  (queda en el repo como registro de versión)"
echo "========================================================"
echo ""
echo "[5/5] Log del último commit:"
git log --oneline -3
