import json
from datetime import datetime
from models import Author, Quote, Tag
import db

def upload_authors():
    with open('json/authors.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
        
    for elem in data:
        born_date_str = elem['born_date']
        elem['born_date'] = datetime.strptime(born_date_str, '%B %d, %Y')
        Author(**elem).save()
        
def upload_quotes():
    with open('json/quotes.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
        
    for elem in data:
        author_name = elem.pop("author")
        author = Author.objects(fullname=author_name).first()
        
        tag_objects = [Tag(name=tag) for tag in elem['tags']]
        elem['tags'] = tag_objects
            
        Quote(author=author, **elem).save()
        
if __name__ == '__main__':
    upload_authors()
    print('uploaded authors')
    
    upload_quotes()
    print('uploaded quotes')

        
        
    
    