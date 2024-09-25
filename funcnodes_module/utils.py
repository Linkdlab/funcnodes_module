from typing import Tuple


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


ENCODINGS = [
    "utf_8",
    "ascii",
    "utf_8_sig",
    "latin_1",  # iso-8859-1 is also known as latin-1
    "utf_16",
    "utf_16_le",
    "utf_16_be",
    "utf_32",
    "utf_32_le",
    "utf_32_be",
    "cp1252",  # Common encoding in Windows
    "cp1250",
    "cp1251",
    "cp1253",
    "cp1254",
    "cp1255",
    "cp1256",
    "cp1257",
    "cp1258",
    "iso8859_1",  # Similar to latin-1
    "iso8859_2",
    "iso8859_3",
    "iso8859_4",
    "iso8859_5",
    "iso8859_6",
    "iso8859_7",
    "iso8859_8",
    "iso8859_9",
    "iso8859_10",
    "iso8859_11",
    "iso8859_13",
    "iso8859_14",
    "iso8859_15",
    "iso8859_16",
    "cp437",
    "cp850",
    "cp1251",  # Common in Windows for Cyrillic
    "koi8_r",  # Common in Russia
    "koi8_u",  # Common in Ukraine
    "big5",  # Traditional Chinese encoding
    "gb2312",  # Simplified Chinese encoding
    "gbk",  # Simplified Chinese encoding
    "gb18030",  # Modern Chinese encoding
    "cp932",  # Shift JIS, commonly used in Japan
    "shift_jis",
    "euc_jp",  # Commonly used in Japan
    "euc_kr",  # Commonly used in Korea
    "iso2022_jp",  # Japanese encoding
    "cp866",  # Common in Russia for DOS
    "cp850",  # Western Europe, DOS encoding
    "cp852",  # Central European, DOS encoding
    "cp855",  # Cyrillic, DOS encoding
    "cp857",  # Turkish, DOS encoding
    "cp860",  # Portuguese, DOS encoding
    "cp861",  # Icelandic, DOS encoding
    "cp862",  # Hebrew, DOS encoding
    "cp863",  # Canadian French, DOS encoding
    "cp865",  # Nordic, DOS encoding
    "mac_roman",  # Western Europe, old Mac encoding
    "mac_cyrillic",  # Cyrillic, old Mac encoding
    "mac_greek",  # Greek, old Mac encoding
    "mac_iceland",  # Icelandic, old Mac encoding
    "mac_latin2",  # Central Europe, old Mac encoding
    "mac_turkish",  # Turkish, old Mac encoding
    "ptcp154",  # Kazakh, Cyrillic
    "shift_jisx0213",  # Extended Shift JIS
    "shift_jis_2004",  # Extended Shift JIS
    "iso2022_jp_1",
    "iso2022_jp_2",
    "iso2022_jp_3",
    "iso2022_jp_2004",
    "iso2022_jp_ext",
    "iso2022_kr",  # Korean encoding
    "big5hkscs",  # Big5 variant for Hong Kong
    "hz",  # Chinese encoding
    "johab",  # Korean encoding
    "cp037",
    "cp273",
    "cp424",
    "cp500",
    "cp720",
    "cp737",
    "cp775",
    "cp858",
    "cp864",
    "cp869",
    "cp874",
    "cp875",
    "cp949",  # Korean encoding
    "cp950",  # Traditional Chinese encoding
    "cp1006",
    "cp1026",
    "cp1125",
    "cp1140",
    "koi8_t",
    "kz1048",  # Kazakh encoding
    "utf_7",
    "euc_jis_2004",
    "euc_jisx0213",
]

# Print sorted encodings


def read_file_content(filepath) -> Tuple[str, str]:
    for enc in ENCODINGS:
        try:
            with open(filepath, "r", encoding=enc) as f:
                return f.read(), enc
        except UnicodeDecodeError:
            continue

    raise UnicodeDecodeError(
        f"Could not decode file {filepath} with any of the encodings {ENCODINGS}"
    )


def write_file_content(filepath, content, enc):
    with open(filepath, "w", encoding=enc) as f:
        f.write(content)
