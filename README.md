# 房屋布局评分系统 (Listing Score Demo)

一个基于中国传统风水学（八宅理论）的智能房屋布局评分系统，通过 OCR 技术识别房屋平面图中的房间标签，并结合九宫格方位分析来评估房屋布局的吉凶。

## 功能特点

- 🏠 **智能 OCR 识别**: 自动识别房屋平面图中的房间标签（卧室、厨房、卫生间等）
- 🧭 **方位分析**: 基于九宫格理论分析房间在房屋中的位置
- 📐 **风水评分**: 根据八宅理论对房屋布局进行综合评分
- 🎯 **详细建议**: 提供针对性的布局优化建议
- 📊 **可视化输出**: 生成结构化的 JSON 评分报告

## 系统架构

系统分为两个主要模块：

1. **`fp2layout.py`** - 平面图解析模块

   - 使用 OpenCV 进行图像预处理
   - 通过 Tesseract OCR 识别房间标签
   - 将房间位置映射到九宫格系统
   - 自动推断房屋朝向

2. **`zhongxuan_scorer.py`** - 风水评分模块
   - 基于八宅理论进行吉凶判断
   - 对各个房间位置进行评分
   - 生成综合评分和建议

## 安装依赖

### 环境要求

- Python 3.9+
- Tesseract OCR

### 安装步骤

1. 创建 conda 环境：

   ```bash
   conda env create -f environment.yaml
   conda activate listing-score-env
   ```

2. 安装 Tesseract OCR：

   **macOS:**

   ```bash
   brew install tesseract
   ```

   **Ubuntu/Debian:**

   ```bash
   sudo apt-get install tesseract-ocr
   ```

**Windows:**
下载并安装 [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)

## 使用方法

### 🌐 Web 应用（推荐）

启动 Web 界面进行交互式分析：

```bash
# 激活环境
conda activate listing-score-env

# 启动 Web 应用
python run_app.py
# 或者直接使用 streamlit
streamlit run app.py
```

然后在浏览器中打开 `http://localhost:8501` 即可使用图形界面。

**Web 应用功能：**

- 📁 拖拽上传平面图
- ⚙️ 可视化参数设置
- 🔍 一键分析评分
- 📊 实时结果展示
- 💡 智能优化建议
- 🌐 中英文语言切换

### 💻 命令行使用

#### 1. 平面图解析

```bash
python fp2layout.py --image data/test.png --north-deg 0.0 --house-facing S --out layout.json
```

**参数说明：**

- `--image`: 输入平面图文件路径
- `--north-deg`: 真北相对于图像上方的角度（顺时针度数）
- `--house-facing`: 房屋朝向（N/NE/E/SE/S/SW/W/NW），可选，系统会自动推断
- `--out`: 输出 JSON 文件路径

#### 2. 风水评分

```bash
python zhongxuan_scorer.py layout.json
```

**输出示例：**

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

## 评分标准

### 八宅理论基础

系统基于传统八宅理论，将房屋分为东四宅和西四宅：

- **东四宅**: 坎宅(南)、离宅(北)、震宅(西)、巽宅(西北)
- **西四宅**: 乾宅(东南)、兑宅(东)、艮宅(西南)、坤宅(东北)

### 评分项目

1. **大门位置** (权重: 20 分)

   - 吉位: +20 分
   - 中宫: -10 分
   - 凶位: -15 分

2. **主卧位置** (权重: 12 分)

   - 吉位: +12 分
   - 中宫: -10 分
   - 凶位: -12 分

3. **厨房位置** (权重: 10 分)

   - 凶位: +10 分 (泄凶)
   - 中宫: -10 分
   - 吉位: -8 分 (泄吉)

4. **卫浴/洗衣房** (权重: 2 分/处)

   - 中宫: -4 分/处
   - 凶位: +2 分/处
   - 吉位: -2 分/处

5. **其他卧室** (权重: 3 分/间)

   - 吉位: +3 分/间
   - 中宫: -4 分/间
   - 凶位: -3 分/间

6. **车库/储物间** (权重: 1 分/处)

   - 凶位: +1 分/处

7. **中宫占用** (权重: 5 分)

   - 厨房/卫浴在中宫: -5 分

8. **穿堂直冲** (权重: 8 分)
   - 入口与后门对穿: -8 分

### 等级评定

- **S 级**: 90-100 分 (优秀)
- **A 级**: 80-89 分 (良好)
- **B 级**: 70-79 分 (中等)
- **C 级**: 60-69 分 (一般)
- **D 级**: 0-59 分 (较差)

## 支持的房间类型

系统可以识别以下房间类型：

- **入口**: entry, porch, foyer
- **卧室**: master_bedroom, bedroom, bedroom_1-5
- **厨房**: kitchen, pantry
- **卫浴**: bath, wc, ensuite, laundry
- **储物**: garage, store, wir, robe
- **其他**: lounge, living_dining, alfresco, study, office

## 技术细节

### OCR 预处理

- 图像灰度化
- 双边滤波去噪
- 自适应阈值二值化
- 形态学膨胀处理

### 九宫格映射

将房屋平面图划分为 3×3 的九宫格：

```text
NW  N  NE
W   C  E
SW  S  SE
```

### 方位计算

- 基于图像中心点计算房间相对位置
- 支持真北角度校正
- 自动推断房屋朝向

## 文件结构

```sh
listing-score-demo/
├── fp2layout.py          # 平面图解析模块
├── zhongxuan_scorer.py   # 风水评分模块
├── app.py               # Streamlit Web 应用
├── run_app.py           # Web 应用启动脚本
├── locales.py           # 多语言配置文件
├── test_i18n.py         # 多语言功能测试
├── environment.yaml      # Conda环境配置
├── layout.json          # 示例输出文件
├── data/
│   └── test.png         # 示例平面图
├── README.md            # 中文说明文档
└── README_EN.md         # 英文说明文档
```

## 注意事项

1. **图像质量**: 确保平面图清晰，房间标签文字可读
2. **朝向设置**: 准确设置真北角度以获得正确的方位分析
3. **标签识别**: 系统依赖 OCR 识别，复杂字体或模糊文字可能影响准确性
4. **文化背景**: 评分标准基于中国传统风水理论，适用于相关文化背景

## 贡献指南

欢迎提交 Issue 和 Pull Request 来改进系统：

1. 增加新的房间类型识别
2. 优化 OCR 识别准确率
3. 完善风水评分算法
4. 添加更多布局分析功能

## 许可证

本项目仅供学习和研究使用。

## 联系方式

如有问题或建议，请通过 Issue 联系。
