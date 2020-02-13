import json
import sys
import re

libraryFile = "bibliography/mylibrary.json"
inputFile = "publicpermissioned.adoc"
biblioFile = "bibliography.adoc"

def formatSingleAuthor(author):
    givenName = author["given"]
    return givenName[0] + ". " + author["family"]

def formatDate(issued):
    year = issued["date-parts"][0][0]
    return str(year)

def formatAuthorList(authorList):
    size = len(authorList)
    if size == 0:
        return ""
    elif size == 1:
        return formatSingleAuthor(authorList[0]) + ". "
    elif size == 2:
        auth1 = formatSingleAuthor(authorList[0])
        auth2 = formatSingleAuthor(authorList[1]) 
        return auth1 + " and " + auth2 + ". "

    # 3 or more authors
    auth1 = formatSingleAuthor(authorList[0])
    auth2 = formatSingleAuthor(authorList[1]) 
    return auth1 + ", " + auth2 + " etAl. "



def formatReference(citeKey, entry):
    # Reference link in Asciidoc
    refEntry = f"* [[[{citeKey}, {citeKey}]]] "

    # The author list
    refEntry = refEntry + formatAuthorList(entry["author"])

    # The title
    refEntry = refEntry + "_" + entry["title"] + "_. " 

    # The date
    refEntry = refEntry + formatDate(entry["issued"])

    # Add a line
    refEntry = refEntry + "\n"

    # Return the resulting formatted entry
    return refEntry


# Check if we have received the name of the file
# Otherwise use the default
if len(sys.argv) > 1:
    inputFile = sys.argv[1]

# Read the full library data
with open(libraryFile, encoding='utf-8-sig') as f:
    libraryData = json.load(f)

# Convert to a dictionary
libraryDict = {}
for item in libraryData:
    libraryDict[item["id"]] = item

# Read the input file
with open(inputFile, encoding='utf-8-sig') as f:
    inputData = f.read()

# Compile the regex string search
p = re.compile('<<(.+?)>>')

# Find all citeKeys in the input file
# Some of them will be figures or tables, but it does not matter
citeKeys = p.findall(inputData)
   
# Create the list of found citeKeys
foundCiteKeys = []
for citeKey in citeKeys:
    if citeKey in libraryDict:
        print ("OK: " + citeKey)
        # Do not add if already in the list
        if not citeKey in foundCiteKeys:
            foundCiteKeys.append(citeKey)
    else:
        print ("NOT FOUND: " + citeKey)

with open(biblioFile, "w", encoding='utf-8-sig') as f:

    # Iterate the list of found citeKeys
    for citeKey in foundCiteKeys:
        item = libraryDict[citeKey]
        reference = formatReference(citeKey, item)
        f.write(reference + '\n')


