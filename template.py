def build_readme(name, category, description, links=None, files=None):
    links_header = ""
    files_header = ""

    if links!=None:
        if links[:2]=="nc":
            links_header = f"\n##### Links: ```{links}```"
        else:
            links_header = f"\n##### Links: [{links}]({links})"
        
    if files!=None:
        files_header = "\n##### Files: "
        for i in files:
            file_name = i.split("?token")[0].split("/")[-1]
            files_header+=f"[{file_name}]({file_name}), "
        files_header=files_header[:-2] #remove ',' for the last element

    readme =  f"""# {name} [{category}]
![challenge](challenge.png)
### Challenge:\n"""

    readme+=description
    readme+=links_header
    readme+=files_header
    
    readme+="""\n\n### Solution:
Solution goes here.

Flag: ```flag{fl4g_g0eS_her3}```"""

    return readme