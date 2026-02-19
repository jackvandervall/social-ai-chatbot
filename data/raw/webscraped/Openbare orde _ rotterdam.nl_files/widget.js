let currentScript = document.querySelector("#chatwidget-script");
const currentScriptUrl = currentScript.src.split("/");
const baseDomain = currentScriptUrl[2];
const scriptBaseUrl = `${currentScriptUrl[0]}//${baseDomain}`;
// Kind of a hack to get the base URL for the CMS, which is used for the widget styling
const cmsBaseUrl = baseDomain.includes('localhost') || baseDomain.includes('ngrok')?scriptBaseUrl:`${currentScriptUrl[0]}//mijn.${baseDomain}`;
const environment = baseDomain.includes('test') ? 'staging' : (baseDomain.includes('localhost') || baseDomain.includes('ngrok') ? 'develop' : 'production');

function addScript(src, attrs={}) {
    return new Promise((resolve, reject) => {
        const s = document.createElement('script');

        // Scripts should load synchronously, because there are dependencies
        s.async = false;

        s.setAttribute('src', src);
        for(let property in attrs) {
            s.setAttribute(property, attrs[property]);
        }

        // Copy nonce from the widget script for CSP compliance
        const widgetScript = document.querySelector("#chatwidget-script");
        if (widgetScript && widgetScript.nonce) {
            s.nonce = widgetScript.nonce;
        }

        s.addEventListener('load', resolve);
        s.addEventListener('error', reject);

        document.body.appendChild(s);
    });
}

let fetchStyle = function(url) {
    return new Promise((resolve, reject) => {
        let link = document.createElement('link');
        link.type = 'text/css';
        link.rel = 'stylesheet';
        link.onload = () => resolve();
        link.onerror = () => reject();
        link.href = url;

        document.head.appendChild(link);
    });
};


// Defaults for custom attributes
let customWidgetAttrs = {
    gemEnabled: true,
    directHandover: false,
    widgetTitle: "Gem",
    widgetSubtitle: "Je digitale hulp van de gemeente",
    popupMessage: "Stel je vraag",
    avatarUrl: `${scriptBaseUrl}/static/img/avatar.png`,
    organisationName: null,
    organisationSlug: null,
    livechatType: null,
    livechatId: null,
    livechatAvatarUrl: null,
}

let allowEmptyAttrs = {
    gemEnabled: true,
    directHandover: true,
    widgetTitle: true,
    widgetSubtitle: true,
    popupMessage: true,
    avatarUrl: false,
    organisationName: true,
    organisationSlug: true,
    livechatType: true,
    livechatId: true,
    livechatAvatarUrl: false,
}

// Override default attrs with values from widget attributes
for(const prop in currentScript.dataset) {
    if (!customWidgetAttrs.hasOwnProperty(prop)) continue;

    let overrideValue = currentScript.dataset[prop];
    if (typeof(customWidgetAttrs[prop]) === "boolean") {
        if(overrideValue === "true") overrideValue = true;
        else overrideValue = false;
    }
    customWidgetAttrs[prop] = overrideValue;
}

async function fetchWithTimeout(resource, options = {}) {
    /* Source: https://dmitripavlutin.com/timeout-fetch-request/ */
    const { timeout = 8000 } = options;

    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), timeout);
    const response = await fetch(resource, {
        ...options,
        signal: controller.signal
    });
    clearTimeout(id);
    return response;
}

// TODO exception handling
async function makeRequest(url = '', data = {}, extraHeaders = {}, method = 'POST') {
    let options = {
        method: method, // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'default', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'omit', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json',
            ...extraHeaders
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        timeout: 2500,
    }
    if(method === 'POST') {
        options.body = JSON.stringify(data)
    }
    // Default options are marked with *
    const response = await fetchWithTimeout(url, options=options);
    return response; // parses JSON response into native JavaScript objects
}

