from datetime import datetime

def generate_markdown(name, email, phone, profile, skills, education, projects, training):
    # Generate the markdown content
    markdown_content = f"# {name}\n\n"
    markdown_content += f"**Email**: {email}\n\n"
    markdown_content += f"**Phone**: {phone}\n\n"
    markdown_content += "\n---\n\n"

    if profile:
        markdown_content += f"### Profile Summary\n\n{profile}\n\n"
    
    if skills:
        markdown_content += f"### Skills\n\n"
        for skill in skills.split(","):
            markdown_content += f"- {skill.strip()}\n"
        markdown_content += "\n"
    
    if education:
        markdown_content += f"### Education\n\n{education}\n\n"
    
    if projects:
        markdown_content += f"### Projects\n\n"
        for project in projects.split("\n"):
            markdown_content += f"- {project}\n"
        markdown_content += "\n"
    
    if training:
        markdown_content += f"### Certifications & Training\n\n{training}\n\n"

    # Define the filename with a .md extension
    markdown_filename = f"static/resume_{name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
    
    # Save the markdown content to a file
    with open(markdown_filename, 'w') as md_file:
        md_file.write(markdown_content)

    return markdown_filename
