from pyppeteer import launch
import asyncio
import os
import sys

async def visit(url):
    admin_token = os.getenv('TOKEN','f50102afcb3a42518cbb1eaac1cbaa52')
    print("Visiting", url)
    try:
        browser = await launch({'args': ['--no-sandbox', '--disable-setuid-sandbox']})
        page = await browser.newPage()
        await page.goto('http://localhost:5000/login',options={"timeout":10000,'waitUntil' : 'domcontentloaded'})
        await asyncio.sleep(3)
        await page.type('#username', 'admin')
        await page.type('#password', admin_token)
        await page.click('#login')
        await asyncio.sleep(3)
        await page.goto(url,options={"timeout":10000,'waitUntil' : 'domcontentloaded'})
        await asyncio.sleep(3)
        await browser.close()
    except Exception as e:
        print(e)
        await browser.close()
        return
if __name__=='__main__':
    asyncio.run(visit(sys.argv[1]))