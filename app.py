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
        'about': 'Python Developer at Concave Tech with expertise in machine learning and deep learning solutions. Specialized in YOLO object detection, web APIs, and desktop applications. Passionate about building intelligent automation systems that solve real-world problems.'
    },
    'skills': {
        'Programming': ['Python', 'Java', 'Javascript', 'HTML', 'XML', 'CSS'],
        'Machine Learning': ['PyTorch', 'TensorFlow Lite', 'NumPy', 'Pandas', 'Matplotlib', 'Natural Language Processing (NLP)', 'Scikit-Learn'],
        # 'Computer Vision': ['YOLO' 'Ultralytics'],
        'Web Development': ['Flask', 'FastAPI'],
        'Desktop Development': ['PyQt5'],
        'Tools & Technologies': ['Docker', 'SQLite', 'Colab', 'Wasabi']
    },
    'experience': [
        {
            'title': 'Python Developer',
            'company': 'Concave Tech',
            'duration': 'May 2024 – Present',
            # previous
            # 'description': 'Gained hands-on experience developing Python applications with focus on machine learning and deep learning solutions. Working with cutting-edge technologies including YOLO object detection, web APIs, and desktop applications.',
            # 'description': 'Developing production-ready Python applications using YOLO for object detection, building REST APIs with FastAPI, and creating desktop applications with PyQt5. Working with Docker containerization and database integration.',
            'description': 'Developing production-ready Python applications using machine learning and deep learning. Key responsibilities include: building YOLO-based object detection systems, creating REST APIs with FastAPI, implementing Docker containerization for deployments, and developing desktop applications with PyQt5. Working with modern DevOps practices including Docker image management and container orchestration.',
            'technologies': ['Python', 'Machine Learning', 'Deep Learning', 'YOLO', 'FastAPI', 'Docker', 'PyQt5'],
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
        {
            'title': 'Sentiment Analysis for Recipe Rating',
            'description': 'Developed a sentiment analysis model for interpreting user feedback in a recipe rating application. Successfully integrated with Flutter mobile app for enhanced user experience.',
            # 'technologies': ['Python', 'Machine Learning', 'Roberta', 'Flutter Integration'],
            'technologies': ['Roberta', 'NLP', 'Flutter Integration'],
            # 'icon': 'fas fa-heart', # Generic heart                    # Better: 'fas fa-brain' or 'fas fa-chart-line'
            'icon': 'fas fa-smile',  # Sentiment analysis icon
            # 'icon': 'fas fa-brain', # Brain icon for ML/AI
            # 'icon': 'fas fa-chart-line',
            'status': 'Completed'
        },
        {
            'title': 'Desktop Task Management App',
            'description': 'Built a comprehensive desktop application featuring Add, Edit, Delete, Undo, Search, Sort operations with Dark/Light mode support. Implements local JSON persistence for data storage.',
            'technologies': ['PyQt5', 'JSON', 'Desktop GUI'],
            # 'icon': 'fas fa-tasks',  # Task management icon
            'icon': 'fas fa-desktop',  # # Desktop icon better than tasks
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
    # Resume file serve karo
    return send_file('static/resume.pdf')

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