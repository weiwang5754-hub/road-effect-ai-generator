#!/usr/bin/env python3
"""
市政横断面道路效果图生成器 - API后端
====================================
部署到任意支持Python的平台（Railway/Render/Vercel/自建服务器）
前端GitHub Pages页面会调用此API进行图片生成

部署方式：
  pip install flask flask-cors
  python api/server.py
  或 gunicorn -w 4 api:app
"""

import json
import base64
import time
import os
import sys
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='../', static_url_path='')
CORS(app)

# ============================================================
# 配置
# ============================================================
PORT = int(os.environ.get('PORT', 8192))

# ============================================================
# 图片生成接口（Tabbit AI Bridge）
# ============================================================

@app.route('/api/generate', methods=['POST'])
def generate_image():
    """接收前端请求，返回生成的图片base64"""
    start_time = time.time()
    
    data = request.get_json(silent=True) or {}
    task_description = data.get('task_description', '')
    resolution = data.get('resolution', '1024x1024')
    reference_images = data.get('reference_images', [])
    model = data.get('model', 'Doubao Seedream 5.0')
    
    if not task_description:
        return jsonify({'success': False, 'error': '提示词不能为空'}), 400
    
    print(f'[生成] 模型={model} | 分辨率={resolution} | 参考图={len(reference_images)}张')
    print(f'[生成] 提示词: {task_description[:120]}...')
    
    try:
        result = _generate_via_siliconflow(task_description, resolution, reference_images)
        
        elapsed = round(time.time() - start_time, 1)
        return jsonify({
            'success': True,
            'image_base64': result,
            'model': model,
            'elapsed_seconds': elapsed
        })
        
    except Exception as e:
        elapsed = round(time.time() - start_time, 1)
        print(f'[错误] 生图失败 ({elapsed}s): {e}')
        return jsonify({
            'success': False,
            'error': str(e),
            'elapsed_seconds': elapsed
        }), 500


def _generate_via_siliconflow(prompt, resolution, ref_images):
    """通过SiliconFlow API生成图片"""
    import urllib.request
    import urllib.error
    
    try:
        w, h = [int(x) for x in resolution.lower().replace(' ', '').split('x')]
    except:
        w, h = 1024, 1024
    
    api_key = os.environ.get('SILICONFLOW_API_KEY', '')
    
    models = [
        'black-forest-labs/FLUX.1-schnell',
        'stabilityai/stable-diffusion-3-5-large',
        'Pro/black-forest-labs/FLUX.1-dev',
    ]
    
    url = 'https://api.siliconflow.cn/v1/images/generations'
    
    for model_name in models:
        payload = {
            'model': model_name,
            'prompt': prompt,
            'image_size': f'{w}:{h}',
            'num_inference_steps': 20,
        }
        
        if ref_images and ref_images[0].get('data_url'):
            b64 = ref_images[0]['data_url']
            if ',' in b64:
                b64 = b64.split(',')[1]
            payload['image'] = b64
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        if api_key:
            headers['Authorization'] = f'Bearer {api_key}'
        
        req_data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=req_data, headers=headers, method='POST')
        
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                images = result.get('images', [])
                if images:
                    img = images[0]
                    if isinstance(img, dict):
                        if img.get('b64_json'):
                            return img['b64_json']
                        elif img.get('url'):
                            return _download_b64(img['url'])
                raise Exception(f'响应异常: {str(result)[:200]}')
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', errors='ignore')[:300]
            print(f'  [{model_name}] HTTP {e.code}: {body}')
            if e.code == 401:
                raise Exception(
                    'SiliconFlow认证失败。请设置环境变量 SILICONFLOW_API_KEY\n'
                    '获取Key: https://cloud.siliconflow.cn/account/ak'
                )
            continue
        except Exception as e:
            print(f'  [{model_name}] 失败: {e}')
            continue
    
    raise Exception('所有生图模型均不可用。请检查API Key配置。')


def _download_b64(url):
    """下载图片URL并转为base64"""
    import urllib.request
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return base64.b64encode(resp.read()).decode('utf-8')


@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        'success': True,
        'status': 'running',
        'backend': 'Tabbit AI Bridge (SiliconFlow)',
        'has_api_key': bool(os.environ.get('SILICONFLOW_API_KEY')),
    })

@app.route('/')
def serve_index():
    return send_from_directory('../', 'road-effect-generator.html')

if __name__ == '__main__':
    print('=' * 55)
    print('  🛤️ 市政道路效果图生成器 - API后端')
    print('=' * 55)
    print(f'  端口: {PORT}')
    print(f'  API: /api/generate')
    print(f'  状态: /api/status')
    print('=' * 55)
    app.run(host='0.0.0.0', port=PORT, debug=False)
