from playwright.sync_api import sync_playwright

def wait_elements(page, locators, timeout=4000):
    time = 0
    find_result = False
    while not find_result and time < timeout:
        for i in range(len(locators)):
            try:
                if locators[i].first.is_visible():
                    find_result = True
                    break
            except Exception:
                pass
        time = time + 500
        page.wait_for_timeout(500)

    return find_result


def get_accounts(username, password):
    timeout = 10000
    obj = {}
    try:
        with sync_playwright() as p:
            navigator = p.chromium.launch()
            page = navigator.new_page()
            page.set_default_timeout(timeout)
            page.goto("https://www.bling.com.br/b/login")
            page.locator('#username').click()
            page.locator('#username').fill(username)
            page.locator('#senha').click()
            page.locator('#senha').fill(password)
            page.locator('#login-buttons-site > button').click()
            locLoginFail = page.locator(
                'text=O nome de usuário ou a senha estão incorretos.')

            if wait_elements(page, [locLoginFail]):
                raise Exception('Usuário ou senha do bling estão incorretos')

            page.locator(
                '#menu-novo > ul:nth-child(1) > li:nth-child(5) > a').click()
            page.locator(
                '#menu-novo > ul:nth-child(1) > li:nth-child(5) > ul > li:nth-child(1) > a').click()
            with page.expect_request('**/caixa.server.php?f=listarCaixa') as request:
                data = request.value.response().json()
                obj = {
                    'total_balance': data["totais"]["saldoGeral"],
                    'balances_on_account': data["totais"]["saldosPorConta"]
                }
            print( data["totais"]["saldoGeral"])
        return obj
    except Exception as e:
        raise e
