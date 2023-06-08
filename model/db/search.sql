#视频简要信息视图
create view video_brief(
        bv,         #视频bv号
        title,      #视频标题
        view,       #视频播放量
        zone,       #视频分区
        up_name     #up主昵称
        ) as
    select 
        video_info.bvid,
        video_info.title,
        video_now.view,
        zone_info.zone_name,
        user_info.name
    from 
        video_info,
        video_now,
        user_info,
        zone_info
        where
            user_info.uid = video_info.uid and
            video_info.tid = zone_info.tid and
            video_info.aid = video_now.aid;
#


#视频全部相关信息视图
create view video_detail(
        aid,            #视频aid
        up_uid,         #UP主uid
        zone_id,        #视频分区tid

        bv,             #视频bv号
        title,          #视频标题
        publish_time,   #发布时间
        introduction,   #简介
        pic_url,        #封面网址

        up_name,        #UP主昵称
        up_face_url,    #UP主头像url
        up_level,       #UP主等级
        up_persign,     #UP主个性签名

        view,           #播放量
        likes,          #获赞数
        coin,           #投币数
        favorite,       #收藏数
        share,          #分享数
        danmaku,        #弹幕量
        comment,        #评论数

        zone_name,      #分区名字
        route,          #子分区路径
        zone_url        #分区url
        ) as
    select
        video_info.aid,
        user_info.uid,
        zone_info.tid,

        video_info.bvid,
        video_info.title,
        video_info.pubtime,
        video_info.introduction,
        video_info.pic_url,

        user_info.name,
        user_info.face_url,
        user_info.level,
        user_info.persign,

        video_now.view,
        video_now.likes,
        video_now.coin,
        video_now.favorite,
        video_now.share,
        video_now.danmaku,
        video_now.comment,

        zone_info.zone_name,
        zone_info.route,
        zone_info.zone_url
    from 
        video_info,
        video_now,
        user_info,
        zone_info
        where
            user_info.uid = video_info.uid and
            video_now.aid = video_info.aid and
            video_info.tid = zone_info.tid;
#

# 用户的全部信息
create view user_detail
    (
        uid,            #用户uid
        name,           #用户昵称
        sex,            #用户性别
        face_url,       #头像url
        persign,        #个性签名
        level,          #用户等级
        official,       #官方认证
        notice,         #公告

        following,      #关注数
        follower,       #粉丝数
        archive,        #视频总播放量
        article,        #专栏总阅读量
        likes           #总获赞数
    ) as
    select
        user_info.uid,
        user_info.name,
        user_info.sex,
        user_info.face_url,
        user_info.persign,
        user_info.level,
        user_info.official,
        user_info.notice,

        user_now.following,
        user_now.follower,
        user_now.archive,
        user_now.article,
        user_now.likes
    from
        user_info,
        user_now
        where
            user_info.uid = user_now.uid;
#


#查询数据库中UP主的发表视频量按数量降序排列
select up_name,count(bv) as video_num 
from video_brief
    group by 
        up_name
    order by 
        count(distinct bv) desc;
#


#查询UP主视频信息（以播放、点赞、时间降序排列）
select 
    bv,
    title,
    publish_time,
    likes,
    view
from video_detail
    where 
        up_name like 'marasy_触手猴'
    /* order by view desc;         #按排放量排序 */
    /* order by likes desc;        #按获赞数排序 */
    order by publish_time desc; #按发布时间排序
#


# 查询目标视频的评论内容(by aid)
select
    user_info.name      as  commenter,      #评论者昵称
    user_info.uid       as  commenter_uid,  #评论者uid
    comment.rptime      as  rptime,         #评论时间
    comment.rcount      as  rcount,         #回复数
    comment.likes       as  likes,          #获赞数
    comment.message     as  message         #评论内容
from
    user_info,
    comment
    where
        user_info.uid = comment.uid and
        comment.aid = 731493438
    /* order by comment.likes desc;    #按获赞数排列 */
    order by comment.rptime desc;   #按回复时间数排列
#


# 查询目标视频的弹幕内容(by aid)
select
    danmaku.dm_time     as  point_time,     #弹幕时间点
    danmaku.send_time   as  send_time,      #发送时间
    danmaku_mode.prompt as  type,           #弹幕类型
    danmaku.content     as  content         #弹幕内容
from
    danmaku,
    danmaku_mode
    where
        danmaku.mode = danmaku_mode.mode and
        danmaku.aid = 731493438
    order by danmaku.dm_time;
#


# 查询注销账户的用户数量
select count(*) from user_info
where name like "账户已注销";


# 查询视频的合作投稿情况（bvid查询）
select
    user_info.uid       as  uid,         #协作者uid
    user_info.name      as  name,        #协作者昵称
    staff.division      as  division     #协作者分工
from
    user_info,
    staff,
    video_info
    where
        user_info.uid = staff.uid  and
        staff.aid = video_info.aid and
        video_info.bvid like "BV1t84y1e7Cg";
#


# 查询UP主的协作投稿情况（按昵称查询）自链接
select
    video_info.bvid     as  bv,             #视频bv   
    video_info.title    as  title,          #视频标题
    owner.name          as  video_owner,    #视频所有者
    staff.division      as  division        #所担任的分工
from
    video_info,
    user_info owner,
    user_info helper,
    staff
    where
        owner.uid = video_info.uid  and
        helper.uid = staff.uid      and
        video_info.aid = staff.aid  and
        helper.name like "香椎モイミ";
#

# 查询各分区（播放|获赞|弹幕|）最高的视频相关信息
select 
    zone_info.zone_name   as  zone,         #分区
    a.bvid                as  bv,           #最高视频bv
    user_info.name        as  owner,        #最高视频UP
    b.view                as  view,         #播放量
    b.likes               as  likes,        #获赞数
    b.danmaku             as  danmaku       #弹幕量
from 
    video_info a,
    video_now b,
    zone_info,
    user_info
    where 
        /* b.view in */
        /* b.likes in */
        b.danmaku in
        (
            select 
                /* max(video_now.view)  */
                /* max(video_now.likes)  */
                max(video_now.danmaku) 
            from 
                video_now,video_info
                where 
                    video_info.aid = video_now.aid
                group by 
                    video_info.tid
        )   and
        a.aid = b.aid and
        a.uid = user_info.uid and
        a.tid = zone_info.tid
    /* order by b.view desc; */
    /* order by b.likes desc; */
    order by b.danmaku desc;
#
