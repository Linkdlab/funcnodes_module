import licensecheck
import os
import json
import requests
import re
import warnings


def get_pypy_data(basedir, package_data, version=True):
    pipydatair = os.path.join(basedir, "pypi_data")
    if not os.path.exists(pipydatair):
        os.makedirs(pipydatair)

    if version:
        target_file = os.path.join(
            pipydatair, f"{package_data['name']}_{package_data['version']}.json"
        )
    else:
        target_file = os.path.join(pipydatair, f"{package_data['name']}_latest.json")

    if os.path.exists(target_file) and os.path.getsize(target_file) > 0 and version:
        with open(target_file, "r") as f:
            return json.load(f)

    if version:
        baseurl = "https://pypi.org/pypi/{package}/{version}/json"
        url = baseurl.format(
            package=package_data["name"], version=package_data["version"]
        )
    else:
        baseurl = "https://pypi.org/pypi/{package}/json"
        url = baseurl.format(package=package_data["name"])

    response = requests.get(url)
    if response.status_code != 200:
        return None

    data = response.json()

    if "info" not in data:
        return None

    with open(target_file, "w+") as f:
        json.dump(data, f, indent=4)

    return data


def get_license_text_pypi(basedir, package_data, version=True):
    data = get_pypy_data(basedir, package_data, version=version)
    if not data:
        return None, None

    info = data["info"]

    if "license" not in info:
        return None, None

    license = info["license"]

    if not license:
        return None, None

    if len(license) < 100 and version:
        return get_license_text_pypi(basedir, package_data, version=False)
    if len(license) < 100:
        return None, None
    return license, data["info"]["release_url"]


def get_license_text_github(basedir, package_data, version=True):
    pypidata = get_pypy_data(basedir, package_data, version=version)
    if not pypidata:
        return (
            get_license_text_github(basedir, package_data, version=False)
            if version
            else (None, None)
        )

    if "project_urls" not in pypidata["info"]:
        return (
            get_license_text_github(basedir, package_data, version=False)
            if version
            else (None, None)
        )

    project_urls = pypidata["info"]["project_urls"]
    if not project_urls:
        return (
            get_license_text_github(basedir, package_data, version=False)
            if version
            else (None, None)
        )

    for possible_key in [
        "Source",
        "source",
        "Source Code",
        "source code",
        "Repository",
        "repository",
        "Homepage",
        "homepage",
        "GitHub",
        "github",
        "Code",
        "code",
    ]:
        if possible_key in project_urls:
            github_url = project_urls[possible_key]
            # check if url matches github.com/username/repo and extract username and repo

            match = re.match(
                ".*github.com/"  # github.com
                "([^/]+)/"  # username
                "([^/]+)",  # repo
                github_url,
            )

            if not match:
                continue

            username, repo = match.groups()
            print(github_url, "-", username, repo)

            if "github.com" not in github_url:
                continue
            for head in ["master", "main"]:
                for file in [
                    "LICENSE",
                    "LICENSE.md",
                    "LICENSE.txt",
                    "COPYRIGHT",
                    "COPYRIGHT.md",
                    "COPYRIGHT.txt",
                ]:
                    url = f"https://raw.githubusercontent.com/{username}/{repo}/refs/heads/{head}/{file}"
                    response = requests.get(url)
                    if response.status_code == 200:
                        return response.text, url

            for head in ["master", "main"]:
                tree_url = (
                    f"https://api.github.com/repos/{username}/{repo}/git/trees/{head}"
                )

                response = requests.get(tree_url)
                if response.status_code != 200:
                    continue

                tree = response.json()

                for item in tree["tree"]:
                    if item["type"] != "blob":
                        continue
                    lowerpath = item["path"].lower()
                    if lowerpath.startswith("license") or lowerpath.startswith(
                        "copyrigh"
                    ):
                        url = f"https://raw.githubusercontent.com/{username}/{repo}/refs/heads/{head}/{item['path']}"
                        response = requests.get(url)
                        if response.status_code == 200:
                            return response.text, url
    return (
        get_license_text_github(basedir, package_data, version=False)
        if version
        else (None, None)
    )


def get_license_text(basedir, package_data):
    license, src = get_license_text_pypi(basedir, package_data, version=True)
    if license:
        return license, src

    license, src = get_license_text_github(basedir, package_data, version=True)
    if license:
        return license, src

    return None, None


def gen_third_party_notice(path: str):
    rawpath = os.path.join(path, ".licensecheck")
    licensecheck_path = os.path.join(rawpath, "licensecheck.json")
    if not os.path.exists(rawpath):
        os.makedirs(rawpath)
    licensecheck.main({"format": "json", "file": licensecheck_path})

    with open(licensecheck_path, "r") as f:
        data = json.load(f)

    packagefile = os.path.join(rawpath, "packages.json")
    try:
        with open(packagefile, "r") as f:
            packages = json.load(f)
    except Exception:
        packages = {}

    for package in data["packages"]:
        if (
            package["name"] not in packages
            or package["version"] != packages[package["name"]]["version"]
        ):
            packages[package["name"]] = package
        else:
            pass

    for packagename, package_data in packages.items():
        if (
            "full_license" in package_data
            and package_data["full_license"]
            and "license_source" in package_data
            and package_data["license_source"]
        ):
            continue
        lic, src = get_license_text(rawpath, package_data)
        package_data["full_license"] = lic
        package_data["license_source"] = src

        if not package_data["full_license"]:
            warnings.warn(
                f"Could not find license for {package_data['name']} {package_data['version']}"
            )

    with open(packagefile, "w+") as f:
        json.dump(packages, f, indent=4)

    out = (
        "This list of licence notices from dependencies is autogenerated and may not be accurate."
        "Please check the dependencies for the correct licence information.\n\n"
    )
    for packagename, package_data in packages.items():
        data = f"### {package_data['name']}-{package_data['version']}\n"
        if package_data["license"]:
            data += f"- License: {package_data['license'].strip()}\n"
        if package_data["license_source"]:
            data += f"- Source: {package_data['license_source'].strip()}\n"
        if package_data["full_license"]:
            data += f"\n{package_data['full_license'].strip()}\n\n"
        data += "-" * 20 + "\n\n"

        out += data

    dec_out = out.encode("utf-8", errors="replace")
    with open(os.path.join(path, "THIRD_PARTY_NOTICES.md"), "wb+") as f:
        f.write(dec_out)


if __name__ == "__main__":
    gen_third_party_notice(os.getcwd())
