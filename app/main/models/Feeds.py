from . import *
from . import Main
from .. import make_res, gen_random
from ..resources.Image import FileProcessor
from ...core.db import Connection


class Feed(Main):
    """docstring for Feeds"""

    def __init__(self):
        super().__init__()
        pass

    @classmethod
    def new(cls):
        print("5656")

        j = request.json
        d = j.get("data")
        if not d:
            return make_res(msg="cannot post empty data")

        status = d.get('status')
        files = d.get("files")
        print(files)
        uid = d.get("user_id")
        if not uid:
            return make_res(msg="user id required")
        if files:
            for file in files:
                file['content'] = base64.b64decode(file['content'])

            files = [
                FileProcessor(file, "feed")
                for file in files
            ]

        post_id = gen_random(20)
        post = {'post_id': post_id,
                'uid': uid,
                'post_on': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'type': 'post'
                }
        feeds = [
            {
                "post_id": post_id,
                "status": status,
                "file": file.new_name,
                "ratio": file.ratio,
                "file_type": file.type
            }
            for file in files
        ]
        if cls.create(cls.T_POSTS, post):
            for i in range(len(feeds)):
                feed = feeds[i]
                if cls.create(cls.T_FEEDS, feed):
                    files[i].upload("feeds")
            return make_res(msg="success", success=1)

        return make_res(msg="failed. Try again", success=0)

    @classmethod
    def all(cls):
        d = Connection().Read(f"select * from {cls.T_POSTS} order by post_on desc")
        return make_res(res=d, success=1)

    @classmethod
    def for_user(cls):
        j = request.json
        d = j.get("data")
        if not d:
            return make_res(msg="failed to fetch feeds")
        filters = d.get("filters")
        pdo = Connection()
        lim = d.get('limits')
        uid = d.get('user_id') or (filters.get("user_id") if filters else None)
        lf = 0
        lr = 15
        if lim:
            lf = lim[0]
            lr = lim[1]
        
        u_only = d.get("useronly")
        if u_only:
            sql = (f"SELECT * from {cls.T_POSTS} where uid = %s order by post_on desc limit %s , %s")
            pdo = pdo.Read(sql, [uid, lf, lr])
        else:
            sql = (f"SELECT * from {cls.T_POSTS} where uid = %s or uid in "
               f"(select followingid from {cls.T_FOLLOW} "
               f"where followerid = %s ) order by post_on desc limit %s , %s")
            pdo = pdo.Read(sql, [uid, uid, lf, lr])

        return make_res(res=pdo, success=1 if pdo else 0)

    @classmethod
    def post(cls):
        j = request.json
        d = Connection().Read(f"select * from {cls.T_FEEDS} where post_id = %s", j.get("data")["post_id"])
        return make_res(res=d, success=1)

    @classmethod
    def info(cls):
        j = request.json
        d = Connection().Read(f"select * from {cls.T_POSTS} where post_id = %s", j.get("data")["post_id"])
        return make_res(res=d, success=1)

    @classmethod
    def videos(cls):
        d = Connection().Read(f"select * from {cls.T_FEEDS} where file_type = %s", "vid")
        return make_res(res=d, success=1)

    @classmethod
    def media(cls):
        j = request.json.get("data")
        uid = j.get("user_id") or j.get("identity")
        t = j.get("type")
        sql = f"SELECT f.*, p.uid FROM {cls.T_FEEDS} f JOIN {cls.T_POSTS} p ON f.post_id = p.post_id WHERE p.uid = %s ORDER BY p.post_on DESC"
        d = Connection().Read(sql, uid)
        return make_res(res=d, success=1)
    @classmethod
    def comments(cls):
        data = request.json.get("data")
        if not data:
            return cls.data_error()

        p_id = data.get("post_id")
        sql = cls.t_data_and(cls.T_COMMENT,target=p_id)
        return make_res(success=1,res=sql)

    @classmethod
    def add_comment(cls):
        data = request.json.get("data")
        if not data:
            return cls.data_error()

        p_id = data.get("post_id")
        c_target = data.get("target")
        uid = data.get("uid")
        files = data.get("files")
        data_cmt = {
            'comment': data.get("comment"),
            'uid': uid,
            'target': p_id,
            'time': getNow(),
        }
        if files:
            for file in files:
                file['content'] = base64.b64decode(file['content'])

            files = [
                FileProcessor(file, "cmt")
                for file in files
            ]
            for f1 in range(len(files)):
                f1_ = files[f1]
                data_cmt[f"file{f1+1}"] = f1_.new_name

        if cls.create(cls.T_COMMENT, data_cmt):
            if c_target != uid:
                data_notify = {
                    'for_': c_target,
                    'from_': uid,
                    'target': p_id,
                    'type': 'comment',
                    'time': getNow(),
                    'count': '0',
                    'status': '0'
                }
                cls.create(cls.T_NOTE,data_notify)
            for f1 in range(len(files)):
                files[f1].upload("comments")
        return make_res(success=1)

# print(file.new_name)
# file.upload("feeds")
