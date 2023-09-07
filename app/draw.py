import uuid
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os


def draw_weather(weather_day: list):
    list_image = []
    font = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf', size=24)
    path_weather = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..", "weather_icon"))
    name_dir = str(uuid.uuid4())
    os.makedirs(os.path.join(path_weather, name_dir))
    if len(weather_day) % 2 != 0:
        count = len(weather_day) + 1
    else:
        count = len(weather_day)
    for part_day in range(0, count, 2):
        image_fon = Image.open(os.path.join(path_weather, 'fon_weather1.jpg'))
        back_im = image_fon.copy()

        for i in range(0, 400, 200):
            count_of_list = int(i / 200 + part_day)
            if count_of_list >= len(weather_day):
                break
            png_ico_path = weather_day[count_of_list]['condition']['icon'].split("/")
            image_00 = Image.open(os.path.join(path_weather, '64x64', png_ico_path[-2], png_ico_path[-1]))
            back_im.paste(image_00, (65 + i, 50), image_00)
            draw_text = ImageDraw.Draw(back_im)
            draw_text.text((30 + i, 10), f"Время: {weather_day[count_of_list]['time'].split(' ')[-1]}",
                           font=font, fill=('#1C0606'))
            if weather_day[count_of_list]['chance_of_snow'] > 0 or weather_day[count_of_list]['chance_of_rain'] > 0:
                if weather_day[count_of_list]['chance_of_snow'] > weather_day[count_of_list]['chance_of_rain']:
                    draw_text.text((30 + i, 35), f"Осадки: {weather_day[count_of_list]['chance_of_snow']} %",
                                   font=font, fill=('#1C0606'))
                else:
                    draw_text.text((30 + i, 35), f"Осадки: {weather_day[count_of_list]['chance_of_rain']} %",
                                   font=font, fill=('#1C0606'))
            draw_text.text((60 + i, 110), f"t: {weather_day[count_of_list]['temp_c']} C", font=font, fill=('#1C0606'))
            image_00.close()
        # back_im.save(os.path.join(path_weather, name_dir, f'fon_weather_new_{part_day}.jpg'), quality=95)
        image_stream = BytesIO()
        back_im.save(image_stream, 'JPEG')
        image_stream.seek(0)
        bytes_image = image_stream.read()
        list_image.append(bytes_image)
        back_im.close()
        image_fon.close()
    # return os.path.join(path_weather, name_dir)
    return list_image



