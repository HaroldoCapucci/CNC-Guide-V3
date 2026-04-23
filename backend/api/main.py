from flask import Flask, request, jsonify
from flask_cors import CORS
from core.gcode_parser import GcodeParser
from core.post_processor import PostProcessorFactory
from core.time_estimator import TimeEstimator

app = Flask(__name__)
CORS(app)

@app.route('/api/parse-gcode', methods=['POST'])
def parse_gcode():
    data = request.json
    gcode = data.get('gcode', '')
    parser = GcodeParser()
    commands = parser.parse(gcode)
    return jsonify({'commands_count': len(commands), 'success': True})

@app.route('/api/post-process', methods=['POST'])
def post_process():
    data = request.json
    gcode = data.get('gcode', '')
    machine = data.get('machine_type', 'mitsubishi')
    parser = GcodeParser()
    commands = parser.parse(gcode)
    processor = PostProcessorFactory.create(machine)
    processed = processor.process(commands)
    return jsonify({'gcode': processed, 'success': True})

@app.route('/api/estimate-time', methods=['POST'])
def estimate():
    data = request.json
    gcode = data.get('gcode', '')
    rate = data.get('hourly_rate', 100.0)
    parser = GcodeParser()
    commands = parser.parse(gcode)
    estimator = TimeEstimator(rate)
    result = estimator.estimate(commands)
    return jsonify({
        'total_time_seconds': result.total_time_seconds,
        'total_distance_mm': result.total_distance_mm,
        'estimated_cost': result.estimated_cost,
        'rapid_moves': result.rapid_moves,
        'cutting_moves': result.cutting_moves
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
