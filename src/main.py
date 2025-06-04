# main.py
import sys
from constants import DATA_PATH, DEFAULT_RECO_N
from recommender import run_pipeline

def main():
    """
    Entry point for the perfume recommendation script.
    """
    if len(sys.argv) < 2:
        print("❌ Please provide a perfume name as a command-line argument.")
        sys.exit(1)

    perfume_name = sys.argv[1]
    top_n = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_RECO_N

    recommendations = run_pipeline(DATA_PATH, perfume_name, top_n)

    if recommendations.empty:
        print(f"🔍 No recommendations found for: {perfume_name}")
    else:
        print(f"\n🎯 Top {top_n} recommendations for '{perfume_name}':\n")
        print(recommendations.to_string(index=False))

if __name__ == "__main__":
    main()
