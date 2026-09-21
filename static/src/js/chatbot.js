// Bus Booking offline FAQ chat widget (Phase 8).
// Plain vanilla JS - no framework. Loaded via web.assets_frontend on all
// frontend pages; it ONLY activates when #bbb-chat-widget exists in the DOM.
//
// Odoo 19 serves web.assets_frontend files as DEFERRED ES modules, which
// means this file can execute before the server-rendered portal HTML has
// been parsed. A single DOMContentLoaded guard is therefore NOT enough:
// we retry via a MutationObserver + requestIdleCallback until the widget
// node appears (capped), so the button can never silently fail to attach.
(function () {
    'use strict';

    var CHAT_WIDGET_ID = 'bbb-chat-widget';
    var MAX_INIT_ATTEMPTS = 20;

    var started = false;
    var attempts = 0;

    function initChatWidget() {
        var root = document.getElementById(CHAT_WIDGET_ID);
        if (!root) {
            return false;
        }

        // Guard against double initialization (observer + DOMContentLoaded
        // can both fire on the same node).
        if (root.dataset.bbbChatInit === '1') {
            return true;
        }
        root.dataset.bbbChatInit = '1';

        var toggleBtn = root.querySelector('.bbb-chat-toggle');
        var panel = root.querySelector('.bbb-chat-panel');
        var messagesEl = root.querySelector('.bbb-chat-messages');
        var inputEl = root.querySelector('.bbb-chat-input input');
        var sendBtn = root.querySelector('.bbb-chat-send');

        if (!toggleBtn || !panel || !messagesEl || !inputEl || !sendBtn) {
            console.error('[bus_booking] Chat widget found but its inner nodes are missing. ' +
                'Is templates/chatbot_widget_template.xml rendering correctly?');
            return false;
        }

        function appendMessage(role, text) {
            var row = document.createElement('div');
            row.className = 'bbb-chat-msg ' + (role === 'user' ? 'bbb-chat-msg-user' : 'bbb-chat-msg-bot');
            var bubble = document.createElement('div');
            bubble.className = 'bbb-chat-bubble';
            bubble.textContent = text;
            row.appendChild(bubble);
            messagesEl.appendChild(row);
            messagesEl.scrollTop = messagesEl.scrollHeight;
        }

        function setPending(pending) {
            sendBtn.disabled = pending;
            inputEl.disabled = pending;
            if (pending) {
                appendMessage('bot', '...');
            }
        }

        function ask(question) {
            setPending(true);
            fetch('/bus/chatbot/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'call',
                    params: {question: question}
                })
            })
                .then(function (resp) {
                    if (!resp.ok) {
                        throw new Error('HTTP ' + resp.status);
                    }
                    return resp.json();
                })
                .then(function (data) {
                    var answer = data && data.result && data.result.answer;
                    if (answer) {
                        appendMessage('bot', answer);
                    } else {
                        appendMessage('bot', 'I could not understand that. Please contact our support desk.');
                    }
                })
                .catch(function () {
                    appendMessage('bot', 'Sorry, I could not reach the support service. Please try again or contact our support desk.');
                })
                .finally(function () {
                    setPending(false);
                });
        }

        function onSend() {
            var question = inputEl.value.trim();
            if (!question) {
                return;
            }
            appendMessage('user', question);
            inputEl.value = '';
            inputEl.focus();
            ask(question);
        }

        toggleBtn.addEventListener('click', function () {
            var hidden = panel.classList.toggle('d-none');
            if (!hidden) {
                inputEl.focus();
            }
        });
        sendBtn.addEventListener('click', onSend);
        inputEl.addEventListener('keydown', function (ev) {
            if (ev.key === 'Enter') {
                onSend();
            }
        });

        appendMessage(
            'bot',
            'Hi! I can answer questions about booking, payments, seats, ' +
            'tickets, cancellations and more. How can I help?'
        );
        return true;
    }

    function tryInit() {
        attempts += 1;
        if (initChatWidget()) {
            started = true;
            if (window.console && window.console.debug) {
                window.console.debug('[bus_booking] Chat widget initialised.');
            }
            return true;
        }
        if (attempts >= MAX_INIT_ATTEMPTS) {
            // Give up polling but keep one last shot on 'load'.
            if (window.console && window.console.debug) {
                window.console.debug(
                    '[bus_booking] #' + CHAT_WIDGET_ID +
                    ' not found after ' + attempts + ' attempts. ' +
                    'Is chatbot_widget_template.xml loaded and ' +
                    'portal.portal_layout inherited on this page?'
                );
            }
            return false;
        }
        return false;
    }

    function start() {
        if (started) {
            return;
        }
        if (tryInit()) {
            return;
        }
        // DOMContentLoaded / load retries.
        document.addEventListener('DOMContentLoaded', function () {
            if (!started) {
                tryInit();
                if (!started) {
                    watchForWidget();
                }
            }
        });
        window.addEventListener('load', function () {
            if (!started) {
                tryInit();
            }
        });
        // Watch for the node appearing late (SPA/portal reload cases).
        watchForWidget();
    }

    function watchForWidget() {
        if (started || attempts >= MAX_INIT_ATTEMPTS) {
            return;
        }
        if (window.MutationObserver) {
            var timer = null;
            var observer = new window.MutationObserver(function () {
                if (tryInit()) {
                    if (timer !== null) {
                        window.clearTimeout(timer);
                    }
                    observer.disconnect();
                }
            });
            observer.observe(document.documentElement, {childList: true, subtree: true});
            timer = window.setTimeout(function () {
                observer.disconnect();
            }, 15000);
        } else {
            var interval = window.setInterval(function () {
                if (started || attempts >= MAX_INIT_ATTEMPTS) {
                    window.clearInterval(interval);
                    return;
                }
                tryInit();
            }, 500);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', start);
    } else {
        start();
    }
})();