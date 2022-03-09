import xml.etree.cElementTree as ET
import re
import utils


class ToolsText:

# Exercice 1, TP1
    def htmlspecialchars(self, text):
        return (
            text.replace("&", "&amp;").
                replace('"', "&quot;").
                replace("<", "&lt;").
                replace(">", "&gt;")
        )

    def extract(self, nb_page, file, list_):

        title = ""
        text = ""
        first_id = True
        new_id = 0
        mlns = "{http://www.mediawiki.org/xml/export-0.10/}"

        # Get an iterable.
        context = ET.iterparse(file, events=("start", "end"))
        nb = 0

        fichier = open("/home/ufrinfo/PycharmProjects/pythonProject/venv/dataResult.xml", "w")
        fichier.write("<mediawiki>\n")

        for index, (event, elem) in enumerate(context):
            # Get the root element.
            if index == 0:
                root = elem

            if event == "end":

                if elem.tag == mlns + "title":

                    if elem.text is None:
                        title = ""
                    else:
                        title = self.htmlspecialchars(elem.text)

                    root.clear()

                if elem.tag == mlns + "id" and first_id:
                    first_id = False
                    root.clear()

                if elem.tag == mlns + "text":

                    if elem.text is None:
                        title = ""
                    else:
                        text = self.htmlspecialchars(elem.text)

                    root.clear()

                if elem.tag == mlns + "page" and any(
                        re.search(r'\b%s\b' % word.lower(), title.lower()) or re.search(r'\b%s\b' % word.lower(), text.lower()) for word in list_):

                    nb += 1
                    fichier.write("<page>\n")
                    fichier.write("<title>" + title + "</title>\n")
                    fichier.write("<id>" + str(new_id) + "</id>\n")
                    fichier.write("<text>" + text + "</text>\n")
                    fichier.write("</page>\n")

                    new_id += 1
                    title = ""
                    text = ""
                    first_id = True

                    root.clear()
            if nb == nb_page:
                break

        fichier.write("</mediawiki>")
        print(nb)
        fichier.close()


# Exercice 2, TP1

    def dict_id_title(self, file):
        title = ""
        id = ""
        first_id = True
        dict = {}
        mlns = ""

        # Get an iterable.
        context = ET.iterparse(file, events=("start", "end"))
        nb = 0
        for index, (event, elem) in enumerate(context):
            # Get the root element.
            if index == 0:
                root = elem

            if event == "end":

                if elem.tag == mlns + "title":

                    if elem.text is None:
                        title = ""
                    else:
                        title = self.htmlspecialchars(elem.text)

                    root.clear()

                if elem.tag == mlns + "id" and first_id:
                    first_id = False

                    id = elem.text
                    root.clear()

                if elem.tag == mlns + "text":  # le text

                    if elem.text is None:
                        title = ""

                    root.clear()

                if elem.tag == mlns + "page":
                    nb += 1
                    dict[title] = id
                    title = ""
                    id = ""
                    first_id = True
                    root.clear()

        return dict

    """def extractLambda(self, nb_page, file, f):

        title = ""
        id = ""
        text = ""
        first_id = True
        mlns = ""

        # Get an iterable.
        context = ET.iterparse(file, events=("start", "end"))
        nb = 0

        fichier = open("./large_files/ExtractLambda.xml", "w")
        fichier.write("<mediawiki>\n")

        for index, (event, elem) in enumerate(context):
            # Get the root element.
            if index == 0:
                root = elem

            if event == "end":  # balise fermante

                if elem.tag == mlns + "title":  # le titre

                    title = self.htmlspecialchars(elem.text)

                    root.clear()

                if elem.tag == mlns + "id" and first_id:  # si premier ID
                    first_id = False

                    id = elem.text

                    root.clear()

                if elem.tag == mlns + "text":  # le text

                    text = self.htmlspecialchars(elem.text)

                    root.clear()

                '''
                    création  de la page  

                '''

                if elem.tag == mlns + "page":
                    nb += 1

                    print(title)

                    fichier.write("<page>\n")
                    fichier.write("<title>" + f(title) + "</title>\n")
                    fichier.write("<id>" + id + "</id>\n")
                    fichier.write("<text>" + f(text) + "</text>\n")
                    fichier.write("</page>\n")

                    title = ""
                    id = ""
                    text = ""
                    first_id = True

                    root.clear()

            if nb == nb_page:
                break

        fichier.write("</mediawiki>")
        fichier.close()"""

    def findPage(self, id_, file):

        first = 0
        id_find = False
        title = ""
        text = ""
        id = ""
        first_id = True
        mlns = ""

        for event, elem in ET.iterparse(file, events=("start", "end")):

            if event == 'start':

                if elem.tag == (mlns + 'title'):
                    title = elem.text
                    elem.clear()

                if elem.tag == (mlns + 'id') and first_id:

                    if elem.text is None:
                        elem.text = ""
                    else:
                        id = elem.text
                        id = int(id)

                    if id == id_:
                        id_find = True

                    first_id = False
                    elem.clear()

                if (elem.tag == (mlns + 'text')):

                    if elem.text is None:
                        elem.text = ""
                    else:
                        text = elem.text

                    if first == 0:
                        if id_find:
                            break

                    first_id = True
                    elem.clear()

            if (event == 'end'):
                if (elem.tag == (mlns + 'text')):

                    first = 1

                    if elem.text is None:
                        elem.text = ""
                    else:
                        text = elem.text

                    if first == 1:

                        if id_find:
                            break

                    first_id = True
                elem.clear()

            elem.clear()

        if id != id_:
            return {"title": "", "id": "", "text": ""}

        return {"title": title, "id": id, "text": text}


a = ToolsText()

#print(a.extract(200_000, "/home/ufrinfo/PycharmProjects/pythonProject/venv/data", ["France", "Paris"]))

#print(a.dict_id_title("/home/ufrinfo/PycharmProjects/pythonProject/venv/dataResult.xml"))
print(a.findPage(1456, "/home/ufrinfo/PycharmProjects/pythonProject/venv/dataResult.xml"))

# ============ main ===================


"""context = ET.iterparse("../large_files/fileResult.xml", events=("start", "end"))

for index, (event, elem) in enumerate(context):
    # Get the root element.
    if index == 0:
        root = elem

    if event == "end":
        if elem.tag == "text":
            print(utils.lien_interne(elem.text))
            break"""
