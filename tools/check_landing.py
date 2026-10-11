"""Browser regression checks for the static landing. No checkout or payment requests.

Run: python3 tools/check_landing.py --screenshots /tmp/recodifica-review
Requires Python Playwright and Chromium (the prepared cloud environment has both).
External Wistia requests are intentionally blocked to test its failure state;
actual playback and PayPal checkout totals require a separate network-enabled review.
"""
from argparse import ArgumentParser
from contextlib import contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import urlsplit, parse_qs
import json
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'Mi-web'
H1 = 'Tus hijos no necesitan que seas una madre perfecta. Necesitan que dejes de luchar con tu propia historia.'

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass

@contextmanager
def server():
    service = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(SITE)))
    worker = Thread(target=service.serve_forever, daemon=True)
    worker.start()
    try:
        yield f'http://127.0.0.1:{service.server_port}'
    finally:
        service.shutdown()
        service.server_close()
        worker.join()

def require(condition, message):
    if not condition:
        raise AssertionError(message)

def ready(page, url):
    page.route('https://fast.wistia.com/**', lambda route: route.abort('blockedbyclient'))
    response = page.goto(url, wait_until='networkidle')
    require(response.status == 200, 'Landing must load successfully')
    page.evaluate('document.fonts.ready')

def check_content(page):
    require(page.locator('h1').count() == 1, 'Exactly one h1')
    require(page.locator('h1').inner_text() == H1, 'Approved hero copy')
    require(page.locator('.resources article').count() == 5, 'Five common resources')
    require(page.locator('.stage-card').count() == 3, 'Three visible stages')
    require(page.locator('.testimonial-card').count() == 5, 'Five authentic excerpts')
    require(page.locator('.capture-button').count() == 5, 'Five supplied captures')
    for index, image in enumerate(page.locator('.capture-button img').all(), 1):
        require(image.get_attribute('src') == f'assets/testimonios/testimonio-{index}.jpg', 'Correct real screenshot route')
        image.scroll_into_view_if_needed()
        image.evaluate('(e) => e.decode()')
        require(image.evaluate('(e) => e.naturalWidth === Number(e.getAttribute("width")) && e.naturalHeight === Number(e.getAttribute("height"))'), 'Actual screenshot dimensions match metadata')
    require(page.locator('.concept-illustration').count() == 2, 'Two supplied illustrations')
    for image in page.locator('.concept-illustration img').all():
        image.scroll_into_view_if_needed()
        image.evaluate('(e) => e.decode()')
        require(image.evaluate('(e) => e.naturalWidth > 0 && e.currentSrc.endsWith(".webp")'), 'Optimized illustration loads')
    require('buscaste acompañamiento' in page.locator('.objection').inner_text(), 'Concise approved objection copy')
    require('podrás seguir aplicando de manera autónoma' in page.locator('.practice-bridge').inner_text(), 'Concise autonomy bridge')
    require(page.locator('.plan-price').all_inner_texts() == ['USD 50', 'USD 100'], 'Correct visible plan prices')
    require(page.locator('#edition-date').get_attribute('datetime') == '2026-10-14', 'Correct edition date')
    require('Hawkins' in page.locator('.foundation').inner_text(), 'Foundation attribution')
    require(page.locator('body').inner_text().count('Hawkins') == 1, 'One Hawkins mention')
    require('Identidad Creadora' in page.locator('.stages').inner_text(), 'Distinctive method content preserved')
    require(page.locator('main > section').evaluate_all('(els) => els[0].id === "hero" && els[1].id === "video-entrenamiento"'), 'Video immediately follows hero')
    for selector, suffix in [('#paypal-basic', 'J62F4J94WSUUS'), ('#paypal-vip', 'KCD2MNCN69K6C')]:
        link = page.locator(selector)
        require(link.get_attribute('href') == f'https://www.paypal.com/ncp/payment/{suffix}', 'User-supplied PayPal destination')
        require('noopener' in link.get_attribute('rel') and 'noreferrer' in link.get_attribute('rel'), 'Safe external payment links')
    for href in page.locator('[data-whatsapp]').evaluate_all('(els) => els.map(e => e.href)'):
        link = urlsplit(href)
        require(link.netloc == 'wa.me' and link.path == '/59897988262', 'Existing WhatsApp number')
        require(parse_qs(link.query)['text'][0] == 'Hola, quiero consultar por otro medio de pago para Recodificá tu Reactividad', 'WhatsApp prefilled message')
    require(page.locator('wistia-player').get_attribute('media-id') == 'ruy9yzgati', 'Real Wistia media ID')
    require(page.locator('wistia-player').get_attribute('auto-play') == 'false', 'No video autoplay')
    require(page.locator('script[src*="player.js"]').count() <= 1, 'No duplicate Wistia SDK')
    require(page.locator('script[src*="embed/ruy9yzgati.js"]').count() <= 1, 'No duplicate media embed')
    for href in page.locator('a[href^="#"]').evaluate_all('(els) => els.map(e => e.getAttribute("href"))'):
        require(page.locator(href).count() == 1, 'Internal anchor target exists: ' + href)


