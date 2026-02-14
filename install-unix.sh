#!/bin/bash
# Apion - Installation Script for Unix/Linux/macOS

set -e

echo "🚀 Apion - HTTP Client Pro"
echo "=========================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.7+ first."
    exit 1
fi

echo "✓ Python 3 detected: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate venv
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Installation complete!"
echo ""
echo "To run Apion:"
echo "  ./run.sh"
echo ""
echo "Or manually:"
echo "  source venv/bin/activate"
echo "  python3 http_client_stable.py"
echo ""

# Create launcher script
cat > apion << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/venv/bin/activate"
python3 "$SCRIPT_DIR/http_client_stable.py" "$@"
EOF

chmod +x apion

echo "💡 Quick start: ./apion"
echo ""
echo "Want to install globally? Run:"
echo "  sudo cp apion /usr/local/bin/"
