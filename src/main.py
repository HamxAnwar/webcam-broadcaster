from flask import Flask, render_template, Response, jsonify
import logging
import os
from camera import Camera

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

camera = None
CAMERA_INDEX = int(os.environ.get('CAMERA_INDEX', '0'))
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', '5000'))

def get_camera():
    global camera
    if camera is None:
        camera = Camera(camera_index=CAMERA_INDEX)
        if not camera.start():
            logger.error('Failed to start camera')
    return camera

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    cam = get_camera()
    if cam is None:
        return 'Camera not available', 503

    def generate():
        while True:
            frame = cam.get_frame()
            if frame is None:
                continue
            yield (b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/status')
def status():
    cam = get_camera()
    if cam is None:
        return jsonify({'error': 'Camera not initialized'}), 503

    return jsonify({
        'camera': cam.get_info(),
        'server': {'host': HOST, 'port': PORT}
    })

@app.route('/api/snapshot')
def snapshot():
    cam = get_camera()
    if cam is None:
        return 'Camera not available', 503

    frame = cam.get_frame()
    if frame is None:
        return 'Failed to capture frame', 503

    return Response(frame, mimetype='image/jpeg')

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

def main():
    logger.info('Starting Camera Server...')
    logger.info('Camera index: {}'.format(CAMERA_INDEX))
    logger.info('Server will run on http://{}:{}'.format(HOST, PORT))
    logger.info('Access the camera feed at: http://<YOUR_IP_ADDRESS>:{}'.format(PORT))

    try:
        app.run(host=HOST, port=PORT, debug=False, threaded=True)
    except KeyboardInterrupt:
        logger.info('Shutting down...')
    finally:
        if camera is not None:
            camera.stop()

if __name__ == '__main__':
    main()
