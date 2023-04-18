import random, base64

def get_user_posts(client):
    db = client.OpioidsData
    collection_PostAnnotatedCounter = db.PostsAnnotatedCounter
    collection_Posts = db.Posts

    cursor_PostAnnotatedCounter = collection_PostAnnotatedCounter.find( { 'count': { '$lt': 3 } } )
    data_PostAnnotatedCounter =  list(cursor_PostAnnotatedCounter)
    random_idx = random.randrange(0, len(data_PostAnnotatedCounter))
    record_user = data_PostAnnotatedCounter[random_idx]

    user_id = record_user['user_id']
    user_id_count = record_user['count']
    user_name = record_user['user_name']

    cursor_Posts = collection_Posts.find({'user_id':user_id})
    data_posts =  list(cursor_Posts)
    data_posts_sorted = sorted(data_posts, key = lambda x:x['time'])
    data_posts_sorted_filtered = []
    for i in data_posts_sorted:
        del i["_id"]
        data_posts_sorted_filtered.append(i)
    return data_posts_sorted_filtered, user_id, user_id_count, user_name


def encode_text(text):
    message_bytes = text.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message

def decode_text(text):
    base64_bytes = text.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return message
