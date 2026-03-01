# app.py - Main Flask Application
from flask import Flask, render_template, request, jsonify, flash, redirect, send_file, url_for
from datetime import datetime
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a random secret key

# Configuration
# UPLOAD_FOLDER = 'static/uploads'

UPLOAD_FOLDER = '/tmp/uploads'  # for Vercel /tmp use and try .

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists - FIX FOR VERCEL
try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
except OSError:
    pass  # Vercel serverless doesn't allow folder creation
# Portfolio data
portfolio_data = {
    'personal_info': {
        'name': 'Ahsan Tahir',
        'title': 'Python Developer | ML/AI Engineer',
        'email': 'ashantahirit@gmail.com',
        'phone': '+92 316 487 0898',
        'linkedin': 'https://linkedin.com/in/ahsan-tahir-880b5324a',
        'github': 'https://github.com/Ahsan-Tahir-Programming',
        'location': 'Lahore, Punjab, Pakistan',
        'about': 'AI Engineer specializing in Computer Vision and MLOps. Proven track record of deploying YOLO models to production using FastAPI and Docker. Experienced in building complex compliance logic for the Retail Tech industry. Passionate about building intelligent automation systems that solve real-world problems.'
    },
    'skills': {
        'Languages': ['Python', 'Java', 'JavaScript', 'C++'],
        'ML & Computer Vision': ['PyTorch', 'YOLO', 'TensorFlow Lite', 'OpenCV', 'NLP', 'Scikit-learn', 'Pandas', 'Geopy'],
        'Frontend': ['HTML5', 'CSS3', 'Gradio'],
        'Backend & Web': ['FastAPI', 'Flask'],
        'Databases': ['MySQL', 'SQLite', 'Firebase'],
        'Cloud & DevOps': ['AWS', 'Docker', 'Git', 'Wasabi', 'S3-compatible Storage'],
        'Desktop': ['PyQt']
    },
    'experience': [
        {
            'title': 'Python/AI Engineer',
            'company': 'Concave Tech',
            'duration': 'May 2024 – Present',
            'description': 'Leading development of AI-powered solutions for Retail Tech. Key achievements: engineered a computer vision pipeline using YOLO & Geometric Algorithms for shelf compliance automation; built and deployed production-grade FastAPI backend for real-time object detection with Docker containerization; developed a full-stack AI-powered clustering and route optimization system with constrained K-means, MySQL, and Numba JIT. Streamlined large-scale dataset management using AWS CLI with S3-compatible storage (Wasabi).',
            'technologies': ['Python', 'YOLO', 'FastAPI', 'Docker', 'Computer Vision', 'MLOps', 'MySQL', 'AWS', 'Gradio', 'Geopy'],
        },
    ],
    'projects': [
        {
            'title': 'Real-Time Object Detection Web App',
            # previous 
            # 'description': 'Built a YOLO-based object detection web application with real-time detection capabilities. Features JSON API responses and is fully deployed and live for production use.',
            'description': 'Built a YOLO-based object detection web application deployed using Docker containerization. Implemented CI/CD pipeline with Docker image builds, push to registry, and automated deployment. Features FastAPI endpoints with real-time detection and JSON responses, currently running in production.',
            'technologies': ['YOLO', 'FastAPI', 'SQLite', 'Docker'],
            # 'icon': 'fas fa-search', Generic search icon
            # 'icon': 'fas fa-video',  # Video/camera better for object detection
            'icon': 'fas fa-camera',
            'status': 'Live',
        },
        # {
        #     'title': 'Sentiment Analysis for Recipe Rating',
        #     'description': 'Developed a sentiment analysis model for interpreting user feedback in a recipe rating application. Successfully integrated with Flutter mobile app for enhanced user experience.',
        #     # 'technologies': ['Python', 'Machine Learning', 'Roberta', 'Flutter Integration'],
        #     'technologies': ['Roberta', 'NLP', 'Flutter Integration'],
        #     # 'icon': 'fas fa-heart', # Generic heart                    # Better: 'fas fa-brain' or 'fas fa-chart-line'
        #     'icon': 'fas fa-smile',  # Sentiment analysis icon
        #     # 'icon': 'fas fa-brain', # Brain icon for ML/AI
        #     # 'icon': 'fas fa-chart-line',
        #     'status': 'Completed'
        # },
        # {
        #     'title': 'Desktop Task Management App',
        #     'description': 'Built a comprehensive desktop application featuring Add, Edit, Delete, Undo, Search, Sort operations with Dark/Light mode support. Implements local JSON persistence for data storage.',
        #     'technologies': ['PyQt5', 'JSON', 'Desktop GUI'],
        #     # 'icon': 'fas fa-tasks',  # Task management icon
        #     'icon': 'fas fa-desktop',  # # Desktop icon better than tasks
        #     'status': 'Completed'
        # },
        {
            'title': 'Retail Planogram Compliance System',
            'description': 'Engineered a computer vision pipeline using YOLO & Geometric Algorithms to automate shelf compliance checks (Horizontal/Vertical matching). Improved complex logic for Brand Blocking detection and Eye-Level (Golden Zone) analysis, directly impacting retail audit efficiency. Architected an interactive audit dashboard using Gradio for visualizing gaps and misplacements.',
            'technologies': ['YOLO', 'Gradio', 'Computer Vision', 'OpenCV'],
            'icon': 'fas fa-store',
            'status': 'Completed'
        },
        {
            'title': 'AI-Powered Clustering & Route Optimization System',
            'description': 'Full-stack web application that intelligently clusters geographic locations and optimizes daily shop visit schedules. Uses constrained K-means clustering to group shops by location (respecting visit limits and distance constraints), distributes visits across days with workload balancing, and optimizes travel routes using heap-based path finding. Includes user authentication with MySQL, Excel import/export for bulk data, interactive dashboard with real-time visualization, REST API with CORS, and Numba JIT for performance-optimized processing.',
            'technologies': ['K-means Clustering', 'MySQL', 'Numba JIT', 'Geopy'],
            'icon': 'fas fa-route',
            'status': 'Completed'
        }
    ],
    'education': {
        # 'degree': 'Bachelor of Science in Information Technology',
        # 'university': 'University of the Punjab',
        # 'duration': '2019 – 2023'
    },
    #  add this by geting acutal certificates like ml , ai , dl from linked in learning , coursera
    # 'certifications': [
    #     'AWS Machine Learning (2023)',
    #     'AWS Web Development (2023)',
    #     'AWS C++ and Data Structures and Algorithms (2023)'
    # ]
}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/favicon.ico')
def favicon():
    return '', 204  # No content response

