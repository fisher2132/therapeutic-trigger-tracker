# 🧠 Therapeutic Trigger Tracker

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

> **A comprehensive, evidence-based mental health tracking application designed to help individuals understand, monitor, and manage their emotional triggers through therapeutic insights and data-driven self-awareness.**

---

## 📋 Table of Contents

- [🌟 Overview](#-overview)
- [✨ Features](#-features)
- [🔬 Therapeutic Framework](#-therapeutic-framework)
- [🚀 Quick Start](#-quick-start)
- [📦 Installation](#-installation)
- [🎯 Usage](#-usage)
- [📊 Screenshots](#-screenshots)
- [🛠️ Technical Details](#️-technical-details)
- [🏗️ Architecture](#️-architecture)
- [🤝 Contributing](#-contributing)
- [📚 Resources](#-resources)
- [📄 License](#-license)
- [👨‍⚕️ Disclaimer](#️-disclaimer)

---

## 🌟 Overview

The **Therapeutic Trigger Tracker** is a sophisticated mental health application that combines evidence-based psychological frameworks with modern data visualization to provide users with deep insights into their emotional patterns and triggers. Built with Python and Streamlit, it offers a professional-grade therapeutic tracking experience while remaining accessible and user-friendly.

### 🎯 Mission
*Empowering individuals with data-driven self-awareness tools to understand, process, and grow from their emotional experiences through evidence-based therapeutic approaches.*

### 🏆 Key Benefits
- **🔍 Pattern Recognition**: Identify recurring triggers and emotional responses
- **📈 Progress Tracking**: Monitor your healing journey with quantifiable metrics
- **🛠️ Coping Tools**: Access evidence-based therapeutic techniques
- **🎯 Personalized Insights**: Receive tailored recommendations based on your data
- **💪 Empowerment**: Take control of your mental health journey

---

## ✨ Features

### 📝 **Comprehensive Entry System**
- **Multi-dimensional trigger categorization** (Interpersonal, Environmental, Cognitive, Physical, etc.)
- **Enhanced emotional tracking** including complex emotions (shame, loneliness, overwhelm)
- **Narrative therapy elements** (before/after contexts, thoughts, physical sensations)
- **Coping strategy effectiveness rating**
- **Therapeutic check-ins** (self-compassion, safety, energy levels)

### 📊 **Advanced Analytics Dashboard**
- **Real-time wellness scoring** algorithm
- **Emotional trend analysis** with moving averages
- **Trigger pattern recognition** across time and location
- **Intensity correlation studies**
- **Progress indicators** with visual feedback

### 🎯 **Therapeutic Insights Engine**
- **Personalized recommendations** based on clinical frameworks
- **Evidence-based intervention suggestions**
- **Crisis support indicators** for high-intensity patterns
- **Pattern analysis** using psychological best practices
- **Growth tracking** with milestone recognition

### 🛠️ **Interactive Coping Tools**
- **Guided breathing exercises** with visual prompts
- **5-4-3-2-1 grounding techniques** with interactive guidance
- **Self-compassion breaks** with therapeutic scripts
- **Personalized coping plans** for different intensity levels
- **Emergency resource management**

### 📈 **Progress & Goal Tracking**
- **SMART goal setting** with progress calculations
- **Achievement system** with therapeutic milestones
- **Consistency tracking** with streak monitoring
- **Long-term trend visualization**
- **Wellness score evolution**

### 📚 **Complete Entry Management**
- **Advanced search and filtering** across all data fields
- **Chronological organization** with multiple sorting options
- **Detailed entry views** with therapeutic context
- **Data export capabilities** for professional consultation

---

## 🔬 Therapeutic Framework

This application integrates multiple evidence-based therapeutic approaches:

### **🧘 Cognitive Behavioral Therapy (CBT)**
- Thought pattern identification and tracking
- Behavioral response analysis
- Mood-behavior correlation studies
- Cognitive restructuring support

### **💎 Dialectical Behavior Therapy (DBT)**
- Distress tolerance skill tracking
- Emotion regulation measurements
- Interpersonal effectiveness indicators
- Mindfulness integration

### **🌱 Acceptance and Commitment Therapy (ACT)**
- Values alignment assessment
- Psychological flexibility tracking
- Mindful awareness practices
- Acceptance-based interventions

### **🛡️ Trauma-Informed Care**
- Safety-focused design principles
- Trustworthiness and transparency
- Choice and collaboration emphasis
- Strengths-based approach

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/worldsocoled/therapeutic-trigger-tracker.git

# Navigate to project directory
cd therapeutic-trigger-tracker

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

**🌐 Open your browser to `http://localhost:8501` to start your therapeutic journey!**

---

## 📦 Installation

### Prerequisites
- **Python 3.7+** (recommended: Python 3.9+)
- **pip** package manager

### Dependencies
```bash
streamlit>=1.25.0
pandas>=1.5.0
plotly>=5.0.0
numpy>=1.20.0
```

### Installation Methods

#### Option 1: Using pip
```bash
pip install streamlit pandas plotly numpy
```

#### Option 2: Using requirements.txt
```bash
pip install -r requirements.txt
```

#### Option 3: Using conda
```bash
conda create -n trigger-tracker python=3.9
conda activate trigger-tracker
pip install -r requirements.txt
```

### Verify Installation
```bash
streamlit --version
python -c "import pandas, plotly, numpy; print('All dependencies installed successfully!')"
```

---

## 🎯 Usage

### 📱 **Application Navigation**

1. **✨ New Entry**: Log detailed trigger experiences with therapeutic context
2. **📊 Dashboard**: View real-time analytics and emotional trends
3. **🎯 Insights**: Receive personalized therapeutic recommendations
4. **🛠️ Coping Tools**: Access evidence-based therapeutic techniques
5. **📈 Progress**: Track long-term growth and set therapeutic goals
6. **📚 All Entries**: Manage and review your complete therapeutic journal

### 💡 **Best Practices**

- **Daily Consistency**: Aim for daily entries to capture comprehensive patterns
- **Honest Reflection**: The app is most effective with genuine, honest entries
- **Regular Review**: Weekly review of insights and progress for optimal growth
- **Professional Integration**: Share data with your therapist for enhanced treatment
- **Goal Setting**: Use the progress tracking to set and achieve therapeutic goals

### 📋 **Entry Guidelines**

1. **Take three deep breaths** before beginning each entry
2. **Be specific** about triggers and circumstances
3. **Include physical sensations** and emotional nuances
4. **Rate coping effectiveness** honestly
5. **Practice self-compassion** in your reflections

---

## 📊 Screenshots

### 🏠 **Main Dashboard**
*Real-time wellness metrics and emotional trend analysis*

### ✨ **Entry Interface**
*Comprehensive trigger logging with therapeutic framework integration*

### 🎯 **Insights Page**
*Personalized recommendations based on evidence-based psychology*

### 🛠️ **Coping Tools**
*Interactive therapeutic techniques with guided instructions*

---

## 🛠️ Technical Details

### **Architecture**
- **Frontend**: Streamlit with custom CSS/HTML
- **Backend**: Python with pandas for data processing
- **Visualization**: Plotly for interactive charts
- **Data Storage**: CSV files (easily portable and readable)
- **Styling**: Glass morphism design with therapeutic color psychology

### **Data Structure**
```python
Entry Schema:
- timestamp: datetime
- trigger: string (categorized)
- intensity: integer (1-10)
- emotions: multiple integers (anxiety, sadness, anger, etc.)
- coping_strategies: array
- effectiveness: integer (1-10)
- context: object (before, after, thoughts, physical)
- therapeutic_metrics: object (self-compassion, safety, energy)
```

### **Key Algorithms**
- **Wellness Score Calculation**: Multi-factor algorithm considering negative emotions, positive emotions, and coping effectiveness
- **Pattern Recognition**: Time-series analysis for trigger identification
- **Progress Tracking**: Trend analysis with moving averages
- **Recommendation Engine**: Rules-based system using therapeutic best practices

### **Performance**
- **Responsive Design**: Mobile-first approach with responsive layouts
- **Fast Loading**: Optimized data processing and caching
- **Scalable**: Handles thousands of entries efficiently
- **Accessible**: WCAG 2.1 compliance with proper contrast ratios

---

## 🏗️ Architecture

```
therapeutic-trigger-tracker/
├── 📄 app.py                    # Main Streamlit application
├── 📁 data/                     # Data storage directory
│   ├── triggers.csv             # Main trigger entries
│   ├── goals.csv               # Goal tracking data
│   └── coping_strategies.csv   # Personal coping plans
├── 📁 utils/                    # Utility functions (future expansion)
├── 📁 assets/                   # Images and static files
├── 📋 requirements.txt          # Python dependencies
├── 📖 README.md                # Project documentation
└── 📄 LICENSE                  # MIT License

Key Components:
├── 🎨 CSS Styling              # Therapeutic design with glass morphism
├── 📊 Data Processing          # Pandas-based analytics
├── 📈 Visualization            # Plotly interactive charts
├── 🧠 Therapeutic Logic        # Evidence-based algorithms
└── 🔧 Helper Functions         # Utility and calculation functions
```

---

## 🤝 Contributing

We welcome contributions from mental health professionals, developers, and users! Here's how you can help:

### **Ways to Contribute**
- 🐛 **Bug Reports**: Submit issues with detailed reproduction steps
- 💡 **Feature Requests**: Suggest new therapeutic tools or insights
- 📝 **Documentation**: Improve README, comments, or user guides
- 🧠 **Therapeutic Input**: Mental health professionals can suggest evidence-based improvements
- 💻 **Code Contributions**: Submit pull requests with new features or fixes

### **Development Setup**
```bash
# Fork the repository
git clone https://github.com/worldsocoled/therapeutic-trigger-tracker.git

# Create a feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git commit -m "Add: therapeutic feature description"

# Push and create pull request
git push origin feature/your-feature-name
```

### **Contribution Guidelines**
- Follow Python PEP 8 style guidelines
- Include docstrings for new functions
- Add comments for therapeutic rationale
- Test changes with sample data
- Update documentation for new features

---

## 📚 Resources

### **Therapeutic References**
- [Cognitive Behavioral Therapy Techniques](https://www.apa.org/ptsd-guideline/patients-and-families/cognitive-behavioral)
- [Dialectical Behavior Therapy Skills](https://behavioraltech.org/resources/faqs/dialectical-behavior-therapy-dbt/)
- [Acceptance and Commitment Therapy](https://contextualscience.org/act)
- [Trauma-Informed Care Principles](https://www.samhsa.gov/concept-trauma-and-guidance)

### **Technical Documentation**
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas User Guide](https://pandas.pydata.org/docs/user_guide/)
- [Plotly Python Documentation](https://plotly.com/python/)

### **Mental Health Resources**
- **Crisis Text Line**: Text HOME to 741741
- **National Suicide Prevention Lifeline**: 988
- **SAMHSA National Helpline**: 1-800-662-4357
- [Psychology Today Therapist Finder](https://www.psychologytoday.com/us/therapists)

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Therapeutic Trigger Tracker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 👨‍⚕️ Disclaimer

### **⚠️ Important Medical Notice**

**This application is designed for educational and self-reflection purposes only and is not intended to replace professional mental health care.**

- 🩺 **Not a Medical Device**: This app is not a substitute for professional diagnosis or treatment
- 👩‍⚕️ **Seek Professional Help**: Always consult qualified mental health professionals for clinical concerns
- 🚨 **Emergency Situations**: If you're experiencing thoughts of self-harm, contact emergency services immediately
- 📊 **Data Privacy**: Your data is stored locally on your device for privacy
- 🔒 **No Guarantees**: While based on evidence-based practices, results may vary

### **Crisis Resources**
- **Immediate Danger**: Call 911 (US) or your local emergency number
- **Suicide Prevention**: Call 988 (US) or visit [suicidepreventionlifeline.org](https://suicidepreventionlifeline.org)
- **Crisis Text Line**: Text HOME to 741741

---

## 📞 Support & Contact

- 🐛 **Issues**: [GitHub Issues](https://github.com/worldsocoled/therapeutic-trigger-tracker/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/worldsocoled/therapeutic-trigger-tracker/discussions)
- 📧 **Email**: worldsocoledwebartistry@gmail.com (for sensitive inquiries)

---

<div align="center">

### 🌟 **Start Your Healing Journey Today**

*"The curious paradox is that when I accept myself just as I am, then I can change."* - Carl Rogers

---

**Made with ❤️ and evidence-based psychology**

⭐ **Star this repository if it helps you on your healing journey!**

</div>
