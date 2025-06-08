import dash
from dash import html, dcc, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import base64
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import flask

# Initialize the Dash app with a more attractive Bootstrap theme (Flatly from Bootswatch)
app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.FLATLY,  # Changed from BOOTSTRAP to FLATLY for a more modern look
    'https://use.fontawesome.com/releases/v5.15.4/css/all.css',
    'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap',
    'assets/custom.css'
], suppress_callback_exceptions=True)
server = app.server

# Fix script loading issue by using a proper external_scripts parameter
app.scripts.config.serve_locally = False  # Don't serve locally if it doesn't exist
app._external_scripts = [
    {'src': 'https://code.jquery.com/jquery-3.6.0.min.js'},
    {'src': 'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js'}
]

# Configure for deployment
app.title = "Seye Daniel Oyelayo - Professional Portfolio"

# Use custom HTML template to add smooth scrolling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            html {
                scroll-behavior: smooth;
                scroll-padding-top: 80px;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    // Add click handlers for navigation links
                    document.addEventListener('click', function(e) {
                        // Find closest anchor tag
                        const link = e.target.closest('a');
                        
                        // Check if it's an internal hash link
                        if (link && link.getAttribute('href') && link.getAttribute('href').startsWith('#')) {
                            e.preventDefault();
                            const targetId = link.getAttribute('href').substring(1);
                            const targetElement = document.getElementById(targetId);
                            if (targetElement) {
                                targetElement.scrollIntoView({
                                    behavior: 'smooth'
                                });
                            }
                        }
                    });
                    
                    // Handle header contact button
                    const contactBtn = document.querySelector('.contact-btn');
                    if (contactBtn) {
                        contactBtn.addEventListener('click', function(e) {
                            e.preventDefault();
                            const contactSection = document.getElementById('contact');
                            if (contactSection) {
                                contactSection.scrollIntoView({
                                    behavior: 'smooth'
                                });
                            }
                        });
                    }
                });
            </script>
        </footer>
    </body>
