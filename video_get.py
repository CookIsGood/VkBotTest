import random
import time
from login import id_video_invite


def get(session_api, vk_id_group, vk_id_group_neg, id_video_invite):
    attachment = ''
    # print('Время до получения пикчи ' + str(time.ctime(time.time())))
    videos = session_api.video.get(owner_id=str(vk_id_group), videos=id_video_invite, album_id='wall', count=1,
                                   offset=None)
    # videos = vk_session.method('video.get',
    # {'owner_id': vk_id_group_neg, 'videos': id_video_invite, 'album_id': album_id, 'count': count,
    # 'offset': offset})
    videos_items = videos["items"]
    buf = []
    for item in videos_items:
        buf.append('video' + str(vk_id_group_neg) + '_' + str(item['id']))
    print(buf)
    attachment = ''.join(buf)
    print(type(attachment))
    # print('Время после получения пикчи '+str(time.ctime(time.time())))
    print(attachment)
    return attachment
