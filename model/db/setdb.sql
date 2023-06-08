#drop database mybilibili2;

#建立数据库
create database mybilibili2;
use mybilibili2;

#建立基本表
create table user_info #用户基本信息
    (
        uid bigint not null,
        name tinytext not null,
        sex text(4),
        face_url text,
        persign text,
        level tinyint,
        official text,
        notice text,
        primary key(uid)
    )charset=utf8mb4;

create table user_now       #用户实时信息
    (
        uid bigint not null,
        following smallint not null,
        follower int not null,
        archive bigint not null,
        article int not null,
        likes int not null,
        primary key(uid)
    )charset=utf8mb4;
 
create table video_info       #视频信息
    (
        bvid char(20) not null,
        aid int not null,
        tid smallint not null,
        title tinytext not null,
        pubtime datetime not null,
        introduction mediumtext not null,
        uid bigint not null,
        pic_url text not null,
        primary key(aid,bvid,uid)
    )charset=utf8mb4;

create table video_now      #视频实时信息
    (
        aid int not null,
        bvid char(20) not null,
        view int not null,
        danmaku smallint not null,
        comment mediumint not null,
        favorite mediumint not null,
        coin mediumint not null,
        share mediumint not null,
        likes mediumint not null,
        primary key(aid,bvid)
    )charset=utf8mb4;

create table comment        #评论信息
    (
        rpid bigint not null,
        aid int not null,
        uid bigint not null,
        rptime datetime not null,
        likes mediumint not null,
        rcount smallint not null,
        message mediumtext not null,
        primary key(rpid)
    )charset=utf8mb4;

create table danmaku       #弹幕信息
    (
        aid int not null,
        did bigint not null,
        content text not null,
        dm_time float(3) not null,
        send_time datetime not null,
        crc32_id char(8) not null,
        mode tinyint not null,
        primary key(did)
    )charset=utf8mb4;

create table zone_info
    (
        tid int not null,
        zone_name  tinytext not null,
        route tinytext not null,
        zone_url text not null,
        primary key(tid)
    )charset=utf8mb4;

create table danmaku_mode
    (
        mode tinyint not null,
        name char(7) not null,
        prompt char(12) not null,
        primary key(mode)
    )charset=utf8mb4;

create table staff
    (
        aid int not null,
        uid bigint not null,
        division char(24)
    )charset=utf8mb4;

insert into danmaku_mode(mode,name,prompt)
values (1,"FLY","飞行弹幕"),
(5,"TOP","顶部弹幕"),
(4,"BOTTOM","底部弹幕"),
(6,"REVERSE","反向弹幕"),
(7,"SPECIAL","高级弹幕");
