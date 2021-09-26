# toString
str(...)

#empty block:
pass

# dict
    _a_dict[key} = value    

    for key in a_dict:      for item in a_dict.items():         for key, value in a_dict.items():
         print(key)          print(item)                            print(key, '->', value)
Also: a_dict.keys(),  a_dict.values(),  len(a_dict)
To delete: del d[key]

# list
    a_list = []
    a_list.append(a_truc)

# Search in string
    if (word.find('pawan') != -1):
        print ("Contains given substring ")
    else:
        print ("Doesn't contains given substring")

# matching expr
    import re
    re.findall(r"#\w+", a_string )

    .     Le point correspond à n'importe quel caractère.
    ^     Indique un commencement de segment mais signifie aussi "contraire de"
    $     Fin de segment
    [xy]  Une liste de segment possibble. Exemple [abc] équivaut à : a, b ou c
    (x|y) Indique un choix multiple type (ps|ump) équivaut à "ps" OU "UMP" 
    \d    le segment est composé uniquement de chiffre, ce qui équivaut à [0-9].
    \D    le segment n'est pas composé de chiffre, ce qui équivaut à [^0-9].
    \s    Un espace, ce qui équivaut à [ \t\n\r\f\v].
    \S    Pas d'espace, ce qui équivaut à [^ \t\n\r\f\v].
    \w    Présence alphanumérique, ce qui équivaut à [a-zA-Z0-9_].
    \W    Pas de présence alphanumérique [^a-zA-Z0-9_].
    \     Est un caractère d'échappement


# Folder and Path
> [more...](https://stackabuse.com/introduction-to-the-python-pathlib-module/)
    import pathlib
    current_dir = pathlib.Path.cwd()
    home_dir = pathlib.Path.home()

    for entry in folder.iterdir(): # Entry is a Path
        entry.name, entry.is_file() .exists(), rename(), parent(), ....
        stem(), suffix(), match()

# write file
 with open(a_filepath, 'w', encoding='utf-8', newline='') as a_file:
    a_file.writeLines
 
# Exception
    class CustomError(Exception):
         pass

    raise CustomError( message="...")
