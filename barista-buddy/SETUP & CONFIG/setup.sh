#!/bin/bash

# Barista Buddy Setup Script
# Automated installation and configuration

echo "======================================================================"
echo "🎯 BARISTA BUDDY - SETUP SCRIPT"
echo "======================================================================"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.8"

if [[ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]]; then 
    echo -e "${RED}✗ Python 3.8+ required. Found: $python_version${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python $python_version${NC}"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}⚠ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}✓ pip upgraded${NC}"

# Install requirements
echo ""
echo "Installing Python packages..."
echo "This may take 5-10 minutes..."
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ All packages installed${NC}"
else
    echo -e "${RED}✗ Package installation failed${NC}"
    exit 1
fi

# Create models directory
echo ""
echo "Creating models directory..."
mkdir -p models
echo -e "${GREEN}✓ Models directory created${NC}"

# Download Vosk model
echo ""
echo "Downloading Vosk speech recognition model..."
echo "Size: ~40MB"

if [ ! -d "models/vosk-model-small-en-us-0.15" ]; then
    cd models
    
    # Download using wget or curl
    if command -v wget &> /dev/null; then
        wget -q --show-progress https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
    elif command -v curl &> /dev/null; then
        curl -L -o vosk-model-small-en-us-0.15.zip https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
    else
        echo -e "${RED}✗ Neither wget nor curl found. Please install one.${NC}"
        exit 1
    fi
    
    # Extract
    if [ -f "vosk-model-small-en-us-0.15.zip" ]; then
        unzip -q vosk-model-small-en-us-0.15.zip
        rm vosk-model-small-en-us-0.15.zip
        echo -e "${GREEN}✓ Vosk model downloaded and extracted${NC}"
    else
        echo -e "${RED}✗ Download failed${NC}"
        exit 1
    fi
    
    cd ..
else
    echo -e "${YELLOW}⚠ Vosk model already exists${NC}"
fi

# Download sentence transformer model (will be cached on first run)
echo ""
echo "Pre-downloading sentence transformer model..."
python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')" 2>&1 | grep -v "Some weights"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Sentence transformer model ready${NC}"
else
    echo -e "${YELLOW}⚠ Model will download on first run${NC}"
fi

# Test microphone
echo ""
echo "Testing microphone..."
python3 -c "import sounddevice as sd; print(sd.query_devices())" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Microphone detected${NC}"
else
    echo -e "${YELLOW}⚠ Microphone test failed (optional)${NC}"
fi

# Create README in models directory
cat > models/README.md << 'EOF'
# Models Directory

## Vosk Model
- **Model**: vosk-model-small-en-us-0.15
- **Size**: 40MB
- **Purpose**: Speech-to-Text
- **Language**: English (US)

## Sentence Transformer
- **Model**: all-MiniLM-L6-v2
- **Size**: ~80MB (cached in ~/.cache/torch/)
- **Purpose**: Semantic search and topic filtering

## Optional: Local LLM
If you want to use the LLM mode, you can download:
- **TinyLlama-1.1B-Chat** (~2GB) - Fast, good quality
- **Phi-3-mini-4k-instruct** (~7GB) - Better quality, slower

These will download automatically on first use.

Note: LLM is optional. The system works great without it using
pure retrieval!
EOF

echo ""
echo "======================================================================"
echo -e "${GREEN}✓ SETUP COMPLETE!${NC}"
echo "======================================================================"
echo ""
echo "To run Barista Buddy:"
echo ""
echo "  1. Activate environment:  source venv/bin/activate"
echo "  2. Run interactive mode:  python main.py"
echo "  3. Run with text only:    python main.py --no-voice-input --no-voice-output"
echo "  4. Run test queries:      python main.py --test"
echo "  5. Single query:          python main.py --query \"how to make espresso\""
echo ""
echo "For help:  python main.py --help"
echo ""
echo "======================================================================"