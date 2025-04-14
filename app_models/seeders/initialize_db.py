import logging

from app_models.models import ServiceCategory, User
from backend.settings import (
    SUPER_USER_EMAIL,
    SUPER_FIRST_NAME,
    SUPER_LAST_NAME,
    SUPER_USER_PASSWORD,
    SUPER_USER_PHONE,
)

# Create super admin user
logging.info("Creating super admin user...")
try:
    super_admin = User.objects.create_superuser(
        username=SUPER_USER_EMAIL,
        email=SUPER_USER_EMAIL,
        phone=SUPER_USER_PHONE,
        password=SUPER_USER_PASSWORD,
        first_name=SUPER_FIRST_NAME,
        last_name=SUPER_LAST_NAME,
        is_active=True,
        is_verified=True,
    )

except Exception as e:
    logging.warning(f"Super admin user already exists: {e}")

# Create categories
logging.info("Creating service proposal categories...")
categories = [
    {
        "fr_name": "Technologie & Informatique",
        "fr_description": "Développement de logiciels, Cybersécurité, Science des données & Analyse, Support informatique & Administration système, Informatique en nuage, Conception UX/UI, Intelligence artificielle & Apprentissage automatique, Développement de blockchain, Développement de jeux",
        "en_name": "Technology & IT",
        "en_description": "Software Development, Cybersecurity, Data Science & Analytics, IT Support & System Administration, Cloud Computing, UX/UI Design, Artificial Intelligence & Machine Learning, Blockchain Development, Game Development",
    },
    {
        "fr_name": "Ingénierie & Architecture",
        "fr_description": "Ingénierie mécanique, Ingénierie civile, Ingénierie électrique, Ingénierie aérospatiale, Ingénierie structurelle, Design industriel, Architecture",
        "en_name": "Engineering & Architecture",
        "en_description": "Mechanical Engineering, Civil Engineering, Electrical Engineering, Aerospace Engineering, Structural Engineering, Industrial Design, Architecture",
    },
    {
        "fr_name": "Affaires & Finance",
        "fr_description": "Comptabilité & Audit, Analyse financière & Investissement, Banque, Développement commercial, Consulting en management, Ressources humaines (RH), Gestion de projet",
        "en_name": "Business & Finance",
        "en_description": "Accounting & Auditing, Financial Analysis & Investment, Banking, Business Development, Management Consulting, Human Resources (HR), Project Management",
    },
    {
        "fr_name": "Ventes & Marketing",
        "fr_description": "Marketing digital, SEO & SEM, Gestion des réseaux sociaux, Ventes & Développement commercial, Gestion de marque, Relations publiques (RP), Publicité",
        "en_name": "Sales & Marketing",
        "en_description": "Digital Marketing, SEO & SEM, Social Media Management, Sales & Business Development, Brand Management, Public Relations (PR), Advertising",
    },
    {
        "fr_name": "Santé & Médical",
        "fr_description": "Soins infirmiers, Pharmacie, Recherche médicale, Physiothérapie, Santé mentale & Conseil, Dentisterie",
        "en_name": "Healthcare & Medical",
        "en_description": "Nursing, Pharmacy, Medical Research, Physical Therapy, Mental Health & Counseling, Dentistry",
    },
    {
        "fr_name": "Éducation & Formation",
        "fr_description": "Enseignement (K-12, Enseignement supérieur), Formation en entreprise, Tutorat, Développement de programmes, Technologie éducative",
        "en_name": "Education & Training",
        "en_description": "Teaching (K-12, Higher Education), Corporate Training, Tutoring, Curriculum Development, Educational Technology",
    },
    {
        "fr_name": "Créatif & Design",
        "fr_description": "Design graphique, Production & Montage vidéo, Photographie, Rédaction & Écriture de contenu, Design de mode, Design d'intérieur",
        "en_name": "Creative & Design",
        "en_description": "Graphic Design, Video Production & Editing, Photography, Copywriting & Content Writing, Fashion Design, Interior Design",
    },
    {
        "fr_name": "Juridique",
        "fr_description": "Droit des affaires, Droit pénal, Droit de la propriété intellectuelle, Droit de la famille, Services de parajuristes",
        "en_name": "Legal",
        "en_description": "Corporate Law, Criminal Law, Intellectual Property Law, Family Law, Paralegal Services",
    },
    {
        "fr_name": "Fabrication & Logistique",
        "fr_description": "Gestion de la chaîne d'approvisionnement, Opérations d'entrepôt, Logistique & Transport, Contrôle de qualité, Approvisionnement",
        "en_name": "Manufacturing & Logistics",
        "en_description": "Supply Chain Management, Warehouse Operations, Logistics & Transportation, Quality Control, Procurement",
    },
    {
        "fr_name": "Hôtellerie & Tourisme",
        "fr_description": "Gestion hôtelière, Voyage & Tourisme, Restauration & Service alimentaire, Planification d'événements",
        "en_name": "Hospitality & Tourism",
        "en_description": "Hotel Management, Travel & Tourism, Restaurant & Food Service, Event Planning",
    },
    {
        "fr_name": "Service client & Support",
        "fr_description": "Support de centre d'appels, Support technique, Relations clients, Service d'assistance",
        "en_name": "Customer Service & Support",
        "en_description": "Call Center Support, Technical Support, Client Relations, Help Desk",
    },
    {
        "fr_name": "Science & Recherche",
        "fr_description": "Biotechnologie & Pharmaceutique, Science de l'environnement, Recherche en science des données, Astronomie",
        "en_name": "Science & Research",
        "en_description": "Biotech & Pharmaceuticals, Environmental Science, Data Science Research, Astronomy",
    },
    {
        "fr_name": "Médias & Communication",
        "fr_description": "Journalisme, Diffusion, Podcasting, Traduction & Interprétation",
        "en_name": "Media & Communication",
        "en_description": "Journalism, Broadcasting, Podcasting, Translation & Interpretation",
    },
    {
        "fr_name": "Construction & Métiers qualifiés",
        "fr_description": "Plomberie, Travail électrique, Charpenterie, Soudure",
        "en_name": "Construction & Skilled Trades",
        "en_description": "Plumbing, Electrical Work, Carpentry, Welding",
    },
    {
        "fr_name": "Gouvernement & Services publics",
        "fr_description": "Application de la loi, Militaire & Défense, Politique publique, Urbanisme",
        "en_name": "Government & Public Services",
        "en_description": "Law Enforcement, Military & Defense, Public Policy, Urban Planning",
    },
]

for category in categories:
    ServiceCategory.objects.get_or_create(
        fr_name=category["fr_name"],
        fr_description=category["fr_description"],
        en_name=category["en_name"],
        en_description=category["en_description"],
    )