function injectScripts(attrs) {
    // Widgetscript attrs
    let widgetAttrs = {
        id: "widget-script",
        "data-widget-enabled": attrs.widgetEnabled,
        "data-organisation-name": attrs.organisationName,
        "data-organisation-slug": attrs.organisationSlug,
        // "data-avatar-url": attrs.avatarUrl,
        "data-direct-handover": attrs.directHandover,
        "data-widget-title": attrs.widgetTitle,
        "data-widget-subtitle": attrs.widgetSubtitle,
        "data-popup-message": attrs.popupMessage,
        "data-livechat-type": attrs.livechatType,
        "data-livechat-id": attrs.livechatId,
        "data-livechat-avatar-url": attrs.livechatAvatarUrl,
    }
    // Custom attr, not part of metadata API
    if(currentScript.dataset.clientName) widgetAttrs["data-client-name"] = currentScript.dataset.clientName
    if(attrs.avatarUrl) widgetAttrs["data-avatar-url"] = attrs.avatarUrl

    let baseStyleUrl = `${scriptBaseUrl}/static/css/widget-v25.6.2-base.css`;
    let customStyleUrl = `${scriptBaseUrl}/static/css/widget-v25.6.1-custom.css`;
    let specificStyleUrl = `${cmsBaseUrl}/${attrs.organisationSlug}/_styling`;
    let webchatScriptUrl = `${scriptBaseUrl}/static/js/webchat-v25.6.2.js`;
    let widgetScriptUrl = `${scriptBaseUrl}/static/js/widget-v25.6.1.js`;
    let sentryScriptUrl = `${scriptBaseUrl}/static/js/sentry-6.13.2.js`;

    if(attrs.widgetEnabled) {
        fetchStyle(baseStyleUrl);
        fetchStyle(customStyleUrl);
        if (!window.location.href.includes("localhost") && !window.location.href.includes("ngrok")) fetchStyle(specificStyleUrl);
        addScript(sentryScriptUrl).then(() => {
            // You can perform actions after the script is loaded.
            Sentry.init({
                dsn: 'https://b8c04895de184d84948d95fce57239f1@virtuele-gemeente-assistent.nl/283',
                environment: environment,
                allowUrls: [scriptBaseUrl],
            });
        }).catch((err) => {
        });;
        addScript(webchatScriptUrl);
        addScript(widgetScriptUrl, attrs=widgetAttrs);
    }
}


function sessionExists() {
    let chatSession = window.sessionStorage.getItem("chat_session");
    return !!JSON.parse(chatSession)?.conversation?.length
}


class CustomDomainMetadata {
    storageKey = "domainMetadata";

    getMetadata(websiteDomain,attrs) {
        console.log("Retrieving domain metadata from endpoint for domain:", websiteDomain);
        if (attrs.organisationName) {
            console.log("However, organisationName is set to %s, not using domain %s", attrs.organisationName, websiteDomain);
            websiteDomain = `#${attrs.organisationName}`
        }

        let gemBaseUrl = baseDomain.split(".").slice(-3).join(".")
        let domainMetadataUrl = `${currentScriptUrl[0]}//${gemBaseUrl}/domain-metadata-api`;

        domainMetadataUrl = `${domainMetadataUrl}?domain=${encodeURIComponent(websiteDomain)}`
        return makeRequest(domainMetadataUrl, { }, { "Cache-Control": "max-age=300, private" }, "GET")
        .then(response => {
            if(!response || (!!response && response.status == 503)) {
                throw "Antwoorden CMS domain metadata API not available";
            }

            if(!!response && response.status === 200) {
                return response.json()
            }
        })
        .then(metadata => {
            this.data = metadata;
            return metadata
        })
        .catch(function(error) {
            // Antwoorden CMS most likely not available, do not show the widget
            console.log("Error occurred while retrieving domain metadata for Gem, not displaying widget");
            console.log(error)
        });
    }
}


