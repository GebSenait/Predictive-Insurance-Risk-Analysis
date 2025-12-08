"""Check if dependencies are properly installed and compatible."""

import sys

def check_numpy():
    """Check numpy installation."""
    try:
        import numpy as np
        version = np.__version__
        print(f"✓ NumPy version: {version}")
        
        # Test basic operations
        arr = np.array([1, 2, 3])
        result = np.vstack([arr, arr])
        print(f"✓ NumPy vstack test passed")
        return True
    except Exception as e:
        print(f"✗ NumPy error: {e}")
        print("  Try reinstalling: pip install --upgrade --force-reinstall numpy")
        return False

def check_pandas():
    """Check pandas installation."""
    try:
        import pandas as pd
        version = pd.__version__
        print(f"✓ Pandas version: {version}")
        
        # Test basic operations
        df1 = pd.DataFrame({"A": [1, 2]})
        df2 = pd.DataFrame({"B": [3, 4]})
        result = pd.concat([df1, df2], axis=1)
        print(f"✓ Pandas concat test passed")
        return True
    except Exception as e:
        print(f"✗ Pandas error: {e}")
        print("  Try reinstalling: pip install --upgrade --force-reinstall pandas")
        return False

def check_sklearn():
    """Check scikit-learn installation."""
    try:
        import sklearn
        version = sklearn.__version__
        print(f"✓ Scikit-learn version: {version}")
        return True
    except Exception as e:
        print(f"✗ Scikit-learn error: {e}")
        return False

def main():
    """Run all checks."""
    print("Checking dependencies...")
    print("=" * 50)
    
    all_ok = True
    all_ok &= check_numpy()
    all_ok &= check_pandas()
    all_ok &= check_sklearn()
    
    print("=" * 50)
    if all_ok:
        print("✓ All dependency checks passed!")
    else:
        print("✗ Some dependency checks failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

