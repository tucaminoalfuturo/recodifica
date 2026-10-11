"""Check direct welcome routing, local assets, responsive layout and WhatsApp.

Run: python3 tools/check_welcome.py --screenshots /tmp/recodifica-welcome
External WhatsApp navigation is intercepted; no messages or payments are sent.
"""
from argparse import ArgumentParser
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
import json
from playwright.sync_api import sync_playwright
from check_landing import ROOT, server, require

MESSAGE = ('Hola Seba, acabo de realizar mi compra del entrenamiento Recodificá tu Reactividad por PayPal\n\n'
           'Mi nombre es:\n\n'
           'El plan que elegí es: Básico / VIP\n\n'
           'Te comparto mi comprobante de pago para coordinar mi ingreso al entrenamiento\n\n'
           '¡Muchas gracias!')


def check_link(page):
    button = page.locator('#welcome-whatsapp')
    parsed = urlsplit(button.get_attribute('href'))
    require(parsed.scheme == 'https' and parsed.netloc == 'wa.me', 'WhatsApp HTTPS destination')
    require(parsed.path == '/59897988262', 'Same existing phone number as the landing')
    require(parse_qs(parsed.query) == {'text': [MESSAGE]}, 'Exact editable message with blank name and both plans')
    require(button.get_attribute('rel') == 'noopener noreferrer', 'Safe external tab')
    return button


def check_navigation(page):
    # Verify click/Enter opens the intended target; do not send a real message.
    page.context.route('https://wa.me/**', lambda route: route.fulfill(status=200, content_type='text/html', body='<p>Navigation intercepted for verification</p>'))
    button = check_link(page)
    button.focus()
    require(button.evaluate('(e) => e === document.activeElement'), 'CTA reachable by keyboard')
    require(button.evaluate('(e) => getComputedStyle(e).outlineStyle') != 'none', 'Visible keyboard focus')
    with page.expect_popup() as opened:
        page.keyboard.press('Enter')
    popup = opened.value
    popup.wait_for_load_state()
    require(parse_qs(urlsplit(popup.url).query)['text'][0] == MESSAGE, 'Keyboard opens WhatsApp with the right message')
    popup.close()


def main():
    parser = ArgumentParser()
    parser.add_argument('--screenshots', type=Path)
    args = parser.parse_args()
    if args.screenshots:
        args.screenshots.mkdir(parents=True, exist_ok=True)
    config = json.loads((ROOT/'Mi-web/vercel.json').read_text())
    require({'source': '/bienvenida', 'destination': '/bienvenida/index.html'} in config['rewrites'], 'Explicit clean Vercel route')
    require((ROOT/'Mi-web/bienvenida/index.html').is_file(), 'Route target included in existing publication directory')
    results = []
    with server() as url, sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path='/usr/bin/chromium')
        for width in [360,390,430,768,1440]:
            page = browser.new_page(viewport={'width':width, 'height':900})
            errors, bad_assets = [], []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.on('response', lambda response: bad_assets.append(response.url) if response.url.startswith(url) and response.status >= 400 else None)
            response = page.goto(url+'/bienvenida', wait_until='networkidle')
            require(response.status == 200, 'Direct clean route loads without 404')
            page.evaluate('document.fonts.ready')
            require(not bad_assets, f'All local styles, scripts and fonts load: {bad_assets}')
            require(page.locator('h1').count() == 1 and page.locator('h1').inner_text() == '¡Bienvenida a esta nueva etapa!', 'One welcome heading')
            require(page.locator('.welcome-steps li').count() == 3, 'Three clearly ordered steps')
            require('Una vez verificado tu pago' in page.locator('.welcome-steps').inner_text(), 'Access follows manual payment verification')
            require(page.locator('nav, form, wistia-player, [href*="paypal.com"], [href*="t.me"]').count() == 0, 'Focused welcome without selling, forms, player or automatic access')
            require(page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'No horizontal overflow at {width}px')
            require(page.evaluate('document.fonts.check("600 16px Montserrat") && [...document.fonts].some(f => f.family === "Montserrat" && f.status === "loaded")'), 'Local Montserrat actually loaded')
            require(page.locator('body').evaluate('(e) => getComputedStyle(e).fontFamily').startswith('Montserrat'), 'Brand typography applied')
            rect = page.locator('#welcome-whatsapp').bounding_box()
            require(rect['height'] >= 48 and rect['x'] >= 0 and rect['x'] + rect['width'] <= width, 'Comfortable CTA inside viewport')
            size = page.locator('h1').evaluate('(e) => parseFloat(getComputedStyle(e).fontSize)')
            require((28 <= size <= 34) if width < 768 else (38 <= size <= 46), 'Responsive title size')
            check_navigation(page)
            require(not errors, f'No JavaScript exceptions: {errors}')
            if args.screenshots:
                page.locator('h1').click()
                page.screenshot(path=str(args.screenshots/f'bienvenida-{width}.png'), full_page=True)
            page.close()
            results.append(f'PASS welcome {width}px: direct URL, assets/font, content, layout, keyboard and WhatsApp target')
        for mode in ['no-js', 'blocked-config', 'blocked-script', 'reduced-motion']:
            page = browser.new_page(java_script_enabled=mode != 'no-js', reduced_motion='reduce' if mode == 'reduced-motion' else 'no-preference', viewport={'width':390,'height':844})
            if mode.startswith('blocked-'):
                pattern = '**/config.js*' if mode == 'blocked-config' else '**/bienvenida/script.js'
                page.route(pattern, lambda route: route.abort('blockedbyclient'))
            page.goto(url+'/bienvenida/?plan=VIP&payment=confirmed&name=Inventado', wait_until='networkidle')
            check_link(page)
            require(page.locator('h1').is_visible() and page.locator('.welcome-steps').is_visible(), 'Fallback content stays visible')
            require('Inventado' not in page.locator('body').inner_text(), 'URL parameters never infer name, plan or payment status')
            require(page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Fallback layout has no horizontal overflow')
            if mode == 'reduced-motion':
                require(page.evaluate('document.getAnimations().length == 0'), 'No animations under reduced motion')
            page.close()
            results.append(f'PASS welcome {mode}: usable CTA, visible content and no URL-based payment confirmation')
        browser.close()
    for result in results:
        print(result)
    print('NOT RUN: actual WhatsApp application/message delivery, live Vercel deployment or any payment transaction.')
    if args.screenshots:
        (args.screenshots/'welcome-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')

if __name__ == '__main__':
    main()
