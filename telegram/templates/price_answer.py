import json
import textwrap


def get_price_answer_auto(price_info, json_response):
    model = (json_response['general']["searchResults"][0]["manufacturer"]
             + json_response['general']["searchResults"][0]["model"]
             + json_response['general']["searchResults"][0]["badge"]
    )
    release_date = str(json_response['general']["searchResults"][0]["year"])
    year, month = int(release_date[:4]), int(release_date[4:])
    mileage = json_response['general']["searchResults"][0]["mileage"]
    price_with_delivery_and_our_tax = price_info["car_rub_price"] + price_info["our_tax"] + price_info["korean_expenses"]

    return textwrap.dedent(f"""
    🚗 Модель: <b>{model}</b>  
    📆 Дата производства: <b>{month}.{year}</b>
    🏁 Пробег: <b>{mileage} км</b>

    <b>В цену включены:</b>  
    - Стоимость авто в Корее c доставкой до Владивостока: <b>{price_with_delivery_and_our_tax} ₽ </b> 
    - Таможенное оформление: <b>{price_info["tax_price"]} ₽ </b> 
    - Брокерские услуги(ЭПТС, СБКТС, СВХ): <b>{price_info["broker"]} ₽  </b>
    - Утилизационный сбор:<b> {price_info["util_price"]} ₽ </b>

    💰 <u>Cтоимость под ключ:</u> <b>{price_info["price"] - 250000} ₽</b>  

    💢 <b>Стоимость авто с прямой таможней на РФ/утилем и всеми необходимыми документами</b> до Владивостока 

    🚛 Доставка до Вашего города рассчитывается логистами индивидуально, в среднем это: Москва/Ростов-на-Дону/Краснодар от <b>180</b> до <b>250</b> тыс ₽  

    📞 <b>Контакт менеджера:</b> +79185439569  
        """)


def get_price_answer_manual(price_info):
    price_with_delivery_and_our_tax = price_info["car_rub_price"] + price_info["our_tax"] + price_info["korean_expenses"]
    return textwrap.dedent(f"""
        <b>В цену включены:</b>  
        - Стоимость авто в Корее c доставкой до Владивостока: <b>{price_with_delivery_and_our_tax} ₽ </b> 
        - Таможенное оформление: <b>{price_info["tax_price"]} ₽ </b> 
        - Брокерские услуги(ЭПТС, СБКТС, СВХ): <b>{price_info["broker"]} ₽  </b>
        - Утилизационный сбор:<b> {price_info["util_price"]} ₽ </b>

        💰 <u>Cтоимость под ключ:</u> <b>{price_info["price"] - 250000} ₽</b>  

        💢 <b>Стоимость авто с прямой таможней на РФ/утилем и всеми необходимыми документами</b> до Владивостока 

        🚛 Доставка до Вашего города рассчитывается логистами индивидуально, в среднем это: Москва/Ростов-на-Дону/Краснодар от <b>180</b> до <b>250</b> тыс ₽  

        📞 <b>Контакт менеджера:</b> +79185439569  
            """)


def get_hello_message():
    return textwrap.dedent("""
    Спасибо за выбор <b>CheckPointAuto</b>!
    Этот бот поможет вам рассчитать стоимость авто из Кореи под ключ!
    Доступно два варианта рассчета:
    """)