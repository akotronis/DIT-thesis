# Commands
## Docker
- Build the image: `../app/front$ docker build -t img-dit-front .[ --no-cache --progress=plain]`
- Run the image: `../app/front$ docker run --name ctr-dit-front -d --rm -v "$(pwd):/opt/front" -p 8501:8501 img-dit-front`

## Streamlit
- Run the app: `/opt/front/dit-app$ steamlit run main.py`

# Resources
## Emojis / Icons
- [Full Emoji List, v16.0 - Unicode](https://unicode.org/emoji/charts/full-emoji-list.html)
- [Emojipedia](https://emojipedia.org/)
- [Google Material Fonts](https://fonts.google.com/icons)
- [Streamlit emoji shortcodes](https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/)
- [Glyphicons (for Folium markers)](https://getbootstrap.com/docs/3.3/components/#glyphicons)

## Streamlit
- [Streamlit login](https://github.com/blackary/streamlit-login/tree/main)
- [Display a race on a live map](https://blog.streamlit.io/display-a-race-on-a-live-map/)
- [Sockets](https://github.com/ash2shukla/streamlit-stream/blob/master/consumer/src/main.py)
- [Streamlit Folium - Dynamic Updates](https://folium.streamlit.app/dynamic_updates)
- [Youtube - Folium + Streamlit - Creating Maps in Streamlit Applications using Folium / Caching in Streamlit](https://www.youtube.com/watch?v=OsGq4LJHOUI)