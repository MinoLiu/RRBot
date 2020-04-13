from app.utils import aobject
from pyppeteer import launch


class Browser(aobject):

    async def __init__(self, headless=True, proxy=None):
        self.browser = await launch({'headless': headless, 'args': [proxy] if proxy else []})
        self.page = (await self.browser.pages())[0]

    def set_default_navigation_timeout(self, ms):
        self.page.setDefaultNavigationTimeout(ms)

    async def goto(self, uri: str, options: dict = None, **kwargs):
        await self.page.goto(uri, options, **kwargs)

    async def reload(self, options: dict = None, **kwargs):
        await self.page.reload(options, **kwargs)

    async def cookies(self, *args):
        return await self.page.cookies(*args)

    async def set_cookie(self, cookie):
        await self.page.setCookie(cookie)

    async def new_page(self):
        self.page = await self.browser.newPage()

    async def switch_page(self, num=0):
        self.page = (await self.browser.pages())[num]

    async def evaluate(self, js: str):
        return await self.page.evaluate(js)

    async def close(self):
        await self.page.close()

    async def quit(self):
        await self.browser.close()

    async def screenshot(self, path: str):
        await self.page.screenshot({'path': path})

    async def query_selector(self, selector: str):
        return await self.page.querySelector(selector)

    async def query_selector_all(self, selector: str):
        return await self.page.querySelectorAll(selector)

    async def query_selector_all_eval(self, selector: str, pageFunction: str, *args):
        return await self.page.querySelectorAllEval(selector, pageFunction, *args)

    async def query_selector_eval(self, selector: str, pageFunction: str, *args):
        return await self.page.querySelectorEval(selector, pageFunction, *args)

    async def click(self, selector: str, options: dict = None, **kwargs):
        """
        Click element which matches selector.

        This method fetches an element with selector, scrolls it into view if needed, and then uses mouse to click in
        the center of the element. If there's no element matching selector, the method raises PageError.
        Available options are:
            button (str): left, right, or middle, defaults to left.
            clickCount (int): defaults to 1.
            delay (int|float): Time to wait between mousedown and mouseup in milliseconds. defaults to 0.
        """
        return await self.page.click(selector, options, **kwargs)

    async def type(self, selector: str, text: str, options: dict = None, **kwargs):
        """
        Type text on the element which matches selector.

        If no element matched the selector, raise PageError.
        """
        await self.page.type(selector, text, options, **kwargs)

    async def clear(self, selector: str):
        await self.page.querySelectorEval(selector, "el => el.value = '' ")

    async def content(self):
        return await self.page.content()

    async def wait_for(self, selectorOrFunctionOrTimeout, options: dict = None, *args, **kwargs):
        return await self.page.waitFor(selectorOrFunctionOrTimeout, options, *args, **kwargs)

    async def wait_for_response(self, urlOrPredicate, options: dict = None, **kwargs):
        return await self.page.waitForResponse(urlOrPredicate, options, **kwargs)

    async def wait_for_navigation(self, options: dict = None, **kwargs):
        await self.page.waitForNavigation(options, **kwargs)
