from bilibili_api import sync, video, user, video_zone
from bilibili_api.comment import get_comments, CommentResourceType, OrderType
from bilibili_api import Credential
from module.tool import read_json
from .myapi import get_up_stat, get_space_notice
from datetime import datetime


class Cred:

    def __init__(self, log_in=False, path='conf\Credential.json') -> None:
        self.path = path
        self.Credential = None
        if log_in:
            self.get_Credential()

    def get_Credential(self):
        data = read_json(self.path)
        self.credential = Credential(sessdata=data['sessdata'],
                                     bili_jct=data['bili_jct'],
                                     buvid3=data['buvid3'],
                                     dedeuserid=['dedeuserid'])


class VIDEO(Cred):

    def __init__(self, aid, log_in=False, path='conf\Credential.json') -> None:
        super().__init__(log_in, path)
        self.aid = aid
        self.__v = video.Video(aid=aid)
        self.bv = self.__v.get_bvid()
        self.infor = None
        self.stat = None
        self.comment = list()
        self._danmaku = list()
        self._tags = list()
        self._staff = list()
        self._info = None
        # self.tags_list()

    def __get__info(self):
        try:
            self._info = sync(self.__v.get_info())
        except:
            pass

    def info(self):
        if self.infor:
            return self.infor
        if not self._info:
            self.__get__info()
        data = self._info
        self.infor = {
            'bvid':
            data['bvid'],  #视频BV
            'aid':
            data['aid'],  #视频aid
            "tid":
            data['tid'],  #视频分区
            'title':
            data['title'],  #标题
            'pubtime':
            datetime.fromtimestamp(
                data['pubdate']).strftime('%Y-%m-%d %H:%M:%S'),  #发布时间
            'introduction':
            data['desc'],  #简介
            'uid':
            data['owner']['mid'],  #发布的UP的mid
            'pic_url':
            data['pic']  #封面url
        }
        return self.infor
        # return data

    def tags_list(self):
        try:
            data = sync(self.__v.get_tags())
        except:
            return False
        for tag in data:
            self._tags.append(tag['tag_id'])
            return data

    def tags(self):
        data = list()
        for order, tid in enumerate(self._tags):
            data.append({'aid': self.aid, 'tid': tid, 'tag_order': order + 1})
        return data

    def now(self):
        if self.stat:
            return self.stat
        data = sync(self.__v.get_stat())
        self.stat = {
            "aid": data["aid"],  #视频aid
            "bvid": data['bvid'],  #视频BV
            "view": data['view'],  #播放量
            "danmaku": data['danmaku'],  #弹幕量
            "comment": data['reply'],  #评论数
            "favorite": data['favorite'],  #收藏量
            "coin": data['coin'],  #投币数
            "share": data['share'],  #分享量
            "likes": data['like'],  #点赞数
        }
        return self.stat

    def reply(self):
        if self.comment:
            return self.comment
        cmt = COMMENT(self.aid)
        self.comment = cmt.List()
        return self.comment

    def danmaku(self):
        if self._danmaku:
            return self._danmaku
        data = sync(self.__v.get_danmakus())
        for dmk in data:
            if dmk.id_ <= 0:
                continue
            self._danmaku.append({
                "aid":
                self.aid,  #视频aid
                "did":
                dmk.id_,  #弹幕id
                "content":
                dmk.text,  #内容
                "dm_time":
                dmk.dm_time,  #视频中的位置s
                "send_time":
                datetime.fromtimestamp(
                    dmk.send_time).strftime('%Y-%m-%d %H:%M:%S'),  #发送时间
                "crc32_id":
                dmk.crc32_id,  #弹幕发送者 UID 经 CRC32 算法取摘要后的值
                "mode":
                dmk.mode  #弹幕模式
            })
        return self._danmaku

    def staff(self):
        if self._staff:
            self._staff
        if not self._info:
            self.__get__info()
        data = self._info

        if not data['rights']['is_cooperation']:
            self._staff.append({
                'aid': self.aid,
                'uid': data['owner']['mid'],
                'division': 'UP主'
            })
            return self._staff

        for stf in data['staff']:
            self._staff.append({
                'aid': self.aid,
                'uid': stf['mid'],
                'division': stf['title']
            })
        return self._staff
        # return self._info


