from module.network import VIDEO, USER, ZONE
from module.tool import read_json, write_json, log
from module.dbcontrol import database
import time


def get_up_db(lst, num):
    db = database('mybilibili2')
    i = 1
    for mid in lst:
        log1 = log(mid)
        user = USER(mid)
        db.insert('user_info', [user.info()])
        db.insert('user_now', [user.now()])
        log1.over_p3('OK')
        print(f'part4:{i}/{num} is {mid} finish')
        if i % 300 == 0:
            print('sleep one min')
            time.sleep(60)
        i += 1

    db.close()
    print('OK!!!!!')
    return 0


def get_zone_db(lst, num):
    db = database('mybilibili2')
    i = 1
    for tid in lst:
        zone = ZONE(tid=tid)
        db.insert('zone_info', [zone.info()])
        print(f'part3:{i}/{num} is {tid} finish')
        if i % 300 == 0:
            print('sleep one min')
            time.sleep(60)
        i += 1

    db.close()


def get_video_db(lst, num):
    db = database('mybilibili2')
    info = list()
    now = list()
    userlist = list()
    zonelist = list()
    i = 1
    for aid in lst:
        log1 = log(aid)
        video = VIDEO(aid)
        video_info = video.info()
        if not video_info:
            log1.over_p2('error')
            print(f"part2:{i}/{num} {aid} is error")
            i += 1
            continue
        info.append(video_info)
        zonelist.append(video_info['tid'])
        userlist.extend([stf['uid'] for stf in video.staff()])  #添加制作人

        now.append(video.now())

        #插入弹幕信息
        db.insert('danmaku', video.danmaku())
        #插入评论信息
        data_comment = video.reply()
        db.insert('comment', data_comment)
        #插入制作人信息
        if len(video._staff) > 1:
            db.insert('staff', video._staff[1:])

        userlist.extend([d["uid"] for d in data_comment])

        log1.over_p2('OK')
        print(f"part2:{i}/{num} {aid} is finish")

        if i % 300 == 0:
            print('sleep one min')
            time.sleep(60)
        i += 1

    db.insert('video_info', info)
    db.insert('video_now', now)
    db.close()
    return userlist, zonelist


def setdata(uid_list):
    video_list = list()
    i = 1
    num = len(uid_list)
    for mid in uid_list:
        user = USER(mid)
        video_list.extend(user.videos())

        print(f"part1:{i}/{num} {mid} is finish")
        i += 1
        if i % 300 == 0:
            print('sleep one min')
            time.sleep(60)

    video_list = list(set(video_list))
    count_video = len(video_list)
    print(f'共{count_video}条视频信息')

    print('sleep one min')
    # time.sleep(30)

    uids, zones = get_video_db(video_list, count_video)
    #用户去重
    uids.extend(uid_list)
    uids = list(set(uids))
    #标签去重
    zones = list(set(zones))

    print('sleep one min')
    # time.sleep(30)

    count_zone = len(zones)
    print(f'共{count_zone}条分区信息')
    get_zone_db(zones, count_zone)

    print('sleep one min')
    # time.sleep(30)

    count_user = len(uids)
    print(f'共{count_user}条用户信息')
    get_up_db(uids, count_user)


def updata():
    pass


if __name__ == "__main__":
    bv = 'BV1BP41127sr'
    mid = 627704742
    video = VIDEO(bv)
    user1 = USER(mid)
    path1 = f'test/{bv}_info.json'
    path2 = f'test/{bv}_now.json'
    path3 = f'test/{bv}_comment.json'
    path4 = f'test/{mid}_info.json'
    path5 = f'test/{mid}_now.json'
    path6 = f'test/{bv}_danmaku.json'
    path7 = f'test/{mid}_videos.json'
    #write_json(path1,video.info())
    #write_json(path2,video.now())
    #write_json(path3,video.reply())
    #write_json(path4,user1.info())
    write_json(path5, user1.now())
    #write_json(path6,video.danmaku())
    #write_json(path7,user1.videos())
