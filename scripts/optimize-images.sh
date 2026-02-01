#!/bin/bash
# Parallel Image Optimization Script using ImageMagick
# Generates WebP versions of images in multiple sizes for responsive loading

# Configuration (match _config.yml settings)
WIDTHS=(480 800 1400)
QUALITY=80
INPUT_DIR="assets"
OUTPUT_FORMAT="webp"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check dependencies
if ! command -v convert &> /dev/null; then
    echo -e "${RED}Error: ImageMagick is not installed or not in PATH${NC}"
    echo "Install with: brew install imagemagick"
    exit 1
fi

if ! command -v parallel &> /dev/null; then
    echo -e "${RED}Warning: GNU parallel not found. Install for faster processing:${NC}"
    echo "  brew install parallel"
    USE_PARALLEL=false
else
    USE_PARALLEL=true
fi

# Count files
EXTENSIONS=("jpg" "jpeg" "png" "JPG" "JPEG" "PNG")
FILE_COUNT=0
for ext in "${EXTENSIONS[@]}"; do
    count=$(find "$INPUT_DIR" -type f -name "*.$ext" 2>/dev/null | wc -l)
    FILE_COUNT=$((FILE_COUNT + count))
done

echo -e "${BLUE}Found $FILE_COUNT images to process${NC}"
echo -e "${BLUE}Generating ${#WIDTHS[@]} sizes per image: ${WIDTHS[*]}${NC}"

# Function to process a single image
process_image() {
    local input_file="$1"
    local filename="${input_file%.*}"
    
    for width in "${WIDTHS[@]}"; do
        output_file="${filename}-${width}.webp"
        
        # Skip if output already exists and is newer than input
        if [[ -f "$output_file" && "$output_file" -nt "$input_file" ]]; then
            continue
        fi
        
        # Generate responsive version
        convert "$input_file" \
            -strip \
            -resize "${width}x>" \
            -quality "$QUALITY" \
            -define webp:method=4 \
            "$output_file" 2>/dev/null
        
        if [[ $? -eq 0 ]]; then
            echo -e "${GREEN}✓${NC} ${input_file} → ${width}w"
        else
            echo -e "${RED}✗${NC} Failed: ${input_file}"
        fi
    done
}

export -f process_image
export WIDTHS QUALITY GREEN RED NC

# Find all images and process
START_TIME=$(date +%s)

if $USE_PARALLEL; then
    echo -e "${BLUE}Using GNU parallel for faster processing...${NC}"
    find "$INPUT_DIR" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) | \
        parallel -j $(sysctl -n hw.ncpu) process_image {}
else
    echo -e "${BLUE}Processing sequentially (install 'parallel' for faster processing)...${NC}"
    find "$INPUT_DIR" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) | \
        while read -r file; do
            process_image "$file"
        done
fi

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}Image optimization complete in ${DURATION} seconds${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
