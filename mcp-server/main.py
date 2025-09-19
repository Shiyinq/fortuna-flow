import sys
from src.server import mcp

def main():
    try:
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        print("\nServer stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()