async function initializeWithMetadata(pageUrl, pageTitle, attrs) {
    const domainMetadata = new CustomDomainMetadata()

    domainMetadata.getMetadata(document.domain, attrs).then((cachedData) => {
        let path = window.location.pathname.replace(/\/+$/, '') || '/';
        // determine if it should use url settings, or not? only use url settings if attrs.organisationName is not set
        if(!cachedData) {
            console.log("No domain metadata found, not initializing widget")
            // injectScripts({})
            return
        }
        // if attrs.organisationName is set, override default widgetEnabled to true (so this can always work on localhost and CMS)
        if(attrs.organisationName) {
            console.log("Organisation name is set, enabling widget by default")
            cachedData.defaults.widgetEnabled = true;
        } else {
            console.log("Organisation name is not set, using enabledPages to determine if widget should be enabled")
        }

        // if page in disablePages list and organisationName is not set, and no session exists, hide the widget
        if(((cachedData.defaults.widgetEnabled === false && !(path in cachedData.enabledPages)) || (cachedData.defaults.widgetEnabled === true && cachedData.disabledPages.includes(path))) && !attrs.organisationName && !sessionExists()) {
            console.log("Page is in disabled pages list, not initializing widget")
            document.querySelector("#webchat").style.display = "none";
        } else {
        
            document.querySelector("#webchat").style.display = "";
            let nattrs = {}
            // first load the default attributes
            for(const prop in cachedData.defaults) {
                // Only override with empty value if allowed
                if(cachedData.defaults[prop] || allowEmptyAttrs[prop]) {
                    nattrs[prop] = cachedData.defaults[prop];
                }
            }
            
            // if not organisationName is set, so url specific settings are used, override the attrs with the url specific settings
            if(!attrs.organisationName) {

                for(const prop in cachedData.enabledPages[path] || {}) {
                    // Only override with empty value if allowed
                    if(cachedData.enabledPages[path][prop] || allowEmptyAttrs[prop]) {
                        propdest = prop;
                        if (prop === 'gemEnabled') propdest = 'widgetEnabled';
                        nattrs[propdest] = cachedData.enabledPages[path][prop];
                    }
                }
            }
            console.log("Using attributes for widget:", nattrs);
            injectScripts(nattrs);
       }
    });
}

initializeWithMetadata(window.location.href, document.title, customWidgetAttrs);

// Rerender the widget in case of React making changes to the DOM
function addReactObserver() {
    let usesReact = !!document.querySelector("[data-reactroot]");

    if (!usesReact) return

    let targetNode = document.querySelector('title');

    if (!targetNode) return

    // Options for the observer (which mutations to observe)
    let config = { attributes: true, childList: true, subtree: true };

    // Callback function to execute when mutations are observed
    let callback = (mutationList, observer) => {
        let title = mutationList[0].addedNodes[0].data
        initializeWithMetadata(window.location.href, title, customWidgetAttrs);
    };

    // Create an observer instance linked to the callback function
    const observer = new MutationObserver(callback);

    // Start observing the target node for configured mutations
    observer.observe(targetNode, config);
}

// Rerender the widget in case of NextJS making changes to the DOM
function addNextJSObserver() {
    let usesNextJS = !!document.querySelector("next-route-announcer");

    if (!usesNextJS) return

    let targetNode = document.querySelector('title');

    if (!targetNode) return

    // Options for the observer (which mutations to observe)
    let config = { attributes: true, childList: true, subtree: true };

    // Callback function to execute when mutations are observed
    let callback = (mutationList, observer) => {
        let title = mutationList[0].addedNodes[0].data
        initializeWithMetadata(window.location.href, title, customWidgetAttrs);
    };

    // Create an observer instance linked to the callback function
    const observer = new MutationObserver(callback);

    // Start observing the target node for configured mutations
    observer.observe(targetNode, config);
}

addReactObserver()
addNextJSObserver()
