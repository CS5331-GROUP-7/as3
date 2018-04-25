- [Design Overview](#design-overview)
  * [Crawler](#crawler)
  * [Payload generation](#payload-generation)
  * [Injector](#injector)
- [Scanner's performance on the attack day](#scanner-s-performance-on-the-attack-day)
- [Appendix](#appendix)
  * [Benchmarks](#benchmarks)
  * [CSRF handling](#csrf-handling)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

# Design Overview 
This is an implementation of automatic web vulnerability scanner for NUS module cs5331. We follow the suggested design where we have three phases:

* crawler
* payload generation
* injector

## Crawler 
Crawler crawl all the web pages given target url and identify possible attack endpoints. Our crawler has the following functionalities:
* allowed_domains(only crawl allowed_domains,configurable per target url)
* nocrawl(do not crawl webpages that match the keyword, used to avoid crawling logout pages)
* able to identify all forms and get requests and list their parameters for next phase
* able to identify all cookies set in all pages in the domain and list them out for next phase
* able to automatically identify csrf vulnerabilities(described in appendix)

## Payload generation
This phase takes the output from crawler and replace the attack fields(cookie or form or get parameters) with the list of payloads that we have developed. To reduce the number of requests, we only inject the payload one by one instead of trying to inject the payload in multiple input parameters.

## Injector
This phase takes the list of parameters generated by the previous phase and compare against response of the original parameter list. The goal is that if payload is successful, the response should be different. To avoid cases where the payload itself is reflected in the webpage, we perform the following normalizations:
* remove payload string from response
* remove numbers from response(this guards against false positives where timestamps are included in the page, thus every page is different, making the injector think every page is a successful attack)

# Scanner's performance on the attack day
Our scanner only perform well on the `Neutron Star Collider` and the CSRF handling works perfectly, able to identify all 3 vulnerabilities. The failures on `Music catalog` has to do with the the fact that our scanner do not execute javascript and rely on identifying `form` and `a` tag in html. This issue can be fixed by using python webclients such as ghostjs or selenium as part of the crawling pipeline. However, the failure on `The terminal` cannot be fixed as it is a single page js app and knowledge of the app structure is required before a working crawler can be designed. However, we are able to semi-automate parts of our attack by manually writing the crawler result and feeding them to later phases.

# Appendix
## Benchmarks
Due to the simplicity of given bencharks, we have developed our own set of benchmarks by combining previous two assignments and using the benchmarks developed by previous year's student(https://github.com/JasonCodeIT/g12code) as starting point. We then tweak these to include new exploits such as csrf. 

## CSRF handling
A csrf attack is where the attacker can submit a request to the page without user knowing. It can be as easy as tricking a user to simply visit a page. If the user is still logged in to the website, the action in the request will be successful without adequate protection. The followings are examples of csrf attacks for GET and POST methods.

GET:

    <html><body>
    <H1>Hello</H1>
    <img src="http://vulnerablesite.com/MyAccount?EmailAddress=anaddress@asite.com" width="1" height="1" />
    </body></html>

POST:

    <html><body>
    <form name="CSRF" method="post" action"http://vulnerablesite.com/MyAccount">
    <input type='hidden' name='EmailAddress' value="anaddress@asite.com"></form>
    <script>document.CSRF.submit()</script>
    </body></html>

The typical prevention measure cited is to include a random,long token along with every request. As the token is needed to successfully validate the request, the attacker cannot construct a valid html page with correct token. Some applications will instead use a session wide csrf token instead of a per-request token. This has some usability improvements as per-request csrf token will limit the user from opening multiple pages as any new page opening will invalidate the previous request.  However, it has slightly diminished security as if the attacker can monitor the traffic, he can generate correct html page within the time window the session token is valid.

Ideally, good csrf targets should be state changing instead of pure viewing states. However, it is not trivial to detect if a request is state changing. Therefore in our scanning, we limit ourselves to simply detecting requests that are not protected by per-request csrf tokens.

To reduce the number of false positives, we also filter out urls that can be accessed without loggin in. Algorithm steps:

* crawl once without logging in 
* results1 <- crawl second time with login
* results2 <- crawl third time with login
* ignore all urls which can be accessed without logging in
* flag the results in results2 which has the exact same parameter name and value as potentially vulnerable. Note that weak csrf protection mechanism where session token is used as csrf token, can also be detected because our crawler code can handle login with session headers(so that session token does not change and incorrectly flagged as secure)