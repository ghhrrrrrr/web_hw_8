import db
from models import Quote, Author, Tag

def parse_input(user_input):
    cmd, args = user_input.split(':')
    cmd = cmd.strip().lower()
    return cmd, args

def find_by_name(args):
    args = args.strip().split(',')
    authors = Author.objects(fullname__in=args)
    quotes = Quote.objects(author__in=authors)
    for quote in quotes:
        print(quote.to_mongo().to_dict())
    
        
def find_by_tags(args):
    tags = [tag.strip() for tag in args.split(',')]
    quotes = Quote.objects(tags__name__in=tags)
    for quote in quotes:
        print(quote.to_mongo().to_dict())


if __name__ == '__main__':
    
    while True:
        user_input = input('>>>')
        
        if user_input.strip().lower() == 'exit':
            break
        
        command, args = parse_input(user_input)
        
        if command == 'name':
            find_by_name(args)
            
        elif command == 'tags':
            find_by_tags(args)
            
        else:
            print(' Unknown command\n Use \'exit\' to quit')
        
        
        