class COMMENT(Cred):

    def __init__(self,
                 oid,
                 type_=1,
                 log_in=False,
                 path='conf\Credential.json') -> None:
        super().__init__(log_in, path)
        type_ = CommentResourceType(type_)
        order = OrderType.LIKE
        if log_in:
            data = sync(
                get_comments(oid=oid,
                             type_=type_,
                             order=OrderType.LIKE,
                             credential=self.Credential))
            self.__comment = self.__choose(data)
        else:
            data = sync(get_comments(oid=oid, type_=type_, order=order))
            self.__comment = self.__choose(data)

    def __choose(self, data):
        result = list()
        for reply in data['replies']:
            result.append({
                'rpid':
                reply['rpid'],  #评论id
                'aid':
                reply['oid'],  #视频id
                'uid':
                reply['mid'],  #用户id
                'rptime':
                datetime.fromtimestamp(
                    reply['ctime']).strftime('%Y-%m-%d %H:%M:%S'),  #发布时间
                'likes':
                reply['like'],  #点赞数
                'rcount':
                reply['rcount'],  #回复数
                'message':
                reply['content']['message']  #评论内容
            })
        return result

    def List(self):
        return self.__comment


class USER(Cred):

    def __init__(self, uid, log_in=False, path='conf\Credential.json') -> None:
        super().__init__(log_in, path)
        self.mid = uid

        if log_in:
            self.__u = user.User(uid=self.mid, credential=self.Credential)
        else:
            self.__u = user.User(uid=self.mid)

        self.infor = dict()
        self.stat = dict()
        self._videos = list()
        self._follower = list()

    def info(self):
        if self.infor:
            return self.infor
        try:
            data = sync(self.__u.get_user_info())
        except:
            self.infor = {
                "uid": self.mid,
                "name": '账户已注销',
                "sex": None,
                "face_url": None,
                "persign": None,
                "level": None,
                "official": None,
                "notice": None
            }
            return self.infor

        self.infor = {
            "uid": data['mid'],
            "name": data['name'],  #用户名
            "sex": data['sex'],  #性别
            "face_url": data['face'],  #头像URL
            "persign": data['sign'],  #个人简介
            "level": data['level'],  #用户等级
            "official": data['official']['title'],  #官方认证
            "notice": get_space_notice(self.mid)['data']  #公告
        }
        return self.infor

    def now(self):
        if self.stat:
            return self.stat
        data1 = sync(self.__u.get_relation_info())
        data2 = get_up_stat(self.mid)
        self.stat = {
            "uid": data1['mid'],
            "following": data1['following'],  #关注数
            "follower": data1['follower'],  #粉丝数
            "archive": data2['data']['archive']['view'],  #播放数
            "article": data2['data']['article']['view'],  #专栏阅读量
            "likes": data2['data']['likes']  #获赞数
        }
        return self.stat

    def videos(self):
        if self._videos:
            return self._videos
        data = sync(self.__u.get_videos(ps=50))
        for v in data['list']['vlist']:
            self._videos.append(v['aid'])
        return self._videos

    def follower(self):
        if self._follower:
            return self._follower
        data = sync(self.__u.get_followings())
        return [u['mid'] for u in data['list']]


class ZONE(Cred):

    def __init__(self, tid=int | None) -> None:
        super().__init__()
        self.tid = tid
        self._info = None

    def info(self):
        if self._info:
            return self._info
        data = video_zone.get_zone_info_by_tid(self.tid)[1]
        self._info = {
            'tid': data['tid'],
            'zone_name': data['name'],
            'route': data['route'],
            'zone_url': data['url'][2:]
        }
        return self._info