def check_interactions(page):
    page.evaluate('window.scrollTo({top:0,behavior:"instant"})')
    page.locator('#hero-cta').click()
    page.wait_for_function('Math.abs(document.getElementById("video-entrenamiento").getBoundingClientRect().top - 24) < 4')
    require(page.url.endswith('#video-entrenamiento'), 'Native anchor hash preserved')
    frame = page.locator('.video-frame').bounding_box()
    require(abs(frame['width'] / frame['height'] - 16 / 9) < .01, 'Reserved 16:9 video frame')
    page.locator('#video-error').wait_for(state='visible')
    require(page.locator('script[src="https://fast.wistia.com/player.js"]').count() == 1, 'Official Wistia SDK loaded once')
    require(page.locator('script[src="https://fast.wistia.com/embed/ruy9yzgati.js"]').count() == 1, 'Supplied media script loaded once')
    vip = page.locator('.vip-details')
    require(not vip.evaluate('(e) => e.open'), 'VIP detail closed by default')
    vip.locator('summary').focus()
    page.keyboard.press('Enter')
    require(vip.evaluate('(e) => e.open'), 'VIP keyboard expansion')
    require('tres días siguientes' in vip.inner_text(), 'VIP follow-up content present')
    page.keyboard.press('Enter')
    require(not vip.evaluate('(e) => e.open'), 'VIP keyboard collapse')
    questions = page.locator('.accordion summary')
    questions.nth(0).focus()
    page.keyboard.press('Enter')
    require(page.locator('.accordion details[open]').count() == 1, 'FAQ keyboard opens')
    questions.nth(1).click()
    require(page.locator('.accordion details[open]').count() == 1, 'Only one FAQ open')
    require(page.locator('.accordion details').nth(1).evaluate('(e) => e.open'), 'Second FAQ has focus/state')
    track = page.locator('#testimonials-track')
    track.scroll_into_view_if_needed()
    track.evaluate('(e) => e.scrollTo({left:0,behavior:"instant"})')
    page.wait_for_function('document.getElementById("testimonials-track").scrollLeft < 5')
    track.focus()
    before = track.evaluate('(e) => e.scrollLeft')
    page.keyboard.press('ArrowRight')
    page.wait_for_function('document.getElementById("testimonials-track").scrollLeft > 50')
    require(track.evaluate('(e) => e.scrollLeft') > before, 'Keyboard moves manual carousel')
    page.locator('#testimonials-prev').click()
    page.wait_for_function('document.getElementById("testimonials-track").scrollLeft < 5')
    page.locator('#testimonials-next').click()
    page.wait_for_function('document.getElementById("testimonials-track").scrollLeft > 50')
    page.evaluate('document.getElementById("testimonials-track").scrollTo({left:100000,behavior:"instant"})')
    page.wait_for_function('document.getElementById("testimonials-next").disabled')


def check_layout(page, width):
    require(page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'No horizontal overflow at {width}')
    require(page.evaluate('document.fonts.check("600 16px Montserrat")'), 'Local Montserrat loaded')
    require(page.locator('.hero-photo img').evaluate('(e) => e.complete && e.naturalWidth > 0'), 'Original optimized hero loads')
    for rect in page.locator('.button, .icon-button, summary').evaluate_all('(els) => els.map(e => ({...e.getBoundingClientRect().toJSON(), visible: !!e.getClientRects().length}))'):
        if rect['visible']:
            require(rect['height'] >= 48, 'Touch target is at least 48px')
            require(rect['x'] >= 0 and rect['right'] <= width + 1, 'Control stays in viewport')
    if width < 768:
        cards = page.locator('.stage-card').evaluate_all('(els) => els.map(e => e.getBoundingClientRect().toJSON())')
        require(all(cards[i]['bottom'] <= cards[i+1]['top'] for i in range(2)), 'Mobile stages stacked')
    else:
        require(page.locator('.stage-card').evaluate_all('(els) => new Set(els.map(e => e.offsetTop)).size === 1'), 'Desktop/tablet stages share a row')