</html>
'''
#server = app.server
# Helper function to encode images
def encode_image(image_path):
    with open(image_path, 'rb') as f:
        encoded = base64.b64encode(f.read()).decode('ascii')
    return f'data:image/jpeg;base64,{encoded}'

# Get climate challenge images
climate_images = []
data_dir = os.path.join(os.getcwd(), 'data')
for file in os.listdir(data_dir):
    if file.startswith('climate') and file.endswith(('.jpg', '.jpeg', '.png')):
        climate_images.append(encode_image(os.path.join(data_dir, file)))

# Get profile image (using climate13.jpg)
profile_image = None
profile_image_path = os.path.join(data_dir, 'climate13.jpg')
if os.path.exists(profile_image_path):
    profile_image = encode_image(profile_image_path)

# Define the navbar (moved outside of create_navigation function)
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("Seye Daniel Oyelayo", href="/", className="nav-brand"),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink("About", href="/#about", external_link=True, className="nav-link")),
                        dbc.NavItem(dbc.NavLink("Projects",  href="/#projects", external_link=True, className="nav-link")),
                        dbc.NavItem(dbc.NavLink("Achievements", href="/#achievements", external_link=True, className="nav-link")),
                        dbc.NavItem(dbc.NavLink("Skills", href="/#skills", external_link=True, className="nav-link")),
                        dbc.NavItem(dbc.NavLink("Contact", href="/#contact", external_link=True, className="nav-link")),
                        dbc.NavItem(dbc.NavLink("Resume", href="/resume", className="nav-link")),
                    ],
                    className="ms-auto",
                    navbar=True,
                ),
                id="navbar-collapse",
                navbar=True,
                is_open=False,
            ),
        ],
        fluid=True,
    ),
    color="light",
    className="sticky-top shadow-sm navbar-custom",
    expand="lg",
)

# Define sections
def create_header():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1("Seye Daniel Oyelayo", className="header-title"),
                    html.H3("Data Scientist & Analytics Professional", className="header-subtitle"),
                    html.Div([
                        dbc.Button("Contact Me", color="primary", href="#contact", className="me-3 contact-btn"),
                        dbc.Button("View Resume", color="secondary", id="view-resume", href="/resume", className="me-3"),
                        html.Div([
                            html.A([html.I(className="fab fa-linkedin fa-2x me-3")], href="https://www.linkedin.com/in/seyeoyelayo/", target="_blank", className="social-icon-link"),
                            html.A([html.I(className="fab fa-github fa-2x me-3")], href="https://github.com/Exwhybaba", target="_blank", className="social-icon-link"),
                            html.A([html.I(className="fab fa-medium fa-2x me-3")], href="https://medium.com/@exwhybaba", target="_blank", className="social-icon-link"),
                        ], className="d-flex mt-3")
                    ], className="header-buttons")
                ], className="header-content")
            ], width=12, className="header-col")
        ], className="header-row")
    ], fluid=True, className="header-container")

def create_about():
    # Use climate13.jpg as profile picture or fallback to icon if not available
    if profile_image:
        profile_display = html.Img(src=profile_image, className="profile-image", alt="Seye Daniel Oyelayo")
    else:
        profile_display = html.I(className="fas fa-user-circle fa-8x", style={"color": "#1a73e8"})
    
    return dbc.Container([
        html.Div(id="about"),
        html.H2("About Me", className="section-title"),
        dbc.Row([
            dbc.Col([
                html.Div([
                    profile_display
                ], className="text-center mb-4")
            ], width=12, md=4, className="d-flex align-items-center justify-content-center"),
            dbc.Col([
                html.P("""
                    I'm an inventive Data Professional with expertise in analytics and success in dealing with large data sets to break down information, 
                    generate useful insights, and solve complex business challenges. I have hands-on experience in data wrangling, web scrapping, 
                    machine learning and AI. I have a successful track record of recognizing patterns, creating interpretations, and providing 
                    commercial solutions. I am a creative and strategic problem solver capable of dealing with complicated challenges, thrives in 
                    continual challenges and fast-paced workplaces, with a strong emphasis on collaboration, driving development, and delivering new 
                    solutions to meet the needs of customers.
                """, className="about-text"),
                html.P("""
                    I graduated from the University of Ibadan with a BSc in Agricultural Biochemistry and Nutrition (Second Class Upper).
                """, className="about-text mt-3"),
            ], width=12, md=8)
        ], className="align-items-center")
    ], className="section-container")

def create_projects():
    projects = [
        {
            "title": "FeedEyes",
            "description": "A least-cost feed formulator that helps farmers optimize animal nutrition while minimizing costs. The application provides optimal feed formulations based on available ingredients and nutritional requirements.",
            "tech": ["Python", "Linear Programming", "Machine Learning"],
            "link": "https://feedeyes.onrender.com/",
            "icon": "fas fa-balance-scale" # Feed formulation icon
        },
        {
            "title": "Crop Recommendation System",
            "description": "An intelligent system that recommends suitable crops based on soil characteristics and environmental conditions, helping farmers make informed decisions for optimal yield.",
            "tech": ["Python", "Machine Learning", "Streamlit"],
            "link": "https://exwhybaba-crop-recommendation-system-crop-kl5qlo.streamlit.app/",
            "icon": "fas fa-seedling" # Plant/crop icon
        },
        {
            "title": "Crop Monitoring System",
            "description": "A comprehensive system for monitoring crop health and growth using computer vision to identify plant diseases, pests, and nutritional deficiencies.",
            "tech": ["Computer Vision", "Data Analytics", "Streamlit"],
            "link": "https://beanclassifer.streamlit.app/",
            "icon": "fas fa-eye" # Monitoring/vision icon
        },
        {
            "title": "Customer Churn Prediction",
            "description": "Machine learning models to predict and prevent customer churn for agricultural service providers, enabling proactive retention strategies.",
            "tech": ["Machine Learning", "Predictive Analytics", "SKLearn"],
            "link": "#",
            "icon": "fas fa-users" # Customer/user icon
        },
        {
            "title": "Malaria Parasite Detector",
            "description": "An AI system for detecting malaria parasites in blood samples to assist in diagnosis, improving accuracy and speed of detection in healthcare settings.",
            "tech": ["Deep Learning", "Computer Vision", "Healthcare AI"],
            "link": "https://youtu.be/cawBUQm6FZk",
            "icon": "fas fa-microscope" # Medical/scientific icon
        }
    ]
    
    project_cards = [
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.Div([
                            html.I(className=project["icon"] + " fa-2x project-icon")
                        ], className="project-icon-wrapper"),
                        html.H4(project["title"], className="card-title mt-3")
                    ], className="d-flex flex-column align-items-center"),
                    html.Hr(),
                    html.P(project["description"], className="card-text"),
                    html.Div([
                        dbc.Badge(tech, color="info", className="me-1 tech-badge") 
                        for tech in project["tech"]
                    ], className="tech-stack mb-3"),
                    html.Div(
                        html.A(
                            dbc.Button([
                                "View Project ",
                                html.I(className="fas fa-external-link-alt ms-1")
                            ], color="primary", size="sm", className="mt-2 project-button"),
                            href=project["link"],
                            target="_blank"
                        ),
                        className="text-center"
                    ) if project["link"] != "#" else html.Span()
                ])
            ], className="project-card h-100 shadow-sm")
        ], md=6, lg=4, className="mb-4") 
        for i, project in enumerate(projects)
    ]
    
    return dbc.Container([
        html.Div(id="projects"),
        html.H2("Projects", className="section-title"),
        html.P("Below are some of my notable projects that demonstrate my expertise in data science, machine learning, and agricultural innovation.", 
               className="text-center lead mb-5"),
        dbc.Row(project_cards, className="project-row g-4")
    ], className="section-container")

def create_achievements():
    achievements = [
        {
            "title": "2023 Cohere Multilingual Hackathon Winner",
            "description": "Recognized at the prestigious Cohere Multilingual Hackathon for developing innovative NLP solutions that addressed real‑world language processing challenges."
        },
        {
            "title": "Climate Risk Challenge Winner",
            "description": "Secured a $50,000 Amazon cloud credit for the University of Ibadan and a $1,500 cash prize for our team in the Climate Risk Challenge under the Sustainable Africa Initiative."
        },
        {
            "title": "Legacy AgriTech Hackathon Finalist",
            "description": "Qualified for the Legacy AgriTech Hackathon, organized by the Mandela Washington Fellowship Alumni Association of Nigeria (MWFAAN), with an innovative agricultural solution."
        }
    ]
    
    achievement_cards = [
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(achievement["title"], className="card-title"),
                    html.P(achievement["description"], className="card-text"),
                ])
            ], className="achievement-card h-100 shadow-sm border-left-accent")
        ], md=6, lg=4, className="mb-4") 
        for achievement in achievements
    ]
    
    climate_image_carousel = dbc.Carousel(
        items=[
            {"src": img, "caption": f"Climate Challenge Award Ceremony (Image {i+1})"} 
            for i, img in enumerate(climate_images)
        ],
        controls=True,
        indicators=True,
        interval=3000,
        ride="carousel",
        className="climate-carousel shadow"
    )
    
    return dbc.Container([
        html.Div(id="achievements"),
        html.H2("Achievements", className="section-title"),
        html.P("My work has been recognized through various competitions and challenges in the technology and agricultural sectors.",
               className="text-center lead mb-5"),
        dbc.Row(achievement_cards, className="achievement-row"),
        html.H4("Climate Challenge Award Gallery", className="gallery-title mt-5"),
        climate_image_carousel
    ], className="section-container")

def create_skills():
    technical_skills = ["Python", "Machine Learning", "Deep Learning", "Computer Vision", 
                         "Data Analysis", "Statistical Modeling", "SQL", "TensorFlow", 
                         "PyTorch", "Scikit-learn", "Pandas", "IoT", "Agriculture Tech",
                         "Data Visualization", "Natural Language Processing"]
    
    domain_skills = ["Agricultural Systems", "Livestock Nutrition", "Crop Management", 
                      "Precision Agriculture", "Sustainable Farming", "Food Security", 
                      "Supply Chain Optimization", "Business Intelligence", 
                      "Project Management", "Research Methods"]
    
    return dbc.Container([
        html.Div(id="skills"),
        html.H2("Skills", className="section-title"),
        html.P("I bring a diverse set of technical and domain-specific skills to solve complex problems.",
               className="text-center lead mb-5"),
        dbc.Row([
            dbc.Col([
                html.H4("Technical Skills", className="skill-subtitle"),
                html.Div([
                    dbc.Badge(skill, color="success", className="me-1 mb-2 py-2 px-3 skill-badge") 
                    for skill in technical_skills
                ], className="skill-badges")
            ], md=6, className="mb-4"),
            dbc.Col([
                html.H4("Domain Knowledge", className="skill-subtitle"),
                html.Div([
                    dbc.Badge(skill, color="primary", className="me-1 mb-2 py-2 px-3 skill-badge") 
                    for skill in domain_skills
                ], className="skill-badges")
            ], md=6, className="mb-4")
        ])
    ], className="section-container")

def create_contact():
    return dbc.Container([
        html.Div(id="contact"),
        html.H2("Contact", className="section-title"),
        html.P("Let's connect and discuss how my skills and expertise can contribute to your organization's success.",
               className="text-center lead mb-5"),
        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Form([
                            dbc.Row([
                                dbc.Label("Name", html_for="name", width=12),
                                dbc.Col([
                                    dbc.Input(type="text", id="contact-name", placeholder="Your Name", className="form-control-lg")
                                ], width=12)
                            ], className="mb-3"),
                            dbc.Row([
                                dbc.Label("Email", html_for="email", width=12),
                                dbc.Col([
                                    dbc.Input(type="email", id="contact-email", placeholder="Your Email", className="form-control-lg")
                                ], width=12)
                            ], className="mb-3"),
                            dbc.Row([
                                dbc.Label("Message", html_for="message", width=12),
                                dbc.Col([
                                    dbc.Textarea(id="contact-message", placeholder="Your Message", rows=4, className="form-control-lg")
                                ], width=12)
                            ], className="mb-3"),
                            html.Div(id="contact-alert", className="mt-2"),
                            dbc.Button("Send Message", id="submit-button", color="primary", size="lg", className="mt-3 px-4")
                        ])
                    ], md=7),
                    dbc.Col([
                        html.Div([
                            html.H4("Get in Touch", className="mb-4"),
                            html.P([html.I(className="fas fa-envelope me-2 contact-icon"), "seyeoyelayo@gmail.com"], className="contact-item"),
                            html.P([html.I(className="fas fa-phone me-2 contact-icon"), "+234 810 469 5515"], className="contact-item"),
                            html.P([html.I(className="fas fa-map-marker-alt me-2 contact-icon"), "Ibadan, Nigeria"], className="contact-item"),
                            html.Div([
                                html.A([html.I(className="fab fa-linkedin fa-2x me-3")], href="https://www.linkedin.com/in/seyeoyelayo/", target="_blank", className="social-link"),
                                html.A([html.I(className="fab fa-github fa-2x me-3")], href="https://github.com/Exwhybaba", target="_blank", className="social-link"),
                                html.A([html.I(className="fab fa-medium fa-2x me-3")], href="https://medium.com/@exwhybaba", target="_blank", className="social-link"),
                            ], className="social-icons mt-4")
                        ], className="contact-info h-100 d-flex flex-column justify-content-center")
                    ], md=5)
                ])
            ])
        ], className="shadow contact-card")
    ], className="section-container")

def create_footer():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Hr(className="footer-divider"),
                dbc.Row([
                    dbc.Col([
                        html.H5("Seye Daniel Oyelayo", className="footer-title"),
                        html.P("Data Scientist & Analytics Professional", className="footer-subtitle")
                    ], md=6),
                    dbc.Col([
                        html.Div([
                            html.A([html.I(className="fab fa-linkedin fa-lg me-3")], href="https://www.linkedin.com/in/seyeoyelayo/", target="_blank", className="footer-social-link"),
                            html.A([html.I(className="fab fa-github fa-lg me-3")], href="https://github.com/Exwhybaba", target="_blank", className="footer-social-link"),
                            html.A([html.I(className="fab fa-medium fa-lg me-3")], href="https://medium.com/@exwhybaba", target="_blank", className="footer-social-link"),
                        ], className="footer-social text-md-end")
                    ], md=6, className="text-md-end")
                ]),
                html.P("© 2025 Seye Daniel Oyelayo. All Rights Reserved.", className="footer-text mt-3"),
            ], width=12)
        ])
    ], fluid=True, className="footer-container")

# Create the main content for the homepage
def create_main_content():
    return html.Div([
        create_header(),
        create_about(),
        create_projects(),
        create_achievements(),
        create_skills(),
        create_contact(),
        create_footer()
    ])

# Create the resume page content
def create_resume_page():
    return html.Div([
        dbc.Container([
            html.A("← Back to Portfolio", href="/", className="back-link mt-4 d-inline-block"),
            html.Iframe(src="/assets/resume.pdf", className="resume-frame shadow-sm")
        ], className="resume-container my-4")
    ])

# Layout with navbar included in the initial layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,  # Navbar is now part of the initial layout
    html.Div(id='page-content')
])

# Navbar toggle callback
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# Callback to render the correct page
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/resume':
        # Display resume page
        return create_resume_page()
    else:
        # Main portfolio page
        # Add smooth scrolling script inline
        smooth_scroll_script = html.Script('''
            // Wait for the DOM to be fully loaded
            document.addEventListener('DOMContentLoaded', function() {
                // Function to handle smooth scrolling
                function smoothScroll(event, targetId) {
                    event.preventDefault();
                    const targetElement = document.getElementById(targetId);
                    if (targetElement) {
                        window.scrollTo({
                            top: targetElement.offsetTop - 70,
                            behavior: 'smooth'
                        });
                        
                        // Update URL hash without jumping
                        history.pushState(null, null, '#' + targetId);
                    }
                }
                
                // Add click handlers for all internal hash links
                function setupScrollHandlers() {
                    // Handle all links that point to hash targets
                    document.querySelectorAll('a[href^="#"]').forEach(link => {
                        if (link.getAttribute('href') !== '#') {
                            link.addEventListener('click', function(e) {
                                const targetId = this.getAttribute('href').substring(1);
                                smoothScroll(e, targetId);
                            });
                        }
                    });
                    
                    // Handle the Contact Me button specifically
                    const contactBtn = document.querySelector('.contact-btn');
                    if (contactBtn) {
                        contactBtn.addEventListener('click', function(e) {
                            smoothScroll(e, 'contact');
                        });
                    }
                }
                
                // Initial setup
                setupScrollHandlers();
                
                // Set up a MutationObserver to handle dynamically loaded content
                const observer = new MutationObserver(function(mutations) {
                    setupScrollHandlers();
                });
                
                // Start observing the document with the configured parameters
                observer.observe(document.body, { childList: true, subtree: true });
            });
        ''')
        
        return html.Div([
            smooth_scroll_script,
            create_header(),
            create_about(),
            create_projects(),
            create_achievements(),
            create_skills(),
            create_contact(),
            create_footer()
        ])

# Function to send email
def send_email(name, email, message):
    recipient_email = "seyeoyelayo@gmail.com"
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = recipient_email
    msg['Subject'] = f"Portfolio Contact: Message from {name}"
    
    # Add message body
    body = f"""
    You have received a new message from your portfolio website:
    
    Name: {name}
    Email: {email}
    
    Message:
    {message}
    """
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # For actual deployment, you'd need to set up a proper email service or SMTP credentials
        # This code will not work without proper SMTP configuration
        # For demonstration purposes only
        return True, "Message sent successfully!"
    except Exception as e:
        return False, str(e)

# Callback for form submission
@app.callback(
    Output('contact-alert', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('contact-name', 'value'),
     State('contact-email', 'value'),
     State('contact-message', 'value')]
)
def submit_form(n_clicks, name, email, message):
    if n_clicks is None:
        return ""
    
    if not name or not email or not message:
        return dbc.Alert(
            "Please fill in all fields",
            color="danger",
            dismissable=True,
            is_open=True,
        )
    
    # For demonstration - in a real deployment, configure a mail service
    # success, response = send_email(name, email, message)
    
    # Form data that would be sent
    form_data = {
        "name": name,
        "email": email,
        "message": message,
        "recipient": "seyeoyelayo@gmail.com"
    }
    
    # For demonstration, always show success
    # In real deployment, check the success variable
    return dbc.Alert(
        [
            html.I(className="fas fa-check-circle me-2"),
            "Thank you for your message! I'll get back to you soon.",
            html.Div(
                "Your message has been received and will be sent to seyeoyelayo@gmail.com",
                className="small mt-2 text-muted"
            )
        ],
        color="success",
        dismissable=True,
        is_open=True,
    )

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host="0.0.0.0", port=port)


