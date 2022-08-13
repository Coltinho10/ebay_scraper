from bs4 import BeautifulSoup
import requests, json, lxml

headers = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 "
        "Safari/537.36 Edge/18.19582 "
}


def get_organic_results():
    html = requests.get("https://www.ebay.com/sch/i.html?_nkw='nintendo gamecube pokemon xd gale of darkness console'",
                        headers=headers).text
    soup = BeautifulSoup(html, 'lxml')

    data = []

    for item in soup.select('.s-item__wrapper.clearfix'):
        title = item.select_one('.s-item__title').text
        link = item.select_one('.s-item__link')['href']

        # Get condition
        # Can add/remove items in list depending on needs
        try:
            condition = item.select_one('.SECONDARY_INFO').text
            if condition not in ['Used', 'New', 'Brand New', 'Pre-Owned']:
                continue
            else:
                condition = item.select_one('.SECONDARY_INFO').text
        except:
            condition = None

        # Gets shipping cost as "+$xx.xx shipping"
        try:
            shipping = item.select_one('.s-item__logisticsCost').text
        except:
            shipping = None

        # Gets location seller is from
        try:
            location = item.select_one('.s-item__itemLocation').text
        except:
            location = None

        # This needs to be fixed
        try:
            watchers_sold = item.select_one('.NEGATIVE').text
        except:
            watchers_sold = None

        # Boolean depending on Ebay's "best seller" badge
        if item.select_one('.s-item__etrs-badge-seller') is not None:
            top_rated = True
        else:
            top_rated = False

        # Gets bid count
        try:
            bid_count = item.select_one('.s-item__bidCount').text
        except:
            bid_count = None

        # Get bid time remaining if applicable as "7d 6h left"
        try:
            bid_time_left = item.select_one('.s-item__time-left').text
        except:
            bid_time_left = None

        # Gets reviews if applicable
        try:
            reviews = item.select_one('.s-item__reviews-count span').text.split(' ')[0]
        except:
            reviews = None

        # Gets buy now option if applicable as "Buy It Now"
        try:
            extension_buy_now = item.select_one('.s-item__purchase-options-with-icon').text
            if extension_buy_now not in ['Buy It Now','or Best Offer']:
                continue
            else:
                extension_buy_now = item.select_one('.s-item__purchase-options-with-icon').text
        except:
            extension_buy_now = None

        # Price filter
        filter = 150.00
        try:
            price = item.select_one('.s-item__price').text
            price = price.replace("$", "").replace(",", "")
            if float(price) < filter:
                price = item.select_one('.s-item__price').text
            else:
                continue
        except:
            price = None

        data.append({
            'item': {'title': title, 'link': link, 'price': price},
            'condition': condition,
            'top_rated': top_rated,
            'reviews': reviews,
            'watchers_or_sold': watchers_sold,
            'buy_now_extension': extension_buy_now,
            'delivery': {'shipping': shipping, 'location': location},
            'bids': {'count': bid_count, 'time_left': bid_time_left},
        })

    print(json.dumps(data, indent=2, ensure_ascii=False))


get_organic_results()
