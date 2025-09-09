# House Layout Scoring System (Listing Score Demo)

An intelligent house layout scoring system based on traditional Chinese Feng Shui (Eight Mansions theory), which uses OCR technology to identify room labels in floor plan images and combines Nine Palace grid analysis to evaluate the auspiciousness of house layouts.

## Features

- 🏠 **Smart OCR Recognition**: Automatically identifies room labels in floor plan images (bedrooms, kitchens, bathrooms, etc.)
- 🧭 **Directional Analysis**: Analyzes room positions based on Nine Palace grid theory
- 📐 **Feng Shui Scoring**: Comprehensive scoring of house layouts based on Eight Mansions theory
- 🎯 **Detailed Recommendations**: Provides targeted layout optimization suggestions
- 📊 **Visual Output**: Generates structured JSON scoring reports

## System Architecture

The system consists of two main modules:

1. **`fp2layout.py`** - Floor Plan Analysis Module

   - Uses OpenCV for image preprocessing
   - Identifies room labels through Tesseract OCR
   - Maps room positions to Nine Palace grid system
   - Automatically infers house orientation

2. **`zhongxuan_scorer.py`** - Feng Shui Scoring Module
   - Performs auspicious/inauspicious judgments based on Eight Mansions theory
   - Scores individual room positions
   - Generates comprehensive scores and recommendations

## Installation

### Requirements

- Python 3.9+
- Tesseract OCR

### Installation Steps

1. Create conda environment:

   ```bash
   conda env create -f environment.yaml
   conda activate listing-score-env
   ```

2. Install Tesseract OCR:

   **macOS:**

   ```bash
   brew install tesseract
   ```

   **Ubuntu/Debian:**

   ```bash
   sudo apt-get install tesseract-ocr
   ```

**Windows:**
Download and install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)

## Usage

### 1. Floor Plan Analysis

```bash
python fp2layout.py --image data/test.png --north-deg 0.0 --house-facing S --out layout.json
```

**Parameters:**

- `--image`: Input floor plan image file path
- `--north-deg`: True north angle relative to image top (clockwise degrees)
- `--house-facing`: House orientation (N/NE/E/SE/S/SW/W/NW), optional, system will auto-infer
- `--out`: Output JSON file path

### 2. Feng Shui Scoring

```bash
python zhongxuan_scorer.py layout.json
```

**Output Example:**

```json
{
  "total": 75,
  "grade": "B",
  "house_gua": "坎宅(东四宅)",
  "breakdown": {
    "main_door": { "score": 20, "why": "大门在S(吉位)" },
    "master_bed": { "score": 0, "why": "未检测到主卧" },
    "kitchen": { "score": -10, "why": "厨房占中宫不宜" },
    "bath_laundry": { "score": 0, "why": "未检测到湿区" },
    "other_bed": { "score": 0, "why": "卧室吉0间、凶2间" },
    "garage_store": { "score": 0, "why": "0处，凶位给+1/处" },
    "center_c": { "score": -5, "why": "中宫包含：kitchen" },
    "throughline": { "score": 0, "why": "未检测/不成立" }
  },
  "advice": [
    "厨房落吉位易泄吉：宜以金属与中性色弱化火气，炉口朝宅吉方。",
    "整体格局稳健：保持整洁、通风、动静分区即可。"
  ]
}
```

## Scoring Criteria

### Eight Mansions Theory Foundation

The system is based on traditional Eight Mansions theory, categorizing houses into East Four Houses and West Four Houses:

- **East Four Houses**: Kan House (South), Li House (North), Zhen House (West), Xun House (Northwest)
- **West Four Houses**: Qian House (Southeast), Dui House (East), Gen House (Southwest), Kun House (Northeast)

### Scoring Items

1. **Main Door Position** (Weight: 20 points)

   - Auspicious position: +20 points
   - Center palace: -10 points
   - Inauspicious position: -15 points

2. **Master Bedroom Position** (Weight: 12 points)

   - Auspicious position: +12 points
   - Center palace: -10 points
   - Inauspicious position: -12 points

3. **Kitchen Position** (Weight: 10 points)

   - Inauspicious position: +10 points (drains negative energy)
   - Center palace: -10 points
   - Auspicious position: -8 points (drains positive energy)

4. **Bathroom/Laundry** (Weight: 2 points each)

   - Center palace: -4 points each
   - Inauspicious position: +2 points each
   - Auspicious position: -2 points each

5. **Other Bedrooms** (Weight: 3 points each)

   - Auspicious position: +3 points each
   - Center palace: -4 points each
   - Inauspicious position: -3 points each

6. **Garage/Storage** (Weight: 1 point each)

   - Inauspicious position: +1 point each

7. **Center Palace Usage** (Weight: 5 points)

   - Kitchen/bathroom in center: -5 points

8. **Direct Line Through** (Weight: 8 points)
   - Entry and back door alignment: -8 points

### Grade Assessment

- **S Grade**: 90-100 points (Excellent)
- **A Grade**: 80-89 points (Good)
- **B Grade**: 70-79 points (Average)
- **C Grade**: 60-69 points (Fair)
- **D Grade**: 0-59 points (Poor)

## Supported Room Types

The system can identify the following room types:

- **Entry**: entry, porch, foyer
- **Bedrooms**: master_bedroom, bedroom, bedroom_1-5
- **Kitchen**: kitchen, pantry
- **Bathroom**: bath, wc, ensuite, laundry
- **Storage**: garage, store, wir, robe
- **Others**: lounge, living_dining, alfresco, study, office

## Technical Details

### OCR Preprocessing

- Image grayscale conversion
- Bilateral filtering for noise reduction
- Adaptive threshold binarization
- Morphological dilation processing

### Nine Palace Grid Mapping

Divides the floor plan into a 3×3 Nine Palace grid:

```text
NW  N  NE
W   C  E
SW  S  SE
```

### Direction Calculation

- Calculates room relative positions based on image center
- Supports true north angle correction
- Automatically infers house orientation

## File Structure

```
listing-score-demo/
├── fp2layout.py          # Floor plan analysis module
├── zhongxuan_scorer.py   # Feng Shui scoring module
├── environment.yaml      # Conda environment configuration
├── layout.json          # Example output file
├── data/
│   └── test.png         # Example floor plan
├── README.md            # Chinese documentation
└── README_EN.md         # English documentation
```

## Important Notes

1. **Image Quality**: Ensure floor plans are clear with readable room label text
2. **Orientation Setting**: Accurately set true north angle for correct directional analysis
3. **Label Recognition**: System relies on OCR recognition; complex fonts or blurry text may affect accuracy
4. **Cultural Context**: Scoring criteria based on traditional Chinese Feng Shui theory, suitable for related cultural backgrounds

## Contributing

We welcome Issues and Pull Requests to improve the system:

1. Add new room type recognition
2. Optimize OCR recognition accuracy
3. Improve Feng Shui scoring algorithms
4. Add more layout analysis features

## License

This project is for learning and research purposes only.

## Contact

For questions or suggestions, please contact us through Issues.
