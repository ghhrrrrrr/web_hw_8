import db
from models import Quote, Author, Tag
import redis
from redis_lru import RedisLRU

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)

def parse_input(user_input):
    cmd, *args = user_input.split(':')
    cmd = cmd.strip().lower()
    return cmd, *args

@cache
def find_by_name(args):
    print('func call\n---------------------------')
    args = ''.join(args).strip().split(',')
    authors = Author.objects(fullname__in=args)
    quotes = Quote.objects(author__in=authors)
    result =[quote.to_mongo().to_dict() for quote in quotes]
    return result

    
@cache
def find_by_tags(args):
    print('func call\n---------------------------')
    tags = [tag.strip() for tag in ''.join(args).split(',')]
    quotes = Quote.objects(tags__name__in=tags)
    result =[quote.to_mongo().to_dict() for quote in quotes]
    return result


if __name__ == '__main__':
    
    while True:
        user_input = input('>>>')
        
        if user_input.strip().lower() == 'exit':
            break
        
        command, *args = parse_input(user_input)
        
        if command == 'name':
            print(find_by_name(args))
            
        elif command == 'tags':
            print(find_by_tags(args))
            
        else:
            print(' Unknown command\n Use \'exit\' to quit')
        
        
        