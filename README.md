To scrape Starhub EPG
- The content is rendered by javascript. Usual curl will not able to see the content.
- Only partial content will be rendered as the webpage unable to fit all information, clickable button on both left and right act as the trigger to render new content accordingly.

Fortunately, I came across this YouTube video https://www.youtube.com/watch?v=Pu3gmdWsLYc&ab_channel=codeRECODE
he teaches me to look into XHR and scrape that content instead via Scrapy.