@app.route('/')
def index():
    """Main portfolio page"""
    return render_template('index.html', data=portfolio_data)


@app.route('/api/contact', methods=['POST'])
def contact():
    """Handle contact form submissions"""
    try:
        data = request.get_json()

        # Basic validation
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'{field.title()} is required'}), 400

        # # Save contact data (in a real app, you might send email or save to database)
        # contact_data = {
        #     'timestamp': datetime.now().isoformat(),
        #     'name': data['name'],
        #     'email': data['email'],
        #     'subject': data['subject'],
        #     'message': data['message']
        # }

        # Save to JSON file (in production, use proper database)
        # contacts_file = 'contacts.json'
        # contacts = []
        # if os.path.exists(contacts_file):
        #     with open(contacts_file, 'r') as f:
        #         contacts = json.load(f)

        # contacts.append(contact_data)

        # this is also fail not good for vercel  
        # Store in memory instead of file
        # contacts_storage.append(contact_data)

        # Optional: Print to logs so you can see messages
        # print(f"New contact from: {data['name']} ({data['email']})")
        # print(f"Subject: {data['subject']}")
        # print(f"Message: {data['message']}")
        

        # with open(contacts_file, 'w') as f:
        #     json.dump(contacts, f, indent=2)

        return jsonify({
            'success': True,
            'message': 'Thank you for your message! I will get back to you soon.'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': 'Something went wrong'}), 500

@app.route('/resume')
def resume():
    resume_path = os.path.join(app.static_folder, 'uploads', 'resume.pdf')
    if not os.path.exists(resume_path):
        resume_path = os.path.join(app.static_folder, 'resume.pdf')
    return send_file(resume_path, as_attachment=False, download_name='Ahsan_Tahir_Resume.pdf')

@app.route('/api/portfolio')
def api_portfolio():
    """API endpoint to get portfolio data as JSON"""
    return jsonify(portfolio_data)


@app.route('/api/skills')
def api_skills():
    """API endpoint to get skills data"""
    return jsonify(portfolio_data['skills'])


@app.route('/api/projects')
def api_projects():
    """API endpoint to get projects data"""
    return jsonify(portfolio_data['projects'])


@app.route('/admin')
def admin():
    """Simple admin panel to view contacts"""
    # this is also fail not good for vercel
    # Use in-memory storage instead of file
    # return render_template('admin.html', contacts=contacts_storage)

    # if not os.path.exists('contacts.json'):
    #     contacts = []
    # else:
    #     with open('contacts.json', 'r') as f:
    #         contacts = json.load(f)

    # return render_template('admin.html', contacts=contacts)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """File upload endpoint for project files or resume"""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File uploaded successfully!')
            return redirect(url_for('upload_file'))
        else:
            flash('Invalid file type')

    return render_template('upload.html')


# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


# Template filters
@app.template_filter('datetime')
def datetime_filter(timestamp):
    """Format datetime string"""
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime('%B %d, %Y at %I:%M %p')
    except:
        return timestamp


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)