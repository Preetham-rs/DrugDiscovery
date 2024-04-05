# Check if seaborn is installed
try:
    import seaborn
    print("seaborn is installed.")
except ImportError:
    print("seaborn is not installed.")

# Check if scikit-learn is installed
try:
    import sklearn
    print("scikit-learn is installed.")
except ImportError:
    print("scikit-learn is not installed.")

# Check if joblib is installed
try:
    import joblib
    print("joblib is installed.")
except ImportError:
    print("joblib is not installed.")

# Check if subprocess is available (it's a built-in module so it should be available)
import subprocess
print("subprocess is available.")
