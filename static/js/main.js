(function() {
    var on = addEventListener,
        $ = function(q) {
            return document.querySelector(q)
        },
        $$ = function(q) {
            return document.querySelectorAll(q)
        },
        $body = document.body,
        $inner = $('.inner'),
        client = (function() {
            var o = {
                    browser: 'other',
                    browserVersion: 0,
                    os: 'other',
                    osVersion: 0,
                    mobile: false,
                    canUse: null
                },
                ua = navigator.userAgent,
                a, i;
            a = [
                ['firefox', /Firefox\/([0-9\.]+)/],
                ['edge', /Edge\/([0-9\.]+)/],
                ['safari', /Version\/([0-9\.]+).+Safari/],
                ['chrome', /Chrome\/([0-9\.]+)/],
                ['chrome', /CriOS\/([0-9\.]+)/],
                ['ie', /Trident\/.+rv:([0-9]+)/]
            ];
            for (i = 0; i < a.length; i++) {
                if (ua.match(a[i][1])) {
                    o.browser = a[i][0];
                    o.browserVersion = parseFloat(RegExp.$1);
                    break;
                }
            }
            a = [
                ['ios', /([0-9_]+) like Mac OS X/, function(v) {
                    return v.replace('_', '.').replace('_', '');
                }],
                ['ios', /CPU like Mac OS X/, function(v) {
                    return 0
                }],
                ['ios', /iPad; CPU/, function(v) {
                    return 0
                }],
                ['android', /Android ([0-9\.]+)/, null],
                ['mac', /Macintosh.+Mac OS X ([0-9_]+)/, function(v) {
                    return v.replace('_', '.').replace('_', '');
                }],
                ['windows', /Windows NT ([0-9\.]+)/, null],
                ['undefined', /Undefined/, null],
            ];
            for (i = 0; i < a.length; i++) {
                if (ua.match(a[i][1])) {
                    o.os = a[i][0];
                    o.osVersion = parseFloat(a[i][2] ? (a[i][2])(RegExp.$1) : RegExp.$1);
                    break;
                }
            }
            if (o.os == 'mac' && ('ontouchstart' in window) && ((screen.width == 1024 && screen.height == 1366) || (screen.width == 834 && screen.height == 1112) || (screen.width == 810 && screen.height == 1080) || (screen.width == 768 && screen.height == 1024))) o.os = 'ios';
            o.mobile = (o.os == 'android' || o.os == 'ios');
            var _canUse = document.createElement('div');
            o.canUse = function(p) {
                var e = _canUse.style,
                    up = p.charAt(0).toUpperCase() + p.slice(1);
                return (p in e || ('Moz' + up) in e || ('Webkit' + up) in e || ('O' + up) in e || ('ms' + up) in e);
            };
            return o;
        }()),
        trigger = function(t) {
            if (client.browser == 'ie') {
                var e = document.createEvent('Event');
                e.initEvent(t, false, true);
                dispatchEvent(e);
            } else dispatchEvent(new Event(t));
        },
        cssRules = function(selectorText) {
            var ss = document.styleSheets,
                a = [],
                f = function(s) {
                    var r = s.cssRules,
                        i;
                    for (i = 0; i < r.length; i++) {
                        if (r[i] instanceof CSSMediaRule && matchMedia(r[i].conditionText).matches)(f)(r[i]);
                        else if (r[i] instanceof CSSStyleRule && r[i].selectorText == selectorText) a.push(r[i]);
                    }
                },
                x, i;
            for (i = 0; i < ss.length; i++) f(ss[i]);
            return a;
        },
        thisHash = function() {
            var h = location.hash ? location.hash.substring(1) : null,
                a;
            if (!h) return null;
            if (h.match(/\?/)) {
                a = h.split('?');
                h = a[0];
                history.replaceState(undefined, undefined, '#' + h);
                window.location.search = a[1];
            }
            if (h.length > 0 && !h.match(/^[a-zA-Z]/)) h = 'x' + h;
            if (typeof h == 'string') h = h.toLowerCase();
            return h;
        },
        scrollToElement = function(e, style, duration) {
            var y, cy, dy, start, easing, offset, f;
            if (!e) y = 0;
            else {
                offset = (e.dataset.scrollOffset ? parseInt(e.dataset.scrollOffset) : 0) * parseFloat(getComputedStyle(document.documentElement).fontSize);
                switch (e.dataset.scrollBehavior ? e.dataset.scrollBehavior : 'default') {
                    case 'default':
                    default:
                        y = e.offsetTop + offset;
                        break;
                    case 'center':
                        if (e.offsetHeight < window.innerHeight) y = e.offsetTop - ((window.innerHeight - e.offsetHeight) / 2) + offset;
                        else y = e.offsetTop - offset;
                        break;
                    case 'previous':
                        if (e.previousElementSibling) y = e.previousElementSibling.offsetTop + e.previousElementSibling.offsetHeight + offset;
                        else y = e.offsetTop + offset;
                        break;
                }
            }
            if (!style) style = 'smooth';
            if (!duration) duration = 750;
            if (style == 'instant') {
                window.scrollTo(0, y);
                return;
            }
            start = Date.now();
            cy = window.scrollY;
            dy = y - cy;
            switch (style) {
                case 'linear':
                    easing = function(t) {
                        return t
                    };
                    break;
                case 'smooth':
                    easing = function(t) {
                        return t < .5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1
                    };
                    break;
            }
            f = function() {
                var t = Date.now() - start;
                if (t >= duration) window.scroll(0, y);
                else {
                    window.scroll(0, cy + (dy * easing(t / duration)));
                    requestAnimationFrame(f);
                }
            };
            f();
        },
        scrollToTop = function() {
            scrollToElement(null);
        },
        loadElements = function(parent) {
            var a, e, x, i;
            a = parent.querySelectorAll('iframe[data-src]:not([data-src=""])');
            for (i = 0; i < a.length; i++) {
                a[i].src = a[i].dataset.src;
                a[i].dataset.src = "";
            }
            a = parent.querySelectorAll('video[autoplay]');
            for (i = 0; i < a.length; i++) {
                if (a[i].paused) a[i].play();
            }
            e = parent.querySelector('[data-autofocus="1"]');
            x = e ? e.tagName : null;
            switch (x) {
                case 'FORM':
                    e = e.querySelector('.field input, .field select, .field textarea');
                    if (e) e.focus();
                    break;
                default:
                    break;
            }
        },
        unloadElements = function(parent) {
            var a, e, x, i;
            a = parent.querySelectorAll('iframe[data-src=""]');
            for (i = 0; i < a.length; i++) {
                if (a[i].dataset.srcUnload === '0') continue;
                a[i].dataset.src = a[i].src;
                a[i].src = '';
            }
            a = parent.querySelectorAll('video');
            for (i = 0; i < a.length; i++) {
                if (!a[i].paused) a[i].pause();
            }
            e = $(':focus');
            if (e) e.blur();
        };
    window._scrollToTop = scrollToTop;
    var thisURL = function() {
        return window.location.href.replace(window.location.search, '').replace(/#$/, '');
    };
    var getVar = function(name) {
        var a = window.location.search.substring(1).split('&'),
            b, k;
        for (k in a) {
            b = a[k].split('=');
            if (b[0] == name) return b[1];
        }
        return null;
    };
    var errors = {
        handle: function(handler) {
            window.onerror = function(message, url, line, column, error) {
                (handler)(error.message);
                return true;
            };
        },
        unhandle: function() {
            window.onerror = null;
        }
    };
    on('load', function() {
        setTimeout(function() {
            $body.className = $body.className.replace(/\bis-loading\b/, 'is-playing');
            setTimeout(function() {
                $body.className = $body.className.replace(/\bis-playing\b/, 'is-ready');
            }, 1000);
        }, 100);
    });
    loadElements(document.body);
    (function() {
        window._scrollToTop = function() {
            scrollToElement(null);
            if (window.location.hash) {
                history.pushState(null, null, '.');
            }
        };
        if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
        on('load', function() {
            var initialScrollPoint, h;
            h = thisHash();
            if (h && !h.match(/^[a-zA-Z0-9\-]+$/)) h = null;
            initialScrollPoint = $('[data-scroll-id="' + h + '"]');
            if (initialScrollPoint) scrollToElement(initialScrollPoint, 'instant');
        });
        on('hashchange', function(event) {
            var scrollPoint, h, pos;
            h = thisHash();
            if (h && !h.match(/^[a-zA-Z0-9\-]+$/)) return false;
            scrollPoint = $('[data-scroll-id="' + h + '"]');
            if (scrollPoint) scrollToElement(scrollPoint);
            else scrollToElement(null);
            return false;
        });
        on('click', function(event) {
            var t = event.target,
                tagName = t.tagName.toUpperCase(),
                scrollPoint;
            switch (tagName) {
                case 'IMG':
                case 'SVG':
                case 'USE':
                case 'U':
                case 'STRONG':
                case 'EM':
                case 'CODE':
                case 'S':
                case 'MARK':
                case 'SPAN':
                    while (!!(t = t.parentElement))
                        if (t.tagName == 'A') break;
                    if (!t) return;
                    break;
                default:
                    break;
            }
            if (t.tagName == 'A' && t.getAttribute('href').substr(0, 1) == '#') {
                if (!!(scrollPoint = $('[data-scroll-id="' + t.hash.substr(1) + '"][data-scroll-invisible="1"]'))) {
                    event.preventDefault();
                    scrollToElement(scrollPoint);
                } else if (t.hash == window.location.hash) {
                    event.preventDefault();
                    history.replaceState(undefined, undefined, '#');
                    location.replace(t.hash);
                }
            }
        });
    })();
    var style, sheet, rule;
    style = document.createElement('style');
    style.appendChild(document.createTextNode(''));
    document.head.appendChild(style);
    sheet = style.sheet;
    if (client.mobile) {
        (function() {
            var f = function() {
                document.documentElement.style.setProperty('--viewport-height', window.innerHeight + 'px');
                document.documentElement.style.setProperty('--background-height', (window.innerHeight + 250) + 'px');
            };
            on('load', f);
            on('resize', f);
            on('orientationchange', function() {
                setTimeout(function() {
                    (f)();
                }, 100);
            });
        })();
    }
    if (client.os == 'android') {
        (function() {
            sheet.insertRule('body::after { }', 0);
            rule = sheet.cssRules[0];
            var f = function() {
                rule.style.cssText = 'height: ' + (Math.max(screen.width, screen.height)) + 'px';
            };
            on('load', f);
            on('orientationchange', f);
            on('touchmove', f);
        })();
        $body.classList.add('is-touch');
    } else if (client.os == 'ios') {
        if (client.osVersion <= 11)(function() {
            sheet.insertRule('body::after { }', 0);
            rule = sheet.cssRules[0];
            rule.style.cssText = '-webkit-transform: scale(1.0)';
        })();
        if (client.osVersion <= 11)(function() {
            sheet.insertRule('body.ios-focus-fix::before { }', 0);
            rule = sheet.cssRules[0];
            rule.style.cssText = 'height: calc(100% + 60px)';
            on('focus', function(event) {
                $body.classList.add('ios-focus-fix');
            }, true);
            on('blur', function(event) {
                $body.classList.remove('ios-focus-fix');
            }, true);
        })();
        $body.classList.add('is-touch');
    } else if (client.browser == 'ie') {
        if (!('matches' in Element.prototype)) Element.prototype.matches = (Element.prototype.msMatchesSelector || Element.prototype.webkitMatchesSelector);
        (function() {
            var a = cssRules('body::before'),
                r;
            if (a.length > 0) {
                r = a[0];
                if (r.style.width.match('calc')) {
                    r.style.opacity = 0.9999;
                    setTimeout(function() {
                        r.style.opacity = 1;
                    }, 100);
                } else {
                    document.styleSheets[0].addRule('body::before', 'content: none !important;');
                    $body.style.backgroundImage = r.style.backgroundImage.replace('url("images/', 'url("static/images/');
                    $body.style.backgroundPosition = r.style.backgroundPosition;
                    $body.style.backgroundRepeat = r.style.backgroundRepeat;
                    $body.style.backgroundColor = r.style.backgroundColor;
                    $body.style.backgroundAttachment = 'fixed';
                    $body.style.backgroundSize = r.style.backgroundSize;
                }
            }
        })();
        (function() {
            var t, f;
            f = function() {
                var mh, h, s, xx, x, i;
                x = $('#wrapper');
                x.style.height = 'auto';
                if (x.scrollHeight <= innerHeight) x.style.height = '100vh';
                xx = $$('.container.full');
                for (i = 0; i < xx.length; i++) {
                    x = xx[i];
                    s = getComputedStyle(x);
                    x.style.minHeight = '';
                    x.style.height = '';
                    mh = s.minHeight;
                    x.style.minHeight = 0;
                    x.style.height = '';
                    h = s.height;
                    if (mh == 0) continue;
                    x.style.height = (h > mh ? 'auto' : mh);
                }
            };
            (f)();
            on('resize', function() {
                clearTimeout(t);
                t = setTimeout(f, 250);
            });
            on('load', f);
        })();
    } else if (client.browser == 'edge') {
        (function() {
            var xx = $$('.container > .inner > div:last-child'),
                x, y, i;
            for (i = 0; i < xx.length; i++) {
                x = xx[i];
                y = getComputedStyle(x.parentNode);
                if (y.display != 'flex' && y.display != 'inline-flex') continue;
                x.style.marginLeft = '-1px';
            }
        })();
    }
    if (!client.canUse('object-fit')) {
        (function() {
            var xx = $$('.image[data-position]'),
                x, w, c, i, src;
            for (i = 0; i < xx.length; i++) {
                x = xx[i];
                c = x.firstElementChild;
                if (c.tagName != 'IMG') {
                    w = c;
                    c = c.firstElementChild;
                }
                if (c.parentNode.classList.contains('deferred')) {
                    c.parentNode.classList.remove('deferred');
                    src = c.getAttribute('data-src');
                    c.removeAttribute('data-src');
                } else src = c.getAttribute('src');
                c.style['backgroundImage'] = 'url(\'' + src + '\')';
                c.style['backgroundSize'] = 'cover';
                c.style['backgroundPosition'] = x.dataset.position;
                c.style['backgroundRepeat'] = 'no-repeat';
                c.src = 'data:image/svg+xml;charset=utf8,' + escape('<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1" viewBox="0 0 1 1"></svg>');
                if (x.classList.contains('full') && (x.parentNode && x.parentNode.classList.contains('full')) && (x.parentNode.parentNode && x.parentNode.parentNode.parentNode && x.parentNode.parentNode.parentNode.classList.contains('container')) && x.parentNode.children.length == 1) {
                    (function(x, w) {
                        var p = x.parentNode.parentNode,
                            f = function() {
                                x.style['height'] = '0px';
                                clearTimeout(t);
                                t = setTimeout(function() {
                                    if (getComputedStyle(p).flexDirection == 'row') {
                                        if (w) w.style['height'] = '100%';
                                        x.style['height'] = (p.scrollHeight + 1) + 'px';
                                    } else {
                                        if (w) w.style['height'] = 'auto';
                                        x.style['height'] = 'auto';
                                    }
                                }, 125);
                            },
                            t;
                        on('resize', f);
                        on('load', f);
                        (f)();
                    })(x, w);
                }
            }
        })();
        (function() {
            var xx = $$('.gallery img'),
                x, p, i, src;
            for (i = 0; i < xx.length; i++) {
                x = xx[i];
                p = x.parentNode;
                if (p.classList.contains('deferred')) {
                    p.classList.remove('deferred');
                    src = x.getAttribute('data-src');
                } else src = x.getAttribute('src');
                p.style['backgroundImage'] = 'url(\'' + src + '\')';
                p.style['backgroundSize'] = 'cover';
                p.style['backgroundPosition'] = 'center';
                p.style['backgroundRepeat'] = 'no-repeat';
                x.style['opacity'] = '0';
            }
        })();
    }
    var scrollEvents = {
        items: [],
        add: function(o) {
            this.items.push({
                element: o.element,
                triggerElement: (('triggerElement' in o && o.triggerElement) ? o.triggerElement : o.element),
                enter: ('enter' in o ? o.enter : null),
                leave: ('leave' in o ? o.leave : null),
                mode: ('mode' in o ? o.mode : 1),
                offset: ('offset' in o ? o.offset : 0),
                state: false,
            });
        },
        handler: function() {
            var height, top, bottom, scrollPad;
            if (client.os == 'ios') {
                height = document.documentElement.clientHeight;
                top = document.body.scrollTop + window.scrollY;
                bottom = top + height;
                scrollPad = 125;
            } else {
                height = document.documentElement.clientHeight;
                top = document.documentElement.scrollTop;
                bottom = top + height;
                scrollPad = 0;
            }
            scrollEvents.items.forEach(function(item) {
                var bcr, elementTop, elementBottom, state, a, b;
                if (!item.enter && !item.leave) return true;
                if (item.triggerElement.offsetParent === null) return true;
                bcr = item.triggerElement.getBoundingClientRect();
                elementTop = top + Math.floor(bcr.top);
                elementBottom = elementTop + bcr.height;
                switch (item.mode) {
                    case 1:
                    default:
                        state = (bottom > (elementTop - item.offset) && top < (elementBottom + item.offset));
                        break;
                    case 2:
                        a = (top + (height * 0.5));
                        state = (a > (elementTop - item.offset) && a < (elementBottom + item.offset));
                        break;
                    case 3:
                        a = top + (height * 0.25);
                        if (a - (height * 0.375) <= 0) a = 0;
                        b = top + (height * 0.75);
                        if (b + (height * 0.375) >= document.body.scrollHeight - scrollPad) b = document.body.scrollHeight + scrollPad;
                        state = (b > (elementTop - item.offset) && a < (elementBottom + item.offset));
                        break;
                }
                if (state != item.state) {
                    item.state = state;
                    if (item.state) {
                        if (item.enter) {
                            (item.enter).apply(item.element);
                            if (!item.leave) item.enter = null;
                        }
                    } else {
                        if (item.leave) {
                            (item.leave).apply(item.element);
                            if (!item.enter) item.leave = null;
                        }
                    }
                }
            });
        },
        init: function() {
            on('load', this.handler);
            on('resize', this.handler);
            on('scroll', this.handler);
            (this.handler)();
        }
    };
    scrollEvents.init();
    var onvisible = {
        effects: {
            'blur-in': {
                transition: function(speed, delay) {
                    return 'opacity ' + speed + 's ease' + (delay ? ' ' + delay + 's' : '') + ', ' + 'filter ' + speed + 's ease' + (delay ? ' ' + delay + 's' : '');
                },
                rewind: function(intensity) {
                    this.style.opacity = 0;
                    this.style.filter = 'blur(' + (0.25 * intensity) + 'rem)';
                },
                play: function() {
                    this.style.opacity = 1;
                    this.style.filter = 'none';
                },
            },
            'zoom-in': {
                transition: function(speed, delay) {
                    return 'opacity ' + speed + 's ease' + (delay ? ' ' + delay + 's' : '') + ', ' + 'transform ' + speed + 's ease' + (delay ? ' ' + delay + 's' : '');
                },
                rewind: function(intensity, alt) {
                    this.style.opacity = 0;
                    this.style.transform = 'scale(' + (1 - ((alt ? 0.25 : 0.05) * intensity)) + ')';
                },
                play: function() {
                    this.style.opacity = 1;
                    this.style.transform = 'none';
                },
            },
            'zoom-out': {
                transition: function(speed, delay) {
                    return 'opacity ' + speed + 's ease' + (delay ? ' ' + delay + 's' : '') + ', ' + 'transform ' + speed + 's ease' + (delay ? ' ' + delay + 's' : '');
                },
                rewind: function(intensity, alt) {
                    this.style.opacity = 0;
                    this.style.transform = 'scale(' + (1 + ((alt ? 0.25 : 0.05) * intensity)) + ')';
                },
                play: function() {
                    this.style.opacity = 1;
                    this.style.transform = 'none';
                },
            },
            'slide-left': {
                transition: function(speed, delay) {
                    return 'transform ' + speed + 's ease' + (delay ? ' ' + delay + 's' : '');
                },
                rewind: function(intensity) {
                    this.style.transform = 'translateX(100vw)';
                },
                play: function() {
                    this.style.transform = 'none';
                },
            },
            'slide-right': {
                transition: function(speed, delay) {
                    return 'transform ' + speed + 's ease' + (delay ? ' ' + delay + 's' : '');
                },
                rewind: function(intensity) {
                    this.style.transform = 'translateX(-100vw)';
                },
                play: function() {
                    this.style.transform = 'none';
                },
            },
            'flip-forward': {
                transition: function(speed, delay) {
                    return 'opacity ' + speed + 's ease' + (delay ? ' ' + delay + 's' : '') + ', ' + 'transform ' + speed + 's ease' + (delay ? ' ' + delay + 's' : '');
                },
                rewind: function(intensity, alt) {
                    this.style.opacity = 0;
                    this.style.transformOrigin = '50% 50%';
                    this.style.transform = 'perspective(1000px) rotateX(' + ((alt ? 45 : 15) * intensity) + 'deg)';
                },
                play: function() {
                    this.style.opacity = 1;
                    this.style.transform = 'none';
                },
            },
            'flip-backward': {
                transition: function(speed, delay) {
                    return 'opacity ' + speed + 's ease' + (delay ? ' ' + delay + 's' : '') + ', ' + 'transform ' + speed + 's ease' + (delay ? ' ' + delay + 's' : '');
                },
                rewind: function(intensity, alt) {
                    this.style.opacity = 0;
                    this.style.transformOrigin = '50% 50%';
                    this.style.transform = 'perspective(1000px) rotateX(' + ((alt ? -45 : -15) * intensity) + 'deg)';
                },
                play: function() {
                    this.style.opacity = 1;
                    this.style.transform = 'none';
                },
            },
            'flip-left': {
                transition: function(speed, delay) {
                    return 'opacity ' + speed + 's ease' + (delay ? ' ' + delay + 's' : '') + ', ' + 'transform ' + speed + 's ease' + (delay ? ' ' + delay + 's' : '');
                },
                rewind: function(intensity, alt) {
                    this.style.opacity = 0;
                    this.style.transformOrigin = '50% 50%';
                    this.style.transform = 'perspective(1000px) rotateY(' + ((alt ? 45 : 15) * intensity) + 'deg)';
                },
                play: function() {
                    this.style.opacity = 1;
                    this.style.transform = 'none';
                },
            },
            'flip-right': {
                transition: function(speed, delay) {
                    return 'opacity ' + speed + 's ease' + (delay ? ' ' + delay + 's' : '') + ', ' + 'transform ' + speed + 's ease' + (delay ? ' ' + delay + 's' : '');
                },
                rewind: function(intensity, alt) {
                    this.style.opacity = 0;
                    this.style.transformOrigin = '50% 50%';
                    this.style.transform = 'perspective(1000px) rotateY(' + ((alt ? -45 : -15) * intensity) + 'deg)';
                },
                play: function() {
                    this.style.opacity = 1;
                    this.style.transform = 'none';
                },
            },
            'tilt-left': {
                transition: function(speed, delay) {
                    return 'opacity ' + speed + 's ease' + (delay ? ' ' + delay + 's' : '') + ', ' + 'transform ' + speed + 's ease' + (delay ? ' ' + delay + 's' : '');
                },
                rewind: function(intensity, alt) {
                    this.style.opacity = 0;
                    this.style.transform = 'rotate(' + ((alt ? 45 : 5) * intensity) + 'deg)';
                },
                play: function() {
                    this.style.opacity = 1;
                    this.style.transform = 'none';
                },
            },
            'tilt-right': {
                transition: function(speed, delay) {
                    return 'opacity ' + speed + 's ease' + (delay ? ' ' + delay + 's' : '') + ', ' + 'transform ' + speed + 's ease' + (delay ? ' ' + delay + 's' : '');
                },
                rewind: function(intensity, alt) {
                    this.style.opacity = 0;
                    this.style.transform = 'rotate(' + ((alt ? -45 : -5) * intensity) + 'deg)';
                },
                play: function() {
                    this.style.opacity = 1;
                    this.style.transform = 'none';
                },
            },
            'fade-right': {
                transition: function(speed, delay) {
                    return 'opacity ' + speed + 's ease' + (delay ? ' ' + delay + 's' : '') + ', ' + 'transform ' + speed + 's ease' + (delay ? ' ' + delay + 's' : '');
                },
                rewind: function(intensity) {
                    this.style.opacity = 0;
                    this.style.transform = 'translateX(' + (-1.5 * intensity) + 'rem)';
                },
                play: function() {
                    this.style.opacity = 1;
                    this.style.transform = 'none';
                },
            },
            'fade-left': {
                transition: function(speed, delay) {
                    return 'opacity ' + speed + 's ease' + (delay ? ' ' + delay + 's' : '') + ', ' + 'transform ' + speed + 's ease' + (delay ? ' ' + delay + 's' : '');
                },
                rewind: function(intensity) {
                    this.style.opacity = 0;
                    this.style.transform = 'translateX(' + (1.5 * intensity) + 'rem)';
                },
                play: function() {
                    this.style.opacity = 1;
                    this.style.transform = 'none';
                },
            },
            'fade-down': {
                transition: function(speed, delay) {
                    return 'opacity ' + speed + 's ease' + (delay ? ' ' + delay + 's' : '') + ', ' + 'transform ' + speed + 's ease' + (delay ? ' ' + delay + 's' : '');
                },
                rewind: function(intensity) {
                    this.style.opacity = 0;
                    this.style.transform = 'translateY(' + (-1.5 * intensity) + 'rem)';
                },
                play: function() {
                    this.style.opacity = 1;
                    this.style.transform = 'none';
                },
            },
            'fade-up': {
                transition: function(speed, delay) {
                    return 'opacity ' + speed + 's ease' + (delay ? ' ' + delay + 's' : '') + ', ' + 'transform ' + speed + 's ease' + (delay ? ' ' + delay + 's' : '');
                },
                rewind: function(intensity) {
                    this.style.opacity = 0;
                    this.style.transform = 'translateY(' + (1.5 * intensity) + 'rem)';
                },
                play: function() {
                    this.style.opacity = 1;
                    this.style.transform = 'none';
                },
            },
            'fade-in': {
                transition: function(speed, delay) {
                    return 'opacity ' + speed + 's ease' + (delay ? ' ' + delay + 's' : '');
                },
                rewind: function(intensity) {
                    this.style.opacity = 0;
                },
                play: function() {
                    this.style.opacity = 1;
                },
            },
            'fade-in-background': {
                custom: true,
                transition: function(speed, delay) {
                    this.style.setProperty('--onvisible-speed', speed + 's');
                    if (delay) this.style.setProperty('--onvisible-delay', delay + 's');
                },
                rewind: function(intensity) {
                    this.style.removeProperty('--onvisible-background-color');
                },
                play: function() {
                    this.style.setProperty('--onvisible-background-color', 'rgba(0,0,0,0.001)');
                },
            },
        },
        add: function(selector, settings) {
            var style = settings.style in this.effects ? settings.style : 'fade',
                speed = parseInt('speed' in settings ? settings.speed : 1000) / 1000,
                intensity = ((parseInt('intensity' in settings ? settings.intensity : 5) / 10) * 1.75) + 0.25,
                delay = parseInt('delay' in settings ? settings.delay : 0) / 1000,
                offset = parseInt('offset' in settings ? settings.offset : 0),
                mode = parseInt('mode' in settings ? settings.mode : 3),
                replay = 'replay' in settings ? settings.replay : false,
                stagger = 'stagger' in settings ? (parseInt(settings.stagger) / 1000) : false,
                effect = this.effects[style];
            if ('CARRD_DISABLE_ANIMATION' in window) {
                if (style == 'fade-in-background') $$(selector).forEach(function(e) {
                    e.style.setProperty('--onvisible-background-color', 'rgba(0,0,0,0.001)');
                });
                return;
            }
            $$(selector).forEach(function(e) {
                var children = (stagger !== false) ? e.querySelectorAll(':scope > li, :scope ul > li') : null,
                    enter = function(staggerDelay = 0) {
                        var _this = this,
                            transitionOrig;
                        if (!effect.custom) {
                            transitionOrig = this.style.transition;
                            this.style.setProperty('backface-visibility', 'hidden');
                            this.style.transition = effect.transition(speed, delay + staggerDelay);
                        } else effect.transition.apply(this, [speed, delay + staggerDelay]);
                        effect.play.apply(this);
                        if (!effect.custom) setTimeout(function() {
                            _this.style.removeProperty('backface-visibility');
                            _this.style.transition = transitionOrig;
                        }, (speed + delay + staggerDelay) * 1000 * 2);
                    },
                    leave = function() {
                        var _this = this,
                            transitionOrig;
                        if (!effect.custom) {
                            transitionOrig = this.style.transition;
                            this.style.setProperty('backface-visibility', 'hidden');
                            this.style.transition = effect.transition(speed);
                        } else effect.transition.apply(this, [speed]);
                        effect.rewind.apply(this, [intensity, !!children]);
                        if (!effect.custom) setTimeout(function() {
                            _this.style.removeProperty('backface-visibility');
                            _this.style.transition = transitionOrig;
                        }, speed * 1000 * 2);
                    },
                    triggerElement;
                if (children) children.forEach(function(e) {
                    effect.rewind.apply(e, [intensity, true]);
                });
                else effect.rewind.apply(e, [intensity]);
                triggerElement = e;
                if (e.parentNode) {
                    if (e.parentNode.dataset.onvisibleTrigger) triggerElement = e.parentNode;
                    else if (e.parentNode.parentNode) {
                        if (e.parentNode.parentNode.dataset.onvisibleTrigger) triggerElement = e.parentNode.parentNode;
                    }
                }
                scrollEvents.add({
                    element: e,
                    triggerElement: triggerElement,
                    offset: offset,
                    mode: mode,
                    enter: children ? function() {
                        var staggerDelay = 0;
                        children.forEach(function(e) {
                            enter.apply(e, [staggerDelay]);
                            staggerDelay += stagger;
                        });
                    } : enter,
                    leave: (replay ? (children ? function() {
                        children.forEach(function(e) {
                            leave.apply(e);
                        });
                    } : leave) : null),
                });
            });
        },
    };
    onvisible.add('#image05', {
        style: 'zoom-in',
        speed: 625,
        intensity: 10,
        delay: 250,
        replay: false
    });
    onvisible.add('#container03', {
        style: 'fade-up',
        speed: 1000,
        intensity: 5,
        delay: 0,
        replay: false
    });
    onvisible.add('.image.style1', {
        style: 'zoom-in',
        speed: 625,
        intensity: 10,
        delay: 375,
        replay: false
    });
    onvisible.add('#container01 > .wrapper > .inner', {
        style: 'zoom-in',
        speed: 1000,
        intensity: 10,
        delay: 0,
        replay: false
    });
    onvisible.add('#container04', {
        style: 'fade-down',
        speed: 1000,
        intensity: 5,
        delay: 0,
        replay: false
    });
    onvisible.add('.container.style1', {
        style: 'zoom-in',
        speed: 1000,
        intensity: 5,
        delay: 0,
        replay: false
    });
    onvisible.add('#container02', {
        style: 'fade-up',
        speed: 1000,
        intensity: 5,
        delay: 0,
        replay: false
    });
    onvisible.add('#container02 > .wrapper > .inner', {
        style: 'fade-in',
        speed: 1000,
        intensity: 10,
        delay: 500,
        replay: false
    });
})();