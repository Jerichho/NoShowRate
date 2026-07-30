# Airline No-Show Rate Prediction

This project aims to predict airline no-show rates to optimize ticket sales and overbooking strategies using SAS Viya Workbench for Learners.

## 🌟 Features

### Web Application
- **Modern UI/UX**: Beautiful, responsive design with gradient backgrounds and smooth animations
- **Interactive Prediction Form**: User-friendly form with floating labels, validation, and helpful tooltips
- **Real-time Predictions**: Instant no-show probability calculations with risk indicators
- **Analytics Dashboard**: Comprehensive dashboard with charts, statistics, and insights
- **Mobile Responsive**: Optimized for all device sizes
- **Demo Mode**: Works even without trained models using intelligent fallback predictions

### Key Improvements
- ✅ Enhanced form validation and user feedback
- ✅ Loading states and error handling
- ✅ Risk level indicators (Low/Medium/High)
- ✅ Auto-calculation of lead times
- ✅ Smooth animations and transitions
- ✅ Professional navigation and footer
- ✅ Data visualization with Chart.js
- ✅ System health monitoring

Project Structure

```
/no-show-analysis
├── data/               # Raw and processed data files
├── sas_scripts/        # SAS analysis scripts
├── python_scripts/     # Python analysis scripts
├── r_scripts/         # R analysis scripts
├── models/            # Saved model files
├── outputs/           # Generated reports and visualizations
└── README.md          # Project documentation
```

Workflow

1. **Data Cleaning** (`01_data_cleaning.sas` / `python_cleaning.py`)
   - Handle missing values
   - Standardize date formats
   - Encode categorical variables
   - Log transformations

2. **Exploratory Data Analysis** (`02_eda.r` / `python_eda.py`)
   - No-show rate distributions
   - Feature correlations
   - Temporal patterns
   - Visualizations

3. **Modeling** (`03_modeling.sas` / `python_model.py`)
   - Logistic Regression
   - Random Forest
   - AutoML (if available)
   - Model comparison

4. **Evaluation** (`04_evaluation.r`)
   - Performance metrics
   - Model validation
   - Business impact analysis

5. **Reporting** (`05_reporting.py`)
   - Dashboard generation
   - Business insights
   - Recommendations

## 🚀 Quick Start

### Running the Web Application
```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask application
python app.py
```

The application will be available at `http://localhost:8080`

### Pages
- **Home** (`/`): Main prediction interface
- **Dashboard** (`/dashboard`): Analytics and system monitoring
- **Health Check** (`/health`): System status endpoint
- **Stats** (`/stats`): System statistics

## 🛠 Tech Stack 

### Backend
- **Flask**: Web framework
- **Python 3.x**: Core language
- **scikit-learn**: Machine learning models
- **pandas/numpy**: Data processing
- **joblib**: Model serialization

### Frontend
- **Bootstrap 5.3**: UI framework
- **Font Awesome**: Icons
- **Chart.js**: Data visualization
- **jQuery**: JavaScript interactions
- **Inter Font**: Typography

### Analysis Tools
- **SAS Viya Workbench**: Statistical analysis
- **R 4.x**: Statistical computing
- **Python**: Data science pipeline

### Required packages (see requirements.txt)