def check_dialog(page):
    for index in range(5):
        button = page.locator('.capture-button').nth(index)
        button.click()
        dialog = page.locator('#testimonial-dialog')
        require(dialog.evaluate('(e) => e.open'), 'Original image dialog opens')
        full = page.locator('#testimonial-full-image')
        full.evaluate('(e) => e.decode()')
        require(full.get_attribute('src') == f'assets/testimonios/testimonio-{index+1}.jpg', 'Correct full original')
        require(page.locator('#testimonial-close').evaluate('(e) => e === document.activeElement'), 'Dialog receives focus')
        page.keyboard.press('Tab')
        require(page.evaluate('document.getElementById("testimonial-dialog").contains(document.activeElement)'), 'Modal traps focus')
        panel = page.locator('.dialog-image-scroll')
        panel.evaluate('(e) => e.scrollTop = e.scrollHeight')
        frame_box = page.locator('#testimonial-image-frame').bounding_box()
        require(frame_box['y'] + frame_box['height'] <= panel.bounding_box()['y'] + panel.bounding_box()['height'] + 1, 'Full message bottom reachable by scrolling')
        original_width = page.locator('#testimonial-image-frame').bounding_box()['width']
        page.locator('#testimonial-zoom').click()
        require(page.locator('#testimonial-zoom').get_attribute('aria-pressed') == 'true', 'Readable zoom state')
        require(page.locator('#testimonial-image-frame').bounding_box()['width'] > original_width * 1.5, 'Zoom enlarges original text')
        require(page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Zoom confined to modal')
        if index == 1:
            require(page.locator('#testimonial-image-frame .capture-redaction').count() == 1, 'Author mask appears in full image')
        if index in [2,3]:
            frame=page.locator('#testimonial-image-frame')
            require(frame.evaluate('(e) => Number(getComputedStyle(e).getPropertyValue("--capture-height"))') < full.evaluate('(e) => e.naturalHeight'), 'Identifying reaction strip excluded')
        page.keyboard.press('Escape')
        page.wait_for_function('!document.getElementById("testimonial-dialog").open && !document.body.classList.contains("modal-open")')
        require(button.evaluate('(e) => e === document.activeElement'), 'Focus returns to trigger')
    page.locator('.capture-button').first.click()
    require(page.locator('#testimonial-zoom').get_attribute('aria-pressed') == 'false', 'Zoom resets on reopen')
    page.locator('#testimonial-close').click()
    require(not page.locator('#testimonial-dialog').evaluate('(e) => e.open'), 'Close button works')


def record_motion(page):
    page.add_init_script('''window.entryAnimations = [];
      const original = Element.prototype.animate;
      Element.prototype.animate = function(frames, options) {
        window.entryAnimations.push({element: this, duration: options.duration});
        return original.call(this, frames, options);
      };''')


def check_motion(page):
    card = page.locator('.stage-card').first
    card.scroll_into_view_if_needed()
    page.wait_for_function('document.querySelector(".stage-card").dataset.reveal === "played"')
    page.wait_for_timeout(800)
    require(page.evaluate('window.entryAnimations.some(a => a.duration >= 500 && a.duration <= 650)'), 'Discreet entry motion executed')
    before=page.evaluate('window.entryAnimations.filter(a => a.element === document.querySelector(".stage-card")).length')
    page.locator('h1').scroll_into_view_if_needed()
    card.scroll_into_view_if_needed()
    page.wait_for_timeout(150)
    require(before == 1 and page.evaluate('window.entryAnimations.filter(a => a.element === document.querySelector(".stage-card")).length') == before, 'Entry animation runs once')


def check_touch(browser,url):
    page=browser.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
    ready(page,url)
    track=page.locator('#testimonials-track')
    track.scroll_into_view_if_needed()
    page.wait_for_timeout(800)
    rectangle=track.bounding_box()
    y=rectangle['y']+min(rectangle['height']/2,70)
    session=page.context.new_cdp_session(page)
    session.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':300,'y':y}]})
    for x in [270,240,210,180,150,120,90,60]:
        session.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x,'y':y}]})
        page.wait_for_timeout(35)
    session.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
    page.wait_for_function('document.getElementById("testimonials-track").scrollLeft > 50')
    page.close()


