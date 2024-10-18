def generate_markdown(name, email, phone, profile, skills, education, projects, training, photo=None):
    markdown_content = f"# {name}\n\n"
    markdown_content += f"**Email**: {email}\n"
    markdown_content += f"**Phone**: {phone}\n\n"

    markdown_content += "\n---\n\n"

    if profile:
        markdown_content += "### Profile Summary\n"
        markdown_content += f"{profile}\n\n"

    if skills:
        markdown_content += "### Skills\n"
        skills_list = skills.splitlines()
        for skill in skills_list:
            skill = skill.strip()
            if skill:  # Ensure the skill is not empty
                markdown_content += f"- {skill}\n"  # Adding bullet point
        markdown_content += "\n"  # Add an extra line for spacing

    if education:
        markdown_content += "### Education\n"
        education_list = education.splitlines()
        markdown_content += "\n\n".join([edu.strip() for edu in education_list if edu]) + "\n\n"

    if projects:
        markdown_content += "### Projects\n"
        projects_list = projects.splitlines()
        markdown_content += "\n\n".join([proj.strip() for proj in projects_list if proj]) + "\n\n"

    if training:
        markdown_content += "### Certifications & Training\n"
        training_list = training.splitlines()
        for cert in training_list:
            cert = cert.strip()
            if cert:  # Ensure the certification is not empty
                markdown_content += f"- {cert}\n"  # Adding bullet point
        markdown_content += "\n"  # Add an extra line for spacing

    markdown_content += "\n---\n\n"

    # Saving the Markdown file
    markdown_output = f'static/{name}_resume.md'
    with open(markdown_output, 'w') as file:
        file.write(markdown_content)

    return markdown_output
