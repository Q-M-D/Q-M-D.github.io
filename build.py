import os
import yaml

keep_files = [
    "alerts.md", "changelog.md", "cta.md", "docs.md", "footer.md", "media.md", 
    "posts.md", "support.md", "translation.md",
    "analytics.md", "comments.md", "customize.md", "faq.md", "hero.md", 
    "navigation.md", "setup.md", "team.md", "videos.md",
    "boxes.md", "contact.md", "development.md", "featured.md", 
    "installation.md", "pages.md", "sources.md", "toc.md"
]

def git_pull(path):
    """
    Pulls the latest changes from the Git repository located at the specified path.

    Args:
        path (str): The path to the Git repository.
    """
    os.chdir(path)
    os.system("git pull")
    os.chdir("..")

def generate_directory_structure(path):
    """
    Generates a directory structure for the specified path.

    Args:
        path (str): The path to generate the directory structure for.

    Returns:
        list: A list of dictionaries representing the directory structure. Each dictionary contains a "title" key and a "docs" key.
    """
    directory_structure = []

    for item in os.listdir(path):
        item_path = os.path.join(path, item)

        if os.path.isdir(item_path):
            docs = []

            for subitem in os.listdir(item_path):
                subitem_path = os.path.join(item_path, subitem)
                if os.path.isdir(subitem_path):
                    docs.append(subitem)

            directory_entry = {
                "title": item,
                "docs": docs
            }
            directory_structure.append(directory_entry)

    return directory_structure

def write_yml(directory_structure):
    """
    Writes the directory structure to a YAML file.

    Args:
        directory_structure (list): A list of dictionaries representing the directory structure. Each dictionary contains a "title" key and a "docs" key.
    """
    with open("_data/navigation_docs.yml", "w") as yaml_file:
        result = ""
        for item in directory_structure:
            if item["title"] in ["基础知识", "数据处理案例", "软件整理", "数据处理/转换脚本", "数据校内镜像"]:
                result += '- title: ' + item["title"] + '\n'
                result += '  docs:\n'
                for doc in item["docs"]:
                    result += '  - ' + doc + '\n'
                result += '\n'
        yaml_file.write(result)

def copy2docs(path, docspath):
    # 自动删除
    for item in os.listdir(docspath):
        # 判断文件是否在keep_files中，在的话保留，不在直接删除文件。如果是文件夹，直接删除文件夹
        if item not in keep_files:
            item_path = os.path.join(docspath, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            else:
                os.system("rm -rf " + item_path)

    for item in os.listdir(path):
        item_path = os.path.join(path, item)

        if os.path.isdir(item_path):
            if item in ["基础知识", "数据处理案例", "软件整理", "数据处理/转换脚本", "数据校内镜像"]:
                os.system("cp -r " + item_path + "/ " + docspath + "/")
                for subitem in os.listdir(item_path):
                    subitem_path = os.path.join(item_path, subitem)
                    if os.path.isdir(subitem_path):
                        for subsubitem in os.listdir(subitem_path):
                            if subsubitem.endswith(".md"):
                                os.system("cp " + os.path.join(subitem_path, subsubitem) + " " + docspath + "/")
                                
                                # with open(os.path.join(docspath, subsubitem), "r") as f:
                                #     content = f.read()
                                # with open(os.path.join(docspath, subsubitem), "w") as f:
                                #     f.write("---\ntitle: " + subsubitem[:-3] + "\n---\n\n * TOC\n {:toc} \n\n" + content)

if __name__ == "__main__":
    root_path = "Open-EM"
    docspath = "_docs"
    git_pull(root_path)
    write_yml(generate_directory_structure(root_path))
    copy2docs(root_path, docspath)
    # os.system("bundle exec jekyll server")
