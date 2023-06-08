from module.network import VIDEO, COMMENT, USER, ZONE
from module.tool import read_json, write_json
from module.api import get_up_db
from bilibili_api import video_zone, sync, DmMode, SpecialDanmaku, user


def uids():
    uids = [524933572]
    return uids


def ex():
    path = 'test/myfollows.json'
    uid = 422535780
    me = USER(uid=uid, log_in=True)
    write_json(path, me.follower())


def dmk():
    print(DmMode(1).name)
    print(SpecialDanmaku(1).name)
    DmMode(4)
    DmMode(5)
    DmMode(6)
    DmMode(9)


if __name__ == "__main__":
    aid = 694448310
    mid = 474012664
    tid = 30
    t_name = "VOCALOID·UTAU"
    video = VIDEO(aid)
    user1 = USER(mid)
    zone = ZONE(tid=tid)
    path1 = f'test/{aid}_info.json'
    path2 = f'test/{aid}_now.json'
    path3 = f'test/{aid}_comment.json'
    path4 = f'test/{mid}_info.json'
    path5 = f'test/{mid}_now.json'
    path6 = f'test/{aid}_danmaku.json'
    path7 = f'test/{mid}_videos.json'
    path8 = f'test/{tid}_zone_info.json'
    path9 = f'test/{aid}_videos_tag.json'
    path10 = f'test/zone.json'
    path11 = f'test/{aid}_video_staff.json'
    # write_json(path1, video.info())
    # write_json(path2,video.now())
    # write_json(path3,video.reply())
    # write_json(path4, user1.info())
    # write_json(path5, user1.now())
    # write_json(path6,video.danmaku())
    write_json(path7, user1.videos())
    # write_json(path8, zone.info())
    # write_json(path9, video.tags_list())
    # write_json(path11, video.staff())
    # uid = uids()
    # get_up_db(uid,10)
    # write_json(path10, video_zone.get_zone_list_sub())
    # dmk()
    # ex()
