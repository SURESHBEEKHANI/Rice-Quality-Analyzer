# 🌾 Rice Quality Analyzer

## 📌 Project Overview
The **Rice Quality Analyzer** is an AI-powered application that analyzes images of rice grains to assess their quality. Using deep learning and computer vision, the app provides accurate insights into **broken grains**, **discoloration**, and **impurities** percentages.

## 🚀 Features
- **Rice Type Classification** (e.g., Basmati, Jasmine, Indica)
- **Quality Analysis** (Broken grains %, Impurities %, Discoloration %)
- **Foreign Object Detection** (Husks, stones, debris)
- **Grain Size & Shape Consistency Check**
- **Processing Recommendations**
- **PDF Report Generation**

## 🛠️ Installation & Setup
### 1️⃣ Prerequisites
Ensure you have **Python 3.8+** installed.

### 2️⃣ Clone the Repository
```bash
git https://github.com/SURESHBEEKHANI/Rice-Quality-Analyzer.git 
cd rice-quality-analyzer
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up API Key
- Create a `.env` file in the project root.
- Add your **Groq API Key**:
```bash
GROQ_API_KEY=your_api_key_here
```

### 5️⃣ Run the Application
```bash
streamlit run app.py
```

## 📷 Usage
1. Upload an image of rice grains.
2. Click **"Analyze Rice Quality"**.
3. Get a structured report with percentages for **broken grains, discoloration, and impurities**.
4. Download the **PDF report** for further analysis.

## 📄 Example Report Output
```
Rice Quality Report
---------------------------
- Rice Type: Basmati
- Broken Grains: 4.5%
- Discoloration: 2.3%
- Impurities: 1.1%
- Foreign Objects: None detected
- Processing Recommendation: Suitable for high-grade packaging
```

## 🛠 Tech Stack
- **Python**
- **Streamlit** (Frontend UI)
- **Pillow** (Image Processing)
- **Groq API** (AI Model for Analysis)
- **ReportLab** (PDF Report Generation)

## 🤝 Contributing
Feel free to fork this repository, make improvements, and submit a pull request!

## 📜 License
This project is licensed under the MIT License.

---
🚀 **Developed with AI for Precision Rice Quality Analysis!**

