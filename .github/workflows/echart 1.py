from flask import Flask, send_file, jsonify
import pandas as pd
import os

app = Flask(__name__)


@app.route('/')
def index():
    return send_file('1.html')


@app.route('/api/modules')
def get_modules():
    df = pd.read_excel("大学生价值观问卷调查V10-2.xlsx")
    return jsonify(df['上课方式'].unique().tolist())


@app.route('/api/analysis/<mode>')
def get_analysis(mode):
    df = pd.read_excel("大学生价值观问卷调查V10-2.xlsx")
    filtered = df[df['上课方式'] == mode]

    # 修正活动处理逻辑
    activities = filtered['周末活动'].str.split(',').explode().str.strip()
    activity_counts = activities.value_counts().head(20)

    return jsonify({
        "学习模式": filtered['学习模式'].value_counts().to_dict(),
        "冲突选择": filtered['冲突选择'].value_counts().to_dict(),
        "周末活动": activity_counts.to_dict()
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)