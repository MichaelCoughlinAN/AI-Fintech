import asyncio
from pytrends.request import TrendReq
import openai
import config as config


async def generate_ai_notes(stocks):
    try:
        openai.api_key = config.ai_key
        message = f"As a seasoned quantitative analyst, provide an analysis on top stocks: {str(stocks)}"
        # print(message)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message}
            ]
        )

        return safeguard_response(response.choices[0].message.content.strip())
    except Exception as e:
        print(e)


def safeguard_response(response):
    # Implement any necessary checks or modifications to the OpenAI response
    return response


async def get_google_trends():
    trending_terms = TrendReq(hl='en-US', tz=360)
    keywords = ['share price', 'stock price']

    trending_terms.build_payload(
        kw_list=keywords,
        cat=0,
        timeframe='now 1-H',
        geo='US',
        gprop=''
    )

    # term_interest_over_time = trending_terms.interest_over_time()
    related_queries = trending_terms.related_queries()

    # Code for cleaning related queries to find top searched queries and rising queries
    top_queries = []
    rising_queries = []

    for key, value in related_queries.items():
        for k1, v1 in value.items():
            if k1 == "top":
                top_queries.append(v1)
            elif k1 == "rising":
                rising_queries.append(v1)

    print(top_queries)
    print(rising_queries)

    # Safely printing top and rising queries
    # for top_query in top_queries:
    #     print(pd.DataFrame(top_query))

    # for rising_query in rising_queries:
    #     print(pd.DataFrame(rising_query))

    print(await generate_ai_notes(top_queries))


def main():
    asyncio.run(get_google_trends())


if __name__ == "__main__":
    main()