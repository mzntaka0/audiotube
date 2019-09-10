<img src=https://github.com/mzntaka0/audiotube/blob/master/docs/_static/audiotube_literal.png width=60%>

Helpful tool for getting YouTube information using Python!
You can do:

  - search YouTube
  - get information of videos
  - get transcription of video


### Installation
#### using setup.py
```
python setup.py install
```

#### using pip
```
pip install audiotube
```

### Usage
```
import audiotube

youtube = audiotube.YouTube()
results = youtube.search('palo alto', search_num=10)
print(results)
# [<YouTube Videos> Num: 10 [<Object: YouTubeAudio, url: https://www.youtube.com/watch?v=wr691AYEu4A>, <Object: YouTubeAudio, url: https://www.youtube.com/watch?v=Dmg-HU-kbV0>, <Object: YouTubeAudio, url: https://www.youtube.com/watch?v=sTqMUu1iTIo>, <Object: YouTubeAudio, url: https://www.youtube.com/watch?v=5G2a93C8pPM>, <Object: YouTubeAudio, url: https://www.youtube.com/watch?v=yuT5IzuXgBw>, <Object: YouTubeAudio, url: https://www.youtube.com/watch?v=Q1Wm0_fOON4>, <Object: YouTubeAudio, url: https://www.youtube.com/watch?v=c-oIfq5mw_g>, <Object: YouTubeAudio, url: https://www.youtube.com/watch?v=xomlcQrefZ8>, <Object: YouTubeAudio, url: https://www.youtube.com/watch?v=N8h34bbQ_2s>, <Object: YouTubeAudio, url: https://www.youtube.com/watch?v=3wKwHX54P9s>] 

print(type(results))  # <class 'audiotube.objects.YouTubeAudios'>
print(type(results[0]))  # <class 'audiotube.objects.YouTubeAudio'>

print(results[1].transcription)
# [{'text': 'ah', 'start': 0.0, 'duration': 2.0}, {'text': 'you', 'start': 4.69, 'duration': 2.06}, {'text': "there's a lot of great attractions in", 'start'$ 12.82, 'duration': 4.39}, {'text': 'San Francisco alone but at the same time', 'start': 15.02, 'duration': 4.17}, {'text': 'there is a lot of different pl$ces you', 'start': 17.21, 'duration': 3.12}, {'text': 'can check out throughout the San', 'start': 19.19, 'duration': 4.35}, {'text': 'Francisco Bay region one of them is Palo', 'start': 20.33, 'duration': 6.21}, {'text': 'Alto California welcome this is Scott', 'start': 23.54, 'duration': 7.91}, {'text': "and we're live here in front of", 'start': 26.54, 'duration': 4.91}, {'text': "Rinconada Park we're at the Embarcadero", 'start': 32.17, 'duration': 6.01}, {'t$xt': 'Road not be confused with the one in', 'start': 36.2, 'duration': 4.98}, {'text': 'downtown San Francisco and then middle', 'start': 38.18, 'duration': 4.8}, {'text': 'field roads over at that light over', 'start': 41.18, 'duration': 6.45},
```