def main():
    parser=ArgumentParser()
    parser.add_argument('--screenshots', type=Path)
    args=parser.parse_args()
    if args.screenshots:
        args.screenshots.mkdir(parents=True, exist_ok=True)
    results=[]
    with server() as url, sync_playwright() as p:
        browser=p.chromium.launch(headless=True, executable_path='/usr/bin/chromium')
        for width in [360,390,430,768,1440,767,1024]:
            page=browser.new_page(viewport={'width':width,'height':900})
            errors=[]
            page.on('pageerror', lambda error: errors.append(str(error)))
            record_motion(page)
            ready(page, url)
            check_content(page)
            check_layout(page,width)
            check_interactions(page)
            check_dialog(page)
            check_motion(page)
            require(not errors, f'No JavaScript exceptions: {errors}')
            if args.screenshots and width in [360,390,430,768,1440]:
                for image in page.locator('img[loading="lazy"]').all():
                    if not image.is_visible():
                        continue
                    image.scroll_into_view_if_needed()
                    image.evaluate('(e) => e.decode()')
                page.evaluate('document.getElementById("testimonials-track").scrollTo({left:0,behavior:"instant"})')
                page.locator('.accordion details[open]').evaluate_all('(els) => els.forEach(e => e.open = false)')
                page.evaluate('window.scrollTo({top:0,behavior:"instant"})')
                page.screenshot(path=str(args.screenshots/f'landing-{width}.png'),full_page=True)
                for selector,label in [('.hero','hero'),('.mentor-grid','mentor'),('.plans-grid','planes'),('.stages','etapas'),('.objection','objecion'),('.foundation','fundamento'),('.testimonials','testimonios')]:
                    page.locator(selector).screenshot(path=str(args.screenshots/f'{label}-{width}.png'))
            results.append(f'PASS {width}px: content, real captures/illustrations, layout, keyboard, carousel, all five modals/zoom and one-shot motion')
            page.close()
        reduced=browser.new_page(reduced_motion='reduce')
        record_motion(reduced)
        ready(reduced,url)
        require(reduced.evaluate('getComputedStyle(document.documentElement).scrollBehavior') == 'auto', 'Reduced-motion scrolling')
        check_interactions(reduced)
        require(reduced.evaluate('window.entryAnimations.length === 0'), 'No entry motion with reduced motion')
        reduced.close()
        results.append('PASS reduced motion')
        nojs=browser.new_page(java_script_enabled=False, viewport={'width':390,'height':844})
        nojs.goto(url,wait_until='networkidle')
        require(nojs.locator('h1').is_visible(), 'Copy available without JS')
        require(nojs.locator('#paypal-basic').get_attribute('href').endswith('J62F4J94WSUUS'), 'Payment link available without JS')
        nojs.locator('.vip-details summary').click()
        require(nojs.locator('.vip-details').evaluate('(e) => e.open'), 'Native details works without JS')
        require(nojs.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'No-JS layout')
        nojs.locator('.capture-fallback summary').first.click()
        nojs.locator('.capture-fallback img').first.evaluate('(e) => e.decode()')
        require(nojs.locator('.capture-fallback img').first.evaluate('(e) => e.naturalWidth > 0'), 'Full original readable without JavaScript')
        require(nojs.locator('.stage-card').first.evaluate('(e) => getComputedStyle(e).opacity') == '1', 'No hidden no-JS content')
        nojs.close()
        results.append('PASS JavaScript disabled')
        noio=browser.new_page()
        noio.add_init_script('delete window.IntersectionObserver')
        ready(noio,url)
        require(noio.locator('.stage-card').evaluate_all('(els) => els.every(e => getComputedStyle(e).opacity === "1")'), 'Missing observer never hides content')
        noio.locator('.capture-button').first.click()
        require(noio.locator('#testimonial-dialog').evaluate('(e) => e.open'), 'Modal functional without observer')
        noio.close()
        results.append('PASS without IntersectionObserver: visible content and functional modal')
        check_touch(browser,url)
        results.append('PASS native mobile touch swipe')
        browser.close()
    for result in results: print(result)
    print('NOT RUN: live Wistia playback, PayPal checkout totals/transactions; no build/lint package scripts exist.')
    if args.screenshots:
        (args.screenshots/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')

if __name__ == '__main__': main()
