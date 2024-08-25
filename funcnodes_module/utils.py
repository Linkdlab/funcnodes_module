def create_names(name):
    project_name = name.replace("_", " ").replace("-", " ").title()
    module_name = name.replace(" ", "_").replace("-", "_").lower()
    package_name = module_name.replace("_", "-")
    return project_name, module_name, package_name


def replace_names(
    content,
    project_name=None,
    module_name=None,
    package_name=None,
    git_user=None,
    git_email=None,
):
    if module_name:
        content = content.replace("{{ module_name }}", module_name)
    if package_name:
        content = content.replace("{{ package-name }}", package_name)
    if project_name:
        content = content.replace("{{ Project Name }}", project_name)
    if git_user:
        content = content.replace("{{ git_user }}", git_user)
    if git_email:
        content = content.replace("{{ git_email }}", git_email)
    return content
